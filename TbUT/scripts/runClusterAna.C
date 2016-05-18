void runClusterAna(int bias = 50){

  gROOT->ProcessLine(".L AnalysisBaseCluOnly.C+");
  gROOT->ProcessLine(".L ClusterAna.C+");
  
  TTree *t;
  ClusterAna a(bias);
  a.Loop();
}
