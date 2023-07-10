#!/bin/bash
wget http://hepmc.web.cern.ch/hepmc/releases/HepMC3-3.2.6.tar.gz
tar -xzf HepMC3-3.2.6.tar.gz
mkdir hepmc3-build
cd hepmc3-build
cmake -DCMAKE_INSTALL_PREFIX=../hepmc3-install   \
    -DHEPMC3_ENABLE_ROOTIO:BOOL=OFF            \
    -DHEPMC3_ENABLE_PROTOBUFIO:BOOL=OFF        \
    -DHEPMC3_ENABLE_TEST:BOOL=OFF              \
    -DHEPMC3_INSTALL_INTERFACES:BOOL=ON        \
    -DHEPMC3_BUILD_STATIC_LIBS:BOOL=OFF        \
    -DHEPMC3_BUILD_DOCS:BOOL=OFF     \
    -DHEPMC3_ENABLE_PYTHON:BOOL=ON   \
    -DHEPMC3_PYTHON_VERSIONS=2.7     \
    -DHEPMC3_Python_SITEARCH27=../hepmc3-install/lib/python2.7/site-packages \
    ../HepMC3-3.2.6
make -j `nproc`
make install


