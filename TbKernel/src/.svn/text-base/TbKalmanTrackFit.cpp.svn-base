// Tb/TbEvent
#include "Event/TbCluster.h"
#include "Event/TbTrack.h"
#include "Event/TbKalmanTrack.h"
#include "Event/TbKalmanNode.h"

// Local
#include "TbKalmanTrackFit.h"

DECLARE_TOOL_FACTORY(TbKalmanTrackFit)

//=============================================================================
// Standard constructor, initializes variables
//=============================================================================
TbKalmanTrackFit::TbKalmanTrackFit(const std::string& type,
                                   const std::string& name,
                                   const IInterface* parent)
    : GaudiTool(type, name, parent), m_fitter(nullptr), m_geomSvc(nullptr) {

  declareInterface<ITbTrackFit>(this);

  declareProperty("MaskedPlanes", m_maskedPlanes = {});
  declareProperty("HitError", m_hiterror = 0.004);
  declareProperty("Noise2", m_scat2 = 1.2e-8);

  m_hiterror2 = m_hiterror * m_hiterror;
}

//=============================================================================
// Destructor
//=============================================================================
TbKalmanTrackFit::~TbKalmanTrackFit() {}

//=============================================================================
// Initialisation
//=============================================================================
StatusCode TbKalmanTrackFit::initialize() {

  // Initialise the base class.
  StatusCode sc = GaudiTool::initialize();
  if (sc.isFailure()) return sc;
  // Get the straight-line fit tool (used for seeding the Kalman filter).
  m_fitter = tool<ITbTrackFit>("TbTrackFit", "StraightLineFitter", this);
  // Get the number of telescope planes.
  const auto nPlanes = geomSvc()->modules().size();
  // Set the flags whether a plane is masked or not.
  m_masked.resize(nPlanes, false);
  for (const unsigned int plane : m_maskedPlanes) {
    m_masked[plane] = true;
    m_fitter->maskPlane(plane);
  }
  return StatusCode::SUCCESS;
}

//=============================================================================
// Exclude a plane from the fit
//=============================================================================
void TbKalmanTrackFit::maskPlane(const unsigned int plane) {

  m_masked[plane] = true;
  m_fitter->maskPlane(plane);
}

//=============================================================================
// (Re-)include a plane in the fit
//=============================================================================
void TbKalmanTrackFit::unmaskPlane(const unsigned int plane) {

  m_masked[plane] = false;
  m_fitter->unmaskPlane(plane);
}

//=========================================================================
// Perform the fit
//=========================================================================
void TbKalmanTrackFit::fit(LHCb::TbTrack* track) {

  // Make a straight-line fit.
  m_fitter->fit(track);
  // Create a Kalman track.
  LHCb::TbKalmanTrack ktrack(*track, m_hiterror2, m_scat2);
  // Run the Kalman filter.
  ktrack.fit();
  // Update the track states.
  track->clearStates();
  auto nodes = ktrack.nodes();
  for (auto it = nodes.cbegin(), end = nodes.cend(); it != end; ++it) {
    track->addToStates((*it)->state());
  }
  // Set the chi2.
  track->setChi2PerNdof(ktrack.chi2PerNdof());
  track->setNdof(ktrack.ndof());
}
