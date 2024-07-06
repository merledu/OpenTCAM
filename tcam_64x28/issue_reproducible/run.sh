#!/bin/sh
dir=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
cd $dir;
export DIODE_CELL='sky130_fd_sc_hd__diode_2';
export GRT_ANT_ITERS='15';
export GRT_ANT_MARGIN='10';
export PACKAGED_SCRIPT_0='openlane/scripts/openroad/repair_antennas.tcl';
TOOL_BIN=${TOOL_BIN:-openroad}
$TOOL_BIN -exit $PACKAGED_SCRIPT_0
