#!/bin/bash
mkdir pythia && cd pythia && wget https://pythia.org/download/pythia83/pythia8309.tar && tar -xf pythia8309.tar 
./configure --with-hepmc3=/home/HepMC3/
make -j `nproc`
make install
