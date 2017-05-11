//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Fri Oct 16 18:02:17 2015 by ROOT version 5.34/32
// from TTree CMS/TbUT nTuple
// found on file: Run_Bias_Scan-B6-A-212-8358_Tuple.root
//////////////////////////////////////////////////////////

#ifndef CMS_h
#define CMS_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

// Fixed size dimensions of array or collections stored in the TTree if any.

class CMS {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
   Double_t        cmsData[512];

   // List of branches
   TBranch        *b_cmsData;   //!

   CMS(TTree *tree=0);
   virtual ~CMS();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif
