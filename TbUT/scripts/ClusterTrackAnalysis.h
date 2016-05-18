#include <string>
//#include <TMath.h>
#include <sstream>
#include <iostream>
#include <fstream>
#include <iomanip>
#include "TChain.h"
#include "TH1.h"
#include "TH2.h"
#include "TFile.h"
#include <TStyle.h>
#include <TLine.h>
#include <TLatex.h>
#include <TF1.h>
#include <vector>
#include <map>
#include <TLegend.h>
#include <ctime>
#include <cstdlib>
#include <TString.h>
#include <TCanvas.h>
#include <CMS.h>
using namespace std;

class ClusterTrackAnalysis {

 public:

  ClusterTrackAnalysis();
  ~ClusterTrackAnalysis();
  ClusterTrackAnalysis(int biasVal);

  // functions
  // void Run();
  void Loop();
  void addGraphics(TH1 *h, int iCol = 1, TString XTitle="", TString YTitle="");
  void addGraphics(TH2 *h, int iCol = 1, TString XTitle="", TString YTitle="");

  
  // just for testing
  vector<int> test;

  CMS *fCMS;
  virtual TString getFileBase(TString scan="Bias", TString board="", TString bias="", TString angle="0", TString sector="1");  

  TFile *fout;

  //
  const TString m_fileIndir = "/afs/cern.ch/user/c/cbetanco/work/LHCb/KeplerDev_v3r0/Tb/TbUT/"; 
const TString m_fileOutDir = "/afs/cern.ch/user/c/cbetanco/work/LHCb/KeplerDev_v3r0/Tb/TbUT/";
const TString m_board 	= "B6"; 
const TString m_bias  	= "300";
const TString m_sector	= "3"; 
//=======
//const TString m_fileIndir = "/data2/pmmannin/FullProcessing/"; 
//const TString m_board 	= "A2"; 

//TString m_bias  	= "300";
//const TString m_sector	= "1"; 
//const TString m_scanType = "Angle";
const TString m_scanType = "Bias";
const TString m_angle = "0";

const TString m_fileOutdir = "~/lhcb/testbeam/"; 
//>>>>>>> .r204986

const TString plotdir 	= "plots";

//<<<<<<< .mine
//const TString f_out			= m_fileOutdir + plotdir + "/AnalysisOutput_" + m_board + "_" + m_bias + "_" + m_sector + ".root"; 
//const TString f_out			= "/afs/cern.ch/user/c/cbetanco/work/LHCb/KeplerDev_v3r0/Tb/TbUT/Run_Bias_Scan-B6-A-299-8431.root"; 

//=======
//>>>>>>> .r204986
const double nChan 			= 512.0;
const double stripPitch = 0.190;

const bool writeEventsWithMissinhHitsToFile = false;   // flag to write events to file with missing DUT hit

const double trackTriggerTimeDiffCut = 2.5;   // Default = 2.5

const bool isPType = true;

const int kClusterChargeMin = 150;
const double ratioForHole 	= 0.05;
const double ratioForDeadStrip 	= 0.6;
const double ratioForNoisyStrip = 1.8;
const bool vetoDeadStripRegions = false;
const double k_DeadStrip 				= 0.12;

const double m_minDistFromHole = 0.05;
const bool removeTracksInHoleDef = false;

 Int_t           clusterNumberPerEvent;
  UInt_t          clustersTDC;
  ULong64_t       timestamps;
  Double_t        clustersPosition[10];
  Int_t           clustersSeedPosition[10];
  Double_t        clustersCharge[10];
  Int_t           clustersSize[10];
  Double_t        clustersSeedCharge[10];
  Double_t        clustersCharge2StripLeft[10];
  Double_t        clustersCharge1StripLeft[10];
  Double_t        clustersCharge1StripRight[10];
  Double_t        clustersCharge2StripRight[10];
  Double_t        dtime;
   
  Int_t           n_tp3_tracks;
  vector<double>  *vec_trk_x;
  vector<double>  *vec_trk_y;
  vector<double>  *vec_trk_tx;
  vector<double>  *vec_trk_ty;
  vector<double>  *vec_trk_chi2ndf;

  // List of branches
  TBranch        *b_clusterNumberPerEvent;   //!
  TBranch        *b_clustersTDC;   //!
  TBranch        *b_timestamps;   //!
  TBranch        *b_clustersPosition;   //!
  TBranch        *b_clustersSeedPosition;   //!
  TBranch        *b_clustersCharge;   //!
  TBranch        *b_clustersSize;   //!
  TBranch        *b_clustersSeedCharge;   //!
  TBranch        *b_clustersCharge2StripLeft;   //!
  TBranch        *b_clustersCharge1StripLeft;   //!
  TBranch        *b_clustersCharge1StripRight;   //!
  TBranch        *b_clustersCharge2StripRight;   //!
  TBranch        *b_n_tp3_tracks;   //!
  TBranch        *b_vec_trk_x;   //!
  TBranch        *b_vec_trk_y;   //!
  TBranch        *b_vec_trk_tx;   //!
  TBranch        *b_vec_trk_ty;   //!
  TBranch        *b_vec_trk_chi2ndf;   //!
  TBranch        *b_dtime;   //!

  //double stripPitch;
  double z_DUT;
  double Rz;
  double Ry;
  double dxWin;
  double xGloOff;
  double yGloOff;
  double xOff;
  

  float iLo, iHi;
  float tdcLo, tdcHi;
  float yMin,yMax;
  float xMin,xMax;
  float yMid, yHi2;
  float tyMin,tyMax;
  float txMin,txMax;
  Int_t skipChannel[512];
  double xLeftHole;
  double xRightHole;
  
  Int_t lowEdge, hiEdge;
  Double_t stripGap[4];
  Double_t deadRegionLo[20];
  Double_t deadRegionHi[20];
  Int_t nDeadRegion;  

  double yInt1[2];
  double yInt2[2];
  double yInt3[2];

  float polarity;

  TH1F *hMeanNoise; 
  TH1F *hWidthNoise; 

  double holeQuadPar[3];
  bool removeTracksInHole;
  double minDistFromHole;
  bool holeSector;
  bool correctForZRotation;

  double chargeCorrSlopeOdd;
  double chargeCorrSlopeEven;
  
  double noise[512];

  double channelOffset;  


};

