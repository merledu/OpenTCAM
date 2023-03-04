"""
List of all pip packages imported
"""

import logging
import os
from migen import *
from migen.fhdl.verilog import convert

# ===========================================================================================
# ======================================= Begin Class =======================================
# ===========================================================================================

class tcamMemBlock7x64(Module):
    """
    Generates the verilog code for a TCAM 7x64 memory block.
    """

    # * ----------------------------------------------------------------- Variables
    def __init__(self):
        """
        Constructor: call IO ports and logic here

        **Variables:**
        :param list inputs          list containing objects for all input ports.
        :param list outputs         list containing objects for all output ports.
        :param str __sramModule:    module definition name of the SRAM block.
        :return str verilogCode:    store RTL code of the encoder.
        """
        # * variables
        self.__sramModule = 'sky130_sram_1kbyte_1rw1r_32x256_8'
        self.verilogCode = ''

        # * signals
        self.inputs = []
        self.outputs = []

        # * setup IO ports
        self.ioPorts()
        # * generate block RTL
        self.logicBlock()

    def ioPorts(self):
        """
        Create Signal objects for all the input ports of various widths and output ports of various widths.
        """
        # * setup input ports
        self.inClk     = Signal(1, name_override='in_clk')
        logging.info('Created tcamMemBlock7x64 input port: {:>s}'.format(self.inClk.name_override))
        self.inCsb     = Signal(1, name_override='in_csb')
        logging.info('Created tcamMemBlock7x64 input port: {:>s}'.format(self.inCsb.name_override))
        self.inWeb     = Signal(1, name_override='in_web')
        logging.info('Created tcamMemBlock7x64 input port: {:>s}'.format(self.inWeb.name_override))
        self.inWmask   = Signal(4, name_override='in_wmask')
        logging.info('Created tcamMemBlock7x64 input port: {:>s}[{:d}:0]'.format(self.inWmask.name_override, 4))
        self.inAddr    = Signal(8, name_override='in_addr')
        logging.info('Created tcamMemBlock7x64 input port: {:>s}[{:d}:0]'.format(self.inAddr.name_override, 8))
        self.inWdata   = Signal(32, name_override='in_wdata')
        logging.info('Created tcamMemBlock7x64 input port: {:>s}[{:d}:0]'.format(self.inWdata.name_override, 32))
        # * add all input ports to an input list
        self.inputs = [self.inClk, self.inCsb, self.inWeb, self.inWmask, self.inAddr, self.inWdata]
        logging.info('Created list of all input ports')
        # * setup output ports
        self.outRdata  = Signal(64, name_override='out_rdata')
        logging.info('Created tcamMemBlock7x64 output port: {:>s}[{:d}:0]'.format(self.outRdata.name_override, 64))
        # * add all output ports to an output list
        self.outputs = [self.outRdata]
        logging.info('Created list of all output ports')

    def logicBlock(self):
        """
        Setup the sequential logic for creating a TCAM 7x64 memory block using migen.
        """
        # * ----- setup write address logic
        awAddr = Signal(8, name_override='aw_addr')
        self.comb += awAddr.eq(Cat(Replicate(~self.inWeb, 8)) & self.inAddr)
        logging.info('Created write address logic')

        # * ----- setup Read/Search address
        arAddr1 = Signal(8, name_override='ar_addr1')
        arAddr2 = Signal(8, name_override='ar_addr2')
        # * always read/search lower 128 rows
        self.comb += arAddr1.eq(Cat(self.inAddr[0:7], 0b0))
        # * always read/search upper 128 rows
        self.comb += arAddr2.eq(Cat(self.inAddr[0:7], 0b1) & Cat(Replicate(self.inWeb, 8)))
        logging.info('Created read/search address logic')

        # * ----- PMA
        rdataLower  = Signal(32, name_override='rdata_lower')
        rdataUpper  = Signal(32, name_override='rdata_upper')
        rdata       = Signal(64, name_override='rdata')

        self.comb += rdata.eq(Cat(rdataLower, rdataUpper))
        self.comb += self.outRdata.eq(rdata)
        logging.info('Created upper and lower potential matcha address logic')

        # * ----- instantiate the sky130 1KB RAM module as submodule
        self.specials += Instance(
            of=self.__sramModule,                       # module name
            name='dut_vtb',                             # instance name
            # Port 0: RW
            i_clk0=self.inClk,                          # input port (use i_<portName>)
            i_csb0=self.inCsb,                          # input port (use i_<portName>)
            i_web0=self.inWeb,                          # input port (use i_<portName>)
            i_wmask0=self.inWmask,                      # input port (use i_<portName>)
            i_addr0=Mux(self.inWeb, arAddr1, awAddr),   # input port (use i_<portName>)
            i_din0=self.inWdata,                        # input port (use i_<portName>)
            o_dout0=rdataLower,                         # output port (use o_<portName>)
            # Port 1: R
            i_clk1=self.inClk,                          # input port (use i_<portName>)
            i_csb1=self.inCsb,                          # input port (use i_<portName>)
            i_addr1=arAddr2,                            # input port (use i_<portName>)
            o_dout1=rdataUpper                          # output port (use o_<portName>)
        )
        logging.info('Instantiated {:s} module'.format(self.__sramModule))

# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================

def genVerilogTcamMemBlock7x64(filePath):
    """
    Main user function for class tcamMemBlock7x64.
    Creates the IO ports for the verilog RTL module definition.
    Generates the verilog code for a TCAM 7x64 memory block.

    :param str filePath:        absolute path for the verilog file.
    :return str:                RTL code of the TCAM 7x64 memory.
    """
    # * instantiate the module
    tcamMem = tcamMemBlock7x64()

    # * ----- setup the IO ports for the verilog module definition
    # * input port set
    inPortsSet = set(tcamMem.inputs)
    # * output port set
    outPortsSet = set(tcamMem.outputs)
    # * combine input and output sets
    moduleIOs = inPortsSet.union(outPortsSet)

    # * generate the verilog code
    moduleName = os.path.basename(filePath).replace('.sv', '')
    tcamMem.verilogCode = convert(tcamMem, name=moduleName, ios=moduleIOs)
    logging.info('Generated TCAM Memory 7x64 verilog module RTL')

    # * write verilog code to a file
    with open(filePath, 'w', encoding='utf-8') as rtl:
        rtl.write(str(tcamMem.verilogCode))
    logging.info('Created rtl file "{:s}"'.format(filePath))

    return str(tcamMem.verilogCode)