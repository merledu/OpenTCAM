#!/bin/bash

cd ~

# install pre-requisites
sudo apt install -y build-essential python3 bison flex gawk git tcl-dev graphviz xdot \
libreadline-dev libffi-dev pkg-config libboost-system-dev libboost-python-dev libboost-filesystem-dev zlib1g-dev

# clone the yosys repo
git clone https://github.com/YosysHQ/yosys.git
cd yosys

# configure the build system to use a specific compiler:
# use clang
# make config-clang
# or clang
make config-gcc

# build yosys
make
# install yosys (also installs ABC)
sudo make install

# execute tests (iverilog required to be built from source)
make test

# clean all
make clean
make clean-abc 

# to uninstall
# sudo make uninstall
