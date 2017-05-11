//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Thu Oct  1 20:13:36 2015 by ROOT version 5.34/10
// from TTree Clusters/TbUT nTuple
// found on file: /data2/pmmannin/BoardA6/Run_Bias_Scan-B6-A-212-8358_Tuple_tracks.root
//////////////////////////////////////////////////////////

#ifndef AdapterAnalysis_h
#define AdapterAnalysis_h

#include <TROOT.h>
#include <iostream>
#include <TChain.h>
#include <TTree.h>
#include <TFile.h>
#include <TH2.h>
#include <TProfile.h>
#include <TString.h>
#include "AnalysisBase.h"
#include "CMS.h"

// Header file for the classes stored in the TTree if any.
#include <vector>
#include <iostream>
#include <fstream>
#include <algorithm>



// Fixed size dimensions of array or collections stored in the TTree if any.

class AdapterAnalysis : public AnalysisBase {
public :

   CMS            *fCMS;

   AdapterAnalysis(TTree *tree=0);
   virtual ~AdapterAnalysis();
   virtual void     Loop();

   virtual TString getFileBase(TString scan="Bias", TString board="", TString bias="", TString angle="0", TString sector="1");  

  TFile *fout;
  std::vector<TObject*> outHistos;
  void writeHistos();

  bool foundClusterWithScaledNoise(size_t idx, double nScale);
  void fillMatchMiss( const std::vector<TH1*> & vh, unsigned int nhists, bool foundHit, int foundIdx, double x_trk, double y_trk, double dxNom, const std::vector<double> & allDx, double nearADC, double twonearADC, double fournearADC, double sumADC);
};

#endif

#ifdef AdapterAnalysis_cxx
AdapterAnalysis::AdapterAnalysis(TTree *tree)
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
  TString filename="";  
  if (tree == 0) {
    //filename = m_filedir+"Run_Bias_Scan-"+getFileBase("Bias",m_board, m_bias, "0",m_sector)+"_Tuple_Tracks.root"; 
    //filename = "output_192/Run_Angle_Scan-M1-FanIn-192-15109_Tracks.root";
    filename = m_fileIndir + "Run_"+m_scanType +"_Scan-" + runplace + "-" + m_board + "-" + consR + "-" + m_runNumb + "_Tracks.root";
    
    //filename = "output_262/Run_Angle_Scan-M3-FanIn-262-15157_Tracks.root";
     
     TFile *f = new TFile(filename);
     tree = (TTree*)f->Get("Clusters");


     hMeanNoise 	= (TH1F*)f->Get("hMeanNoise"); 
     hWidthNoise 	= (TH1F*)f->Get("hWidthNoise"); 

     TFile * f2 = new TFile(filename.ReplaceAll("_Tracks",""));
     fCMS=0;
     if(f2) {
       TTree * tree2 = (TTree*) f2->Get("TbUT/CMS");
       if(tree2) {
         tree->AddFriend(tree2);
         fCMS = new CMS(tree2);
       }
     }

   }
   Init(tree);
 


   // Get mask file and set mask
   // TString badStripFileName = maskFile;
   // ifstream badStripFile;

   // int iVal = 0;   
   // int iChan = 0;
   // badStripFile.open(badStripFileName); 
   // for(int i=0; i<nChan; i++){
   //   badStrips[i] = 1; // all channels good to start
   // }
 

   // if(!badStripFile) { // file couldn't be opened
   //    cerr << "Error: bad strip file does not exist -- assume all strips are good" << endl;
   // }else{
   //   while ( !badStripFile.eof() ) {
   //     badStripFile >> iVal;
   //     badStrips[iChan] = iVal;
   //     if(iVal==0) nbadStrips++;
   //     iChan++;
   //     if(iChan>=nChan) break;
   //     if(iVal==1) cout << "Good Strip, Chan# " << iChan << endl;
   //   }
   // }
   // cout << "MaskFile: Found " << nbadStrips << " masked strips" << endl;
}

AdapterAnalysis::~AdapterAnalysis()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

TString AdapterAnalysis::getFileBase(TString scan, TString board, TString bias, TString angle, TString sector) {

  TString tag = "";

  if(board == "A6"){
    if(sector == "1") {
      if ( bias == "300" ) tag = "B6-A-212-8358";
    } else if(sector == "2"){
      if ( bias == "300" ) tag = "B6-A-242-8389";
    } else if(sector == "3"){
      if ( bias == "300" ) tag = "B6-A-293-8425";
    } else if(sector == "4"){
      if ( bias == "300" ) tag = "B6-A-326-8452";
    } else if(sector == "5"){
      if ( bias == "300" ) tag = "B6-A-377-8494";
    } else if(sector == "6"){
      if ( bias == "250" ) tag = "B6-A-409-8524";
    }
  } else if (board == "A4") {
    if(sector == "1") {
      tag = "B4-A-210-8552";
    } else {
      tag = "B4-A-275-8615";
    }
  } else if (board == "A8") {
    if(sector == "3") 
      tag = "B8-A-359-13386";
  } else if (board == "M1") 
  {
    if (sector == "1")
      tag = "";
  }
  

  return tag;
}

#endif // #ifdef AdapterAnalysis_cxx
