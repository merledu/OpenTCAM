"""
List of all pip packages imported
"""

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
        """
        self.numInputs = ports
        self.numInputWidth = dataWidth
        self.verilogCode = ""


# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================
