# NP-MC-JetTuning

Rivet + Different MC Generators for Jet Studies

## Running on a [rivet docker](https://hub.docker.com/u/hepstore)

TODO: File better directory management. 
- export `DOCKER` as the path to the docker work dir, and `REPO` as the shared directory inside docker, where my repo is mounted
- Go to `DOCKER` to install all the stuff, and `REPO` where you run stuff

1. Run the image interactively

```bash
docker run --rm -v /home/ali/Desktop/Pulled_Github_Repositories/NP-MC-JetTuning:/work/shared --privileged -it hepstore/prof2-tutorial 
```


3. Get HEPMC
```
 git clone https://gitlab.cern.ch/hepmc/HepMC3.git
mkdir hepmc3-build
  cd hepmc3-build
```

3. Get the pythia example files, compile main42 and test it
mkdir pythia && cd pythia && wget https://pythia.org/download/pythia83/pythia8309.tar && tar -xf pythia8309.tar && export PYTHIA_EXAMPLE_DIR=/work/pythia/pythia8309/examples

3. Compile `main42.cc` for your system

4. Make rivet analysis and compile (with root flag `-r`)
```
rivet-build -r RivetRIVET_NTUPLIZER.so RIVET_NTUPLIZER.cc
rivet --pwd -a RIVET_NTUPLIZER ../pythia/pythia8309/examples/42_test.hepmc
```


## Running on a cvmfs cluster like lxplus
