"""
List of all pip packages imported
"""

import logging
from migen import *
from migen.fhdl.verilog import convert

# ===========================================================================================
# ======================================= Begin Class =======================================
# ===========================================================================================

class tcamMemory7x64(Module):
    """
    _summary_

    :param _type_ Module: _description_
    """

    # * ----------------------------------------------------------------- Variables
    def __init__(self):
        """
        _summary_
        """
        # * variables
        self.__sramModule = 'sky130_sram_1kbyte_1rw1r_32x256_8'

        # * setup IO ports
        self.ioPorts()
        # * generate block RTL
        self.logicBlock()

    def ioPorts(self):
        """
        _summary_
        """
        self.inputs = []
        # * setup input ports
        self.inClk     = Signal(1, name_override='in_clk')
        logging.info('Created tcamMemory7x64 input port: {:>s}'.format(self.inClk.name_override))
        self.inCsb     = Signal(1, name_override='in_csb')
        logging.info('Created tcamMemory7x64 input port: {:>s}'.format(self.inCsb.name_override))
        self.inWeb     = Signal(1, name_override='in_web')
        logging.info('Created tcamMemory7x64 input port: {:>s}'.format(self.inWeb.name_override))
        self.inWmask   = Signal(4, name_override='in_wmask')
        logging.info('Created tcamMemory7x64 input port: {:>s}[{:d}:0]'.format(self.inWmask.name_override, 4))
        self.inAddr    = Signal(8, name_override='in_addr')
        logging.info('Created tcamMemory7x64 input port: {:>s}[{:d}:0]'.format(self.inAddr.name_override, 8))
        self.inWdata   = Signal(32, name_override='in_wdata')
        logging.info('Created tcamMemory7x64 input port: {:>s}[{:d}:0]'.format(self.inWdata.name_override, 32))
        # * add all input ports to an input list
        self.inputs = [self.inClk, self.inCsb, self.inWeb, self.inWmask, self.inAddr, self.inWdata]
        logging.info('Created list of all input ports')
        # * setup output ports
        self.outRdata  = Signal(64, name_override='out_rdata')
        logging.info('Created tcamMemory7x64 output port: {:>s}[{:d}:0]'.format(self.outRdata.name_override, 64))
        # * add all output ports to an output list
        self.outputs = self.outRdata
        logging.info('Created list of all output ports')
