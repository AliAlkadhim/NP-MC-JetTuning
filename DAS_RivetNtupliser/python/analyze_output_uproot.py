import uproot
import pandas as pd
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import awkward as awk
import hist
file = 'output.root'
f = uproot.open(file)['inclusive_jets']
# print(f.keys())
branches=['event', 'genJets', 'recJets']

event_tree=f['event']
genJet_tree=f['genJets']

# print(event_tree.keys())

df = {}
df_genJet_weight_tree=event_tree.arrays('genWgts', library='np')
# df['genJetPt']=genJet_tree.arrays('genJets.p4.fPt', library='pd')
# df_genJet_tree=genJet_tree.arrays('genJets.p4.fPt', library='pd')
df_genJet_tree=genJet_tree.arrays('genJets.p4.fPt',library='np')
# awk_genJet_pT = awk.Array(df_genJet_tree['genJets.p4.fPt'])
# N=df_genJet_tree.shape[0]
# print('N=',N)
df_genJet_weight_tree=df_genJet_weight_tree['genWgts']
df_genJet_tree=df_genJet_tree['genJets.p4.fPt']
print(df_genJet_tree)
print(df_genJet_tree.shape)
print('\n WEIGHT ARRAY \n')
print(df_genJet_weight_tree)
print('\n BROADCASTED \n')
# print(awk.broadcast_arrays(
#     df_genJet_weight_tree[:,np.newaxis], df_genJet_tree)
#       )
N=10
# hist.Hist(hist.axis.Regular(100, 0, 300, label="pT [GeV]")).fill(

#     awk.ravel(df_genJet_tree),
#     # df_genJet_tree doesnt work (have to ravel) 
#     # weight=awk.ravel(df_genJet_weight_tree)

# ).plot()
# plt.show()
exit()
print('event weight tree shape = ', df_genJet_weight_tree.shape)
# print(df_genJet_tree[:3].tolist())
print(df_genJet_tree)
jetpt_l=[]
for event in range(N):
    event_i_pT = df_genJet_tree[event].tolist()
   
    
    weight_i = float(df_genJet_weight_tree.iloc[event,:])
    # print('\n')
    
    
    event_i_pT=event_i_pT['genJets.p4.fPt']
    print('pT list in event event: \t', event_i_pT, 'of type')
    jetpt_l.append(event_i_pT)
    # event_i_wt
    # if event < 10:
        # print('the weight in this event', weight_i )
        # print('NUM_JETS: ' , len(event_i_pt))
    # print('\n')
    
print(f'jetpt_l= {jetpt_l}')

jetpt_l=np.array(jetpt_l)
weights=np.array(df_genJet_weight_tree.iloc[:,0])
print(weights.shape)
print(jetpt_l.shape)

### TODO program that extends the weights of one list to the, which look like
# weight_l = [ 0.9, 0.4, 1, 0, ...] . Of length L
# to the jet_pT array, which is like
# jet_pT_l = [ [123,124,36], [1241], [124, 352] , ...] , ie eah element is a list of different legth, which corresponds to the number of jets in the event
# I just want a weight list that is like
# weight_l_aug = [[0.9, 0.9, 0.9], [0.], [ 0.8,0.9]]  ie keeps the same shape as jet_pT_l
# np.repeat

def extend_w(weight_l, jet_pT_l):
    for jet_i, jetpt in enumerate(jet_pT_l):
        n_jets=len(jetpt)
        
        jet_weight=weight_l[jet_i]
        
        jet_weight=jet_weight * n_jets
        
    return weight_l, jet_pT_l

# weight_l, jet_pT_l = extend_w(weights, jetpt_l)
# print(weight_l)


# h = hist.Hist(hist.axis.Regular(1000, 0, 3000, 
#                                 label='Number of muons in event')
#               )
# h.fill(awk_genJet_pT)
# plt.show()
# plt.hist(jetpt_l, 
#          bins=100, 
#         #  range=(0,200),
#         # weights=weights
#         )
         
# plt.show()


