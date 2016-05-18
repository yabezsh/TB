// local
#include "Event/TbKalmanNode.h"

/** @file FitNode.cpp
 *
 *  This File contains the implementation of the FitNode.
 *  A FitNode is a basket of objects at a given z position.
 *  The information inside the FitNode has to be sufficient
 *  to allow smoothing and refitting.
 *  At the moment a FitNode contains or allows you to access
 *  info on the the (kth) measurement,
 *  transport from k --> k + 1 , predicted state at k+1
 *  (predicted from filter step)  and the best state at k
 *  (notation note filter procedes from k -> k + 1 -> k + 2 ......)
 * 
 *  @author Victor Coco and Wouter Hulsbergen (moved K-math here)
 *  @date   2011-02-01
 *
 *  @author Eduardo Rodrigues (adaptations to the new track event model)
 *  @date   2005-04-15
 *
 *  @author Matt Needham
 *  @date   11-11-1999
 */

namespace LHCb {

/// Standard constructor, initializes variables
// TbKalmanNode::TbKalmanNode():
//   m_prevNode(0),
//   m_nextNode(0),
//   m_parent(0)
// {
//   // TbKalmanNode default constructor
//   m_filterStatus[Forward] = m_filterStatus[Backward] = Uninitialized ;
//   m_hasInfoUpstream[Forward] = m_hasInfoUpstream[Backward] = Unknown ;
// }

/// Constructor from a z position
TbKalmanNode::TbKalmanNode(TbKalmanTrack& parent, double z)
    : m_parent(&parent), m_prevNode(0), m_nextNode(0), m_Q(0) {
  m_state.setZ(z);
  m_filterStatus[Forward] = m_filterStatus[Backward] = Uninitialized;
  m_hasInfoUpstream[Forward] = m_hasInfoUpstream[Backward] = Unknown;
}

/// Destructor
TbKalmanNode::~TbKalmanNode() {
  if (m_prevNode && m_prevNode->m_nextNode == this) m_prevNode->m_nextNode = 0;
  if (m_nextNode && m_nextNode->m_prevNode == this) m_nextNode->m_prevNode = 0;
}

// Clone the node
//LHCb::TbKalmanNode* TbKalmanNode::clone() const
//{
//  LHCb::TbKalmanNode* rc = new LHCb::TbKalmanNode(*this) ;
//  rc->m_prevNode = rc->m_nextNode = 0 ;
//  return rc ;
//}

//=========================================================================
// Helper function to decide if we need to use the upstream filtered state
//=========================================================================
bool TbKalmanNode::hasInfoUpstream(int direction) const {
  if (m_hasInfoUpstream[direction] == LHCb::TbKalmanNode::Unknown) {
    bool rc = false;
    const TbKalmanNode* prev = prevNode(direction);
    if (prev) {
      if (prev->hasInfo())
        rc = true;
      else
        rc = prev->hasInfoUpstream(direction);
    }
    unConst().m_hasInfoUpstream[direction] =
        rc ? LHCb::TbKalmanNode::True : LHCb::TbKalmanNode::False;
  }
  return (m_hasInfoUpstream[direction] == LHCb::TbKalmanNode::True);
}

void TbKalmanNode::resetHasInfoUpstream(int direction) {
  m_hasInfoUpstream[direction] = False;
  if (!hasInfo()) {
    TbKalmanNode* next = const_cast<TbKalmanNode*>(nextNode(direction));
    if (next) next->resetHasInfoUpstream(direction);
  }
}

//=========================================================================
// Reset the status of this node
//=========================================================================
void TbKalmanNode::resetFilterStatus(int direction, FilterStatus s) {
  // The logic here is tedious, because of the smoothed states have
  // a strange depence, which depends on the type of smoother.
  if (m_filterStatus[direction] > s) {
    m_filterStatus[direction] = s;

    if (s < Filtered) {
      // if the backward filter is in 'Smoothed' state, it needs to be
      // reset to filtered, because the bi-directional smoother relies
      // on both filtered states
      if (m_filterStatus[Backward] ==
          Smoothed)  // Note: Backward=Smoothed means 'bi-directional smoother'
        m_filterStatus[Backward] = Filtered;

      // reset the status of any node that depends on this one. now
      // be careful: if this node has been copied it may be pointing
      // to a wrong node.
      const TbKalmanNode* next = nextNode(direction);
      if (next && next->m_filterStatus[direction] > s &&
          next->prevNode(direction) == this)
        const_cast<TbKalmanNode*>(next)
            ->resetFilterStatus(direction, std::min(s, Initialized));
    }

    if (direction == Forward) {
      // for the classical filter, we actually need to put the
      // upstream node back to filtered, if it is in a classicly
      // smoothed status
      const TbKalmanNode* prev = prevNode(Forward);
      if (prev && prev->m_filterStatus[Forward] == Smoothed &&
          prev->nextNode(Forward) ==
              this)  // Note: Forward=Smoothed means 'classical smoother'
        const_cast<TbKalmanNode*>(prev)->resetFilterStatus(Forward, Filtered);
    }
  }
}

//=========================================================================
// Predict the state to this node
//=========================================================================
void TbKalmanNode::computePredictedState(int direction) {
  //std::cout << "In TbKalmanNode::computePredictedState( "
  //<< direction << " ) for node " << index() << std::endl ;

  // get the filtered state from the previous node. if there wasn't
  // any, we will want to copy the reference vector and leave the
  // covariance the way it is
  m_predictedState[direction].setZ(z());
  StateParameters& stateVec = m_predictedState[direction].parameters();
  StateCovariance& stateCov = m_predictedState[direction].covariance();

  const TbKalmanNode* prevnode = prevNode(direction);
  if (prevnode) {
    const State& prevState = prevnode->filteredState(direction);
    if (!hasInfoUpstream(direction)) {
      // just _copy_ the covariance matrix from upstream, assuming
      // that this is the seed matrix. (that saves us from copying
      // the seed matrix to every state from the start.
      stateCov = prevState.covariance();
      // new: start the backward filter from the forward filter
      if (direction == Backward) stateVec = filteredState(Forward).parameters();
      //std::cout << "no information upstream. copying seed." << index() <<
      //std::endl ;
    } else {

      // For the testbeam, the transport is really trivial, assuming x and y are
      // uncorrelated
      double dz = z() - prevnode->z();
      stateVec = prevState.parameters();
      stateVec[0] += dz * stateVec[2];
      stateVec[1] += dz * stateVec[3];

      // compute the predicted covariance
      stateCov = prevState.covariance();
      stateCov(0, 0) += 2 * dz * stateCov(0, 2) + dz * dz * stateCov(2, 2);
      stateCov(0, 2) += dz * stateCov(2, 2);
      stateCov(1, 1) += 2 * dz * stateCov(1, 3) + dz * dz * stateCov(3, 3);
      stateCov(1, 3) += dz * stateCov(3, 3);

      // finally add the noise, on the direction only
      double Q = direction == Forward ? prevnode->m_Q : m_Q;
      stateCov(2, 2) += Q;
      stateCov(3, 3) += Q;
    }
  }
  // update the status flag
  m_filterStatus[direction] = Predicted;
}

//=========================================================================
// Filter this node
//=========================================================================
void TbKalmanNode::computeFilteredState(int direction) {
  //std::cout << "In TbKalmanNode::computeFilteredState( "
  //          << direction << " ) for node " << index() << std::endl ;

  // copy the predicted state
  State& state = m_filteredState[direction];
  state = predictedState(direction);

  // apply the filter if needed
  m_deltaChi2[direction] = filter(state);

  //std::cout << "Filtering node " << index() << " " << direction
  //<< " chi2 = "
  //<< m_deltaChi2[direction] << std::endl ;

  m_filterStatus[direction] = Filtered;
}

//=========================================================================
// Bi-directional smoother
//=========================================================================
void TbKalmanNode::computeBiSmoothedState() {
  //std::cout << "In TbKalmanNode::computeBiSmoothedState() for node " <<
  //index() << std::endl ;

  State& state = m_state;
  if (!hasInfoUpstream(Forward)) {
    // last node in backward direction
    state = filteredState(Backward);
  } else if (!hasInfoUpstream(Backward)) {
    // last node in forward direction
    state = filteredState(Forward);
  } else {
    // Take the weighted average of two states. We now need to
    // choose for which one we take the filtered state. AFAIU the
    // weighted average behaves better if the weights are more
    // equal. So, we filter the 'worst' prediction. In the end, it
    // all doesn't seem to make much difference.

    const State* s1, *s2;
    if (predictedState(Backward).covariance()(0, 0) >
        predictedState(Forward).covariance()(0, 0)) {
      s1 = &(filteredState(Backward));
      s2 = &(predictedState(Forward));
    } else {
      s1 = &(filteredState(Forward));
      s2 = &(predictedState(Backward));
    }

    const StateParameters& X1 = s1->parameters();
    const StateCovariance& C1 = s1->covariance();
    const StateParameters& X2 = s2->parameters();
    const StateCovariance& C2 = s2->covariance();

    //state = predictedState(Forward) ;
    StateParameters& X = state.parameters();
    StateCovariance& C = state.covariance();

    // compute the inverse of the covariance in the difference: R=(C1+C2)
    static StateCovariance invR;
    invR = C1 + C2;
    bool success = invR.InvertChol();
    if (!success) {
      std::cout << "error inverting cov matrix in smoother" << std::endl;
      //&& !m_parent->inError())
      //m_parent->setErrorFlag(2,KalmanFitResult::Smooth
      //,KalmanFitResult::MatrixInversion ) ;
    }
    // compute the gain matrix:
    static ROOT::Math::SMatrix<double, 4, 4> K;
    K = C1 * invR;
    X = X1 + K * (X2 - X1);
    ROOT::Math::AssignSym::Evaluate(C, K * C2);
    // the following used to be more stable, but isn't any longer, it seems:
    //ROOT::Math::AssignSym::Evaluate(C, -2 * K * C1) ;
    //C += C1 + ROOT::Math::Similarity(K,R) ;

    //std::cout << "smoothing two states with errors on slope: "
    //<< std::sqrt(C1(2,2)) << " " << std::sqrt(C2(2,2)) << " "
    //<< std::sqrt(C(2,2)) << std::endl ;

  }
  //if(!isPositiveDiagonal(state.covariance())&& !m_parent->inError()){
  //  m_parent->setErrorFlag(2,KalmanFitResult::Smooth
  // ,KalmanFitResult::AlgError ) ;
  //}
  updateResidual(state);

  // bug fix: we cannot set backward to state 'Smoothed', unless we have passed
  // its filter step!
  filteredState(Backward);
  m_filterStatus[Backward] = Smoothed;
}

int TbKalmanNode::index() const {
  int rc = 0;
  if (m_prevNode) rc = m_prevNode->index() + 1;
  return rc;
}
}
