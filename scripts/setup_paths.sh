#!/bin/bash

# ------------------------------ add folder compiler file path here
export DIR_COMPILER         = ${OPENTCAM_ROOT}/compiler

# --------------- config files
export DIR_COMP_CONFIGS     = ${DIR_COMPILER}/configs

# --------------- py source code
export DIR_COMP_SRC         = ${DIR_COMPILER}/src

# --------------- py tests
export DIR_COMP_TESTS       = ${DIR_COMPILER}/tests

# ------------------------------ add folder scripts file path here
export DIR_SCRIPTS     = ${OPENTCAM_ROOT}/scripts
export SETUP_PATHS     = ${OPENTCAM_ROOT}/scripts/setup_paths.sh
export SETUP_VENV      = ${OPENTCAM_ROOT}/scripts/setup_venv.sh

# ------------------------------ add folder py venv file path here
export DIR_VENV         = ${OPENTCAM_ROOT}/.pyVenvOpenTcam

# ------------------------------ add folder docs file path here
export DIR_DOCS        = ${OPENTCAM_ROOT}/docs

# ------------------------------ add folder images file path here
export DIR_IMAGES      = ${OPENTCAM_ROOT}/images
