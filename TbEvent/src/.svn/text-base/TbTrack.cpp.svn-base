#include "Event/TbTrack.h"

using namespace LHCb;

//=============================================================================
// Track copy constructor 
//=============================================================================
TbTrack::TbTrack(const LHCb::TbTrack& rhs) :
  KeyedObject<int>(),
  m_time(rhs.m_time),
  m_htime(rhs.m_htime),
  m_firstState(rhs.m_firstState),
  m_chi2PerNdof(rhs.m_chi2PerNdof),
  m_ndof(rhs.m_ndof),
  m_clusters(rhs.m_clusters),
  m_triggers(rhs.m_triggers),
  m_associatedClusters(rhs.m_associatedClusters) {

  // Copy the states
  for (auto it = rhs.m_states.begin(), end = rhs.m_states.end(); it != end; ++it) {
    addToStates(*it);
  }
}


//=============================================================================
// Track clone method
//=============================================================================
TbTrack* TbTrack::clone() {
  TbTrack* track = new TbTrack();
  track->setTime(time());
  track->setHtime(htime());
  track->setFirstState(firstState());
  track->setChi2PerNdof(chi2PerNdof());
  track->setNdof(ndof());

  // Copy the states
  for (auto it = m_states.begin(), end = m_states.end(); it != end; ++it) {
    track->addToStates(*it);
  }

  return track;
}

//=============================================================================
// States clone method
//=============================================================================
void TbTrack::addToStates(const TbState& state) {
  m_states.push_back(state);
}

//=============================================================================
// Clear the states
//=============================================================================
void TbTrack::clearStates() {
  m_states.clear() ;
}
