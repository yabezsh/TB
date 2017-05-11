#define AdapterTiming_cxx
#include "AdapterTiming.h"

#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TGraph.h>
#include <TProfile.h>
#include <cmath>
#include <vector>
#include <string>

namespace {

  //Use this unnamed namespace for making the definitions about how to recreate plots
  //current sensor edge info 
  // ymax - 0.875 to ymax - 1.1 is the bond pad region
  // add 19 to first channel to get the start of bond pad region, then add 44 to get the end.
  // A3 : first channel = 156, y=3.85
  // 
  enum {
    A3, A5, A10, A12, A13, A6, P14HM1, P13HM1, P13HM2, P18HM1, P18HM2, P17HM2, NBOARDS};
  double sensorYmax[NBOARDS] = { 3.75, 3.64, 3.72, 3.71, 3.82, 3.78, 3.82, 3.75, 3.8, 3.72, 3.85, 3.8 };
  double firstChan[NBOARDS] = { 156., 411., 153., 407., 135., 391., 135., 391., 144., 400., 144., 400.};
  
  int getBoardIndex(const TString & boardname ){
    // TObjString * os = (TObjString*) boardname.Tokenize("_")->At(0);
    // TString newstring(os->GetString());
    

    if ( boardname == "A3_Lower")
      return A3;
    else if ( boardname == "A5_Lower" )
      return A5;
    else if ( boardname == "A10_FanIn" )
      return A10;
    else if ( boardname == "A12_FanIn" )
      return A12;
    else if ( boardname == "A13_FanIn" )
      return A13;
    else if ( boardname == "A6_Lower" )
      return A6;
    else if ( boardname == "14_HM1")
      return P14HM1;
    else if ( boardname == "13_HM1" )
      return P13HM1;
    else if ( boardname == "13_HM2" )
      return P13HM2;
    else if ( boardname == "18_HM1" )
      return P18HM1;
    else if ( boardname == "18_HM2" )
      return P18HM2;
    else if ( boardname == "17_HM2" )
      return P17HM2;
    
    return -1;
  }

  //Checks y-height for adapter or control region
  int checkTrkY( const double & yTrk ) {
    if ( yTrk < sensorYmax[getBoardIndex(m_board)] - 0.85 && yTrk > sensorYmax[getBoardIndex(m_board)] - 1.125 )
      return 1; //adapter region
    else if ( yTrk < sensorYmax[getBoardIndex(m_board)] - 1.5 && yTrk > sensorYmax[getBoardIndex(m_board)] - 1.5 - (1.125-0.85) )
      return 2; //control region
    return 0;
  }
  
  //Returns channel number coupled via pitch adapter for current track
  // returns -1 if not a couple channel
  const int nPairs = 14;
  int coupledChannel[nPairs] = { 1, 6, 11, 14, 19, 24, 29, 34, 39, 44, 49, 52, 57, 62 };
  double lossyStrip[nPairs] = { 19., 21., 23., 24., 26., 28., 30., 32., 34., 36., 38., 39., 41., 43. };
  double fc = firstChan[getBoardIndex(m_board)];

  //Returns index of channel that is coupled to the track when track between two strips of interest
  int paCoupledChannel( const double & nomStrip ) {
  
    for (int i=0; i < nPairs; ++i ) {
      if ( nomStrip > fc + lossyStrip[i] + 0.4 && nomStrip < fc + lossyStrip[i] + 0.6 )
        return i;
    }
    
    return -1;
    
  }

  //plot enumeration
  //PA = pitch adapter (bondpad) region, CTL = control region
  enum {
    PANEARUNDER, //Trk under this strip
    PANEXTUNDER, //Other strip of pair when track under one
    PANEARBTWN, //Trk halfway, left side
    PANEXTBTWN, //Trk halfway, right side
    PASUMBTWN, //Trk halfway, sum of two
    PAFARUNDER, //Trk under a strip, this is signal on PA coupled channel
    PAFARBTWN, //Trk halfway, PA coupled channel
    PAFARBTWNHI,
    PAFARBTWNLO,
    PAOUTUNDER, //Trk under, neighbor *not* part of pair
    PAOUTBTWN, //Trk halfway, neighbors not part of pair
    CTLNEARUNDER,
    CTLNEXTUNDER,
    CTLNEARBTWN,
    CTLNEXTBTWN,
    CTLSUMBTWN,
    CTLFARUNDER,
    CTLFARBTWN,
    CTLOUTUNDER,
    CTLOUTBTWN,
    NPLOTS
  };

  std::string plotnames[NPLOTS] = { 
    "pa_near_under",
    "pa_next_under",
    "pa_near_btwn",
    "pa_next_btwn",
    "pa_sum_btwn",
    "pa_far_under",
    "pa_far_btwn",
    "pa_far_btwn_hi",
    "pa_far_btwn_lo",
    "pa_out_under",
    "pa_out_btwn",
    "ctl_near_under",
    "ctl_next_under",
    "ctl_near_btwn",
    "ctl_next_btwn",
    "ctl_sum_btwn",
    "ctl_far_under",
    "ctl_far_btwn",
    "ctl_out_under",
    "ctl_out_btwn"
  };
}
  
void AdapterTiming::Loop() {

  if (fChain == 0) return;

  Long64_t nentries = fChain->GetEntriesFast();
  
  TString myoutdir(getenv("MYOUTPUTPATH"));
  TString biasv(getenv("BIASV"));
  TString f_out = myoutdir + "/AdapterTiming_" + runplace + "_" + m_board + "_" + biasv + "_" + consR + ".root";

  fout = new TFile(f_out,"RECREATE");
  
  double symax = sensorYmax[getBoardIndex(m_board)];

  
  std::cout << "Board 1st channel = " << fc << std::endl;
  std::cout << "Analyze " << nPairs << " pairs" << std::endl;

  //Couple diagnostic histograms
  TH1F * hnoise = new TH1F("noise_selected","CMS Noise; Channel; ADC", nPairs*3, -0.5, nPairs*3. - 0.5);
  TH1F * hmask = new TH1F("mask_selected","Masked channels among selected; Channel; Good", nPairs*3, -0.5, nPairs*3. - 0.5);
  int bincnt = 1;
  char buf[5];
  for (int ic=0; ic < nPairs; ++ic ) {
    int strip = fc + lossyStrip[ic] + 0.1;
    int label = lossyStrip[ic] + 0.1;
    sprintf(buf,"%d", label );
    hnoise->GetXaxis()->SetBinLabel(bincnt, buf );
    hnoise->SetBinContent(bincnt, hWidthNoise->GetBinContent(strip+1) );
    hmask->GetXaxis()->SetBinLabel(bincnt, buf );
    hmask->SetBinContent( bincnt, badStrips[strip] );
    bincnt++;
    
    sprintf(buf,"%d", label +1 );
    hnoise->GetXaxis()->SetBinLabel(bincnt, buf );
    hnoise->SetBinContent(bincnt, hWidthNoise->GetBinContent(strip+2) );
    hmask->GetXaxis()->SetBinLabel(bincnt, buf );
    hmask->SetBinContent( bincnt, badStrips[strip+1] );
    bincnt++;

    int cc = fc + coupledChannel[ic]+  0.1;
    int cclabel = coupledChannel[ic];
    sprintf(buf,"%d", cclabel );
    hnoise->GetXaxis()->SetBinLabel(bincnt, buf );
    hnoise->SetBinContent(bincnt, hWidthNoise->GetBinContent(cc+1) );
    hmask->GetXaxis()->SetBinLabel(bincnt, buf );
    hmask->SetBinContent( bincnt, badStrips[cc] );
    bincnt++;
    
  }
  outHistos.push_back(hnoise);
  outHistos.push_back(hmask);
  
  //Create a set of histograms for each channel coupling under study
  std::vector<std::vector<TH2*> > channelPlots( nPairs );
  TH2F * hbase = new TH2F("adcbase","Base histogram for ADCs; TDC; ADC",10,-0.5,9.5,250,-250,1000);
  hbase->Sumw2();
  char hname[50];
  for ( int ic=0; ic < nPairs; ++ic ) {
    channelPlots[ic].resize( NPLOTS );
    int strip = lossyStrip[ic] + 0.1;
    for ( unsigned int ip=0; ip < NPLOTS; ++ip) {
      sprintf(hname,"%s_chan%i", plotnames[ip].c_str(), strip);
      channelPlots[ic][ip] = (TH2F*) hbase->Clone(hname);
      outHistos.push_back( channelPlots[ic][ip] );
    }
  }


  //Create some TTree to try to fit pulse shapes for 4 cases - under strip, sum between adapter and control, far adapter
  double tradc=0;
  double trkx=0;
  double trky=0;
  int trtdc=0;
  int trstrip=0;
  TTree * tr_under = new TTree("TrUnder","TrUnder");
  TTree * tr_btwn_ctl = new TTree("TrBtwnCtl","TrBtwnCtl");
  TTree * tr_btwn_pa = new TTree("TrBtwnPa","TrBtwnPa");
  TTree * tr_btwn_farhi = new TTree("TrBtwnFarHi","TrBtwnFarHi");
  TTree * tr_btwn_farlo = new TTree("TrBtwnFarLo","TrBtwnFarLo");
  
  tr_under->Branch("adc",&tradc);
  tr_under->Branch("tdc",&trtdc);
  tr_under->Branch("x",&trkx);
  tr_under->Branch("y",&trky);
  tr_under->Branch("strip",&trstrip);

  tr_btwn_ctl->Branch("adc",&tradc);
  tr_btwn_ctl->Branch("tdc",&trtdc);
  tr_btwn_ctl->Branch("x",&trkx);
  tr_btwn_ctl->Branch("y",&trky);
  tr_btwn_ctl->Branch("strip",&trstrip);
  tr_btwn_pa->Branch("adc",&tradc);
  tr_btwn_pa->Branch("tdc",&trtdc);
  tr_btwn_pa->Branch("x",&trkx);
  tr_btwn_pa->Branch("y",&trky);
  tr_btwn_pa->Branch("strip",&trstrip);
  tr_btwn_farhi->Branch("adc",&tradc);
  tr_btwn_farhi->Branch("tdc",&trtdc);
  tr_btwn_farhi->Branch("x",&trkx);
  tr_btwn_farhi->Branch("y",&trky);
  tr_btwn_farhi->Branch("strip",&trstrip);
  tr_btwn_farlo->Branch("adc",&tradc);
  tr_btwn_farlo->Branch("tdc",&trtdc);
  tr_btwn_farlo->Branch("x",&trkx);
  tr_btwn_farlo->Branch("y",&trky);
  tr_btwn_farlo->Branch("strip",&trstrip);

  outHistos.push_back( tr_under );
  outHistos.push_back( tr_btwn_ctl );
  outHistos.push_back( tr_btwn_pa );
  outHistos.push_back( tr_btwn_farhi );
  outHistos.push_back( tr_btwn_farlo );
  
  ////THEIR PREP
  PrepareDUT();
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


      double tx = 1000*vec_trk_tx->at(k);
      double ty = 1000*vec_trk_ty->at(k);

      //cut out flagged bad channels
      int idetStrip = detStrip + 0.5;
      if(idetStrip>=1 && idetStrip<=nChan-2 && (badStrips[idetStrip]==0 || badStrips[idetStrip-1]==0 || badStrips[idetStrip+1]==0))
        continue;

      //Check that the track passes our cuts
      bool goodTrack = false;
      if(tx>txMin && tx<txMax && ty>tyMin && ty<tyMax) goodTrack = true;        
        
      bool goodTime =  (clustersTDC >= tdcLo && clustersTDC <= tdcHi);

      if( !goodTrack ) continue;

      //Now check if its in adapter or control region in y
      int yRegion = checkTrkY( y_trk );
      if( !yRegion ) continue;
      
      bool inPA = (yRegion == 1);


      double interx = nomStrip - (int) nomStrip;
      
      //Check if we are under a strip of interest
      for ( int is=0; is < nPairs; ++is ) {
        int strip = fc + lossyStrip[is] + 0.1; //make sure don't accidently underflow and pick lower strip
        int cc = fc + coupledChannel[is] + 0.1;
        
        if ( fabs(nomStrip - (strip)) < 0.1 ) {
          //under near strip
          trstrip = strip;
          trkx = (nomStrip - (strip) > 0 ) ? interx : interx - 1;
          trky = symax - y_trk;
          tradc = polarity*fCMS->cmsData[ strip ];
          trtdc = clustersTDC;
          tr_under->Fill();
          if ( inPA ) {
            channelPlots[is][ PANEARUNDER ]->Fill( clustersTDC, polarity*fCMS->cmsData[ strip ] );
            channelPlots[is][ PANEXTUNDER ]->Fill( clustersTDC, polarity*fCMS->cmsData[ strip + 1 ] );
            channelPlots[is][ PAOUTUNDER ]->Fill( clustersTDC, polarity*fCMS->cmsData[ strip - 1 ] );
            channelPlots[is][ PAFARUNDER ]->Fill( clustersTDC, polarity*fCMS->cmsData[ cc ] );
          } else {
            channelPlots[is][ CTLNEARUNDER ]->Fill( clustersTDC, polarity*fCMS->cmsData[ strip ] );
            channelPlots[is][ CTLNEXTUNDER ]->Fill( clustersTDC, polarity*fCMS->cmsData[ strip + 1 ] );
            channelPlots[is][ CTLOUTUNDER ]->Fill( clustersTDC, polarity*fCMS->cmsData[ strip - 1 ] );
            channelPlots[is][ CTLFARUNDER ]->Fill( clustersTDC, polarity*fCMS->cmsData[ cc ] );
          }
        } else if ( fabs(nomStrip - (strip + 1)) < 0.1) {
          //under next strip over
          trstrip = strip + 1;
          trkx = (nomStrip - (strip + 1) > 0 ) ? interx + 1 : interx;
          trky = symax - y_trk;
          tradc = polarity*fCMS->cmsData[ strip + 1 ];
          trtdc = clustersTDC;
          tr_under->Fill();
          if ( inPA ) {
            channelPlots[is][ PANEARUNDER ]->Fill( clustersTDC, polarity*fCMS->cmsData[ strip + 1] );
            channelPlots[is][ PANEXTUNDER ]->Fill( clustersTDC, polarity*fCMS->cmsData[ strip ] );
            channelPlots[is][ PAOUTUNDER ]->Fill( clustersTDC, polarity*fCMS->cmsData[ strip + 2 ] );
            channelPlots[is][ PAFARUNDER ]->Fill( clustersTDC, polarity*fCMS->cmsData[ cc ] );
          } else {
            channelPlots[is][ CTLNEARUNDER ]->Fill( clustersTDC, polarity*fCMS->cmsData[ strip + 1] );
            channelPlots[is][ CTLNEXTUNDER ]->Fill( clustersTDC, polarity*fCMS->cmsData[ strip ] );
            channelPlots[is][ CTLOUTUNDER ]->Fill( clustersTDC, polarity*fCMS->cmsData[ strip + 2 ] );
            channelPlots[is][ CTLFARUNDER ]->Fill( clustersTDC, polarity*fCMS->cmsData[ cc ] );
          }
        }
      }
      
      int paIdx = paCoupledChannel( nomStrip );
      if( paIdx == -1 )
        continue;
      
      //Now we are in between two strips of interest
      bool closeLow = ( interx < 0.5);

      int nearChan, nextChan;
      if (closeLow ) {
        nearChan = fc + lossyStrip[paIdx] + 0.1;
        nextChan = nearChan + 1;
      } else {
        nextChan = fc + lossyStrip[paIdx] + 0.1;
        nearChan = nextChan + 1;
      }
      int outChan1 = fc + lossyStrip[paIdx] + 0.1 - 1;
      int paChan = fc + coupledChannel[paIdx]+0.1;
    
      if (inPA) {
        double sumadc = polarity*fCMS->cmsData[ nearChan ] + polarity*fCMS->cmsData[ nextChan ];
        
        channelPlots[paIdx][ PANEARBTWN ]->Fill( clustersTDC, polarity*fCMS->cmsData[ nearChan ] );
        channelPlots[paIdx][ PANEXTBTWN ]->Fill( clustersTDC, polarity*fCMS->cmsData[ nextChan ] );
        channelPlots[paIdx][ PASUMBTWN ]->Fill(  clustersTDC, sumadc );
        channelPlots[paIdx][ PAFARBTWN ]->Fill(  clustersTDC, polarity*fCMS->cmsData[ paChan ] );
        channelPlots[paIdx][ PAOUTBTWN ]->Fill(  clustersTDC, polarity*fCMS->cmsData[ outChan1 ] );
        channelPlots[paIdx][ PAOUTBTWN ]->Fill(  clustersTDC, polarity*fCMS->cmsData[ outChan1 + 3 ] );


        trstrip = lossyStrip[paIdx];
        trkx = interx;
        trky = symax - y_trk;
        tradc = sumadc;
        trtdc = clustersTDC;
        tr_btwn_pa->Fill();

        
        tradc = polarity*fCMS->cmsData[ paChan ];
        
        if ( sumadc > 150 ) {
          channelPlots[paIdx][ PAFARBTWNHI ]->Fill(  clustersTDC, polarity*fCMS->cmsData[ paChan ] );
          tr_btwn_farhi->Fill();
        } else {
          channelPlots[paIdx][ PAFARBTWNLO ]->Fill(  clustersTDC, polarity*fCMS->cmsData[ paChan ] );
          tr_btwn_farlo->Fill();
        }

      } else {
        channelPlots[paIdx][ CTLNEARBTWN ]->Fill( clustersTDC, polarity*fCMS->cmsData[ nearChan ] );
        channelPlots[paIdx][ CTLNEXTBTWN ]->Fill( clustersTDC, polarity*fCMS->cmsData[ nextChan ] );
        channelPlots[paIdx][ CTLSUMBTWN ]->Fill(  clustersTDC, polarity*fCMS->cmsData[ nearChan ] + polarity*fCMS->cmsData[ nextChan ] );
        channelPlots[paIdx][ CTLFARBTWN ]->Fill(  clustersTDC, polarity*fCMS->cmsData[ paChan ] );
        channelPlots[paIdx][ CTLOUTBTWN ]->Fill(  clustersTDC, polarity*fCMS->cmsData[ outChan1 ] );
        channelPlots[paIdx][ CTLOUTBTWN ]->Fill(  clustersTDC, polarity*fCMS->cmsData[ outChan1 + 3 ] );

        trstrip = lossyStrip[paIdx];
        trkx = interx;
        trky = symax - y_trk;
        tradc = polarity*fCMS->cmsData[ nearChan ] + polarity*fCMS->cmsData[ nextChan ];
        trtdc = clustersTDC;
        tr_btwn_ctl->Fill();
      }



      
    } //loop tracks
  } //loop entries

  writeHistos();

}



void AdapterTiming::writeHistos() {

  fout->cd();
  for ( size_t i=0; i<outHistos.size(); ++i ) {
    outHistos[i]->Write();
  }
  fout->Close();
}
