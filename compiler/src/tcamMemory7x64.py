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

    def logicBlock(self):
        """
        _summary_
        """
        # * ----- setup write address logic
        awAddr = Signal(8, name_override='aw_addr')
        self.comb += awAddr.eq(Cat(Replicate(~self.inWeb, 8)) & self.inAddr)
        logging.info('Created write address logic')

        # * ----- setup Read/Search address
        arAddr1 = Signal(8, name_override='ar_addr1')
        arAddr2 = Signal(8, name_override='ar_addr2')
        # * always read/search lower 128 rows
        self.comb += arAddr1.eq(Cat(self.inAddr[0:6], 0))
        # * always read/search upper 128 rows
        self.comb += arAddr2.eq(Cat(self.inAddr[0:6], 1) & Cat(Replicate(self.inWeb, 8)))
        logging.info('Created read/search address logic')

        # * ----- PMA
        rdataLower  = Signal(32, name_override='rdata_lower')
        rdataUpper  = Signal(32, name_override='rdata_upper')
        rdata       = Signal(64, name_override='rdata')

        self.comb += rdata.eq(Cat(rdataLower, rdataUpper))
        self.comb += self.outputs.eq(rdata)
        logging.info('Created upper and lower potential matcha address logic')

        # * ----- instantiate the sky130 1KB RAM module as submodule
        self.specials += Instance(
            of=self.__sramModule,                       # module name
            name='dut_vtb',                             # instance name
            i_clk0=self.inClk,                          # input port (use i_<portName>)
            i_csb0=self.inCsb,                          # input port (use i_<portName>)
            i_web0=self.inWeb,                          # input port (use i_<portName>)
            i_wmask0=self.inWmask,                      # input port (use i_<portName>)
            i_addr0=Mux(self.inWeb, arAddr1, awAddr),   # input port (use i_<portName>)
            i_din0=self.inWdata,                        # input port (use i_<portName>)
            o_dout0=rdataLower,                         # input port (use i_<portName>)
            i_clk1=self.inClk,                          # input port (use i_<portName>)
            i_csb1=self.inCsb,                          # input port (use i_<portName>)
            i_addr1=arAddr2,                            # input port (use i_<portName>)
            o_dout1=rdataUpper                          # output port (use o_<portName>)
        )
        logging.info('Instantiated {:s} module'.format(self.__sramModule))

# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================
