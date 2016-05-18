#include "Event/TbKalmanPixelMeasurement.h"
#include "Event/TbKalmanTrack.h"

namespace {
/// Helper function to filter one hit
inline double filterX(double& x, double& tx, double& covXX, double& covXTx,
                      double& covTxTx, const double xhit,
                      const double xhitcov) {
  const double predcovXX = covXX;
  const double predcovXTx = covXTx;
  const double predcovTxTx = covTxTx;
  const double predx = x;
  const double predtx = tx;

  // compute the gain matrix
  const double R = xhitcov + predcovXX;
  const double Kx = predcovXX / R;
  const double KTx = predcovXTx / R;
  // update the state vector
  double r = xhit - predx;
  x = predx + Kx * r;
  tx = predtx + KTx * r;
  // update the covariance matrix. we can write it in many ways ...
  covXX /*= predcovXX  - Kx * predcovXX */ = (1 - Kx) * predcovXX;
  covXTx /*= predcovXTx - predcovXX * predcovXTx / R */ = (1 - Kx) * predcovXTx;
  covTxTx = predcovTxTx - KTx * predcovXTx;
  // return the chi2
  return r * r / R;
}
}

namespace LHCb {

LHCb::ChiSquare TbKalmanPixelMeasurement::filter(State& state) const {
  // filter X and Y independently. could easily be complicated if needed.

  double chi2(0);
  Gaudi::SymMatrix4x4& stateCov = state.covariance();
  Gaudi::Vector4& stateVec = state.parameters();

  // first X
  chi2 += filterX(stateVec(0), stateVec(2), stateCov(0, 0), stateCov(0, 2),
                  stateCov(2, 2), m_x, m_covx);

  // then Y
  chi2 += filterX(stateVec(1), stateVec(3), stateCov(1, 1), stateCov(1, 3),
                  stateCov(3, 3), m_y, m_covy);
  // chi2 has 2 dofs

  return LHCb::ChiSquare(chi2, 2);
}

// compute residual with respect to given (smoothed) state
void TbKalmanPixelMeasurement::updateResidual(const State& state) {
  m_residualX = m_x - state.x();
  m_residualY = m_y - state.y();
  int sign = m_isactive ? -1 : +1;
  m_residualCovX = m_covx + sign * state.covariance()(0, 0);
  m_residualCovY = m_covy + sign * state.covariance()(1, 1);
}

void TbKalmanPixelMeasurement::deactivateMeasurement(bool deactivate) {
  // only do something if this is actually an active hit
  if ((deactivate && m_isactive) || (!deactivate && !m_isactive)) {
    // set type to outlier
    m_isactive = !deactivate;
    // this will take care of upstream and downstream nodes as well:
    // they will be reset to initialized. we need to check this
    // carefully
    resetFilterStatus(Predicted);
    // make sure the KalmanFitResult knows something has changed
    if (parent()) parent()->resetCache();
    // now make sure others do not rely on this one anymore
    if (!hasInfoUpstream(Forward)) resetHasInfoUpstream(Forward);
    if (!hasInfoUpstream(Backward)) resetHasInfoUpstream(Backward);
  }
}

}
