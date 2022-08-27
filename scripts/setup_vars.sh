#!/bin/bash

# virtual env names
VIRENV      := .pyVenvOpenTcam

# python compiler src main args
TCAMCONFIG 	:= tcamTable2
EXCEL       := 1
HTML        := 0
JSON        := 0
TXT         := 1
DEBUG 		:= 0
VERBOSE 	:= 1

# python pytest testing framework
RUNNER      := pytest
TESTCLASS   := 
TESTNAME    := 
MARKER      := 

# python coverage args
COV_TITLE   := "OpenTCAM Coverage"
COV_FOLDER  := "coverage_html"