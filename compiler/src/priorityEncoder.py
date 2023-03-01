"""
List of all pip packages imported
"""

import logging
import math
import sys
from migen import *
from migen.fhdl.verilog import convert

# ===========================================================================================
# ======================================= Begin Class =======================================
# ===========================================================================================

class priorityEncoder(Module):
    """
    Generates the verilog code for a Priority Encoder with N-bit input and log2(N) bit output.
    """

    # * ----------------------------------------------------------------- Functions
    def __init__(self, ports):
        """
        Constructor: call IO ports and logic here

        **Public Variables:**
        :param list inputs          list containing objects for all input ports.
        :param list outputs         list containing objects for all output ports.
        :param int ports:           number of input ports.
        :return str verilogCode:    store RTL code of the encoder.
        """
        # * variables
        self.inputWidth = ports
        self.outputWidth = 0
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
        Create a Signal object for an input port of width N bits and an output port of width log2(N) bits.
        """
        # * check if input port width is of 2^N
        if math.floor(math.log2(self.inputWidth)) == math.ceil(math.log2(self.inputWidth)):
            logging.info('"VALID": priority encoder input width {:d} is of 2^N'.format(self.inputWidth))
            # * set output port width of log2(N)
            self.outputWidth = int(math.log2(self.inputWidth))
            logging.info('priority encoder output width: {:d}'.format(self.outputWidth))
            # * create IO port objects
            self.inputs = Signal(self.inputWidth, name_override='in_data')
            logging.info('Created priority encoder input port: {:>s}[{:d}:0]'.format('in_data', self.inputWidth-1))
            self.outputs = Signal(self.outputWidth, name_override='out_data')
            logging.info('Created priority encoder output port: {:>s}[{:d}:0]'.format('out_data', self.outputWidth-1))
        else:
            print('num isnt 2^N', type(self.inputWidth))
            logging.error('"INVALID": priority encoder input width {:d} isnt of 2^N'.format(self.inputWidth))
            sys.exit('"INVALID": priority encoder input width {:d} isnt of 2^N'.format(self.inputWidth))

    def logicBlock(self):
        """
        Setup the sequential logic for creating a priority encoder using migen.
        """
        # * dict to store priority cases
        priorityCases = {}
        # * create N priority cases
        for i in reversed(range(self.inputWidth)):
            # * generate one hot encoding
            oneHotEncode = bin(pow(2,i))
            # * add ith priority case
            priorityCases[int(oneHotEncode, 2)] = self.outputs.eq(i)
            logging.info('Created priority case for {:3d} input bit'.format(i))
        # * concat using case
        self.comb += Case(self.inputs, priorityCases)

# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================

def genVerilogPriorityEncoder(ports, filePath):
    """
    Main user function for class priorityEncoder.
    Creates the IO ports for the verilog RTL module definition.
    Generates the verilog code for a Priority Encoder with N-bit input and log2(N) bit output.

    :param int ports:           number of input ports.
    :param str filePath:        absolute path for the verilog file.
    :return str:                RTL code of the encoder.
    """
    # * instantiate the module
    encoder = priorityEncoder(ports=ports)

    # * ----- setup the IO ports for the verilog module definition
    # * input port set
    inPortsSet = {encoder.inputs}
    # * output port set
    outPortsSet = {encoder.outputs}
    # * combine input and output sets
    moduleIOs = inPortsSet.union(outPortsSet)
    logging.info('Generated Priority Encoder verilog module definition')

    # * generate the verilog code
    encoder.verilogCode = convert(encoder, name='priorityEncoder', ios=moduleIOs)
    logging.info('Generated Priority Encoder verilog module RTL')

    # * write verilog code to a file
    with open(filePath, 'w', encoding='utf-8') as rtl:
        rtl.write(str(encoder.verilogCode))
    logging.info('Created rtl file {:s}'.format(filePath))

    return str(encoder.verilogCode)
