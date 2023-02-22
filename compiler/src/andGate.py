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

        # * setup IO ports
        self.ioPorts()
        # * generate block RTL
        self.logicBlock()

    def ioPorts(self):
        """
        declare all the input output ports here

        :param _type_ inputs: _description_
        :param _type_ dataWidth: _description_
        """
        self.inputs = []
        for port in range(self.numInputs):
            tempPort = Signal(self.numInputWidth, name_override='in_data{}'.format(port))
            self.inputs.append(tempPort)
            logging.info('Created AND gate input port: {:>s}{:d}'.format('in_data', port))
        self.outputs = Signal(self.numInputWidth, name_override='out_data')
        logging.info('Created AND gate output port: {:>s}{:d}'.format('out_data', port))

    def logicBlock(self):
        """
        Example of using reduce() to create an AND gate
        """
        self.comb += self.outputs.eq(reduce(lambda x, y: x & y, self.inputs))
        logging.info('Generated AND gate logic')

# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================

def genVerilogAndGate(ports, dataWidth, filePath):
    """
    _summary_

    :param _type_ ports: _description_
    :param _type_ dataWidth: _description_
    :param _type_ filePath: _description_
    :return _type_: _description_
    """
    # * instantiate the module
    gate = andGate(ports=ports, dataWidth=dataWidth)

    # * ----- setup the IO ports for the verilog module definition
    # * input port set
    myinputs = {gate.inputs[i] for i in range(ports)}
    # * output port set
    myoutputs = {gate.outputs}
    # * combine input and output sets
    myports = myinputs.union(myoutputs)
    logging.info('Generated AND gate verilog module definition')

    # * generate the verilog code
    gate.verilogCode = convert(gate, name='andGate', ios=myports)
    logging.info('Generated AND gate verilog module RTL')

    # * write verilog code to a file
    with open(filePath, 'w', encoding='utf-8') as rtl:
        rtl.write(str(gate.verilogCode))
    logging.info('Created rtl file {:s}'.format(filePath))

    return str(gate.verilogCode)
