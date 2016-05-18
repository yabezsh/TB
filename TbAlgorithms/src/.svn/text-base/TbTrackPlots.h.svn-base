#ifndef TB_TRACKPLOTS_H
#define TB_TRACKPLOTS_H 1

// AIDA
#include "AIDA/IHistogram1D.h"
#include "AIDA/IHistogram2D.h"

#include "AIDA/IProfile2D.h"
#include "AIDA/IProfile1D.h"

// Tb/TbEvent
#include "Event/TbTrack.h"

// Tb/TbKernel
#include "TbKernel/ITbTrackFit.h"
#include "TbKernel/TbAlgorithm.h"

/** @class TbTrackPlots TbTrackPlots.h
 *
 *  Algorithm to produce monitoring histograms for telescope tracks.
 *
 *  @author Dan Saunders
 */

class TbTrackPlots : public TbAlgorithm {
 public:
  /// Constructor
  TbTrackPlots(const std::string& name, ISvcLocator* pSvcLocator);
  /// Destructor
  virtual ~TbTrackPlots() {}

  virtual StatusCode initialize();  ///< Algorithm initialization
  virtual StatusCode execute();     ///< Algorithm execution
  virtual StatusCode finalize();    ///< Algorithm finalization

 private:
  std::string m_trackLocation;
  std::string m_clusterLocation;

  /// Track intercepts.
  std::vector<AIDA::IHistogram2D*> m_hIntercepts;
  std::vector<AIDA::IHistogram2D*> m_hInterceptsAssociated;
  std::vector<AIDA::IHistogram2D*> m_hInterceptsNonAssociated;
  /// Biased residuals.
  std::vector<AIDA::IHistogram1D*> m_hBiasedResGX;
  std::vector<AIDA::IHistogram1D*> m_hBiasedResGY;
  std::vector<AIDA::IHistogram1D*> m_hBiasedResLX;
  std::vector<AIDA::IHistogram1D*> m_hBiasedResLY;
  /// Unbiased residuals.
  std::vector<AIDA::IHistogram1D*> m_hUnbiasedResGX;
  std::vector<AIDA::IHistogram1D*> m_hUnbiasedResGY;
  std::vector<AIDA::IHistogram1D*> m_hUnbiasedResLX;
  std::vector<AIDA::IHistogram1D*> m_hUnbiasedResLY;

  /// Biased residuals as functions of x/y.
  std::vector<AIDA::IHistogram2D*> m_hBiasedResGXvsLX;
  std::vector<AIDA::IHistogram2D*> m_hBiasedResGYvsLY;
  /// Unbiased residuals as functions of x/y.
  std::vector<AIDA::IHistogram2D*> m_hUnbiasedResGXvsGX;
  std::vector<AIDA::IHistogram2D*> m_hUnbiasedResGYvsGY;
  /// Biased residuals as functions of track probability.
  std::vector<AIDA::IHistogram2D*> m_hBiasedResGXvsTrackProb;
  std::vector<AIDA::IHistogram2D*> m_hBiasedResGYvsTrackProb;

  /// Cluster time residuals.
  std::vector<AIDA::IHistogram1D*> m_hBiasedResT;
  /// Cluster time residuals as function of global x.
  std::vector<AIDA::IHistogram2D*> m_hBiasedResTvsGX;
  /// Pixel time residuals as function of column number.
  std::vector<AIDA::IHistogram2D*> m_hBiasedResPixelTvsColumn;

  /// Tracking efficiency plots.
  AIDA::IHistogram1D* m_hRatioTracksClustersCentral;
  AIDA::IHistogram1D* m_hnClustersPerPlaneCentral;
  AIDA::IHistogram1D* m_hnTracksInterceptCentral;
  AIDA::IHistogram1D* m_hFractionTrackedClusters;
  AIDA::IHistogram1D* m_hnClustersPerPlane;
  AIDA::IHistogram1D* m_hnTrackedClusters;

  /// Other.
  AIDA::IHistogram1D* m_hTimeDifferenceTrackTrigger;

  std::vector<AIDA::IHistogram1D*> m_hSyncDifferences;
  std::vector<AIDA::IProfile1D*> m_syncInRun;

  AIDA::IHistogram1D* m_hChi2;
  AIDA::IHistogram1D* m_hProb;
  AIDA::IHistogram1D* m_hTrackSize;
  AIDA::IHistogram1D* m_hSlopeXZ;
  AIDA::IHistogram1D* m_hSlopeYZ;
  AIDA::IHistogram1D* m_hFirstStateX;
  AIDA::IHistogram1D* m_hFirstStateY;
  AIDA::IHistogram2D* m_hSlopeXvsX;
  AIDA::IHistogram2D* m_hSlopeYvsY;

  /// Parameters for chi-squared distribution
  Gaudi::Histo1DDef m_parChi2;
  /// Parameters for x/y residual distributions
  Gaudi::Histo1DDef m_parResidualsXY;
  /// Parameters for time residual distributions
  Gaudi::Histo1DDef m_parResidualsT;
  /// Parameters for x/y histograms (hitmaps)
  Gaudi::Histo1DDef m_parXY;
  /// Parameters for track slope distributions
  Gaudi::Histo1DDef m_parSlope;
  /// Parameters for central region cuts.
  Gaudi::Histo1DDef m_parCentral;

  /// Name of the track fit tool
  std::string m_trackFitTool;
  /// Track fit tool
  ITbTrackFit* m_trackFit;

  void setupPlots();
  void fillClusterLoopPlots(const LHCb::TbClusters* clusters,
                            const unsigned int plane);
  void fillTrackLoopPlots(LHCb::TbTracks* tracks);
  void fillResiduals(LHCb::TbTrack* track);
};
#endif
