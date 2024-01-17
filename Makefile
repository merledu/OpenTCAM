# OpenTCAM Root
OPENTCAM_ROOT = $(shell git rev-parse --show-toplevel)

# ------------------------------------------ PATHS
include ./scripts/setup_paths.sh

# ------------------------------------------ VARIABLES
include ./scripts/setup_vars.sh

# ------------------------------------------ TARGETS
default: help

loadpaths:
	$(info DIR_COMPILER:		$(DIR_COMPILER))
	$(info DIR_COMP_CONFIGS:	$(DIR_COMP_CONFIGS))
	$(info DIR_COMP_LIB:		$(DIR_COMP_LIB))
	$(info DIR_COMP_SRC:		$(DIR_COMP_SRC))
	$(info DIR_COMP_TESTS:		$(DIR_COMP_TESTS))
	$(info DIR_SCRIPTS:		$(DIR_SCRIPTS))
	$(info DIR_VENV:		$(DIR_VENV))
	$(info DIR_DOCS:		$(DIR_DOCS))
	$(info DIR_IMAGES:		$(DIR_IMAGES))
	$(info DIR_LOGS:		$(DIR_LOGS))

install_dependencies:
	@ clear
	@ echo ----------------------- Installing basic dependencies ----------------------
	@ sudo apt install git make python3 python3-pip python3-venv
	@ sudo python3 -m pip install --user virtualenv
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

venv_opentcam:
	clear
	@ echo ------------------- Creating OpenTCAM Virtual Environment ------------------
	@ echo " "
	@ bash ${DIR_SCRIPTS}/setup_venv.sh
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

sram_tablemap:
	@ echo " "
	@ echo ---------------------------- OpenTCAM Table Map ----------------------------
	@ [ -d ${DIR_LOGS} ] || mkdir -p ${DIR_LOGS}
	@ python3 $(DIR_COMP_SRC)/mainTableMapping.py \
	--tcamConfig $(TCAMCONFIG) \
	-excel $(EXCEL) -html $(HTML) -json $(JSON) -txt $(TXT) \
	--debug $(DEBUG) --verbose $(VERBOSE)
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

tcam_rtl:
	@ echo " "
	@ echo ------------------------------- OpenTCAM RTL -------------------------------
	@ [ -d ${DIR_LOGS} ] || mkdir -p ${DIR_LOGS}
	@ python3 $(DIR_COMP_SRC)/mainTcamRTLGenerator.py \
	--tcamWrapConfig $(TCAMWRAPCONFIG) \
	--timeunit $(TIMEUNIT) --timeprecision $(TIMEPRECISION) \
	--debug $(DEBUG) --verbose $(VERBOSE)
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

run_unittest:
	@ echo " "
	@ echo --------------------------- OpenTCAM Unit Test -----------------------------
	@ python3 -m pytest -v -m ${MARKER} compiler/tests/*.py
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "
# run single test using test_class_name and test_name
# @ python3 -m pytest -v compiler/tests/${TESTCLASS}.pytepy::${TESTCLASS}::${TESTNAME}

run_regression:
	@ echo " "
	@ echo --------------------------- OpenTCAM Unit Tests ----------------------------
	@ python3 -m pytest -v -s --ff --cache-clear ${DIR_COMP_TESTS}/*.py
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

testmarkers:
	@ echo " "
	@ echo -------------------------- OpenTCAM Test Markers ---------------------------
	@ pytest --markers
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

run_coverage:
	@ echo " "
	@ echo -------------------------- OpenTCAM Test Coverage --------------------------
	@ coverage erase
	@ echo " "
	@ coverage run --branch -m pytest -v --ff --cache-clear ${DIR_COMP_TESTS}/*.py
	@ echo " "
	@ coverage report -m
	@ echo " "
	@ coverage html --precision=4 --title=${COV_TITLE} -d ${COV_FOLDER}
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

gen_apidocs:
	@ echo " "
	@ echo ------------------------ OpenTCAM API Documentation ------------------------
	@ pdoc ./compiler/src/tableMapping.py -o ${DIR_DOCS}
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

run_pylint:
	@ echo " "
	@ echo ------------------------------ Running PyLint ------------------------------
	@ [ -d ${DIR_LOGS} ] || mkdir -p ${DIR_LOGS}
	@ pylint ${DIR_COMP_SRC}/mainTableMapping.py \
	--output-format=${FORMAT}:./logs/pylint.log,${COLOR} \
	--score=${SCORE} --reports=${REPORTS} \
	--rcfile=.pylintrc
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

# @ pylint ${DIR_COMP_SRC}/*.py \

run_isort:
	@ echo " "
	@ echo ------------------------------ Running iSort ------------------------------
	@ isort -v compiler/src/mainTableMapping.py
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

run_black:
	@ echo " "
	@ echo ------------------------------ Running Black ------------------------------
	@ black -v compiler/src/mainTableMapping.py
	@ echo ---------------------------------- DONE -----------------------------------
	@ echo " "

format_pycode: run_isort run_black

install_iverilog:
	@ echo " "
	@ echo ------------------------- INSTALLING Icarus Verilog ------------------------
	@ bash ${DIR_SCRIPTS}/install_iverilog.sh
	@ echo ----------------------------------- DONE -----------------------------------
	@ echo " "

install_yosys:
	@ echo " "
	@ echo ------------------- INSTALLING Yosys Open SYnthesis Suite ------------------
	@ bash ${DIR_SCRIPTS}/install_yosys.sh
	@ echo ----------------------------------- DONE -----------------------------------
	@ echo " "

clean_venv:
	@ echo " "
	@ echo ------------------- Deleting Python Virtual Environment/s ------------------
	@ echo " "
	@ rm -rf .py* venv* .venv*
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

clean_logs:
	@ echo " "
	@ echo --------------------------- Deleting Log File/s ----------------------------
	@ rm -rf logs
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

clean_sramtablemap:
	@ echo " "
	@ echo ---------------------- Deleting SRAM Table Map File/s ----------------------
	@ rm -rf sramTables
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

clean_apidocs:
	@ echo " "
	@ echo --------------------- Deleting API Documentation File/s --------------------
	@ rm -rf docs
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

clean_tcamrtl:
	@ echo " "
	@ echo ------------------------- Deleting TCAM RTL File/s -------------------------
	@ rm -rf tcam_mem_rtl
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

clean_tests:
	@ echo " "
	@ echo --------------------------- Deleting Test Cache ----------------------------
	@ rm -rf ${DIR_COMP_TESTS}/.test_cache
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

clean_coverage:
	@ echo " "
	@ echo ------------------------- Deleting Coverage File/s -------------------------
	@ rm -rf coverage* htmlcov .coverage
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

clean_all: 
	@ make clean_logs clean_sramtablemap clean_tcamrtl clean_tests clean_coverage clean_apidocs

deepclean:
	clear
	@ echo " "
	@ echo ------------------------- Deep Cleaning Environment ------------------------
	@ echo " "
	@ make cleanvenv
	@ make clean_all
	@ echo ------------------------------------ DONE ----------------------------------
	@ echo " "

help:
	clear
	@ echo " "
	@ echo ---------------------------- Targets in Makefile ---------------------------
	@ echo ----------------------------------------------------------------------------
	@ echo " "
	@ echo " loadpaths:			display various loaded file paths"
	@ echo " install_dependencies:		install basic dependencies"
	@ echo " install_iverilog:		install Icarus Verilog (OPTIONAL)"
	@ echo " install_yosys:			install Yosys Open SYnthesis Suite (OPTIONAL)"
	@ echo " "
	@ echo " opentcam_venv:			create virtual environment to simulate code "
	@ echo " "
	@ echo " tcamtablemap:			generate TCAM -> SRAM table mapping"
	@ echo " 	TCAMCONFIG=tcamTableX			tcam table config name"
	@ echo " 	DEBUG=1/0				debugging on/off"
	@ echo " 	VERBOSE=1/0				verbosity on/off"
	@ echo " "
	@ echo " tcamrtl:			generate TCAM memory RTL wrapper"
	@ echo "	TCAMWRAPCONFIG=tcamMemWrapper_XxY	tcam memory config name"
	@ echo "	TIMEUNIT=1ns				set timeunit resolution" 
	@ echo "	TIMEPRECISION=1ps			set timeprecision resolution"
	@ echo "	DEBUG=1/0				debugging on/off"
	@ echo "	VERBOSE=1/0				verbosity on/off"
	@ echo " "
	@ echo " gen_apidocs:			generate OpenTCAM API Documentation"
	@ echo " "
	@ echo " run_unittest:			run single table mapping test case "
	@ echo " run_regression:			run pytest regression"
	@ echo " testmarkers:			view opentcam table mapping test/s markers"
	@ echo " run_coverage:			run opentcam table mapping test/s coverage"
	@ echo " "
	@ echo " cleanvenv:			delete python virtual environment/s"
	@ echo " cleanlogs:			delete log files"
	@ echo " cleanapidocs:			delete generated API documentation"
	@ echo " cleansramtables:		delete TCAM -> SRAM table maps "
	@ echo " cleantcamrtl:			delete TCAM memory block RTL files"
	@ echo " cleantests:			delete py tests cache "
	@ echo " cleancoverage:			delete coverage stats"
	@ echo " clean_all:			delete all dump files"
	@ echo " deepclean:			delete all dump files + virtual environment/s"
	@ echo " "
	@ echo " help:				humble people ask for help :)"
	@ echo " "
	@ echo ----------------------------------------------------------------------------
	@ echo " "
