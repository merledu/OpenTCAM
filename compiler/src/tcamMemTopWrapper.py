"""
List of all pip packages imported
"""

import logging
import math
from migen import *
from migen.fhdl.verilog import convert

# ===========================================================================================
# ======================================= Begin Class =======================================
# ===========================================================================================

class tcamMemTopWrapper(Module):
    """
    _summary_

    :param _type_ Module: _description_
    """

    # * ----------------------------------------------------------------- Variables
    def __init__(self, memBlocks):
        """
        _summary_
        """
        # * variables
        self.memBlocks = memBlocks  # 4
        self.__inAddrWidth = 0
        self.verilogCode = ''

        # * setup IO ports
        self.ioPorts()
        # * generate block RTL
        self.logicBlock()

    def ioPorts(self):
        """
        _summary_
        """
        self.inputs = []
        # * setup input ports
        self.inClk     = Signal(1, name_override='in_clk')
        logging.info('Created tcamMemTopWrapper input port: {:>s}'.format(self.inClk.name_override))
        self.inCsb     = Signal(1, name_override='in_csb')
        logging.info('Created tcamMemTopWrapper input port: {:>s}'.format(self.inCsb.name_override))
        self.inWeb     = Signal(1, name_override='in_web')
        logging.info('Created tcamMemTopWrapper input port: {:>s}'.format(self.inWeb.name_override))
        self.inWmask   = Signal(4, name_override='in_wmask')
        logging.info('Created tcamMemTopWrapper input port: {:>s}[{:d}:0]'.format(self.inWmask.name_override, 3))
        self.__inAddrWidth = self.memBlocks * 7
        self.inAddr    = Signal(self.__inAddrWidth, name_override='in_addr')
        logging.info('Created tcamMemTopWrapper input port: {:>s}[{:d}:0]'.format(self.inAddr.name_override, self.__inAddrWidth-1))
        self.inWdata   = Signal(32, name_override='in_wdata')
        logging.info('Created tcamMemTopWrapper input port: {:>s}[{:d}:0]'.format(self.inWdata.name_override, 31))
        # * add all input ports to an input list
        self.inputs = [self.inClk, self.inCsb, self.inWeb, self.inWmask, self.inAddr, self.inWdata]
        logging.info('Created list of all input ports')
        # * setup output ports
        self.outPma  = Signal(6, name_override='out_pma')
        logging.info('Created tcamMemTopWrapper output port: {:>s}[{:d}:0]'.format(self.outPma.name_override, 5))
        # * add all output ports to an output list
        self.outputs = self.outPma
        logging.info('Created list of all output ports')

    def logicBlock(self):
        # * ----- memory block selection for write logic
        # * setup wire
        blockSel = Signal(self.memBlocks, name_override='block_sel')
        # * calculate width for inAddr slice
        inAddrWidth = int(math.ceil(math.log2(self.memBlocks))) + 8
        # * combinational logic for block sel
        for i in range(self.memBlocks):
            self.comb += blockSel[i].eq(self.inAddr[8:inAddrWidth] == i)

        # * ----- generating logic for write mask
        wMaskList = []
        for i in range(self.memBlocks):
            # * setup wire
            tempWire = Signal(4, name_override='wmask{:d}'.format(i))
            wMaskList.append(tempWire)
            # * combinational logic for write mask
            self.comb += wMaskList[i].eq(Replicate(blockSel[i], 4) & self.inWmask)

        # * ----- generating logic for write addresses
        awAddrList = []
        for i in range(self.memBlocks):
            # * setup wire
            tempWire = Signal(8, name_override='aw_addr{:d}'.format(i))
            awAddrList.append(tempWire)
            # * combinational logic for write addresses
            self.comb += awAddrList[i].eq(Replicate(blockSel[i], 8) & self.inAddr[0:8])

        # * ----- generating address mux for all N blocks (selects between read or write addresses)
        vtbAddrList = []
        for i in range(self.memBlocks):
            # * setup wire
            tempWire = Signal(7, name_override='vtb_addr{:d}'.format(i))
            vtbAddrList.append(tempWire)
            # * combinational logic for address mux
            self.comb += If(self.inWeb,
                            vtbAddrList[i].eq(Cat(self.inAddr[i*7 : (i*7)+7], 0b0)),
                        ).Else(
                            vtbAddrList[i].eq(awAddrList[i])
                        )

        # * ----- adding TCAM memory block instances
        # * setup rdata output signals
        outRdataList = []
        for i in range(self.memBlocks):
            tempWire = Signal(64, name_override='out_rdata{:d}'.format(i))
            outRdataList.append(tempWire)

            # * tcam memory block 7x64 instantiations
            self.specials += Instance(
                of='tcamMemBlock7x64',
                name='tcam_mem_7x64_dut{:d}'.format(i),
                i_in_clk=self.inClk,
                i_in_csb=self.inCsb,
                i_in_web=self.inWeb,
                i_in_wmask=self.inWmask,
                i_in_addr=vtbAddrList[i],
                i_in_wdata=self.inWdata,
                o_out_rdata=outRdataList[i]
            )

        # * ------ AND gate instantiations
        outAndGateList = []
        for i in range(self.memBlocks-1):
            # * setup AND gate output signals
            tempWire = Signal(64, name_override='out_gate{:d}'.format(i))
            outAndGateList.append(tempWire)
            if i == 0:
                self.specials += Instance(
                    of='and_gate',
                    name='and_gate_dut{:d}'.format(i),
                    i_in_dataA=outRdataList[i],     # out_rdata0
                    i_in_dataB=outRdataList[i+1],   # out_rdata1
                    o_out_data=outAndGateList[i]    # out_gate0
                )
            else:
                self.specials += Instance(
                    of='and_gate',
                    name='and_gate_dut{:d}'.format(i),
                    i_in_dataA=outRdataList[i+1],   # out_rdata2
                    i_in_dataB=outAndGateList[i-1], # out_gate0
                    o_out_gate=outAndGateList[i]    # out_gate1
                )

        # * ------ Priority encoder instantiations
        self.specials += Instance(
            of='priority_encoder',
            name='priority_encoder_dut0',
            i_in_data=outAndGateList[-1],
            o_out_data=self.outputs
        )

# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================

def genVerilogTcamMemTopWrapper(memBlocks, filePath):
    """
    _summary_

    :param _type_ filePath: _description_
    :return _type_: _description_
    """
    # * instantiate the module
    tcamMemTop = tcamMemTopWrapper(memBlocks)

    # * generate the verilog code
    tcamMemTop.verilogCode = convert(tcamMemTop, name='tcamMemBlock7x64')
    logging.info('Generated TCAM Memory Top Wrapper verilog module RTL')

    # * write verilog code to a file
    with open(filePath, 'w', encoding='utf-8') as rtl:
        rtl.write(str(tcamMemTop.verilogCode))
    logging.info('Created rtl file {:s}'.format(filePath))

    return str(tcamMemTop.verilogCode)