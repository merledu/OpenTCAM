"""
List of all pip packages imported
"""

from migen import *
from migen.fhdl.verilog import convert

# ===========================================================================================
# ======================================= Begin Class =======================================
# ===========================================================================================

class tcamMemTopwrapper(Module):
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

        # * setup IO ports
        self.ioPorts()
        # * generate block RTL
        # self.logicBlock()
