//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Thu Oct  1 20:13:36 2015 by ROOT version 5.34/10
// from TTree Clusters/TbUT nTuple
// found on file: /data2/pmmannin/BoardA6/Run_Bias_Scan-B6-A-212-8358_Tuple_tracks.root
//////////////////////////////////////////////////////////

#ifndef FullAnalysis_h
#define FullAnalysis_h

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

class FullAnalysis : public AnalysisBase {
public :

   CMS            *fCMS;

   FullAnalysis(TTree *tree=0);
   virtual ~FullAnalysis();
   virtual void     Loop();

  TFile *fout;
  std::vector<TObject*> outHistos;
  void writeHistos();

  bool foundClusterWithScaledNoise(size_t idx, double nScale);
  void fillMatchMiss( const std::vector<TH1*> & vh, unsigned int nhists, bool foundHit, int foundIdx, double x_trk, double y_trk, double dxNom, const std::vector<double> & allDx, double nearADC, double twonearADC, double fournearADC, double sumADC);
};

#endif

#ifdef FullAnalysis_cxx
FullAnalysis::FullAnalysis(TTree *tree)
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
  TString filename="";  
  if (tree == 0) {
    filename = m_fileIndir + "Run_"+m_scanType +"_Scan-" + runplace + "-" + m_board + "-" + consR + "-" + m_runNumb + "_Tracks.root";
    
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
   TString badStripFileName = maskFile;
   ifstream badStripFile;

   int iVal = 0;   
   int iChan = 0;
   badStripFile.open(badStripFileName); 
   for(int i=0; i<nChan; i++){
     badStrips[i] = 1; // all channels good to start
   }
 

   if(!badStripFile) { // file couldn't be opened
      cerr << "Error: bad strip file does not exist -- assume all strips are good" << endl;
   }else{
     while ( !badStripFile.eof() ) {
       badStripFile >> iVal;
       badStrips[iChan] = iVal;
       if(iVal==0) nbadStrips++;
       iChan++;
       if(iChan>=nChan) break;
       if(iVal==1) cout << "Good Strip, Chan# " << iChan << endl;
     }
   }
   cout << "MaskFile: Found " << nbadStrips << " masked strips" << endl;
}

FullAnalysis::~FullAnalysis()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

#endif // #ifdef FullAnalysis_cxx
