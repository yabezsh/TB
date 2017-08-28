#define SummaryAnalysis_cxx
#include "SummaryAnalysis.h"
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
    N8, N9, P1, N3M1, N3M6, N4M1, N4M6, N6M1, N6M6, N3M2, N3M7, N7M2, N4M7, N6M2, N6M7, NSENSOR };
  const TString boardNames[NSENSOR] = { "N_8", "N_9", "P_1", "N_3_mini1", "N_3_mini6", "N_4_mini1", "N_4_mini6",
                                        "N_6_mini1", "N_6_mini6", "N_3_mini2", "N_3_mini7", 
                                        "N_7_mini2", "N_4_mini7", "N_6_mini2", "N_6_mini7" };
  //For all sensors, the last channel bonded is also the last on the sensor.
  double lastChan[NSENSOR] = { 469, 466, 383, 486, 230, 478, 224, 500,243, 511, 191, 447, 193, 453, 200};
  
  int getBoardIndex(const TString & boardname ){
    // TObjString * os = (TObjString*) boardname.Tokenize("_")->At(0);
    // TString newstring(os->GetString());
    
    for ( unsigned int i=0; i< NSENSOR; ++i ) {
      if (boardname == boardNames[i] )
        return i;
    }

    return -1;
  }
    

  //Easy method to add additional cuts to inclusive fiducial region
  bool inFiducialRegion(  const double & xTrk, const double & yTrk ) {
    return true;
  }
  
  // Make regions
  // 0 = very top edge of sensors
  // 1 = control region for top edge
  // 2 = close to top edge
  // 3 = control region for above
  // 4 = Densest PA region ( traces for fan-up, bond pads for fan-in )
  // 5 = Control region for 2
  // 6-11 = region 0-5 and between strips
  // 12-17 = region 0-5 and under strip
  const unsigned int nCuts=6;
  const unsigned int nRegions= 3*nCuts;
  bool passFiducialCut( const int & iCut, const double & xTrk, const double & yTrk, const double &dxNom, const double & nomStrip, const double & yMax ) 
  {

    if ( yTrk > yMax ) return false;

    // this defines cut based on dx
    int dxGroup = iCut / nCuts;   
    bool dxcent = fabs(dxNom) < 0.1;
    bool dxout = fabs(dxNom) > 0.4;
    if ( dxGroup == 1 && !dxcent ) {
      return false;
    } else if (dxGroup == 2 && !dxout) {
      return false;
    }

    //Now do the actual regions
    int myCut = iCut % nCuts;
    
    double dy = yMax - yTrk;
    bool inReg[nCuts];
    inReg[0] = (dy<0.02);
    inReg[1] = (dy>0.8) && (dy<1.3);
    inReg[2] = (dy > 0.04) && (dy < 0.5);
    inReg[3] = inReg[1];

    if ( myCut < 4 ) {
      return inReg[myCut];
    }
    
    // PA regions take a bit more doing
    int boardIdx = getBoardIndex(m_board);
    bool isMini = (boardIdx > 1);
    double sensorStrip = nomStrip - lastChan[boardIdx]; // negative from right side of sensor
    if ( !isMini ) {
      sensorStrip += 511; //now starts from 0
      //Find the thickest part of the PA region
      double r = fmod( sensorStrip, 128 ); //get the remainder after dividing by 128
      bool inPAx = ( r > 24 && r < 48 ) || ( r > 80 && r < 104 );

      inReg[4] = (dy > 0.04) && (dy < 0.5) && inPAx;
      inReg[5] = (dy > 0.8) && (dy < 1.3) && inPAx;
      
    } else {
      sensorStrip += 63; //now starts form 0
      bool isFanin = (boardIdx > N6M6);
      if (isFanin) {
        inReg[4] = (dy>0.9) && (dy<1.1) && (sensorStrip < 27 );
        inReg[5] = (dy>1.5) && (dy<1.7) && (sensorStrip < 27 );
      } else {
        inReg[4] = (sensorStrip > 24) && (sensorStrip < 48) && (dy > 0.04) && (dy<0.5);
        inReg[5] = (sensorStrip > 24) && (sensorStrip < 48) && (dy > 0.8) && (dy<1.3);
      }      
    }

    return inReg[myCut];
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
    NOMSTRIPALL,
    NOMSTRIPMATCH,
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
    CHYALL,
    CHYMATCH,
    NSTRIPPLOT
  };
    
  const char * stripPlotNames[NSTRIPPLOT] = {"adcAll", "adcMatch", "snrAll", "snrMatch", "yAll", "yMatch"};
 
  //How many levels of scaled noise to check
  const unsigned int nNoiseScale = 4;
  const double noiseScales[nNoiseScale] = { 4.0/3.0, 2.0, 3.0, 4.0 };

  //strips to investigate their cluster size
  const int nOddStrips = 7;
  int oddStrips[nOddStrips] = {414,420,422,424,434,436,449};
  enum {
    ODDADC,
    ODDSIZE,
    ODDASYMM,
    ODDPARTNERS,
    ODDDX,
    NODD
  };
  const char * oddPlotNames[NODD] = {"adc","size","asymm","partners","dx"};
}

void SummaryAnalysis::Loop()
{
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   //Create the output file bsaed on environment
   TString myoutdir(getenv("MYOUTPUTPATH"));
   TString f_out = myoutdir + "/" + m_board + "/output_" + consR + "/SummaryAnalysis_" + m_board + "_" + consR + ".root";

   //First prepare the run, this sets beam location and some other things
   PrepareDUT();


   fout = new TFile(f_out,"RECREATE");


   //-------------------------------------------------------------------//
   //------------------ Inclusive histograms here ----------------------//
   //-------------------------------------------------------------------//

   TH1F* hXTrk = new TH1F("XTrk","X position of track; x [mm]",400,-10.0,10.0);
   TH1F* hYTrk = new TH1F("YTrk","Y position of track; y [mm]",400,-10.0,10.0);
   //outHistos.push_back( hXTrk );
   //outHistos.push_back( hYTrk );
   TH1F* hXTrkMatch = new TH1F("XTrkMatch","X position of track; x [mm]",400,-10.0,10.0);
   TH1F* hYTrkMatch = new TH1F("YTrkMatch","Y position of track; y [mm]",400,-10.0,10.0);
   //outHistos.push_back( hXTrkMatch );
   //outHistos.push_back( hYTrkMatch );

   //Keep an eye on beam shape
   TH2F* hXYTrk = new TH2F("XYTrk","X,Y position of track; x [mm]; y[mm]",50, -25.0*stripPitch, 25.0*stripPitch, 60, -2, 4);
   //outHistos.push_back( hXYTrk );
   TH2F* hStripYTrk = new TH2F("StripYTrk","strip,Y position of track; Channel #; y [mm]", 512,-0.5,511.5, 60, -2,4);
   //outHistos.push_back( hStripYTrk );
   
   TH1F * hStrip = new TH1F("clusterStrip","cluster seed strip",512,-0.5,511.5);
   //outHistos.push_back(hStrip);

   TH1F* hXDut = new TH1F("XDut","X position of cluster",100, -50.0*stripPitch, 50.0*stripPitch);
   //outHistos.push_back( hXDut);

   TH1F * hNomStrip = new TH1F("NomStrip","nominal strip",512,-0.5,511.5);
   //outHistos.push_back(hNomStrip);

   TProfile * adcvdx = new TProfile("adcvdx","mean adc v. interstrip",95,-0.5,0.5 );
   //outHistos.push_back(adcvdx);
   TProfile * sizevdx = new TProfile("sizevdx","mean size v. interstrip",95,-0.5,0.5 );
   TProfile * sizevstrip = new TProfile("sizevstrip","mean size v. channel; Channel; <Cluster size>",512,-0.5,511.5);
   //outHistos.push_back(sizevdx);

   //X-ray graphs inclusive
   TGraph * grMissed = new TGraph();
   grMissed->SetName("grMissed");
   grMissed->SetTitle( "missed hits");
   grMissed->SetMarkerStyle(1);
   outHistos.push_back(grMissed);
   
   TGraph * grMissedStrips = new TGraph();
   grMissedStrips->SetName("grMissedStrips");
   grMissedStrips->SetTitle( "missed hits");
   grMissedStrips->SetMarkerStyle(1);
   outHistos.push_back(grMissedStrips);

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
   inclusivePlots[CLADCMATCH] = new TH1F("adcMatch","cluster adc for matched;Cluster ADC",100,0,1000);
   inclusivePlots[CLSNRALL] = new TH1F("snrAll","cluster s/n;Cluster S/N",100,0,50);
   inclusivePlots[CLSNRMATCH] = new TH1F("snrMatch","cluster s/n for matched;Cluster S/N",100,0,50);
   // 7.581 = 199.5 bins of 38 micron
   inclusivePlots[DXMATCH] = new TH1F("dxMatch","#Delta x (cluster-track) when there is *any* match;#Deltax [mm]",798,-7.581, 7.581 );
   inclusivePlots[DXMISS] = new TH1F("dxMiss","#Delta x (cluster-track) when there is no match;#Deltax [mm]",798,-7.581, 7.581 );;
   inclusivePlots[INTERALL] = new TH1F("interAll","Distance to strip center divided by pitch; #Delta x/P",100,-0.5,0.5);
   inclusivePlots[INTERMATCH] = new TH1F("interMatch","Distance to strip center divided by pitch; #Delta x/P",100,-0.5,0.5);;
   inclusivePlots[YALL] = new TH1F("yAll","All track y; y [mm]",360, -4.5,4.5);
   inclusivePlots[YMATCH] = new TH1F("yMatch","Matched track y; y [mm]",360,-4.5,4.5);
   inclusivePlots[XALL] = new TH1F("xAll","All track x; x [mm]",100, -25.0*stripPitch, 25.0*stripPitch);
   inclusivePlots[XMATCH] = new TH1F("xMatch","Matched track x; x [mm]",100, -25.0*stripPitch, 25.0*stripPitch);
   inclusivePlots[NOMSTRIPALL] = new TH1F("stripAll","All trk strip; Channel #",1024, -0.25, 512-0.25);
   inclusivePlots[NOMSTRIPMATCH] = new TH1F("stripMatch","All trk strip; Channel #",1024, -0.25, 512-0.25);
   unsigned int hi = 0;
   //for(; hi < NEARADC1ALL; ++hi)
     //outHistos.push_back( inclusivePlots[hi] );

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
     //for(; hi < NREGIONPLOT; ++hi)
       //outHistos.push_back( inclusivePlots[hi] );
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
       //outHistos.push_back( inclusivePlots[ hi + nreghists*(ni+1)] );
     }

   }

   //Now make a version of the region plots for each defined region and noise scale combination
   std::vector< std::vector<TH1*> > vRegionPlots(nRegions);
   for (unsigned int i =0; i<nRegions; ++i ) {
     //make an output directory
     sprintf(hname,"Region_%i",i);
     TDirectory * newdir = fout->mkdir( hname );
     newdir->cd();

     vRegionPlots[i].resize( nreghists*(1 + nNoiseScale) );

     for (unsigned int j=0; j<inclusivePlots.size(); ++j) {
       sprintf(hname,"%s_reg%u", inclusivePlots[j]->GetName(), i );
       vRegionPlots[i][ j ] = (TH1*) inclusivePlots[j]->Clone( hname );
       //outHistos.push_back( vRegionPlots[i][j] );
     }   
   }

   //Now make a version with a tight cut on track timing
   std::vector<TH1*> vTightTiming;
   vTightTiming.resize( nreghists*(1 + nNoiseScale) );
   TDirectory * tightdir = fout->mkdir( "TightTime");
   tightdir->cd();
   for (unsigned int j=0; j<inclusivePlots.size(); ++j) {
     sprintf(hname,"%s_tightTime", inclusivePlots[j]->GetName() );
     vTightTiming[ j ] = (TH1*) inclusivePlots[j]->Clone( hname );
     //outHistos.push_back( vRegionPlots[i][j] );
   }   

   // Make the strip level plots for each channel in the beam location from iLo to iHi
   // these were found in PrepareDUT().  they are floats set to halway between two strips
   // For ADC and SNR *ALL* the strip is defined based on cluster seed strip
   // For the rest its always based on the track -- so you can do y efficiency w/o worrying about migration
   int nStripsInBeam = iHi - iLo;
   int firstStrip = iLo +0.51; //make sure we get the first strip inside the range
   std::vector<std::vector<TH1*> > stripPlots( nStripsInBeam );
   TDirectory * newdir = fout->mkdir( "Strips");
   newdir->cd();
   for ( int i =0; i < nStripsInBeam; ++i ) {     
     stripPlots[i].resize( NSTRIPPLOT );
     sprintf( hname, "%s_ch%i", stripPlotNames[CHADCALL], firstStrip+i);
     stripPlots[i][CHADCALL] = new TH1F(hname,"ADC all for channel; Cluster ADC", 100, 0, 1000);
     sprintf( hname, "%s_ch%i", stripPlotNames[CHADCMATCH], firstStrip+i);
     stripPlots[i][CHADCMATCH] = new TH1F(hname,"ADC match for channel; Cluster ADC", 100, 0, 1000);
     sprintf( hname, "%s_ch%i", stripPlotNames[CHSNRALL], firstStrip+i);
     stripPlots[i][CHSNRALL] = new TH1F(hname, "S/N all for channel; Cluster S/N", 100, 0, 50);
     sprintf( hname, "%s_ch%i", stripPlotNames[CHSNRMATCH], firstStrip+i);
     stripPlots[i][CHSNRMATCH] = new TH1F(hname, "S/N match for channel; Cluster S/N", 100, 0, 50);
     sprintf( hname, "%s_ch%i", stripPlotNames[CHYALL], firstStrip+i);
     stripPlots[i][CHYALL] = new TH1F(hname, "Y all for channel; y_{trk} [mm]", 40, -10., 10.);
     sprintf( hname, "%s_ch%i", stripPlotNames[CHYMATCH], firstStrip+i);
     stripPlots[i][CHYMATCH] = new TH1F(hname, "Y match for channel; y_{trk} [mm]", 40, -10., 10.); 
     for(unsigned int j=0; j<NSTRIPPLOT; ++j) {
       //outHistos.push_back( stripPlots[i][j] );
     }       
   }

   std::vector<std::vector<TH1*> > oddPlots( nOddStrips );
   newdir = fout->mkdir( "OddStrips");
   newdir->cd();
   for ( int i =0; i < nOddStrips; ++i ) {     
     oddPlots[i].resize( NODD );
     sprintf( hname, "%s_ch%i", oddPlotNames[ODDADC], oddStrips[i] );
     oddPlots[i][ODDADC] = new TH1F(hname,"ADC match for channel; Cluster ADC", 100, 0, 1000);
     sprintf( hname, "%s_ch%i", oddPlotNames[ODDSIZE], oddStrips[i] );
     oddPlots[i][ODDSIZE] = new TH1F(hname,"ADC match for channel; N channel", 10, 0.5, 10.5);
     sprintf( hname, "%s_ch%i", oddPlotNames[ODDASYMM], oddStrips[i] );
     oddPlots[i][ODDASYMM] = new TH1F(hname,"ADC match for channel; Seed fraction", 100, 0, 1);
     sprintf( hname, "%s_ch%i", oddPlotNames[ODDPARTNERS], oddStrips[i] );
     oddPlots[i][ODDPARTNERS] = new TH1F(hname,"ADC match for channel; Partner", 5, -2.5, 2.5);
     sprintf( hname, "%s_ch%i", oddPlotNames[ODDDX], oddStrips[i] );
     oddPlots[i][ODDDX] = new TH1F(hname,"DX match for channel; Cluster #DeltaX", 100, -0.250, 0.25);
   }
   
   int njump = 10000;   
   if(nentries > 100000) njump = 50000;
   Long64_t nbytes = 0, nb = 0;
   cout << "Begin loop over " << nentries << " events" << endl;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      if(jentry%njump==0) cout << "====> At entry = " << jentry << endl;

      //Only consider events with 1 track and 10 or less clusters
      if(n_tp3_tracks > 1 || clusterNumberPerEvent > 10) continue;

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
        hXYTrk->Fill(x_trk,y_trk);

        double tx = 1000*vec_trk_tx->at(k);
        double ty = 1000*vec_trk_ty->at(k);

        
        //Fill the nominal strip track should hit
        hNomStrip->Fill(nomStrip);
        hStripYTrk->Fill(nomStrip,y_trk);
        
        // nom strip is a float. now we want the interstrip position
        // 0 = halfway between two strips
        // -0.5 lower strip, 0.5 higher strip
        int iNom = nomStrip;
        double dxNom = nomStrip - iNom - 0.5;
        //this is the closest strip to the track
        int closeStrip = (dxNom > 0) ? iNom + 1 : iNom;


        //Keep a graph of where the strips are for visualization
        if ( fabs(dxNom) > 0.48 ) grCenters->SetPoint(grCenters->GetN(), x_trk, y_trk );

        if( passFiducialCut( 4,  x_trk, y_trk, dxNom, nomStrip, yMax )  )
          grStartBondPads->SetPoint( grStartBondPads->GetN(), x_trk, y_trk);

        // Exclude found dead regions
        bool goodRegion = true;
        for(int id = 0; id<nDeadRegion; id++){
          if(x_trk>=deadRegionLo[id]  && x_trk<=deadRegionHi[id]) goodRegion = false;  
        }
        if(!goodRegion) continue;


        //Bad strip cut
        int idetStrip = detStrip + 0.5;
        
        
        if(idetStrip>=1 && idetStrip<=nChan-2 && (badStrips[idetStrip]==0 || badStrips[idetStrip-1]==0 || badStrips[idetStrip+1]==0))
          continue;

        //Check that the track passes our cuts
        bool goodTrack = false;
        bool inFiducialX = false;
        bool inFiducialY = false;
        bool inTightFiducialY = false;
        if(x_trk>xMin && x_trk<xMax ) inFiducialX = true;          
        if(y_trk>yMin && y_trk<yMax + 1.) inFiducialY = true;   
        if(y_trk>yMin && y_trk<yMax - 0.02) inTightFiducialY = true;
        bool inFiducial = inFiducialX && inFiducialY && (x_trk<xLeftHole || x_trk>xRightHole) && inFiducialRegion(x_trk, y_trk);
        
        //Cuts on track angle
        if(tx>txMin && tx<txMax && ty>tyMin && ty<tyMax) goodTrack = true;        
        
        bool goodTime =  (clustersTDC >= tdcLo && clustersTDC <= tdcHi);

        //all good?
        if( !goodTrack || !inFiducial || !goodTime ) continue;

        //Things to fill for all good tracks, inclusive
        inclusivePlots[YALL]->Fill(y_trk);
        if ( dtime < 1.0 )
          vTightTiming[YALL]->Fill(y_trk);
        int stripIdx = closeStrip - firstStrip;
        if( stripIdx >= 0 && stripIdx < nStripsInBeam ) {
          stripPlots[ stripIdx ][CHYALL]->Fill(y_trk);
        }
        double nearADC = 0;
        double twonearADC = 0;
        double sumADC = 0;
        double fournearADC = 0;

        if (inTightFiducialY) {
          inclusivePlots[INTERALL]->Fill(dxNom);
          inclusivePlots[XALL]->Fill(x_trk);
          inclusivePlots[NOMSTRIPALL]->Fill(nomStrip);

          if ( dtime < 1.0 ) {
            vTightTiming[INTERALL]->Fill(dxNom);
            vTightTiming[XALL]->Fill(x_trk);
            vTightTiming[NOMSTRIPALL]->Fill(nomStrip);
          }
          
          if( fCMS != 0  ) {
            nearADC = polarity*fCMS->cmsData[closeStrip];
            twonearADC = nearADC;
            if( iNom < inChan-1 )
              twonearADC = polarity*( fCMS->cmsData[iNom] + fCMS->cmsData[iNom+1] );

            fournearADC = twonearADC;
            if( iNom < inChan-2) 
              fournearADC += polarity*fCMS->cmsData[iNom+2];
            if( iNom > 0 )
              fournearADC += polarity* fCMS->cmsData[iNom-1];

            unsigned int lowstrip = (iNom > 50) ? iNom-50 : 0;
            for(unsigned int j = lowstrip; j < lowstrip+100; ++j ) {
              sumADC += polarity*fCMS->cmsData[j];
            }

            inclusivePlots[NEARADC1ALL]->Fill( nearADC );
            inclusivePlots[NEARADC2ALL]->Fill( twonearADC );
            inclusivePlots[NEARADC4ALL]->Fill( fournearADC );
            inclusivePlots[NEARADC100ALL]->Fill( sumADC );
            if ( dtime < 1.0 ) {
              vTightTiming[NEARADC1ALL]->Fill( nearADC );
              vTightTiming[NEARADC2ALL]->Fill( twonearADC );
              vTightTiming[NEARADC4ALL]->Fill( fournearADC );
              vTightTiming[NEARADC100ALL]->Fill( sumADC );
            }
          }

          //Noise variations
          for( unsigned int ni=0; ni < nNoiseScale; ++ni ) {
            inclusivePlots[YALL + nreghists*(ni+1)]->Fill(y_trk);
            inclusivePlots[INTERALL + nreghists*(ni+1)]->Fill(dxNom);
            inclusivePlots[XALL + nreghists*(ni+1)]->Fill(x_trk);
            inclusivePlots[NOMSTRIPALL + nreghists*(ni+1)]->Fill(nomStrip);
            if(fCMS) {
              inclusivePlots[NEARADC1ALL + nreghists*(ni+1)]->Fill( nearADC );
              inclusivePlots[NEARADC2ALL + nreghists*(ni+1)]->Fill( twonearADC );
              inclusivePlots[NEARADC4ALL + nreghists*(ni+1)]->Fill( fournearADC );
              inclusivePlots[NEARADC100ALL + nreghists*(ni+1)]->Fill( sumADC );
            }
            if ( dtime < 1.0 ) {
              vTightTiming[YALL + nreghists*(ni+1)]->Fill(y_trk);
              vTightTiming[INTERALL + nreghists*(ni+1)]->Fill(dxNom);
              vTightTiming[XALL + nreghists*(ni+1)]->Fill(x_trk);
              vTightTiming[NOMSTRIPALL + nreghists*(ni+1)]->Fill(nomStrip);
              if(fCMS) {
                vTightTiming[NEARADC1ALL + nreghists*(ni+1)]->Fill( nearADC );
                vTightTiming[NEARADC2ALL + nreghists*(ni+1)]->Fill( twonearADC );
                vTightTiming[NEARADC4ALL + nreghists*(ni+1)]->Fill( fournearADC );
                vTightTiming[NEARADC100ALL + nreghists*(ni+1)]->Fill( sumADC );
              }
            }
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

          if(applyClusterCorrection) correctCluster(j);

          // Load the current cluster information
          double position = clustersPosition[j];
          int charge = polarity*clustersCharge[j]; 
          int seedPosition = clustersSeedPosition[j];
          int size = clustersSize[j];
          int seedCharge = polarity*clustersSeedCharge[j];
          int charge2StripLeft	= polarity*clustersCharge2StripLeft[j];
          int charge1StripLeft	= polarity*clustersCharge1StripLeft[j];
          int charge1StripRight	= polarity*clustersCharge1StripRight[j];
          int charge2StripRight	= polarity*clustersCharge2StripRight[j];
           
          //Simple plot of hit strips
          hStrip->Fill(position);

          float seedNoise = noise[seedPosition];

          //check for a good hit location
          if( !(position>(iLo-2) && position<(iHi+2)) ) continue;
          if(badStrips[seedPosition]==0) continue;

          inclusivePlots[CLADCALL]->Fill(charge);
          inclusivePlots[CLSNRALL]->Fill(float(charge)/seedNoise);
          if ( dtime < 1.0 ) {
            vTightTiming[CLADCALL]->Fill(charge);
            vTightTiming[CLSNRALL]->Fill(float(charge)/seedNoise);
          }
          int clusterStripIdx = seedPosition - firstStrip;
          if ( clusterStripIdx >=0 && clusterStripIdx < nStripsInBeam ) {
            stripPlots[clusterStripIdx][CHADCALL]->Fill( charge );
            stripPlots[clusterStripIdx][CHSNRALL]->Fill( float(charge)/seedNoise );
          }

          for(unsigned int ri = 0; ri< nRegions; ++ri ) {
            if(! passFiducialCut( ri, x_trk, y_trk, dxNom, nomStrip, yMax ) ) continue;
            vRegionPlots[ri][CLADCALL]->Fill(charge);
            vRegionPlots[ri][CLSNRALL]->Fill(float(charge)/seedNoise);
          }
            
          for( unsigned int ni=0; ni < nNoiseScale; ++ni ) {
            if(foundClusterWithScaledNoise( j, noiseScales[ni] ) ) {
              inclusivePlots[CLADCALL + nreghists*(ni+1)]->Fill(charge);
              if ( dtime < 1.0 ) {
                vTightTiming[CLADCALL + nreghists*(ni+1)]->Fill(charge);
              }
            }
          }


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
     
          hYTrkMatch->Fill(y_trk);
          adcvdx->Fill( dxNom, clustersCharge[foundIdx] );
          sizevdx->Fill( dxNom, clustersSize[foundIdx] );
          // fill only if not near a masked channel -- its neighbors only have 2 strip clusters with their other neighbor
          if( badStrips[clustersSeedPosition[foundIdx]-1] && badStrips[clustersSeedPosition[foundIdx]+1] )
            sizevstrip->Fill( clustersSeedPosition[foundIdx], clustersSize[foundIdx] );
          if (stripIdx >=0 && stripIdx < nStripsInBeam ) {
            stripPlots[stripIdx][CHYMATCH]->Fill( y_trk );
            stripPlots[stripIdx][CHADCMATCH]->Fill( polarity*clustersCharge[foundIdx] );
            stripPlots[stripIdx][CHSNRMATCH]->Fill( polarity*float(clustersCharge[foundIdx])/noise[clustersSeedPosition[foundIdx]] );
          }

          if (inTightFiducialY) {
            hXTrkMatch->Fill(x_trk);

            for(size_t ni=0; ni < nNoiseScale; ++ni ) {
              if(!foundClusterWithScaledNoise( foundIdx, noiseScales[ni] ) )
                vNoiseScaleXray[ni]->SetPoint( vNoiseScaleXray[ni]->GetN(), x_trk, y_trk );
            }
          }

          for (int j=0; j < nOddStrips; ++j ) {
            if ( oddStrips[j] == clustersSeedPosition[foundIdx] ) {
              oddPlots[j][ODDADC]->Fill( clustersCharge[foundIdx] );
              oddPlots[j][ODDSIZE]->Fill( clustersSize[foundIdx] );
              oddPlots[j][ODDASYMM]->Fill( clustersSeedCharge[foundIdx]/clustersCharge[foundIdx] );
              oddPlots[j][ODDDX]->Fill( foundDx );
              if( polarity*clustersCharge2StripLeft[foundIdx] > 2.5*noise[clustersSeedPosition[foundIdx]-2] )
                oddPlots[j][ODDPARTNERS]->Fill(-2);
              if( polarity*clustersCharge1StripLeft[foundIdx] > 2.5*noise[clustersSeedPosition[foundIdx]-1] )
                oddPlots[j][ODDPARTNERS]->Fill(-1);
              if( polarity*clustersCharge1StripRight[foundIdx] > 2.5*noise[clustersSeedPosition[foundIdx]+1] )
                oddPlots[j][ODDPARTNERS]->Fill(1);
              if( polarity*clustersCharge2StripRight[foundIdx] > 2.5*noise[clustersSeedPosition[foundIdx]+2] )
                oddPlots[j][ODDPARTNERS]->Fill(2);
            }
          }
        } else {
          //Fill all the x-ray plots if we don't find it at all
          if (inTightFiducialY) {
            grMissed->SetPoint( grMissed->GetN(), x_trk, y_trk );
            grMissedStrips->SetPoint( grMissedStrips->GetN(), nomStrip, y_trk );
            for(size_t ni=0; ni < nNoiseScale; ++ni ) {
              vNoiseScaleXray[ni]->SetPoint( vNoiseScaleXray[ni]->GetN(), x_trk, y_trk );
            }
          }
        }

        fillMatchMiss( inclusivePlots, nreghists, foundHit, foundIdx, x_trk, y_trk, inTightFiducialY, nomStrip, dxNom, allDx, nearADC,  twonearADC,  fournearADC,  sumADC);
        if ( dtime < 1.0 ) {
          fillMatchMiss( vTightTiming, nreghists, foundHit, foundIdx, x_trk, y_trk, inTightFiducialY, nomStrip, dxNom, allDx, nearADC,  twonearADC,  fournearADC,  sumADC);
        }
        for(unsigned int ri = 0; ri< nRegions; ++ri ) {
          if(! passFiducialCut( ri, x_trk, y_trk, dxNom, nomStrip, yMax ) ) continue;

          //Regions automatically have tight fiducial y applied, so don't have to worry
          vRegionPlots[ri][INTERALL]->Fill(dxNom);
          vRegionPlots[ri][XALL]->Fill(x_trk);
          vRegionPlots[ri][NOMSTRIPALL]->Fill(nomStrip);
          vRegionPlots[ri][YALL]->Fill(y_trk);
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
            vRegionPlots[ri][NOMSTRIPALL + nreghists*(ni+1)]->Fill(nomStrip);
            if(fCMS) {
              vRegionPlots[ri][NEARADC1ALL + nreghists*(ni+1)]->Fill( nearADC );
              vRegionPlots[ri][NEARADC2ALL + nreghists*(ni+1)]->Fill( twonearADC );
              vRegionPlots[ri][NEARADC4ALL + nreghists*(ni+1)]->Fill( fournearADC );
              vRegionPlots[ri][NEARADC100ALL + nreghists*(ni+1)]->Fill( sumADC );
            }
          }


          fillMatchMiss( vRegionPlots[ri], nreghists, foundHit, foundIdx, x_trk, y_trk, true, nomStrip, dxNom,  allDx, nearADC,  twonearADC,  fournearADC,  sumADC);

	} //loop over regions


      } //loop tracks

   } //loop entries
   
   
   writeHistos();
}



void SummaryAnalysis::writeHistos() {
  fout->Write();

  //now outHistos is really all the graphs which don't get a directory by default
  fout->cd();
  hWidthNoise->Write("noise");
  for ( size_t i=0; i<outHistos.size(); ++i ) {
    outHistos[i]->Write();
  }
  fout->Close();
}

bool SummaryAnalysis::foundClusterWithScaledNoise( size_t idx, double nScale) {

  // guess 3*noise high cut and 2.5* noise low cut

  // think about how to reimplement -- if its just whether you pass or not just need to check the seed passes new threshold.  but if we care about 1->2 strip clutsers could repurpose this function

  return fabs(clustersSeedCharge[idx]) > 3*nScale*hWidthNoise->GetBinContent( clustersSeedPosition[idx] );


}

void SummaryAnalysis::fillMatchMiss( const std::vector<TH1*> & vh, unsigned int nhists, bool foundHit, int foundIdx, double x_trk, double y_trk, bool tightFidY, double nomStrip, double dxNom, const std::vector<double> & allDx, double nearADC, double twonearADC, double fournearADC, double sumADC) {

  //Fill the matching histograms now
  if(foundHit) {
    vh[CLADCMATCH]->Fill(polarity*clustersCharge[foundIdx]);
    vh[CLSNRMATCH]->Fill(polarity*float(clustersCharge[foundIdx])/noise[clustersSeedPosition[foundIdx]]);
    vh[YMATCH]->Fill(y_trk);
            
    for(size_t ci=0; ci<allDx.size(); ++ci)
      vh[DXMATCH]->Fill( allDx[ci]);

    if( tightFidY ) {
      vh[INTERMATCH]->Fill(dxNom);
      vh[XMATCH]->Fill(x_trk);
      vh[NOMSTRIPMATCH]->Fill(nomStrip);
      if (fCMS) {   
        vh[NEARADC1MATCH]->Fill( nearADC );
        vh[NEARADC2MATCH]->Fill( twonearADC );
        vh[NEARADC4MATCH]->Fill( fournearADC );
        vh[NEARADC100MATCH]->Fill( sumADC );
      }
    }

    //Fill as if missing if the seed fails the new cut on noise,
    //otherwise fill the plots for inclusive version of noise
    for(size_t ni=0; ni < nNoiseScale; ++ni ) {
      if( !foundClusterWithScaledNoise( foundIdx, noiseScales[ni] ) ) {
              
        //This plot is still broken until i have a good way of checking the dxlist for passing clusters
        for(size_t ci=0; ci<allDx.size(); ++ci)
          vh[DXMISS + nhists*(ni+1)]->Fill( allDx[ci]);

      } else {

        vh[CLADCMATCH + nhists*(ni+1)]->Fill(polarity*clustersCharge[foundIdx]);
       
        //This plot is still broken until i have a good way of checking the dxlist for passing clusters
        for(size_t ci=0; ci<allDx.size(); ++ci)
          vh[DXMATCH + nhists*(ni+1)]->Fill( allDx[ci]);

        vh[YMATCH + nhists*(ni+1)]->Fill(y_trk);

        if( y_trk < yMax ) {
          vh[INTERMATCH + nhists*(ni+1)]->Fill(dxNom);
          vh[XMATCH + nhists*(ni+1)]->Fill(x_trk);
          vh[NOMSTRIPMATCH + nhists*(ni+1)]->Fill(nomStrip);
          if (fCMS) {   
            vh[NEARADC1MATCH + nhists*(ni+1)]->Fill( nearADC );
            vh[NEARADC2MATCH + nhists*(ni+1)]->Fill( twonearADC );
            vh[NEARADC4MATCH + nhists*(ni+1)]->Fill( fournearADC );
            vh[NEARADC100MATCH + nhists*(ni+1)]->Fill( sumADC );
          }
        }
      }
    }


  } else { //no match found
    for(size_t ci=0; ci<allDx.size(); ++ci)
      vh[DXMISS]->Fill( allDx[ci]);
 
  }

}
