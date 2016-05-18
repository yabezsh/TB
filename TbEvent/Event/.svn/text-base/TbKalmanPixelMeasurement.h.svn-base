#ifndef TBKALMANPIXELMEASUREMENT
#define TBKALMANPIXELMEASUREMENT

#include "Event/TbKalmanNode.h"

namespace LHCb {
class TbKalmanPixelMeasurement : public TbKalmanNode {
 public:
  // create from a cluster
  TbKalmanPixelMeasurement(TbKalmanTrack& parent, const TbCluster& cluster,
                           double measerr2)
      : TbKalmanNode(parent, cluster.z()),
        m_cluster(&cluster),
        m_isactive(true) {
    m_x = m_cluster->x();
    m_covx = measerr2;
    m_y = m_cluster->y();
    m_covy = measerr2;
  }

  // filter this hit
  LHCb::ChiSquare filter(State& state) const;

  // compute residual with respect to given (smoothed) state
  void updateResidual(const State& state);

  // tell if this meausurement should be used in fit
  bool hasInfo() const { return m_isactive; }

  //=========================================================================
  // Turn this node into an outlier
  //=========================================================================
  void deactivateMeasurement(bool deactivate);

  double residualX() const { return m_residualX; }
  double residualCovX() const { return m_residualCovX; }
  double residualY() const { return m_residualY; }
  double residualCovY() const { return m_residualCovY; }
  double covX() const { return m_covx; }
  double covY() const { return m_covy; }

  const TbCluster& cluster() const { return *m_cluster; }

  LHCb::ChiSquare chi2() const {
    return LHCb::ChiSquare(m_residualX * m_residualX / m_residualCovX +
                           m_residualY * m_residualY / m_residualCovY,
                           2);
  }

 private:
  const TbCluster* m_cluster;
  bool m_isactive;
  /// Measured X coordinate
  double m_x;
  /// Error^2 in X
  double m_covx;  
  /// Measured Y coordinate
  double m_y;     
  /// Error^2 in Y
  double m_covy;
  double m_residualX;
  double m_residualY;
  double m_residualCovX;
  double m_residualCovY;
};
}

#endif
