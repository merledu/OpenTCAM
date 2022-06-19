#!/bin/bash

cd ~

# instal dependencies
sudo apt install -y build-essential bison flex gperf termcap autoconf

# readline alternatives
sudo apt install -y lib32readline7 lib32readline-dev

# clone iverilog repo
git clone https://github.com/steveicarus/iverilog.git
cd iverilog

# generate the "configure" file
sh autoconf.sh

# compile the source
./configure
make

# run a simple test before installation
make check

# install iverilog
sudo make install

# clean dump
make clean
make disclean

# uninstall iverilog
# sudo make uninstall

