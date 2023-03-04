"""
List of all pip packages imported
"""
from andGate import *
from priorityEncoder import *
from tcamMemBlock7x64 import *
from tcamMemTopWrapper import *
import os
import sys
import shutil
import logging
import argparse
# os.system('clear')


def main():
    """
    main func for implementing py class TcamMemTopWrapper
    """
    # * ----- variables
    pwd = os.getcwd()
    logsDirPath = ''
    tcamRtlDirPath = ''
    tcamRtlConfigDirPath = ''
    rtlFilePath = ''
    memLength = 0
    memWidth = 0
    pathSram1kb = 'compiler/lib/tcam_block_rtl/sky130_sram_1kbyte_1rw1r_32x256_8.sv'

    # create logs dir if it doesn't exist
    logsDirPath = os.path.join(pwd, 'logs')
    if os.path.exists(logsDirPath) is False:
        os.makedirs('logs')
    # create rtl dir if it doesn't exist
    tcamRtlDirPath = os.path.join(pwd, 'tcam_mem_rtl')
    if os.path.exists(tcamRtlDirPath) is False:
        os.makedirs('tcam_mem_rtl')
    # logging config
    logging.basicConfig(
        level=logging.DEBUG,
        filename='./logs/tcamMemoryWrapper.log',
        format="%(asctime)s | %(filename)s | %(funcName)s | %(levelname)s | %(lineno)d | %(message)s",
    )

    # set arguments for OpenTCAM RTL memory generator
    parser = argparse.ArgumentParser(
        prog='OpenTCAM',
        usage='%(prog)s [options] path',
        description='TCAM memory generator',
        epilog='Python framework for generating configurable SRAM based TCAM memories',
    )
    # list of all possible args for OpenTCAM
    parser.add_argument('-conf', '--tcamConfig',
                        type=str, default='tcam_64x28', metavar='', required=True, nargs='?', help='name of specific TCAM mem wrapper config')
    parser.add_argument('-d', '--debug',
                        type=int, default=0, metavar='', required=False, nargs='?', help='print debugging mode')
    parser.add_argument('-v','--verbose',
                        type=int, default=0, metavar='', required=False, nargs='?', help='print verbose mode')
    arg = parser.parse_args()

    # ====================================================== code main body

    # * calculate how many tcam block are required
    if arg.tcamConfig:
        memLength=int(arg.tcamConfig[5:7])
        memWidth=int(arg.tcamConfig[8:10])
        if (memLength == 64) and (memWidth%7 == 0):
            print('"VALID" TCAM memory wrapper config. tcam_[64]x[7*N] == %s\n', arg.tcamConfig)
            logging.info('"VALID" TCAM memory wrapper config. tcam_[64]x[7*N] == %s', arg.tcamConfig)
            logging.info('Total TCAM memory 64x7 blocks required: %d', int(memWidth/7))
            # * create rtl dir for specific tcam mem wrap config
            tcamRtlConfigDirPath = os.path.join(tcamRtlDirPath, arg.tcamConfig)
            if os.path.exists(tcamRtlConfigDirPath):
                shutil.rmtree(tcamRtlConfigDirPath)
            os.makedirs(tcamRtlConfigDirPath)
            logging.info('Created TCAM memory RTL dir: %s', tcamRtlConfigDirPath)
            # * copy sky130 block to required config dir
            shutil.copy(pathSram1kb, tcamRtlConfigDirPath)
            logging.info('Copied file "%s" to dir "%s"', pathSram1kb, tcamRtlConfigDirPath)
            print('Copied rtl file "%s" to dir "%s"', os.path.basename(pathSram1kb), tcamRtlConfigDirPath)
            # * generate verilog for TCAM memory MxN top wrapper
            fileName = 'top_tcam_mem_' + str(memLength) + 'x' + str(memWidth) + '.sv'
            rtlFilePath = os.path.join(tcamRtlConfigDirPath, fileName)
            codeTcamMemTopWrapper = genVerilogTcamMemTopWrapper(memBlocks=int(memWidth/7), filePath=rtlFilePath)
            print('Created rtl file: "%s"', rtlFilePath)
            if arg.debug:
                print(codeTcamMemTopWrapper)
            # * generate verilog for TCAM memory block 7x64
            rtlFilePath = os.path.join(tcamRtlConfigDirPath, 'tcam_mem_7x64.sv')
            codeTcamMemBlock7x64 = genVerilogTcamMemBlock7x64(filePath=rtlFilePath)
            print('Created rtl file: "%s"', rtlFilePath)
            if arg.debug:
                print(codeTcamMemBlock7x64)
            # * generate verilog for andgate
            rtlFilePath = os.path.join(tcamRtlConfigDirPath, 'and_gate.sv')
            codeAndGate = genVerilogAndGate(inputPorts=2, dataWidth=64, filePath=rtlFilePath)
            print('Created rtl file: "%s"', rtlFilePath)
            if arg.debug:
                print(codeAndGate)
            # * generate verilog for priority encoder
            rtlFilePath = os.path.join(tcamRtlConfigDirPath, 'priority_encoder_64x6.sv')
            codePriorityEncoder = genVerilogPriorityEncoder(inDataWidth=64, filePath=rtlFilePath)
            print('Created rtl file: "%s"', rtlFilePath)
            if arg.debug:
                print(codePriorityEncoder)
        else:
            logging.info('"INVALID" TCAM memory wrapper config. tcam_[64]x[7*N] != %s', arg.tcamConfig)
            sys.exit('"INVALID" TCAM memory wrapper config. tcam_[64]x[7*N] != %s', arg.tcamConfig)


if __name__ == '__main__':
    main()
