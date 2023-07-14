1. Setup naf: `source setup_naf.sh`
```
#!/bin/sh
module use -a /afs/desy.de/group/cms/modulefiles/
module load cmssw
ls -la /cvmfs/cms.cern.ch/
source /cvmfs/cms.cern.ch/cmsset_default.sh
```


2 Install `Darwin`
```
https://gitlab.cern.ch/DasAnalysisSystem/Darwin.git
cd Darwin
source setup
make clean
make
```

(don't use `make -j ...`. )

3. Use `Core` within Darwin
```
cd Darwin/CMSSW_12_4_0/src
cmenv
scram b -j `nproc`
```
4. make `Ntupliser/src` directory and put RivetNtupliser.c

5. Make Configuration file in `/python`. See https://github.com/cms-sw/cmssw/tree/master/Configuration/Generator/python for some of the MC generation parameters
