#!/bin/bash

mkdir -p MERGED
cd PREHADRON
source /afs/desy.de/user/a/aalkadhi/poweheg/rivet+pythia/installnew.sh
yodamerge_tmp.py -o ../MERGED/suppr_0_500M_prehadron_merged.yoda pre*
rm *.yoda

cd ../POSTHADRON

yodamerge_tmp.py -o ../MERGED/suppr_0_500M_posthadron_merged.yoda post*
rm *.yoda	

