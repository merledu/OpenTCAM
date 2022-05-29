#!/bin/bash

# virtualenv name
VIRENV=.pyVenvOpenTcam

# check python3 version
check1=$(python3 --version)
echo -e "$check1 \n" 

# check if pip package virtualenv is installed
check2=$(pip show virtualenv)
echo $check2

if [[ $check2 = 'WARNING: Package(s) not found: virtualenv' ]]
then
    echo -e "PIP package virtualenv INSTALLED. \n\n"
else
    echo -e "INSTALLING PIP package virtualenv \n\n"
    sudo apt install -y python3-virtualenv
fi

# create virtual env
echo -e "\n\n--- Creating local python virtual environment ---\n\n"
virtualenv $VIRENV
# activate the py virtual environment
echo -e "\n\n--- Activating local python virtual environment ---\n\n"
source $VIRENV/bin/activate

# upgrade pip in virtual environment
echo -e "--- Upgrading virtual environment pip ---\n\n"
pip install --upgrade pip
echo -e "\n"

# display packages installed
pip list -v
echo -e "\n"

# install necessary pip packages
echo -e "--- INSTALLING pip packages ---\n\n"
python3 -m pip install -r requirements.txt
echo -e "\n"

# display upated packages installed
pip list -v
echo -e "\n"
