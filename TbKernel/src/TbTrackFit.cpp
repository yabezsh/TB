// Tb/TbEvent
#include "Event/TbCluster.h"
#include "Event/TbTrack.h"

// Local
#include "TbTrackFit.h"

DECLARE_TOOL_FACTORY(TbTrackFit)

//=============================================================================
// Standard constructor, initializes variables
//=============================================================================
TbTrackFit::TbTrackFit(const std::string& type, const std::string& name,
                       const IInterface* parent)
    : GaudiTool(type, name, parent), m_geomSvc(nullptr) {

  declareInterface<ITbTrackFit>(this);

  declareProperty("MaskedPlanes", m_maskedPlanes = {});
}

//=============================================================================
// Destructor
//=============================================================================
TbTrackFit::~TbTrackFit() {}

//=============================================================================
// Initialisation
//=============================================================================
StatusCode TbTrackFit::initialize() {

  // Initialise the base class.
  StatusCode sc = GaudiTool::initialize();
  if (sc.isFailure()) return sc;
  // Get the number of telescope planes.
  const auto nPlanes = geomSvc()->modules().size();
  // Set the flags whether a plane is masked or not.
  m_masked.resize(nPlanes, false);
  for (const unsigned int plane : m_maskedPlanes) {
    m_masked[plane] = true;
  }
  return StatusCode::SUCCESS;
}

//=============================================================================
// Exclude a plane from the fit
//=============================================================================
void TbTrackFit::maskPlane(const unsigned int plane) {

  m_masked[plane] = true;
}

//=============================================================================
// (Re-)include a plane in the fit
//=============================================================================
void TbTrackFit::unmaskPlane(const unsigned int plane) {

  m_masked[plane] = false;
}

//=========================================================================
/// Perform a straight-line fit to the clusters of a given track
//=========================================================================
void TbTrackFit::fit(LHCb::TbTrack* track) {

  // Sums for the x-slope fit
  double s0 = 0.;
  double sx = 0.;
  double sz = 0.;
  double sxz = 0.;
  double sz2 = 0.;
  // Sums for the y-slope fit
  double u0 = 0.;
  double uy = 0.;
  double uz = 0.;
  double uyz = 0.;
  double uz2 = 0.;

  // Count the number of planes included in the fit.
  unsigned int nd = 0;

  // Loop through the clusters.
  auto clusters = track->clusters();
  for (auto it = clusters.cbegin(), end = clusters.cend(); it != end; ++it) {
    if (!(*it)) continue;
    // Skip masked planes.
    if (m_masked[(*it)->plane()]) continue;
    ++nd;
    const double wx = (*it)->wx();
    const double wy = (*it)->wy();
    const double x = (*it)->x();
    const double y = (*it)->y();
    const double z = (*it)->z();

    // Straight line fit in x
    s0 += wx;
    sx += wx * x;
    sz += wx * z;
    sxz += wx * x * z;
    sz2 += wx * z * z;
    // Straight line fit in y
    u0 += wy;
    uy += wy * y;
    uz += wy * z;
    uyz += wy * y * z;
    uz2 += wy * z * z;
  }
  //  if (nd < 3) {
  //    error() << "Invalid track. Only " << nd << " non-masked clusters" <<
  // endmsg;
  //    return;
  //  }
  // Compute the track parameters for x.

  double den = (sz2 * s0 - sz * sz);

  if (fabs(den) < 10e-10) den = 1.;
  const double tx = (sxz * s0 - sx * sz) / den;
  const double x0 = (sx * sz2 - sxz * sz) / den;

  // Compute the track parameters for y.
  den = (uz2 * u0 - uz * uz);
  if (fabs(den) < 10e-10) den = 1.;
  const double ty = (uyz * u0 - uy * uz) / den;
  const double y0 = (uy * uz2 - uyz * uz) / den;

  // Calculate the covariance matrix.
  // Ad hoc matrix inversion, as it is almost diagonal.
  // Some terms vanish since we calculate the covariance matrix at z = 0.
  const double m00 = s0;
  const double m11 = u0;
  const double m20 = sz;
  const double m31 = uz;
  const double m22 = sz2;
  const double m33 = uz2;
  const double den20 = m22 * m00 - m20 * m20;
  const double den31 = m33 * m11 - m31 * m31;

  Gaudi::SymMatrix4x4 cov;
  cov(0, 0) = m22 / den20;
  cov(2, 0) = -m20 / den20;
  cov(2, 2) = m00 / den20;

  cov(1, 1) = m33 / den31;
  cov(3, 1) = -m31 / den31;
  cov(3, 3) = m11 / den31;

  // Create the first state.
  LHCb::TbState fstate(Gaudi::Vector4(x0, y0, tx, ty), cov, 0., 0);

  fstate.covariance()(0, 0) = cov(0, 0);
  fstate.covariance()(0, 2) = cov(2, 0);
  fstate.covariance()(1, 1) = cov(1, 1);
  fstate.covariance()(2, 2) = cov(2, 2);
  fstate.covariance()(1, 3) = cov(3, 1);
  fstate.covariance()(3, 3) = cov(3, 3);
  // Update the firstState of the track.
  track->setFirstState(fstate);

  // Compute chi2 and track time.
  double chi2 = 0.;
  double time = 0.;
  for (auto it = clusters.cbegin(), end = clusters.cend(); it != end; ++it) {
    if (!(*it)) continue;
    // Skip masked planes.
    if (m_masked[(*it)->plane()]) continue;
    const double wx = (*it)->wx();
    const double wy = (*it)->wy();
    const unsigned int plane = (*it)->plane();
    // Calculate global (biased) residuals in x and y.
    const Gaudi::XYZPoint intercept = geomSvc()->intercept(track, plane);
    const Gaudi::XYZPoint local = geomSvc()->globalToLocal(intercept, plane);

    const double dx = (*it)->xloc() - local.x();
    const double dy = (*it)->yloc() - local.y();
    chi2 += (dx * dx) * wx + (dy * dy) * wy;
    time += (*it)->htime();
  }
  // Set track chi2PerNdof and ndof.
  const unsigned int ndof = 2 * nd - 4;
  track->setNdof(ndof);
  track->setChi2PerNdof(chi2 / (double)ndof);

  // Finally, set the track time.
  time /= nd;
  track->setHtime(time);
}
