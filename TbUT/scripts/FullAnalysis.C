#define FullAnalysis_cxx
#include "FullAnalysis.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TGraph.h>
#include <TProfile.h>
#include <cmath>
#include <vector>

namespace {

  //Use this unnamed namespace for making the definitions about how to create regions plots
  //current sensor edge info 
  // ymax - 0.875 to ymax - 1.1 is the bond pad region
  // add 19 to first channel to get the start of bond pad region, then add 44 to get the end.
  // A3 : first channel = 156, y=3.85
  // 
  enum {
    A3, A5, A10, A12, A13, A6};
  double sensorYmax[6] = { 3.85, 3.72, 3.8, 3.8, 3.95, 3.89 };
  double firstChan[6] = { 156., 411., 153., 407., 135., 391.};
  
  int getBoardIndex(const TString & boardname ){
    TObjString * os = (TObjString*) boardname.Tokenize("_")->At(0);
    TString newstring(os->GetString());
    

    if ( newstring == "A3")
      return A3;
    else if ( newstring == "A5" )
      return A5;
    else if ( newstring == "A10" )
      return A10;
    else if ( newstring == "A12" )
      return A12;
    else if ( newstring == "A13" )
      return A13;
    else if ( newstring == "A6" )
      return A6;
    return -1;
  }
    

  // double sensorXmax = 2.55;
  // double sensorYmax = 3.85;

  //Setup Fiducial region definitions here -- for now it is not easily configurable for different sectors/detectors without rewriting
  bool inFiducialRegion(  const double & xTrk, const double & yTrk ) {
    //    return yTrk > -1.6 && yTrk < 1.6 && xTrk > -1.5 && xTrk < 1.5;
    return true;
  }
  
  const unsigned int nRegions=6;
  bool passFiducialCut( const int & iCut, const double & xTrk, const double & yTrk, const double &dxNom, const double & nomStrip) 
  {

    // Bond pad region for minis --  ~ 875um from top edge to ~1100um
    //                               3450um from either side ==   12000um total width.  12000 - (3450x2) = 5100 wide
    
    //bool inadapterx = xTrk < sensorXmax - 3.45 && xTrk > sensorXmax - 3.45 - 5.1;
    bool inadapterx = nomStrip > firstChan[getBoardIndex(m_board)] + 19. && nomStrip < firstChan[getBoardIndex(m_board)] + 44.;
    bool inadaptery = yTrk < sensorYmax[getBoardIndex(m_board)] - 0.85 && yTrk > sensorYmax[getBoardIndex(m_board)] - 1.125;
    bool incontroly = yTrk < sensorYmax[getBoardIndex(m_board)] - 1.5 && yTrk > sensorYmax[getBoardIndex(m_board)] - 1.5 - (1.125-0.85);

    // bool intrace = xTrk > -1.5 && xTrk < 1.4 && ( (yTrk > 1.2 && yTrk < 1.4) || (yTrk > 0.5 && yTrk < 0.7));
    // bool tracecontrol  = xTrk > -1.5 && xTrk < 1.4 && yTrk > -0.4 && yTrk < 0;

    // bool inpads = yTrk > 0.8 && yTrk < 1.2 && xTrk > -1.5 && xTrk < -0.3;
    // bool padcontrol =  xTrk > -1.5 && xTrk < -0.3 && yTrk > -0.8 && yTrk < -0.4;

    // bool inadapter = xTrk > -1.6 && xTrk < 0.4 && yTrk > 2 && yTrk < 3.5;//intrace || inpads;
    // bool control =  xTrk > -1.6 && xTrk < 0.4 && yTrk > 0 && yTrk < 1.5;//tracecontrol || padcontrol;

    bool inadapter = inadapterx && inadaptery;
    bool control = inadapterx && incontroly;

    bool dxcent = fabs(dxNom) < 0.1;
    bool dxout = fabs(dxNom) > 0.4;

    switch (iCut) 
    {
    case 0:
      return inadapter;
    case 1:
      return control;
    case 2:
      return inadapter && dxcent;
    case 3:
      return control && dxcent;
    case 4:
      return inadapter && dxout;
    case 5:
      return control && dxout;
    // case 6: 
    //   return inpads;
    // case 7:
    //   return padcontrol;
    // case 8:
    //   return intrace;
    // case 9:
    //   return tracecontrol;
    default:
      return false;
    }
  }
  
  //Region plot enumeration
  //Most things are automatic -- but make sure that all plots that depend on the full channel data are after NEARADC1ALL, and if the plots doesn't depend on that it should be before
  enum {
    CLADCALL,
    CLADCMATCH,
    CLSNRALL,
    CLSNRMATCH,
    DXMATCH,
    DXMISS,
    INTERALL,
    INTERMATCH,
    YALL,
    YMATCH,
    XALL,
    XMATCH,
    NEARADC1ALL,
    NEARADC2ALL,
    NEARADC4ALL,
    NEARADC100ALL,
    NEARADC1MATCH,
    NEARADC2MATCH,
    NEARADC4MATCH,
    NEARADC100MATCH,
    NREGIONPLOT
  };

  //Strip-level plot enumeration.  some are cluster only based and some track, but all for each strip
  enum {
    CHADCALL,
    CHADCMATCH,
    CHSNRALL,
    CHSNRMATCH,
    YALL,
    YMATCH,
    NSTRIPPLOT
  };
    
  
  //How many levels of scaled noise to check
  const unsigned int nNoiseScale = 4;
  const double noiseScales[nNoiseScale] = { 4.0/3.0, 2.0, 3.0, 4.0 };

}

void FullAnalysis::Loop()
{
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   //Create the output file bsaed on environment
   TString myoutdir(getenv("MYOUTPUTPATH"));
   TString biasv(getenv("BIASV"));
   TString f_out = myoutdir + "/FullAnalysis_" + runplace + "_" + m_board + "_" + biasv + "_" + consR + ".root";

   fout = new TFile(f_out,"RECREATE");


   //First prepare the run, this sets beam location and some other things
   PrepareDUT();


   //-------------------------------------------------------------------//
   //------------------ Inclusive histograms here ----------------------//
   //-------------------------------------------------------------------//

   TH1F* hXTrk = new TH1F("XTrk","X position of track",400,-10.0,10.0);
   TH1F* hYTrk = new TH1F("YTrk","Y position of track",400,-10.0,10.0);
   outHistos.push_back( hXTrk );
   outHistos.push_back( hYTrk );
   TH1F* hXTrkMatch = new TH1F("XTrkMatch","X position of track",400,-10.0,10.0);
   TH1F* hYTrkMatch = new TH1F("YTrkMatch","Y position of track",400,-10.0,10.0);
   outHistos.push_back( hXTrkMatch );
   outHistos.push_back( hYTrkMatch );

   TH1F * hStrip = new TH1F("clusterStrip","cluster seed strip",512,-0.5,511.5);
   outHistos.push_back(hStrip);

   TH1F* hXDut = new TH1F("XDut","X position of cluster",400,-10,10);
   outHistos.push_back( hXDut);

   TH1F * hNomStrip = new TH1F("NomStrip","nominal strip",512,-0.5,511.5);
   outHistos.push_back(hNomStrip);

   TProfile * adcvdx = new TProfile("adcvdx","mean adc v. interstrip",95,-0.5,0.5 );
   outHistos.push_back(adcvdx);
   TProfile * sizevdx = new TProfile("sizevdx","mean size v. interstrip",95,-0.5,0.5 );
   outHistos.push_back(sizevdx);

   //X-ray graphs inclusive
   TGraph * grMissed = new TGraph();
   grMissed->SetName("grMissed");
   grMissed->SetTitle( "missed hits");
   grMissed->SetMarkerStyle(1);
   outHistos.push_back(grMissed);

   TGraph * grCenters = new TGraph();
   grCenters->SetName("grCenters");
   grCenters->SetMarkerStyle(1);
   grCenters->SetMarkerColor(kBlue);
   outHistos.push_back(grCenters);

   TGraph * grStartBondPads = new TGraph();
   grStartBondPads->SetName("grBondPadEdge");
   grStartBondPads->SetMarkerStyle(1);
   outHistos.push_back(grStartBondPads);

   //Create the region plots for inclusive events, use these to copy for different regions
   std::vector<TH1 *> inclusivePlots( NREGIONPLOT );
   
   inclusivePlots[CLADCALL] = new TH1F("adcAll","cluster adc;Cluster ADC",100,0,1000);
   inclusivePlots[CLADCMATCH] = new TH1F("adcMatch","cluster adc for matched;Cluster S/N",100,0,50);
   inclusivePlots[CLSNRALL] = new TH1F("snrAll","cluster s/n;Cluster ADC",100,0,1000);
   inclusivePlots[CLSNRMATCH] = new TH1F("snrMatch","cluster s/n for matched;Cluster S/N",100,0,50);
   // 7.581 = 199.5 bins of 38 micron
   inclusivePlots[DXMATCH] = new TH1F("dxMatch","#Delta x (cluster-track) when there is *any* match;#Deltax [mm]",798,-7.581, 7.581 );
   inclusivePlots[DXMISS] = new TH1F("dxMiss","#Delta x (cluster-track) when there is no match;#Deltax [mm]",798,-7.581, 7.581 );;
   inclusivePlots[INTERALL] = new TH1F("interAll","Distance to strip center divided by pitch; #Delta x/P",100,-0.5,0.5);
   inclusivePlots[INTERMATCH] = new TH1F("interMatch","Distance to strip center divided by pitch; #Delta x/P",100,-0.5,0.5);;
   inclusivePlots[YALL] = new TH1F("yAll","All track y; y [mm]",100,-5,5);
   inclusivePlots[YMATCH] = new TH1F("yMatch","Matched track y; y [mm]",100,-5,5);
   inclusivePlots[XALL] = new TH1F("xAll","All track x; x [mm]",40,-1.9,1.9);
   inclusivePlots[XMATCH] = new TH1F("xMatch","Matched track x; x [mm]",40,-1.9,1.9);
   unsigned int hi = 0;
   for(; hi < NEARADC1ALL; ++hi)
     outHistos.push_back( inclusivePlots[hi] );

   unsigned int nreghists = NEARADC1ALL;
   if (fCMS) {     
     nreghists = NREGIONPLOT;
     inclusivePlots[NEARADC1ALL]   = new TH1F("nearADC1All","All track nearest strip ADC; ADC",110,-100,1000);  
     inclusivePlots[NEARADC2ALL]   = new TH1F("nearADC2All","All track nearest 2 strip ADC; ADC",110,-100,1000);
     inclusivePlots[NEARADC4ALL]   = new TH1F("nearADC4All","All track nearest 4 strip ADC; ADC",110,-100,1000);
     inclusivePlots[NEARADC100ALL] = new TH1F("nearADC100All","All track 100 strip ADC; ADC",200,-500,1500);    
     inclusivePlots[NEARADC1MATCH] = new TH1F("nearADC1Match","Match track nearest strip ADC; ADC",110,-100,1000);
     inclusivePlots[NEARADC2MATCH] = new TH1F("nearADC2Match","Match track nearest 2 strip ADC; ADC",110,-100,1000);
     inclusivePlots[NEARADC4MATCH] = new TH1F("nearADC4Match","Match track nearest 4 strip ADC; ADC",110,-100,1000);
     inclusivePlots[NEARADC100MATCH] = new TH1F("nearADC100Match","Match track 100 strip ADC; ADC",200,-500,1500);
     for(; hi < NREGIONPLOT; ++hi)
       outHistos.push_back( inclusivePlots[hi] );
   }

   //Use this to print to for histo names
   char hname[50];

   //Make an x-ray and a set of inclusive plots for each noise level
   std::vector<TGraph* > vNoiseScaleXray(nNoiseScale);
   inclusivePlots.resize( nreghists*( 1 + nNoiseScale ) );
   for (unsigned int ni=0; ni < nNoiseScale; ++ni ) {
     vNoiseScaleXray[ni] = new TGraph();
     outHistos.push_back( vNoiseScaleXray[ni]);
     sprintf(hname,"xray_noise%.1f",noiseScales[ni]);
     vNoiseScaleXray[ni]->SetName(hname);

     for( hi=0; hi < nreghists; ++hi ) {
       sprintf(hname,"%s_noise%.1f", inclusivePlots[hi]->GetName(), noiseScales[ni] );
       inclusivePlots[ hi + nreghists*(ni+1) ] = (TH1*) inclusivePlots[hi]->Clone( hname );
       outHistos.push_back( inclusivePlots[ hi + nreghists*(ni+1)] );
     }

   }

   //Now make a version of the region plots for each defined region and noise scale combination
   std::vector< std::vector<TH1*> > vRegionPlots(nRegions);
   for (unsigned int i =0; i<nRegions; ++i ) {
     vRegionPlots[i].resize( nreghists*(1 + nNoiseScale) );

     for(unsigned int j=0; j<inclusivePlots.size(); ++j) {
       sprintf(hname,"%s_reg%u", inclusivePlots[j]->GetName(), i );
       vRegionPlots[i][ j ] = (TH1*) inclusivePlots[j]->Clone( hname );
       outHistos.push_back( vRegionPlots[i][j] );
     }   
   }
  

   // Make the strip level plots for each channel in the beam location from iLo to iHi
   // these were found in PrepareDUT().  they are floats set to halway between two strips
   int nStripsInBeam = iHi - iLo;
   int firstStrip = iLo +0.51; //make sure we get the first strip inside the range
   std::vector<std::vector<TH1*> > stripPlots( nStripsInBeam );
   //Set up the first channel then copy
   stripPlots[0].resize( NSTRIPPLOTS );
   
   for ( int i =0; i < nStripsInBeam; ++i ) {
     stripPlots[i].resize( NSTRIPPLOTS );
     
     for(unsigned int j=0; j<NSTRIPPLOTS; ++j) {
       sprintf(hname,"%s


   int njump = 10000;   
   if(nentries > 100000) njump = 50000;
   Long64_t nbytes = 0, nb = 0;
   cout << "Begin loop over " << nentries << " events" << endl;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      if(jentry%njump==0) cout << "====> At entry = " << jentry << endl;

      //Only consider events with 1 track
      if(n_tp3_tracks > 1) continue;

      //------------- Loop over TPIX tracks in event ---------------//
      //------------------------------------------------------------//
      for(int k=0; k<n_tp3_tracks; k++){
        if(dtime > trackTriggerTimeDiffCut) continue;

        //Get the coordinates to use
        double x_trk = vec_trk_tx->at(k)*z_DUT+vec_trk_x->at(k);
        double y_trk = vec_trk_ty->at(k)*z_DUT+vec_trk_y->at(k);
        double nomStrip, detStrip;
        transformTrackToDUTFrame( k, x_trk, y_trk, nomStrip, detStrip );

        hXTrk->Fill(x_trk);
        hYTrk->Fill(y_trk);

        double tx = 1000*vec_trk_tx->at(k);
        double ty = 1000*vec_trk_ty->at(k);

        
        //Fill the nominal strip track should hit
        hNomStrip->Fill(nomStrip);

        // distance to closest integer
        int iNom = nomStrip;
        //        double dxNom = nomStrip -  ((double) iNom);
        double dxNom = nomStrip - iNom - 0.5;
        if ( dxNom > 0.5 ) dxNom-=1.;


        //Keep a graph of where the strips are for visualization
        if ( fabs(dxNom) > 0.48 ) grCenters->SetPoint(grCenters->GetN(), x_trk, y_trk );

        if( passFiducialCut( 0,  x_trk, y_trk, dxNom, nomStrip )  )
          grStartBondPads->SetPoint( grStartBondPads->GetN(), x_trk, y_trk);

        // Exclude found dead regions
        bool goodRegion = true;
        for(int id = 0; id<nDeadRegion; id++){
          if(x_trk>=deadRegionLo[id]  && x_trk<=deadRegionHi[id]) goodRegion = false;  
        }
        if(!goodRegion) continue;


        int idetStrip = detStrip + 0.5;
        if(idetStrip>=1 && idetStrip<=nChan-2 && (badStrips[idetStrip]==0 || badStrips[idetStrip-1]==0 || badStrips[idetStrip+1]==0))
          continue;

        //Check that the track passes our cuts
        bool goodTrack = false;
        bool inFiducialX = false;
        bool inFiducialY = false;
        if(x_trk>xMin && x_trk<xMax ) inFiducialX = true;          
        if(y_trk>yMin && y_trk<yMax + 1.) inFiducialY = true;          
        bool inFiducial = inFiducialX && inFiducialY && (x_trk<xLeftHole || x_trk>xRightHole) && inFiducialRegion(x_trk, y_trk);
        
        if(tx>txMin && tx<txMax && ty>tyMin && ty<tyMax) goodTrack = true;        
        
        bool goodTime =  (clustersTDC >= tdcLo && clustersTDC <= tdcHi);

        //all good?
        if( !goodTrack || !inFiducial || !goodTime ) continue;

        //Things to fill for all good tracks, inclusive
        inclusivePlots[INTERALL]->Fill(dxNom);
        inclusivePlots[YALL]->Fill(y_trk);
        inclusivePlots[XALL]->Fill(x_trk);
        
        double nearADC = 0;
        double twonearADC = 0;
        double sumADC = 0;
        double fournearADC = 0;
        if( fCMS != 0  ) {
          nearADC = (dxNom > 0) ? polarity*fCMS->cmsData[iNom] : polarity*fCMS->cmsData[iNom+1];
          twonearADC = polarity*( fCMS->cmsData[iNom] + fCMS->cmsData[iNom+1] );
          fournearADC = polarity*( fCMS->cmsData[iNom-1] + fCMS->cmsData[iNom] + fCMS->cmsData[iNom+1] + fCMS->cmsData[iNom+2] );
          
          unsigned int lowstrip = (iNom > 50) ? iNom-50 : 0;
          for(unsigned int j = lowstrip; j < lowstrip+100; ++j ) {
            sumADC += polarity*fCMS->cmsData[j];
          }

          inclusivePlots[NEARADC1ALL]->Fill( nearADC );
          inclusivePlots[NEARADC2ALL]->Fill( twonearADC );
          inclusivePlots[NEARADC4ALL]->Fill( fournearADC );
          inclusivePlots[NEARADC100ALL]->Fill( sumADC );
        }

        //Noise variations
        for( unsigned int ni=0; ni < nNoiseScale; ++ni ) {
          inclusivePlots[INTERALL + nreghists*(ni+1)]->Fill(dxNom);
          inclusivePlots[YALL + nreghists*(ni+1)]->Fill(y_trk);
          inclusivePlots[XALL + nreghists*(ni+1)]->Fill(x_trk);
          if(fCMS) {
            inclusivePlots[NEARADC1ALL + nreghists*(ni+1)]->Fill( nearADC );
            inclusivePlots[NEARADC2ALL + nreghists*(ni+1)]->Fill( twonearADC );
            inclusivePlots[NEARADC4ALL + nreghists*(ni+1)]->Fill( fournearADC );
            inclusivePlots[NEARADC100ALL + nreghists*(ni+1)]->Fill( sumADC );
          }
        }

        
        //----------- Iterate over the found clusters in the event -----------//
        bool foundHit = false;
        int foundIdx = -1;
        double foundDx = -1e6;
        
        int nClusters = min((int)clusterNumberPerEvent,10);
        std::vector<double> allDx;
        for(int j=0; j<nClusters; j++){
          if(clustersPosition[j] < 0.1) continue;

          // Load the current cluster information
          double position = clustersPosition[j];
          int charge = clustersCharge[j]; 
          int seedPosition = clustersSeedPosition[j];
          int size = clustersSize[j];
          int seedCharge = clustersSeedCharge[j];
          int charge2StripLeft	= polarity*clustersCharge2StripLeft[j];
          int charge1StripLeft	= polarity*clustersCharge1StripLeft[j];
          int charge1StripRight	= polarity*clustersCharge1StripRight[j];
          int charge2StripRight	= polarity*clustersCharge2StripRight[j];
           
          //check for a good hit location
          if( !(position>(iLo-2) && position<(iHi+2)) ) continue;
          if(badStrips[seedPosition]==0) continue;

          inclusivePlots[CLADCALL]->Fill(charge);
          for( unsigned int ni=0; ni < nNoiseScale; ++ni ) {
            if(foundClusterWithScaledNoise( j, noiseScales[ni] ) )
              inclusivePlots[CLADCALL + nreghists*(ni+1)]->Fill(charge);
          }

          hStrip->Fill(position);

          bool deadStrip = false;
          
          // --- in the case of D sensors, the position needs to be shifted --- //
          double pos = getCorrChannel(position);

          // Detector x-coordinate
          double x_dut = getDUTHitPosition( j );
          hXDut->Fill(x_dut);
          
          // Difference between the track x and detector x
          double dx = x_dut - x_trk;
          allDx.push_back(dx);
          
          if(fabs(dx)<dxWin && fabs(dx) < fabs(foundDx)) {
            foundHit = true;
            foundIdx = j;
            foundDx = dx;
          }          

        }


        //Fill the really inclusive xy plot and the xrays here
        if(foundHit) {
          hXTrkMatch->Fill(x_trk);
          hYTrkMatch->Fill(y_trk);

          adcvdx->Fill( dxNom, clustersCharge[foundIdx] );
          sizevdx->Fill( dxNom, clustersSize[foundIdx] );

          for(size_t ni=0; ni < nNoiseScale; ++ni ) {
            if(!foundClusterWithScaledNoise( foundIdx, noiseScales[ni] ) )
            vNoiseScaleXray[ni]->SetPoint( vNoiseScaleXray[ni]->GetN(), x_trk, y_trk );
          }
        } else {
          //Fill all the x-ray plots if we don't find it at all
          grMissed->SetPoint( grMissed->GetN(), x_trk, y_trk );
          for(size_t ni=0; ni < nNoiseScale; ++ni ) {
            vNoiseScaleXray[ni]->SetPoint( vNoiseScaleXray[ni]->GetN(), x_trk, y_trk );
          }
        }

        fillMatchMiss( inclusivePlots, nreghists, foundHit, foundIdx, x_trk, y_trk, dxNom, allDx, nearADC,  twonearADC,  fournearADC,  sumADC);


        for(unsigned int ri = 0; ri< nRegions; ++ri ) {
          if(! passFiducialCut( ri, x_trk, y_trk, dxNom, nomStrip ) ) continue;

          vRegionPlots[ri][INTERALL]->Fill(dxNom);
          vRegionPlots[ri][YALL]->Fill(y_trk);
          vRegionPlots[ri][XALL]->Fill(x_trk);
          if( fCMS != 0  ) {

            vRegionPlots[ri][NEARADC1ALL]->Fill( nearADC );
            vRegionPlots[ri][NEARADC2ALL]->Fill( twonearADC );
            vRegionPlots[ri][NEARADC4ALL]->Fill( fournearADC );
            vRegionPlots[ri][NEARADC100ALL]->Fill( sumADC );
          }

          //Noise variations
          for( unsigned int ni=0; ni < nNoiseScale; ++ni ) {
            vRegionPlots[ri][INTERALL + nreghists*(ni+1)]->Fill(dxNom);
            vRegionPlots[ri][YALL + nreghists*(ni+1)]->Fill(y_trk);
            vRegionPlots[ri][XALL + nreghists*(ni+1)]->Fill(x_trk);
            if(fCMS) {
              vRegionPlots[ri][NEARADC1ALL + nreghists*(ni+1)]->Fill( nearADC );
              vRegionPlots[ri][NEARADC2ALL + nreghists*(ni+1)]->Fill( twonearADC );
              vRegionPlots[ri][NEARADC4ALL + nreghists*(ni+1)]->Fill( fournearADC );
              vRegionPlots[ri][NEARADC100ALL + nreghists*(ni+1)]->Fill( sumADC );
            }
          }


          fillMatchMiss( vRegionPlots[ri], nreghists, foundHit, foundIdx, x_trk, y_trk, dxNom, allDx, nearADC,  twonearADC,  fournearADC,  sumADC);

	} //loop over regions


      } //loop tracks

   } //loop entries
   
   
   writeHistos();
}



void FullAnalysis::writeHistos() {

  fout->cd();
  for ( size_t i=0; i<outHistos.size(); ++i ) {
    outHistos[i]->Write();
  }
  fout->Close();
}

bool FullAnalysis::foundClusterWithScaledNoise( size_t idx, double nScale) {

  // guess 3*noise high cut and 2.5* noise low cut

  // think about how to reimplement -- if its just whether you pass or not just need to check the seed passes new threshold.  but if we care about 1->2 strip clutsers could repurpose this function

  return fabs(clustersSeedCharge[idx]) > 3*nScale*hWidthNoise->GetBinContent( clustersSeedPosition[idx] );


}

void FullAnalysis::fillMatchMiss( const std::vector<TH1*> & vh, unsigned int nhists, bool foundHit, int foundIdx, double x_trk, double y_trk, double dxNom, const std::vector<double> & allDx, double nearADC, double twonearADC, double fournearADC, double sumADC) {

  //Fill the matching histograms now
  if(foundHit) {
    vh[CLADCMATCH]->Fill(clustersCharge[foundIdx]);
            
    for(size_t ci=0; ci<allDx.size(); ++ci)
      vh[DXMATCH]->Fill( allDx[ci]);

    vh[INTERMATCH]->Fill(dxNom);
    vh[YMATCH]->Fill(y_trk);
    vh[XMATCH]->Fill(x_trk);
    if (fCMS) {   
      vh[NEARADC1MATCH]->Fill( nearADC );
      vh[NEARADC2MATCH]->Fill( twonearADC );
      vh[NEARADC4MATCH]->Fill( fournearADC );
      vh[NEARADC100MATCH]->Fill( sumADC );
    }

    //Fill as if missing if the seed fails the new cut on noise,
    //otherwise fill the plots for inclusive version of noise
    for(size_t ni=0; ni < nNoiseScale; ++ni ) {
      if( !foundClusterWithScaledNoise( foundIdx, noiseScales[ni] ) ) {
              
        //This plot is still broken until i have a good way of checking the dxlist for passing clusters
        for(size_t ci=0; ci<allDx.size(); ++ci)
          vh[DXMISS + nhists*(ni+1)]->Fill( allDx[ci]);

      } else {

        vh[CLADCMATCH + nhists*(ni+1)]->Fill(clustersCharge[foundIdx]);
       
        //This plot is still broken until i have a good way of checking the dxlist for passing clusters
        for(size_t ci=0; ci<allDx.size(); ++ci)
          vh[DXMATCH + nhists*(ni+1)]->Fill( allDx[ci]);

        vh[INTERMATCH + nhists*(ni+1)]->Fill(dxNom);
        vh[YMATCH + nhists*(ni+1)]->Fill(y_trk);
        vh[XMATCH + nhists*(ni+1)]->Fill(x_trk);
        if (fCMS) {   
          vh[NEARADC1MATCH + nhists*(ni+1)]->Fill( nearADC );
          vh[NEARADC2MATCH + nhists*(ni+1)]->Fill( twonearADC );
          vh[NEARADC4MATCH + nhists*(ni+1)]->Fill( fournearADC );
          vh[NEARADC100MATCH + nhists*(ni+1)]->Fill( sumADC );
        }

      }
    }


  } else { //no match found
    for(size_t ci=0; ci<allDx.size(); ++ci)
      vh[DXMISS]->Fill( allDx[ci]);
 
  }

}
