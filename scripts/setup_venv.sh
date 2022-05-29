#!/bin/bash

# create virtual env
python3 -m venv .pyvenv
# activate the py virtual environment
source .pyvenv/bin/activate

# upgrade pip in virtual environment
pip install --upgrade pip
echo -e "\n"
# display packages installed
pip list
echo -e "\n"
# install necessary pip packages
python3 -m pip install -r requirements.txt
echo -e "\n"
# display upated packages installed
pip list
echo -e "\n"
