#!/bin/bash

# export start_time=$SECONDS
export start_time=$(date +%s.%3N)

# virtualenv name
export VIRENV=.pyVenvOpenTcam

# python3 -m pip uninstall -y virtualenv

# check python3 version
echo -e "$(python3 --version)"
echo -e "$(command -v python3)\n"

# check if pip package virtualenv is installed
CHECK=$(pip show virtualenv 2>&1 >/dev/null)
# echo "output: $CHECK"

if [[ $CHECK = "WARNING: Package(s) not found: virtualenv" ]]
then
    echo -e "package virtualenv NOT FOUND"
    echo -e "INSTALLING pip package virtualenv\n"
    python3 -m pip install --user virtualenv
    echo -e "\n\n"
else
    echo -e "pip package virtualenv already INSTALLED\n\n"
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
python3 -m pip install --no-cache-dir -r requirements.txt
echo -e "\n"

# display upated packages installed
pip list -v
echo -e "\n"

# script simuation time
export end_time=$(date +%s.%3N)
export elapsed_time=$(echo "scale=3; $end_time - $start_time" | bc)
echo -e "Total time: ${elapsed_time} sec"
