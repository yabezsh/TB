#ifndef TBTRACKFITNODE_H
#define TBTRACKFITNODE_H 1

// from TbEvent
#include "Event/TbState.h"
#include "Event/TbCluster.h"
#include "Event/ChiSquare.h"

// forward declarations
namespace LHCb { class TbKalmanTrack; }

namespace LHCb {

/** @class TbKalmanFitNode TbKalmanFitNode.h Event/TbKalmanFitNode.h
  *
  *  This File contains the declaration of the TbKalmanFitNode.
  *
  *  A TbKalmanFitNode represents a node in the kalman fit.
  *
  */

class TbKalmanNode {
 public:
  // important note: for the Forward fit, smoothed means
  // 'classical'. for the backward fit, it means 'bidirectional'.
  enum FilterStatus {
    Uninitialized,
    Initialized,
    Predicted,
    Filtered,
    Smoothed
  };
  enum Direction {
    Forward = 0,
    Backward = 1
  };
  enum Type {
    Reference,
    Measurement,
    Outlier
  };
  enum CachedBool {
    False = 0,
    True = 1,
    Unknown = 2
  };

  typedef LHCb::TbState State;
  typedef Gaudi::Vector4 StateParameters;
  typedef Gaudi::SymMatrix4x4 StateCovariance;

  // helper class that contains data for forward fit
  /* struct ForwardFitState { */
  /* ForwardFitState() : */
  /*   deltaChi2(0), status(Initialized) {} */
  /*   typedef  */
  /*   enum FilterStatus {Initialized, Predicted, Filtered, Smoothed } ; */
  /*   enum CachedBool   {False=0, True=1, Unknown=2;} ; */
  /*   TbState           predictedState ;  ///< predicted state of
   * forward/backward filter */
  /*   TbState           filteredState ;   ///< filtered state of forward filter
   */
  /*   double            deltaChi2 ;       ///< chisq contribution in forward
   * filter */
  /*   FilterStatus      status ;          ///< Status of the Node in the fit
   * process */
  /* } ; */

  /// Default constructor
  TbKalmanNode();

  /// Constructor from a z position
  TbKalmanNode(TbKalmanTrack& parent, double zPos);

  /// Destructor
  virtual ~TbKalmanNode();

  /// Clone the Node
  //virtual TbKalmanNode* clone() const;

  /// set the seed matrix
  void setSeedCovariance(const StateCovariance& cov) {
    m_predictedState[Forward].covariance() = cov;
    m_predictedState[Backward].covariance() = cov;
    resetFilterStatus();
  }

  /// set the seed
  void setSeed(const State& seedstate) {
    // just copy covariance (assuming it to be rather meaningless), but
    // transport the state
    State astate(seedstate);
    double dz = z() - seedstate.z();
    astate.parameters()(0) += dz * astate.parameters()(2);
    astate.parameters()(1) += dz * astate.parameters()(3);
    astate.setZ(z());
    m_predictedState[Forward] = astate;
    m_predictedState[Backward] = astate;
    resetFilterStatus();
  }

  /// retrieve chisq contribution in upstream filter
  const LHCb::ChiSquare& deltaChi2(int direction) const {
    filteredState(direction);
    return m_deltaChi2[direction];
  }

  /// get the z
  double z() const { return m_state.z(); }

  /// get the filter status (only useful for debugging)
  FilterStatus filterStatus(int direction) const {
    return m_filterStatus[direction];
  }

  /// return whether or not this node has active nodes upstream
  bool hasInfoUpstream(int direction) const;

  /// Get the index of this node. For debugging only.
  int index() const;

  /// Unlink this node
  void unLink() {
    m_prevNode = m_nextNode = 0;
    m_parent = 0;
  }

  void link(TbKalmanNode* prevnode) {
    m_prevNode = prevnode;
    if (m_prevNode) m_prevNode->m_nextNode = this;
    m_nextNode = 0;
  }

  /// set the parent
  void setParent(TbKalmanTrack* p) { m_parent = p; }

  /// get the parent
  TbKalmanTrack* parent() { return m_parent; }

 public:
  const TbKalmanNode* prevNode(int direction) const {
    return direction == Forward ? m_prevNode : m_nextNode;
  }
  const TbKalmanNode* nextNode(int direction) const {
    return direction == Forward ? m_nextNode : m_prevNode;
  }

  /// retrieve the predicted state
  const State& predictedState(int direction) const {
    if (m_filterStatus[direction] < Predicted)
      unConst().computePredictedState(direction);
    return m_predictedState[direction];
  }

  /// retrieve the filtered state
  const State& filteredState(int direction) const {
    if (m_filterStatus[direction] < Filtered)
      unConst().computeFilteredState(direction);
    return m_filteredState[direction];
  }

  /// retrieve the bismoothed state
  const State& state() const {
    if (m_filterStatus[Backward] < Smoothed) unConst().computeBiSmoothedState();
    return m_state;
  }

  /// This is used from the projectors (or from any set method?)
  void resetFilterStatus(FilterStatus s = Initialized) {
    resetFilterStatus(Forward, s);
    resetFilterStatus(Backward, s);
  }

  /// Set the noise term
  void setNoise2(double noise2) { m_Q = noise2; }

 protected:
  /// virtual function to be overloaded by Measurement implementations
  virtual void updateResidual(const State& /* state */) {}
  virtual LHCb::ChiSquare filter(State& /* state */) const {
    return LHCb::ChiSquare();
  }
  virtual bool hasInfo() const { return false; }
  virtual void deactivateMeasurement(bool /* deactivate */) {}

 private:
  void computePredictedState(int direction);
  void computeFilteredState(int direction);
  void computeBiSmoothedState();
  void computeClassicalSmoothedState();
  TbKalmanNode& unConst() const { return const_cast<TbKalmanNode&>(*this); }

 protected:
  /// reset the cache for the previous function
  void resetHasInfoUpstream(int direction);

  /// reset the filter status
  void resetFilterStatus(int direction, FilterStatus s = Initialized);

 private:

  TbKalmanTrack* m_parent;         ///< Owner
  FilterStatus m_filterStatus[2];  ///< Status of the Node in the fit process
  CachedBool m_hasInfoUpstream[
      2];  ///< Are the nodes with active measurement upstream of this node?
  State m_predictedState[2];  ///< predicted state of forward/backward filter
  State m_filteredState[2];   ///< filtered state of forward filter
  State m_state;              ///< Smoothed state
  LHCb::ChiSquare m_deltaChi2[2];  ///< chisq contribution in forward filter
  //LHCb::ChiSquare       m_totalChi2[2];          ///< total chi2 after this
  //filterstep
  //Gaudi::TrackMatrix    m_smootherGainMatrix ;   ///< smoother gain matrix
  //(smoothedfit only)
  TbKalmanNode* m_prevNode;        ///< Previous Node
  TbKalmanNode* m_nextNode;        ///< Next Node

  double m_Q;  ///< noise between this node and the next node
};

}  // namespace LHCb

#endif  // TRACKFITEVENT_FITNODE_H
