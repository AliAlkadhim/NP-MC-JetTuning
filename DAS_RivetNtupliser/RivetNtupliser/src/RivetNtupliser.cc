// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/SmearedJets.hh"
#include "Rivet/Projections/Smearing.hh"
#include "Rivet/Tools/BinnedHistogram.hh"

#include "Core/Objects/interface/Event.h"
#include "Core/Objects/interface/Jet.h"

#include <TTree.h>
#include <TFile.h>

namespace Rivet {


  /// Inclusive jet pT at 13 TeV
  class RivetNtupliser : public Analysis {

     DAS::Event * event_;
     vector<DAS::GenJet> * genJets_;
     vector<DAS::RecJet> * recJets_;

    char rec[] = "FALSE";
     // output file and tree
     TFile * file; 
     TTree * tree; 
    
  public:

     /// Constructor
     RIVET_DEFAULT_ANALYSIS_CTOR(RivetNtupliser);

     void init() {

       file = TFile::Open("output.root", "RECREATE");
       tree = new TTree("inclusive_jets","inclusive_jets");

       // Set up branches
       event_ = new DAS::Event;
       tree->Branch("event", &event_);

       genJets_ = new vector<DAS::GenJet>;
       genJets_->reserve(25);  // estimation of the number of Gen jets in the event
	   tree->Branch("genJets", &genJets_);

       recJets_ = new vector<DAS::RecJet>;
       recJets_->reserve(25);  // estimation of the number of Gen jets in the event
       if (rec == "TRUE") {
	   tree->Branch("recJets", &recJets_);
       }
 
       // Initialize the projections
       const FinalState fs;
       declare(FastJets(fs, FastJets::ANTIKT, 0.4), "JetsAK4"); // TODO: make parameter for 0.4?
       declare(SmearedJets(FastJets(fs, FastJets::ANTIKT, 0.4), JET_SMEAR_CMS_RUN2), "JetsAK4Rreco");

       //BOOK HISTOGRAMS?
             // Book sets of histograms, binned in absolute rapidity
      // Histo1DPtr tmp;
      // for(int y = 0; y < 4; ++y) {
      //    _hist_sigmaAK4.add(0.5*y, 0.5*(y+1), book(tmp,y+1, 1, 1)); // d0?-x01-y01
      //    _hist_sigmaAK7.add(0.5*y, 0.5*(y+1), book(tmp,20+y+1, 1, 1)); // d2?-x01-y01
      // }
     }


     /// Per-event analysis
     void analyze(const Event &event) {
     
       event_->clear();
       genJets_->clear();
           if (rec == "TRUE") {
       recJets_->clear();
           }
       // For Rivet3 event.weight() is obsolete (always 1) https://rivet.hepforge.org/code/dev/classRivet_1_1Event.html
       // Instead there is weights() public member function (multiple weights probably for PDF, scale variations etc.)
       // In the case of NP corrections calculation the size of valarray is 1 (only one event weight) 
       const auto& weights = event.weights();
       event_->genWgts.reserve(weights.size());  
       for (auto& w : weights){ 
           // cout << "Weight = " << w << endl;
           event_->genWgts.push_back(w);
       }

       // AK4 gen jets
       const FastJets& fjAK4 = apply<FastJets>(event, "JetsAK4"); // TODO: make parameter for AK4?
       const Jets& jetsAK4 = fjAK4.jets(Cuts::pT > 10*GeV && Cuts::abseta < 5.0); // Ntupliser cuts 
      
       for (const Jet& j : jetsAK4) {
           DAS::GenJet genJet;
		   genJet.p4.SetPt(j.pT());
		   genJet.p4.SetEta(j.eta());
           genJet.p4.SetPhi(j.phi()); 
           genJet.p4.SetM(j.mass()); 
           genJets_->push_back(genJet);
       }

       // AK4 rec jets
       if (rec == "TRUE") {
       const SmearedJets& AK4reco = apply<SmearedJets>(event,"JetsAK4Rreco");
       const Jets& jetsAK4reco = AK4reco.jets(Cuts::pT > 10*GeV && Cuts::abseta < 5.0);

       for (const Jet& j : jetsAK4reco) {
           DAS::RecJet recJet;
           recJet.p4.SetPt(j.pT());
           recJet.p4.SetEta(j.eta());
           recJet.p4.SetPhi(j.phi());
           recJet.p4.SetM(j.mass());
           recJets_->push_back(recJet);
       }
       }
       tree->Fill();

     }

	 // Finalize
	 void finalize() {
	
        tree->Write();
        file->Close();
	 
     }

  };

  // This global object acts as a hook for the plugin system.
  RIVET_DECLARE_PLUGIN(RivetNtupliser);

}
