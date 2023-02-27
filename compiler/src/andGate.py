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
    Generates the verilog code for an AND gate with N inputs each input M bits wide.
    The output is M bits wide.
    """

    # * ----------------------------------------------------------------- Variables
    def __init__(self, ports, dataWidth):
        """
        Constructor: call IO ports and logic here

        **Public Variables:**
        :param int ports:           number of input ports.
        :param int dataWidth:       width of input ports.
        :return str verilogCode:    store RTL code of the gate.
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
        Create a list of Signal objects for N input ports each of width M. Create a Signal object for an output port of width M.
        """
        self.inputs = []
        for port in range(self.numInputs):
            tempPort = Signal(self.numInputWidth, name_override='in_data{}'.format(port))
            self.inputs.append(tempPort)
            logging.info('Created AND gate input port: {:>s}{:d}[{:d}:0]'.format('in_data', port, self.numInputWidth-1))
        self.outputs = Signal(self.numInputWidth, name_override='out_data')
        logging.info('Created AND gate output port: {:>s}[{:d}:0]'.format('out_data', self.numInputWidth-1))

    def logicBlock(self):
        """
        Setup the combinatorial logic for creating an AND gate using migen. Using the reduce() function to combine all input signals into a single output signal.
        """
        self.comb += self.outputs.eq(reduce(lambda x, y: x & y, self.inputs))
        logging.info('Generated AND gate logic')

# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================

def genVerilogAndGate(ports, dataWidth, filePath):
    """
    Main user function for class andGate.
    Creates the IO ports for the verilog RTL module definition.
    Generates the verilog code for an AND gate with N inputs each input M bits wide. The output is M bits wide.

    :param int ports:           number of input ports.
    :param int dataWidth:       width of input ports.
    :param str filePath:        absolute path for the verilog file.
    :return str:                RTL code of the gate.
    """
    # * instantiate the module
    gate = andGate(ports=ports, dataWidth=dataWidth)

    # * ----- setup the IO ports for the verilog module definition
    # * input port set
    inPortsSet = {gate.inputs[i] for i in range(ports)}
    # * output port set
    outPortsSet = {gate.outputs}
    # * combine input and output sets
    moduleIOs = inPortsSet.union(outPortsSet)
    logging.info('Generated AND gate verilog module definition')

    # * generate the verilog code
    gate.verilogCode = convert(gate, name='andGate', ios=moduleIOs)
    logging.info('Generated AND gate verilog module RTL')

    # * write verilog code to a file
    with open(filePath, 'w', encoding='utf-8') as rtl:
        rtl.write(str(gate.verilogCode))
    logging.info('Created rtl file {:s}'.format(filePath))

    return str(gate.verilogCode)
