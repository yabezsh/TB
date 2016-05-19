//const TString m_fileIndir = "/data2/pmmannin/"; 
//const TString m_fileIndir = "/data2/pmmannin/FullProcessing/Nov2015/"; 
//const TString m_fileIndir = "/data2/pmmannin/FullProcessing/July2015/"; 
//const TString m_fileIndir = "/data2/pmmannin/November2015/";
//const TString m_board 	= "A1_Full"; 
//const TString m_board 	= "D7_All"; 
// Board, use: _board = "D5_All", A8_All" - October TB
// const TString m_board 	= "D5_All"; 

// =========================================================

//<<<<<<< .mine
/* /\* const TString m_fileIndir = "/data2/sblusk/TB/July2015/AnaFiles/";  *\/ */
// const TString m_fileIndir = "/afs/cern.ch/user/c/cbetanco/work/LHCb/KeplerDev_v3r0/Tb/TbUT/";  
/* //const TString m_fileOutdir = "~/lhcb/testbeam/";  */
// const TString m_fileOutdir = "/afs/cern.ch/user/c/cbetanco/work/LHCb/KeplerDev_v3r0/Tb/TbUT/"; 
/* const TString m_board 	= "B6";  */
/* const TString m_bias  	= "50"; */
/* const TString m_sector	= "3";  */
//=======
//const TString m_fileIndir = "/data2/pmmannin/FullProcessing/"; 

//const TString m_board 	= "M1_test"; 


#include <sstream>
const TString m_fileIndir = TString(getenv("KEPLERROOT"))+"/eos/lhcb/testbeam/ut/TemporaryData/May2016/DQM/"+TString(getenv("BOARD"))+"/"+TString(getenv("RUNPLACE"))+"/output_"+TString(getenv("RUNNUMBER"))+"/";
const TString m_board   = TString(getenv("BOARD"));

const TString m_runNumb = TString(getenv("DEFRUN"));
//--------------------------------------------------------------------------------------
const TString runplace = TString(getenv("RUNPLACE"));
const TString consR = TString(getenv("RUNNUMBER"));
//


//-----------------------------------------------------------------------------------------
TString m_bias  	= "300";
const TString m_sector	= "PA"; 
const TString m_scanType = TString(getenv("SCANTYPE"));
//const TString m_scanType = "Bias";
const TString m_angle = "0";

const TString m_fileOutdir = ""; 
//>>>>>>> .r204986

const TString plotdir 	= "Plots";




//=======
//>>>>>>> .r204986
const double nChan 			= 512.0;
const double stripPitch = 0.190;

const bool writeEventsWithMissinhHitsToFile = false;   // flag to write events to file with missing DUT hit

const double trackTriggerTimeDiffCut = 2.5;   // Default = 2.5

const bool isPType = false;

const int kClusterChargeMin = 150;
const double ratioForHole 	= 0.05;
const double ratioForDeadStrip 	= 0.6;
const double ratioForNoisyStrip = 1.8;
const bool vetoDeadStripRegions = false;
const double k_DeadStrip 				= 0.12;

const double m_minDistFromHole = 0.05;
const bool removeTracksInHoleDef = false;
