"""
List of all pip packages imported
"""

import logging
import math
import os

from migen import *
from migen.fhdl.verilog import convert

# ===========================================================================================
# ======================================= Begin Class =======================================
# ===========================================================================================


class TcamMemTopWrapper(Module):
    """
    Generates the verilog code for a TCAM memory block N*64 Wrapper.
    """

    # * ----------------------------------------------------------------- Variables
    def __init__(self, memBlocks):
        """
        Constructor: call IO ports and logic here

        **Signals:**
        :param list inputs              list containing objects for all input ports.
        :param list outputs             list containing objects for all output ports.
        :param Signal __blockSel:       signals object for block_sel
        :param list __wMaskList:        list to store signal objects for wmaskN
        :param list __awAddrList:       list to store signal objects for aw_addrN
        :param list __vtbAddrList:      list to store signal objects for vtb_addrN
        :param list __outRdataList:     list to store signal objects for out_rdataN
        :param list __outAndGateList:   list to store signal objects for out_andgateN

        **Variables:**
        :param int memBlocks:       instantiate N instances of module tcamMemBlock7x64
        :param int __inAddrWidth:   store bit width of signal in_addr
        :return str verilogCode:    store RTL code of the encoder.
        """
        # * variables
        self.memBlocks = memBlocks  # 4
        self.__inAddrWidth = 0
        self.verilogCode = ""

        # * signals
        self.__blockSel = Signal()
        self.__wMaskList = []
        self.__awAddrList = []
        self.__vtbAddrList = []
        self.__outRdataList = []
        self.__outAndGateList = []
        self.inputs = []
        self.outputs = []

        # * setup IO ports
        self.ioPorts()
        # * generate block RTL
        self.logicBlock()

    def ioPorts(self):
        """
        Create Signal objects for all the input ports of various widths and output ports of various widths.
        """
        self.inputs = {}
        # * setup input ports
        self.inClk = Signal(1, name_override="in_clk")
        logging.info("Created TcamMemTopWrapper input port: %s", self.inClk.name_override)
        self.inCsb = Signal(1, name_override="in_csb")
        logging.info("Created TcamMemTopWrapper input port: %s", self.inCsb.name_override)
        self.inWeb = Signal(1, name_override="in_web")
        logging.info("Created TcamMemTopWrapper input port: %s", self.inWeb.name_override)
        self.inWmask = Signal(4, name_override="in_wmask")
        logging.info("Created TcamMemTopWrapper input port: %s[%d:0]", self.inWmask.name_override, 3)
        self.__inAddrWidth = self.memBlocks * 7
        self.inAddr = Signal(self.__inAddrWidth, name_override="in_addr")
        logging.info("Created TcamMemTopWrapper input port: %s[%d:0]", self.inAddr.name_override, self.__inAddrWidth - 1)
        self.inWdata = Signal(32, name_override="in_wdata")
        logging.info("Created TcamMemTopWrapper input port: %s[%d:0]", self.inWdata.name_override, 31)
        # * add all input ports to an input list
        self.inputs = [self.inClk, self.inCsb, self.inWeb, self.inWmask, self.inAddr, self.inWdata]
        logging.info("Created list of all input ports")
        # * setup output ports
        self.outPma = Signal(6, name_override="out_pma")
        logging.info("Created TcamMemTopWrapper output port: %s[%d:0]", self.outPma.name_override, 5)
        # * add all output ports to an output list
        self.outputs = [self.outPma]
        logging.info("Created list of all output ports")

    def logicBlock(self):
        """
        Setup the logic for creating a TCAM Mx64 wrapper consisting of M/7 TCAM 7x64 memory block using migen.
        """
        # * ----- memory block selection for write logic
        # * setup wire
        self.__blockSel = Signal(self.memBlocks, name_override="block_sel")
        logging.info("Created wire %s[%d:0]", self.__blockSel.name_override, self.__blockSel.nbits - 1)
        # * calculate width for inAddr slice
        inAddrWidth = int(math.ceil(math.log2(self.memBlocks))) + 8
        logging.info("Calculated bit slice for signal in_addr[%d:%d]", inAddrWidth, 8)
        # * combinational logic for block sel
        for i in range(self.memBlocks):
            self.comb += self.__blockSel[i].eq(self.inAddr[8:inAddrWidth] == i)
            logging.info("Created logic for signal %s[%d]", self.__blockSel.name_override, i)

        # * ----- generating logic for write mask
        for i in range(self.memBlocks):
            # * setup wire
            tempWmask = Signal(4, name_override=f"wmask{i}")
            self.__wMaskList.append(tempWmask)
            logging.info("Created wire %s[%d:0]", self.__wMaskList[i].name_override, self.__wMaskList[i].nbits - 1)
            # * combinational logic for write mask
            self.comb += self.__wMaskList[i].eq(Replicate(self.__blockSel[i], 4) & self.inWmask)
            logging.info("Created logic for signal %s", self.__wMaskList[i].name_override)

        # * ----- generating logic for write addresses
        for i in range(self.memBlocks):
            # * setup wire
            tempAwAddr = Signal(8, name_override=f"aw_addr{i}")
            self.__awAddrList.append(tempAwAddr)
            logging.info("Created wire %s[%d:0]", self.__awAddrList[i].name_override, self.__awAddrList[i].nbits - 1)
            # * combinational logic for write addresses
            self.comb += self.__awAddrList[i].eq(Replicate(self.__blockSel[i], 8) & self.inAddr[0:8])
            logging.info("Created logic for signal %s", self.__awAddrList[i].name_override)

        # * ----- generating address mux for all N blocks (selects between read or write addresses)
        for i in range(self.memBlocks):
            # * setup wire
            tempVtbAddr = Signal(8, name_override=f"vtb_addr{i}")
            self.__vtbAddrList.append(tempVtbAddr)
            logging.info("Created wire %s[%d:0]", self.__vtbAddrList[i].name_override, self.__vtbAddrList[i].nbits - 1)
            # * combinational logic for address mux
            self.comb += If(
                self.inWeb,
                self.__vtbAddrList[i].eq(Cat(self.inAddr[i * 7 : (i * 7) + 7], 0b0)),
            ).Else(self.__vtbAddrList[i].eq(self.__awAddrList[i]))
            logging.info("Created logic for signal %s", self.__vtbAddrList[i].name_override)

        # * ----- adding TCAM memory block instances
        # * setup rdata output signals
        for i in range(self.memBlocks):
            tempRdata = Signal(64, name_override=f"out_rdata{i}")
            self.__outRdataList.append(tempRdata)
            logging.info("Created wire %s[%d:0]", self.__outRdataList[i].name_override, self.__outRdataList[i].nbits - 1)

            # * tcam memory block 7x64 instantiations
            dutName = f"tcam_mem_7x64_dut{i}"
            self.specials += Instance(
                of="tcam_mem_7x64",
                name=dutName,
                i_in_clk=self.inClk,
                i_in_csb=self.inCsb,
                i_in_web=self.inWeb,
                i_in_wmask=self.inWmask,
                i_in_addr=self.__vtbAddrList[i],
                i_in_wdata=self.inWdata,
                o_out_rdata=self.__outRdataList[i],
            )
            logging.info('Created instance "%s" of module "tcamMemBlock7x64"', dutName)

        # * ------ AND gate instantiations
        for i in range(self.memBlocks - 1):
            # * setup AND gate output signals
            tempOutAndGate = Signal(64, name_override=f"out_andgate{i}")
            self.__outAndGateList.append(tempOutAndGate)
            logging.info("Created wire %s[%d:0]", self.__outAndGateList[i].name_override, self.__outAndGateList[i].nbits - 1)
            dutName = f"and_gate_dut{i}"
            if i == 0:
                self.specials += Instance(
                    of="and_gate",
                    name=dutName,
                    i_in_data0=self.__outRdataList[i],
                    i_in_data1=self.__outRdataList[i + 1],
                    o_out_data=self.__outAndGateList[i],
                )
            else:
                self.specials += Instance(
                    of="and_gate",
                    name=dutName,
                    i_in_data0=self.__outRdataList[i + 1],
                    i_in_data1=self.__outAndGateList[i - 1],
                    o_out_data=self.__outAndGateList[i],
                )
            logging.info('Created instance "%s" of module "tcamMemBlock7x64"', dutName)

        # * ------ Priority encoder instantiations
        self.specials += Instance(
            of="priority_encoder_64x6", name="priority_encoder_dut0", i_in_data=self.__outAndGateList[-1], o_out_data=self.outputs[0]
        )
        logging.info('Created instance "priority_encoder_dut0" of module "priority_encoder"')


# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================


def genVerilogTcamMemTopWrapper(memBlocks, filePath):
    """
    Main user function for class TcamMemTopWrapper.
    Creates the IO ports for the verilog RTL module definition.
    Generates the verilog code for a TCAM Mx64 memory block wrapper.

    :param int memBlocks:       instantiate N instances of module tcamMemBlock7x64
    :param str filePath:        absolute path for the verilog file.
    :return str:                RTL code of the TCAM 7x64 memory.
    """
    # * instantiate the module
    tcamMemTop = TcamMemTopWrapper(memBlocks)

    # * ----- setup the IO ports for the verilog module definition
    # * input port set
    inPortsSet = set(tcamMemTop.inputs)
    # * output port set
    outPortsSet = set(tcamMemTop.outputs)
    # * combine input and output sets
    moduleIOs = inPortsSet.union(outPortsSet)

    # * generate the verilog code
    moduleName = os.path.basename(filePath).replace(".sv", "")
    tcamMemTop.verilogCode = convert(tcamMemTop, name=moduleName, ios=moduleIOs)
    logging.info("Generated TCAM Memory Top Wrapper verilog module RTL")

    # * write verilog code to a file
    with open(filePath, "w", encoding="utf-8") as rtl:
        rtl.write(str(tcamMemTop.verilogCode))
    logging.info('Created rtl file "%s"', filePath)

    return str(tcamMemTop.verilogCode)
