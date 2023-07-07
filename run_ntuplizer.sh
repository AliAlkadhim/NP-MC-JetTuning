#!/bib/bash
./template_run/pythia_standalone_scripts/main42 template_run/pythia_standalone_scripts/main42_prehadron.cmnd test_pre.fifo &
rivet --pwd --ignore-beams -o test_pre.yoda -a RIVET_NTUPLIZER test_pre.fifo

#rivet-mkanalysis RIVET_NTUPLIZER
#build with: rivet-build RivetRIVET_NTUPLIZER.so RIVET_NTUPLIZER.cc
# export RIVET_ANALYSIS_PATH=`pwd`
#export RIVET_DATA_PATH=/cvmfs/atlas.cern.ch/repo/sw/software/21.6/sw/lcg/releases/LCG_88b/MCGenerators/rivet/3.1.4/x86_64-centos7-gcc62-opt/share/Rivet
# cp $RIVET_DATA_PATH/CMS_2019_I1764472.yoda .
#mv CMS_2019_I1764472.yoda RIVET_NTUPLIZER.yoda
