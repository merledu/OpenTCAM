"""
List of all pip packages imported
"""

import logging
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
    # * ----------------------------------------------------------------- Variables
    def __init__(self, ports):
        self.numInputs = ports
        self.verilogCode = ''

        # * setup IO ports
        # self.ioPorts()
        # * generate block RTL
        # self.logicBlock()


# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================
