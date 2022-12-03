#!/bin/bash

# virtual env names
VIRENV      := .pyVenvOpenTcam

DEBUG 		:= 0
VERBOSE 	:= 1

# python opentcam table generator main args
TCAMCONFIG 	:= tcamTable2
EXCEL       := 1
HTML        := 0
JSON        := 0
TXT         := 1

# python opentcam RTL generator main args
TCAMWRAPCONFIG  := tcamMemWrapper_64x28
TIMEUNIT        := 1ns
TIMEPRECISION   := 100ps

# python pytest testing framework
RUNNER      := pytest
TESTCLASS   := 
TESTNAME    := 
MARKER      := 

# python coverage args
COV_TITLE   := "OpenTCAM Coverage"
COV_FOLDER  := "coverage_html"

# python pylint args
# to configure OUTPUT_FMT see output-format flag in compiler/configs/.pylintrc
FORMAT      := msvs
COLOR       := colorized
SCORE       := y
REPORTS     := y
