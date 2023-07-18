#!/bin/bash                                                                                              

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
lsetup asetup
asetup 21.6.72,AthGeneration
#export DQ2_LOCAL_SITE_ID=DESY-HH_SCRATCHDISK
source setupRivet.sh


#lsetup "lcgenv -p LCG_96 x86_64-centos7-gcc62-opt Python3"
#lsetup "lcgenv -p LCG_96 x86_64-centos7-gcc62-opt cython"
#export PATH=/cvmfs/sft.cern.ch/lcg/external/texlive/2016/bin/x86_64-linux:$PATH


#PYTHIA 306
source /cvmfs/sft.cern.ch/lcg/releases/LCG_88b/MCGenerators/pythia8/306/x86_64-centos7-gcc62-opt/pythia8env-genser.sh


#source /cvmfs/sft.cern.ch/lcg/contrib/gcc/5.1/x86_64-centos7/setup.sh
#source /cvmfs/sft.cern.ch/lcg/contrib/gcc/4.9/x86_64-centos7-gcc49-opt/setup.sh
#source /cvmfs/sft.cern.ch/lcg/contrib/gcc/4.9/x86_64-centos7/setup.sh

#RIVET USE 3.1.6
#source /cvmfs/sft.cern.ch/lcg/releases/LCG_88b/MCGenerators/rivet/3.1.5p1/x86_64-centos7-gcc62-opt/rivetenv.sh
source /cvmfs/sft.cern.ch/lcg/releases/LCG_88b/MCGenerators/rivet/3.1.6/x86_64-centos7-gcc62-opt/rivetenv-genser.sh

#PYTHIA8 DATA
export PYTHIA8DATA=/cvmfs/sft.cern.ch/lcg/releases/LCG_88b/MCGenerators/pythia8/306/x86_64-centos7-gcc62-opt/share/Pythia8/xmldoc/


#copy Makefile and Makefile.inc from /cvmfs/sft.cern.ch/lcg/releases/LCG_88b/MCGenerators/pythia8/306/x86_64-centos7-gcc62-opt/share/Pythia8/examples/

#Get the appropriate gcc version from https://gcc.gnu.org/onlinedocs/libstdc++/manual/abi.html
#GCC 4.9.0: GLIBCXX_3.4.20, CXXABI_1.3.8
#GCC 5.1.0: GLIBCXX_3.4.21, CXXABI_1.3.9
#source /cvmfs/sft.cern.ch/lcg/contrib/gcc/4.9.3/x86_64-centos7-gcc49-opt/setup.sh
source /cvmfs/sft.cern.ch/lcg/contrib/gcc/5.1/x86_64-centos7/setup.sh



#mkdir -p examples_from_lcg_306
# cd examples_from_lcg_306
# cp /cvmfs/sft.cern.ch/lcg/releases/LCG_88b/MCGenerators/pythia8/306/x86_64-centos7-gcc62-opt/share/Pythia8/examples/* .
# make main42 -j 12
