FROM hepstore/prof2-tutorial

MAINTAINER Ali AlKadhim vsp_ali@yahoo.com
RUN yum -y update && yum clean all 

RUN yum install -y \
	gcc \
	openssl-devel \
	bzip2-devel \
	libffi-devel \
	zlib-devel \
	xz-devel \
	httpd \
	nano \
	git \
	python-virtualenv.noarch \
	which \
	mlocate \
	dnf
# INSTALL HEPMC
git clone https://gitlab.cern.ch/hepmc/HepMC3.git
 mkdir hepmc3-build
  cd hepmc3-build

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:path_to_ROOT6_libraries

RUN cmake -DHEPMC3_ENABLE_ROOTIO=ON -DROOT_DIR=path_to_ROOT6_installation -DHEPMC3_ENABLE_ROOTIO=OFF -DCMAKE_INSTALL_PREFIX=../hepmc3-install .
RUN make -j8 install

##### EXPERIMENTAL
#   wget http://hepmc.web.cern.ch/hepmc/releases/HepMC3-3.2.6.tar.gz
#   tar -xzf HepMC3-3.2.6.tar.gz
#   mkdir hepmc3-build
#   cd hepmc3-build
#   cmake -DCMAKE_INSTALL_PREFIX=../hepmc3-install   \
#         -DHEPMC3_ENABLE_ROOTIO:BOOL=OFF            \
#         -DHEPMC3_ENABLE_PROTOBUFIO:BOOL=OFF        \
#         -DHEPMC3_ENABLE_TEST:BOOL=OFF              \
#         -DHEPMC3_INSTALL_INTERFACES:BOOL=ON        \
#         -DHEPMC3_BUILD_STATIC_LIBS:BOOL=OFF        \
#         -DHEPMC3_BUILD_DOCS:BOOL=OFF     \
#         -DHEPMC3_ENABLE_PYTHON:BOOL=ON   \
#         -DHEPMC3_PYTHON_VERSIONS=2.7     \
#         -DHEPMC3_Python_SITEARCH27=../hepmc3-install/lib/python2.7/site-packages \
#         ../HepMC3-3.2.6
#   make
#   make install

###############################
# INSTALL PYTHIA EXAMPLES
cd /work
mkdir pythia && cd pythia && wget https://pythia.org/download/pythia83/pythia8309.tar && tar -xf pythia8309.tar 
./configure --with-hepmc3=/home/HepMC3/
make -j 8
make install
cd examples && make main42
# && export PYTHIA_EXAMPLE_DIR=/work/pythia/pythia8309/examples
# git clone https://gitlab.cern.ch/DasAnalysisSystem/Core.git