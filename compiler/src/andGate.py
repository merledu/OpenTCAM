"""
List of all pip packages imported
"""

import logging
from migen import *
from migen.fhdl.verilog import convert

# ===========================================================================================
# ======================================= Begin Class =======================================
# ===========================================================================================

class andGate(Module):
    """
    _summary_

    """

    # * ----------------------------------------------------------------- Variables
    # Constructor: setup IO ports and logic here
    def __init__(self, ports, dataWidth) -> None:
        """
        _summary_

        :param _type_ ports: _description_
        :param _type_ dataWidth: _description_
        :return _type_ verilogCode: _description_
        """
        self.numInputs = ports
        self.numInputWidth = dataWidth
        self.verilogCode = ""

    def ioPorts(self, inputs, dataWidth):
        """
        _summary_

        :param _type_ inputs: _description_
        :param _type_ dataWidth: _description_
        """
        self.inputs = []
        for inputs in range(inputs):
            tempPort = Signal(dataWidth, name_override='in_data{}'.format(inputs))
            self.inputs.append(tempPort)
            logging.info('Created AND gate input port: {:>s}{:d}'.format('in_data', inputs))
        self.outputs = Signal(dataWidth, name_override='out_data')
        logging.info('Created AND gate output port: {:>s}{:d}'.format('in_data', inputs))



# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================
