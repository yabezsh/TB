
#include "Event/TbKalmanTrack.h"
#include "Event/TbKalmanPixelMeasurement.h"

namespace {

struct OrderInZ {
  bool operator()(const LHCb::TbKalmanNode* lhs,
                  const LHCb::TbKalmanNode* rhs) const {
    return lhs->z() < rhs->z();
  }
};

double errorfromcov(double cov) { return cov > 0 ? std::sqrt(cov) : cov; }

void printState(const LHCb::TbState& state, std::ostream& os) {
  os << "(" << state.parameters()(0) << "," << state.parameters()(1) << ","
     << state.parameters()(2) << "," << state.parameters()(3) << ") +/- ("
     << errorfromcov(state.covariance()(0, 0)) << ","
     << errorfromcov(state.covariance()(1, 1)) << ","
     << errorfromcov(state.covariance()(2, 2)) << ","
     << errorfromcov(state.covariance()(3, 3)) << ")";
}
}

namespace LHCb {
//============================================================================
// Constructor
//============================================================================
TbKalmanTrack::TbKalmanTrack(const LHCb::TbTrack& track, const double hiterror2,
                             const double noise2)
    : TbTrack(track) {
  // Create nodes for all clusters
  for (const LHCb::TbCluster* cluster : track.clusters()) {
    TbKalmanNode* node = new TbKalmanPixelMeasurement(*this, *cluster, hiterror2);
    node->setNoise2(noise2);
    m_nodes.push_back(node);
  }

  // Make sure they are sorted in z
  std::sort(m_nodes.begin(), m_nodes.end(), OrderInZ());

  // Now set the links
  TbKalmanNode* prevnode(nullptr);
  for (LHCb::TbKalmanNode* node : m_nodes) {
    node->link(prevnode);
    prevnode = node;
  }
}

//============================================================================
// Destructor
//============================================================================
TbKalmanTrack::~TbKalmanTrack() {
  for (LHCb::TbKalmanNode* node : m_nodes) delete node;
}

//============================================================================
// Add a node
//============================================================================
void TbKalmanTrack::addNode(TbKalmanNode* node) {
  // This can be optimized a little bit by insorting in the right place.
  // If so, make sure to fix the 'link' method in TbKalmanNode
  m_nodes.push_back(node);
  // Make sure the nodes are sorted in z
  std::sort(m_nodes.begin(), m_nodes.end(), OrderInZ());
  // Now set the links
  TbKalmanNode* prevnode(nullptr);
  for (LHCb::TbKalmanNode* node : m_nodes) {
    node->link(prevnode);
    prevnode = node;
  }
}

//============================================================================
// Add a reference node 
//============================================================================
void TbKalmanTrack::addReferenceNode(double z) {
  addNode(new TbKalmanNode(*this, z));
}

//============================================================================
// Deactivate a measurement 
//============================================================================
void TbKalmanTrack::deactivateCluster(const TbCluster& clus) {
  for (LHCb::TbKalmanNode* node : m_nodes) {
    TbKalmanPixelMeasurement* meas =
        dynamic_cast<TbKalmanPixelMeasurement*>(node);
    if (meas && &(meas->cluster()) == &clus)
      meas->deactivateMeasurement(true);
  }
}

//============================================================================
// Perform the fit
//============================================================================
void TbKalmanTrack::fit() {
  // remove existing states
  clearStates();

  // do the fit
  if (!m_nodes.empty()) {
    // initialize the seed: very simple for now. later we may want
    // to run some iterations and then this becomes more
    // complicated.
    LHCb::TbState seedstate(firstState());
    Gaudi::SymMatrix4x4 seedcov;
    seedcov(0, 0) = seedcov(1, 1) = 1e4;
    seedcov(2, 2) = seedcov(3, 3) = 1;
    seedstate.covariance() = seedcov;
    m_nodes.front()->setSeed(seedstate);
    m_nodes.back()->setSeed(seedstate);

    // everything happens on demand, I hope. so all we need to do is copy the
    // smoothed states back.
    LHCb::ChiSquare chi2(0, -4);
    for (LHCb::TbKalmanNode* node : m_nodes) {
      // get the smoothed state
      addToStates(node->state());
      // add to the chi2
      chi2 += node->deltaChi2(0);
    }

    setNdof(chi2.nDoF());
    if (chi2.nDoF() > 0) {
      setChi2PerNdof(chi2.chi2() / chi2.nDoF());
    } else {
      setChi2PerNdof(0);
    }
  }
}

//============================================================================
// Print some debug info
//============================================================================
void TbKalmanTrack::print() const {
  std::cout << "This is a kalman fitted tracks with chi2/ndof=" << chi2() << "/"
            << ndof() << std::endl;
  // compute forward/backward chi2
  LHCb::ChiSquare forwardchi2, backwardchi2;
  double chi2X(0), chi2Y(0);
  std::cout << "These are the nodes, with some residuals: " << std::endl;
  for (const LHCb::TbKalmanNode * node : m_nodes) {
    std::cout << node->index() << " " << node->z() << " ";
    //<< node->hasInfoUpstream( LHCb::TbKalmanNode::Forward) << " "
    //<< node->hasInfoUpstream( LHCb::TbKalmanNode::Backward) << " " ;
    printState(node->state(), std::cout);
    //std::cout << node->filterStatus( LHCb::TbKalmanNode::Forward) << " "
    //<< node->filterStatus( LHCb::TbKalmanNode::Backward) << " " ;
    const TbKalmanPixelMeasurement* pixelhit =
        dynamic_cast<const TbKalmanPixelMeasurement*>(node);
    if (pixelhit) {
      std::cout << "residual x = " << pixelhit->residualX() << " +/- "
                << std::sqrt(pixelhit->residualCovX()) << " "
                << "residual y = " << pixelhit->residualY() << " +/- "
                << std::sqrt(pixelhit->residualCovY()) << " ";
      chi2X += pixelhit->residualX() * pixelhit->residualX() / pixelhit->covX();
      chi2Y += pixelhit->residualY() * pixelhit->residualY() / pixelhit->covY();
    }
    std::cout << std::endl;
    forwardchi2 += node->deltaChi2(LHCb::TbKalmanNode::Forward);
    backwardchi2 += node->deltaChi2(LHCb::TbKalmanNode::Backward);
  }
  std::cout << "Forward/backward chi2: " << forwardchi2.chi2() << "/"
            << backwardchi2.chi2() << std::endl;
  std::cout << "X/Y chi2: " << chi2X << "/" << chi2Y << std::endl;
}
}
