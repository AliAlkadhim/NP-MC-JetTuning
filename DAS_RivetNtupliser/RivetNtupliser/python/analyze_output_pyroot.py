import ROOT
# import pandas as pd
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np

file = 'output.root'
branches=['event', 'genJets', 'recJets']

file = ROOT.TFile(file)
incl_jet_tree=file.Get('inclusive_jets')
print(incl_jet_tree)


# genJet_weight_tree=file.Get(
    
# conda update -n base -c conda-forge conda