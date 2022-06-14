# OpenTCAM Root
OPENTCAM_ROOT = $(shell git rev-parse --show-toplevel)

# ------------------------------------------ PATHS
include ./scripts/setup_paths.sh

# ------------------------------------------ VARIABLES
# ------------------------------------------ TARGETS
default: help

loadpaths:
	$(info DIR_COMPILER:	$(DIR_COMPILER))
	$(info DIR_COMP_MAIN:	$(DIR_COMP_MAIN))
	$(info DIR_SCRIPTS:	$(DIR_SCRIPTS))
	$(info SETUP_PATHS:	$(SETUP_PATHS))
	$(info SETUP_VENV:	$(SETUP_VENV))
	$(info DIR_DOCS:	$(DIR_DOCS))
	$(info DIR_IMAGES:	$(DIR_IMAGES))

setupvenv:
	clear
	@ echo -------------------- Creating Python Virtual Environment -------------------
	@ echo " "
	@ bash ${SETUP_VENV}
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

runpycode:
	clear
	@ echo " "
	@ echo --------------------------------- OpenTCAM ---------------------------------
	@ python3 $(DIR_COMPILER)/main.py
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

cleanvenv:
	@ echo ------------------- Deleting Python Virtual Environment/s ------------------
	@ echo " "
	@ rm -rf .py*
	@ echo ------------------------------------ DONE ----------------------------------

cleanlogs:
	@ echo -------------------------- Deleting all log files --------------------------
	@ rm -rf *.log
	@ echo ------------------------------------ DONE ----------------------------------

cleandumpfiles: cleanlogs

deepclean:
	clear
	@ echo ------------------------- Deep Cleaning Environment ------------------------
	@ echo " "
	@ make cleanvenv 
	@ make cleandumpfiles
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

help:
	clear
	@ echo " "
	@ echo ---------------------------- Targets in Makefile ---------------------------
	@ echo ----------------------------------------------------------------------------
	@ echo " "
	@ echo " loadpaths:		display various loaded file paths"
	@ echo " setupvenv:		create a virtual environemnt with all necessary dependencies"
	@ echo " runpycode:		simulate openTCAM"
	@ echo " "
	@ echo " cleanvenv:		remove the virtual env"
	@ echo " cleanlogs:		remove all .log files"
	@ echo " cleandumpfiles:	removes all files generated"
	@ echo " "
	@ echo " deepclean:		delete everything (cleandumpfiles + cleanvenv)"
	@ echo " "
	@ echo " help:			humble people ask for help :)"
	@ echo ----------------------------------------------------------------------------
	@ echo " "

