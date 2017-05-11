#ifndef AdapterTiming_h
#define AdapterTiming_h

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

class AdapterTiming : public AnalysisBase {
public :

   CMS            *fCMS;

   AdapterTiming(TTree *tree=0);
   virtual ~AdapterTiming();
   virtual void     Loop();


  TFile *fout;
  std::vector<TObject*> outHistos;
  void writeHistos();

};

#endif

#ifdef AdapterTiming_cxx
AdapterTiming::AdapterTiming(TTree *tree)
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

     TFile * f2 = new TFile(filename.ReplaceAll("_Tracks","_Tuple"));
     fCMS=0;
     if(f2) {
       TTree * tree2 = (TTree*) f2->Get("TbUT/CMS");
       if(tree2) {
         std::cout << "Adding CMS data tree" << std::endl;
         tree->AddFriend(tree2);
         fCMS = new CMS(tree2);
       }
     }

   }
   Init(tree);
 
}

AdapterTiming::~AdapterTiming()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}
#endif
