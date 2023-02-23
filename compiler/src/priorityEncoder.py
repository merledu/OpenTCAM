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
    _summary_

    :param _type_ Module: _description_
    :return _type_: _description_
    """
    # * ----------------------------------------------------------------- Functions
    def __init__(self, ports):
        """
        _summary_

        :param _type_ ports: _description_
        """
        self.inputWidth = ports
        self.outputWidth = 0
        self.verilogCode = ''

        # * setup IO ports
        self.ioPorts()
        # * generate block RTL
        self.logicBlock()

    def ioPorts(self):
        """
        _summary_
        """
        # * check if input port width is of 2^N
        if math.floor(math.log2(self.inputWidth)) == math.ceil(math.log2(self.inputWidth)):
            logging.info('"VALID": priority encoder input width {:d} is of 2^N'.format(self.inputWidth))
            # * set output port width of log2(N)
            self.outputWidth = int(math.log2(self.inputWidth))
            logging.info('priority encoder output width: {:d}'.format(self.outputWidth))
            # * create IO port objects
            self.inputs = Signal(self.inputWidth, name_override='in_data')
            logging.info('Created priority encoder input port: {:>s}'.format('in_data'))
            self.outputs = Signal(self.outputWidth, name_override='out_data')
            logging.info('Created priority encoder output port: {:>s}'.format('out_data'))
        else:
            print('num isnt 2^N', type(self.inputWidth))
            logging.error('"INVALID": priority encoder input width {:d} isnt of 2^N'.format(self.inputWidth))
            sys.exit('"INVALID": priority encoder input width {:d} isnt of 2^N'.format(self.inputWidth))

    def logicBlock(self):
        """
        _summary_
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
    _summary_

    :param _type_ ports: _description_
    :param _type_ filePath: _description_
    :return _type_: _description_
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
