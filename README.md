# NP-MC-JetTuning

Rivet + Different MC Generators for Jet Studies


# Installation on naf as a DAS package

## Installation
1. Setup naf: `source setup_naf.sh`
```bash setup_naf.sh
#!/bin/sh
module use -a /afs/desy.de/group/cms/modulefiles/
module load cmssw
ls -la /cvmfs/cms.cern.ch/
source /cvmfs/cms.cern.ch/cmsset_default.sh
```



2 Install [Darwin](https://gitlab.cern.ch/DasAnalysisSystem/Darwin)
```
https://gitlab.cern.ch/DasAnalysisSystem/Darwin.git
cd Darwin
source setup
make clean
make
```

(don't use `make -j ...`. )

3.  Compile Darwin
```
cd Darwin/CMSSW_12_4_0/src
cmenv
scram b -j `nproc`
```
4. make `Ntupliser/src` directory and put RivetNtupliser.cc and BuildFile.xml there and python config file.

3. Install [Core](https://gitlab.cern.ch/DasAnalysisSystem/Core): `source setup_DAS.sh` and build the `Rivet` 
```
#!/bin/bash
cmsrel CMSSW_10_6_30
cd CMSSW_10_6_30/src
cmsenv
git clone https://gitlab.cern.ch/gparaske/Core.git
git checkout Rivet
scram b -j `nproc`
```

4. Clone this repo and put its DAS workflow on Darwin, recompile

```
git clone https://github.com/AliAlkadhim/NP-MC-JetTuning.git
cp -r DAS_RivetNtupliser/RivetNtupliser/* Core

```






## Running RivetNtuplizer



Running `cd Ntupliser && tree` displays all the different directories and files in each directory

`tree`




# Explanation of RivetNtupliser
Starting a blank EDAnalyzer (with `mkedanlzr DemoAnalyzer`) gives the following template
![](Pasted%20image%2020230718183351.png)

With the Buildfile in plugins being
![](Pasted%20image%2020230718183630.png)
DAS kind of follows this, but with internally defined plugins, with Core having these subpackages
![](Pasted%20image%2020230718183727.png)

For example, the JEC subpackage:

![](Pasted%20image%2020230718183848.png)


# Running on a [rivet docker](https://hub.docker.com/u/hepstore)

TODO: File better directory management. 
- export `DOCKER` as the path to the docker work dir, and `REPO` as the shared directory inside docker, where my repo is mounted
- Go to `DOCKER` to install all the stuff, and `REPO` where you run stuff

1. Run the image interactively

```bash
docker run --rm -v /home/ali/Desktop/Pulled_Github_Repositories/NP-MC-JetTuning:/work/shared --privileged -it hepstore/prof2-tutorial 
```


2. Get HEPMC3
```
source install_hepmc3.sh
```

3. Get the pythia example files, compile main42 and test it

```
mkdir pythia && cd pythia && wget https://pythia.org/download/pythia83/pythia8309.tar 
&& tar -xf pythia8309.tar
```

3. Compile `main42.cc` for your system

4. Make rivet analysis and compile (with root flag `-r`)
```
rivet-build -r RivetRIVET_NTUPLIZER.so RIVET_NTUPLIZER.cc
rivet --pwd -a RIVET_NTUPLIZER ../pythia/pythia8309/examples/42_test.hepmc
```


## Running on a other cvmfs cluster like lxplus
