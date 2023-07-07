#!/bin/bash
echo "starting"

echo "shell" $0
rnd=$(($1 + 1))
#if the run directories have been made before (i.e. not running in this directory for the first time, the line below can access each directory)
# rnd=$(printf "%01d\n" $rnd)
#current_dir=$(pwd)
#ENVIRONMENTS
# export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
# source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
# lsetup asetup
# asetup 21.6.72,AthGeneration
# source setupRivet.sh


# lsetup "lcgenv -p LCG_96 x86_64-centos7-gcc62-opt Python3"
# lsetup "lcgenv -p LCG_96 x86_64-centos7-gcc62-opt cython"

#source /cvmfs/sft.cern.ch/lcg/releases/Python/3.8.6-3199b/x86_64-centos7-gcc8-opt/Python-env.sh
#FASTJET
#source /cvmfs/sft.cern.ch/lcg/releases/LCG_96/fastjet/3.3.2/x86_64-centos7-gcc62-opt/fastjet-env.sh 

# source /cvmfs/sft.cern.ch/lcg/releases/LCG_96/MCGenerators/rivet/3.1.2/x86_64-centos7-gcc62-opt/rivetenv.sh
#USE NEW RIVET 3.1.6
#source /cvmfs/sft.cern.ch/lcg/releases/LCG_88b/MCGenerators/rivet/3.1.6/x86_64-centos7-gcc62-opt/rivetenv.sh


#PYTHIA8 : 302
#source /cvmfs/sft.cern.ch/lcg/releases/LCG_96/MCGenerators/pythia8/302/x86_64-centos7-gcc62-opt/pythia8env-genser.sh

#MAKE SURE THE PYTHIA8 DATA MATCHES THE PYTHIA8 CODE VERSION

#export PYTHIA8DATA=/cvmfs/sft.cern.ch/lcg/releases/LCG_96/MCGenerators/pythia8/302/x86_64-centos7-gcc62-opt/share/Pythia8/xmldoc

#export PYTHIA_LIB_PATH=/cvmfs/sft.cern.ch/lcg/releases/LCG_96/MCGenerators/pythia8/302/x86_64-centos7-gcc62-opt/lib/



#SOURCE PYTHIA 306 and RIVET and HEPMC and FASTJET
source /nfs/dust/cms/user/aalkadhi/PYTHIA_STANDALONE/setup_pythia_306.sh

#LHAPDF
export LHAPDF_DATA_PATH=/cvmfs/sft.cern.ch/lcg/external/lhapdfsets/current/:/cvmfs/sft.cern.ch/lcg/releases/LCG_96/MCGenerators/lhapdf/6.2.3/x86_64-centos7-gcc62-opt/share/LHAPDF/



export LD_LIBRARY_PATH=$PYTHIA_LIB_PATH:$LD_LIBRARY_PATH




# ON DUST
current_dir=/nfs/dust/cms/user/aalkadhi/PYTHIA_STANDALONE/Monash_HardQCD_1B_2

mkdir -p /nfs/dust/cms/user/aalkadhi/PYTHIA_STANDALONE/Monash_HardQCD_1B_2/run_${rnd}

#go to the run directory
cd /nfs/dust/cms/user/aalkadhi/PYTHIA_STANDALONE/Monash_HardQCD_1B_2/run_${rnd}

#remove everything but the pwgevents.lhe files
#GCC 4.9.0: GLIBCXX_3.4.20, CXXABI_1.3.8
#GCC 5.1.0: GLIBCXX_3.4.21, CXXABI_1.3.9
#source /cvmfs/sft.cern.ch/lcg/contrib/gcc/4.9.3/x86_64-centos7-gcc49-opt/setup.sh
source /cvmfs/sft.cern.ch/lcg/contrib/gcc/5.1/x86_64-centos7/setup.sh

#source env


#copy main pythia script to this directory
cp /nfs/dust/cms/user/aalkadhi/PYTHIA_STANDALONE/Monash_HardQCD_1B_2/pythia_standalone_scripts/* .



#PREHADRON
#make a fifo associated with that run in that run directory. First generate the hepmc events into fifo
#mkfifo prehadron${rnd}.fifo
./main42 main42_prehadron.cmnd prehadron${rnd}.fifo &

#then attach the analysis at the opposite end
rivet --ignore-beams -o prehadron${rnd}.yoda -a CMS_2021_I1972986 prehadron${rnd}.fifo

rm prehadron${rnd}.fifo

#remove the fifo file
#copy the yoda hist file into COMPLETE_YODAS dir
mv prehadron${rnd}.yoda /nfs/dust/cms/user/aalkadhi/PYTHIA_STANDALONE/Monash_HardQCD_1B_2/COMPLETE_YODAS/PREHADRON/



#POSTHADRON
#make a fifo associated with that run in that run directory. First generate the hepmc events into fifo
#mkfifo posthadron${rnd}.fifo
./main42 main42_posthadron.cmnd posthadron${rnd}.fifo &

#then attach the analysis at the opposite end
rivet --ignore-beams -o posthadron${rnd}.yoda -a CMS_2021_I1972986 posthadron${rnd}.fifo

#rm posthadron${rnd}.fifo
#rivet --ignore-beams -o prehadron${rnd}.yoda -a CMS_2016_I1487277 posthadron${rnd}.fifo
#remove the fifo file
rm posthadron${rnd}.fifo
#copy the yoda hist file into COMPLETE_YODAS dir
mv posthadron${rnd}.yoda /nfs/dust/cms/user/aalkadhi/PYTHIA_STANDALONE/Monash_HardQCD_1B_2/COMPLETE_YODAS/POSTHADRON/


echo $1,$rnd
#Finally, go back to current_dir
cd /nfs/dust/cms/user/aalkadhi/PYTHIA_STANDALONE/Monash_HardQCD_1B_2


