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
        # self.logicBlock()
    
    def ioPorts(self):
        """
        _summary_
        """        
        # * check if input port width is of 2^N
        if math.floor(math.log2(self.inputWidth)) == math.ceil(math.log2(self.inputWidth)):
            logging.info('"VALID": prioirty encoder input width {:d} is of 2^N'.format(self.inputWidth))
            # * set output port width of log2(N)
            self.outputWidth = int(math.log2(self.inputWidth))
            logging.info('prioirty encoder output width: {:d}'.format(self.outputWidth))
            # * create IO port objects
            self.inputs = Signal(self.inputWidth, name_override='in_data')
            logging.info('Created prioirty encoder input port: {:>s}'.format('in_data'))
            self.outputs = Signal(self.outputWidth, name_override='out_data')
            logging.info('Created prioirty encoder output port: {:>s}'.format('out_data'))
            print(self.inputs)
            print(self.outputs)
        else:
            print('num isnt 2^N', type(self.inputWidth))
            logging.error('"INVALID": prioirty Encoder input width {:d} isnt of 2^N'.format(self.inputWidth))
            sys.exit('"INVALID": prioirty encoder input width {:d} isnt of 2^N'.format(self.inputWidth))


# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================
