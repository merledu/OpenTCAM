import shutil
import logging
import math
import yaml
import json
import sys
import os
import re

# ===========================================================================================
# ======================================= Begin Class =======================================
# ===========================================================================================

class TcamRtlWrapperGenerator:
    # * ----------------------------------------------------------------- Variables
    def __init__(self):
        # * ------------------- public vars
        self.prjWorkDir = str()
        self.tcamMemWrapperConfigsFilePath  = str()
        self.tcamMemWrapperConfigsFileName  = str()
        self.tcamMemWrapperRTLFolderPath    = str()
        self.tcamMemWrapperRTLFilePath      = str()

        # * ------------------- protected vars
        self._currConfig            = dict()
        self._tcamMemWrapperConfigs = dict()
        self._topWrapperFileName    = str()

        # * ------------------- private vars
        self.__tcamRtlWrapLine  = list()
        self.__rtlBlocks        = [ 'and_gate.sv', 'priority_encoder_64x6.sv', 
                                    'sky130_sram_1kbyte_1rw1r_32x256_8.sv', 'tcam_7x64.sv']
        
        # * logging config
        logging.basicConfig(level=logging.DEBUG, filename='./logs/TcamRtlWrapperGenerator.log',
                            format='%(asctime)s | %(filename)s | %(funcName)s | %(levelname)s | %(lineno)d | %(message)s')
    
    
    # * ----------------------------------------------------------------- Functions
    def getPrjDir(self,verbose):
        """
        what does this func do ?
        input args:
        return val:
        """
        self.prjWorkDir=os.getcwd()
        logging.info('Project working dir: {:<s}'.format(self.prjWorkDir))
        printVerbose(verbose,'Project working dir: {:<s}'.format(self.prjWorkDir))
        return self.prjWorkDir
    
    
    def getYAMLFilePath(self,verbose):
        """
        what does this func do ?
        input args:
        return val:
        """
        # * get tcamTables config file path
        tempPath = os.path.join(self.prjWorkDir,'compiler/configs/tcamMemWrapper.yaml')
        if os.path.isfile(tempPath) is True:
            self.tcamMemWrapperConfigsFilePath = tempPath
            self.tcamMemWrapperConfigsFileName = os.path.basename(tempPath)
            logging.info('"FOUND": TCAM memory wrapper config file path: {:<s}'.format(self.tcamMemWrapperConfigsFilePath))
            printVerbose(verbose,'"FOUND": TCAM memory wrapper config file path: {:<s}'.format(self.tcamMemWrapperConfigsFileName))
            return self.tcamMemWrapperConfigsFilePath
        else:
            logging.error('"NOT FOUND": TCAM memory wrapper config file path: {:<s}'.format(self.tcamMemWrapperConfigsFilePath))
            sys.exit('"NOT FOUND": TCAM memory wrapper config file path: {:<s}'.format(self.tcamMemWrapperConfigsFileName))
    
    
    def readYAML(self,filePath,verbose):
        """
        what does this func do ?
        input args:
        return val:
        """
        with open(filePath) as file:
            self._tcamMemWrapperConfigs=yaml.full_load(file)
        # print(json.dumps(self._tcamMemWrapperConfigs, indent=4))
        # print(yaml.dump(self._tcamMemWrapperConfigs, sort_keys=False, default_flow_style=False))
        logging.info('Read TCAM memory wrapper config file: {:<s}'.format(self.tcamMemWrapperConfigsFilePath))
        printVerbose(verbose,'Read TCAM memory wrapper config file: {:<s}'.format(self.tcamMemWrapperConfigsFileName))
        return self._tcamMemWrapperConfigs
    
    
    def printYAML(self,debug):
        """
        what does this func do ?
        input args:
        return val:
        """
        printDebug(debug, 'Printing TCAM memory wrapper configs')
        print(json.dumps(self._tcamMemWrapperConfigs, indent=4))
        # print(yaml.dump(self._tcamMemWrapperConfigs, sort_keys=False, default_flow_style=False))
        logging.info('Printed TCAM memory wrapper configs')
    
    
    def getTCAMWrapperConfig(self, tcamWrapConfig):
        """
        what does this func do ?
        input args:
        return val:
        """
        # * look for specific tcam config in compiler/configs/tcamTables.yaml
        if tcamWrapConfig in self._tcamMemWrapperConfigs.keys():
            self._currConfig = self._tcamMemWrapperConfigs[tcamWrapConfig]
            # * save tcam config vars
            # self.__inputWMask       = self._currConfig['inputWMask']
            # self.__inputAddress     = self._currConfig['inputAddress']
            # self.__outputReadData   = self._currConfig['outputReadData']
            # self.__blockSelect      = self._currConfig['blockSelect']
            # * print specific tcam config
            # print(self._currConfig)
            logging.info('"FOUND" Required TCAM Memory Wrapper Config [{:<s}]'.format(tcamWrapConfig))
            print('\n"FOUND" Required TCAM Memory Wrapper Config [{:<s}]'.format(tcamWrapConfig))
            logging.info('TCAM Memory Wrapper Config Data [{:<s}] = {}'.format(tcamWrapConfig, self._currConfig))
            return self._currConfig
        else:
            logging.error('"NOT FOUND": TCAM Memory Wrapper Config [{:<s}]'.format(tcamWrapConfig))
            sys.exit('"NOT FOUND": Required TCAM Memory Wrapper Config [{:<s}]'.format(tcamWrapConfig))
    
    
    def createWrapConfigDir(self, tcamWrapConfig, verbose):
        """
        what does this func do ?
        input args:
        return val:
        """
        self.tcamMemWrapperRTLFolderPath = os.path.join(self.prjWorkDir, 'tcam_mem_rtl', tcamWrapConfig)
        if os.path.exists(self.tcamMemWrapperRTLFolderPath) is False:
            os.makedirs(self.tcamMemWrapperRTLFolderPath)
            logging.info('Created TCAM memory "{:<s}" RTL folder: {:<s}'.format(tcamWrapConfig, self.tcamMemWrapperRTLFolderPath))
            printVerbose(verbose, 'Created TCAM memory "{:<s}" RTL folder: {:<s}'.format(tcamWrapConfig, self.tcamMemWrapperRTLFolderPath))
    
    
    def createWrapConfigFile(self, tcamWrapConfig):
        """
        what does this func do ?
        input args:
        return val:
        """
        self._topWrapperFileName = 'top_' + str(tcamWrapConfig).replace('MemWrapper_','_mem_') + '.sv'
        self.tcamMemWrapperRTLFilePath = os.path.join(self.tcamMemWrapperRTLFolderPath, self._topWrapperFileName)
        logging.info('Created TCAM memory "{:<s}" wrapper: {:<s}'.format(tcamWrapConfig, self.tcamMemWrapperRTLFilePath))
    
    
    def insertComment(self, comment):
        """
        what does this func do ?
        input args:
        return val:
        """
        # * insert comment in code
        tempLine = '{:<4s}// {:<s}'.format(' ', comment)
        self.__tcamRtlWrapLine.append(tempLine)
        logging.info('Added comment {:s} in: {:<s}'.format(comment, self._topWrapperFileName))
    
    
    def insertBlankLine(self, blankLines):
        """
        what does this func do ?
        input args:
        return val:
        """
        for i in range(blankLines):
            tempLine = ''
            self.__tcamRtlWrapLine.append(tempLine)
        logging.info('Added {:d} line space definition in: {:<s}'.format(blankLines, self._topWrapperFileName))
    
    
    def printWrapper(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        with open(self.tcamMemWrapperRTLFilePath, 'w') as file1:
            for line in self.__tcamRtlWrapLine:
                file1.write(line + '\n')
        file1.close()
    
    
    def insertTimeScale(self, timeUnit, timePrecision):
        """
        what does this func do ?
        input args:
        return val:
        """
        # Force timescale to 1ns/1ps as requested
        tempLine = '`timescale 1ns/1ps'
        self.__tcamRtlWrapLine.append(tempLine)
        logging.info('Added timescale in: {:<s}'.format(self._topWrapperFileName))
    
    
    def insertModuleDefinition(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        # * write module definition
        tempLine = 'module ' +  self._currConfig['moduleName'] + ' ('
        self.__tcamRtlWrapLine.append(tempLine)
        logging.info('Added module definition in: {:<s}'.format(self._topWrapperFileName))
        
        # * write IO ports
        for i in range(len(self._currConfig['ports'])):
            port = self._currConfig['ports'][i]
            if port['width'] == 0:
                tempLine = '{:4s}{:s}\t{:s}\t{:s}'.format(' ', port['direction'], 'logic', port['name'])
            else:
                tempLine = '{:4s}{:s}\t{:s}\t[{:^d}:0]\t{:s}'.format(' ', port['direction'], 'logic', port['width']-1, port['name'])
            # * add a , for N-1 ports in definition
            if i != len(self._currConfig['ports']) - 1:
                tempLine += ','            
            self.__tcamRtlWrapLine.append(tempLine)
        logging.info('Added IO ports in module definition in: {:<s}'.format(self._topWrapperFileName))
        
        # * write closing bracket
        tempLine = ');'
        self.__tcamRtlWrapLine.append(tempLine)
    
    
    def insertBlockSelect(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        blockSel = self._currConfig['wireBlockSel']
        
        # * create wire/s for block_sel
        tempLine = '{:4s}wire\t[{:^d}:0]\t{:s};'.format(' ', blockSel['width']-1, blockSel['name'])
        self.__tcamRtlWrapLine.append(tempLine)
        
        # * create assign statements
        for index in range(blockSel['width']):
            tempLine = "{:4s}assign {:<s}[{:^d}] = (in_addr[{:^d}:{:^d}] == {:^d}'d{:d});" \
            .format(' ', blockSel['name'], index, blockSel['inputAddr'][0], blockSel['inputAddr'][1], int(math.log2(blockSel['width'])), index)  
            self.__tcamRtlWrapLine.append(tempLine)
    
    
    def insertWriteMask(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        writeMask = self._currConfig['wireWriteMask']
        
        # * create wire/s for wmask
        for i in range(self._currConfig['tcamBlocks']):
            tempLine = '{:4s}wire\t[{:^d}:0]\t{:s}{:d};'.format(' ', writeMask['width']-1, writeMask['name'], i)
            self.__tcamRtlWrapLine.append(tempLine)
        
        # * create assign statements
        for i in range(self._currConfig['tcamBlocks']):
            tempLine1 = '{:4s}assign {:<s}{:d} = '.format(' ', writeMask['name'], i)
            tempLine2 = '{:s}{:^d}{:s}{:<s}[{:d}]{:s} & {:<s};' \
            .format('{ ', writeMask['width'], '{', self._currConfig['wireBlockSel']['name'], i, '} }', self._currConfig['ports'][3]['name'])
            tempLine = tempLine1 + tempLine2
            self.__tcamRtlWrapLine.append(tempLine)
    
    
    def insertAwAddr(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        awAddr = self._currConfig['wireAwAddr']
        
        # * create wire/s for awaddr
        for i in range(self._currConfig['tcamBlocks']):
            tempLine = '{:4s}wire\t[{:^d}:0]\t{:s}{:d};'.format(' ', awAddr['width']-1, awAddr['name'], i)
            self.__tcamRtlWrapLine.append(tempLine)
        
        # * create assign statements
        for i in range(self._currConfig['tcamBlocks']):
            tempLine1 = '{:4s}assign {:<s}{:d} = '.format(' ', awAddr['name'], i)
            tempLine2 = '{:s}{:^d}{:s}{:<s}[{:d}]{:s} & {:<s}[{:d}:0];' \
            .format('{ ', awAddr['width'], '{', self._currConfig['wireBlockSel']['name'], i, '} }', self._currConfig['ports'][4]['name'], awAddr['width']-1)
            tempLine = tempLine1 + tempLine2
            self.__tcamRtlWrapLine.append(tempLine)
    
    
    def insertVtbAddr(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        vtbAddr = self._currConfig['wireVtbAddr']
        
        # * create wire/s for vtb_addr
        for i in range(self._currConfig['tcamBlocks']):
            tempLine = '{:4s}wire\t[{:^d}:0]\t{:s}{:d};'.format(' ', vtbAddr['width'], vtbAddr['name'], i)
            self.__tcamRtlWrapLine.append(tempLine)
        
        # * create assign statements
        for i in range(self._currConfig['tcamBlocks']):
            lsb = 7 * i
            msb = lsb + 6
            tempLine1 = '{:4s}assign {:<s}{:d} = '.format(' ', vtbAddr['name'], i)
            tempLine2 = "{:s} ? {:s} 1'b0, {:s}[{:>3d}:{:>3d}]{:s} : {:s}{:d};" \
            .format(self._currConfig['ports'][2]['name'], '{', self._currConfig['ports'][4]['name'], msb, lsb, ' }', self._currConfig['wireAwAddr']['name'], i)
            tempLine = tempLine1 + tempLine2
            self.__tcamRtlWrapLine.append(tempLine)
    
    
    def insertTcamInstances(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        outRData = self._currConfig['wireOutRData']
        ports = self._currConfig['ports']
        
        # * create wire/s for out_rdata
        for i in range(self._currConfig['tcamBlocks']):
            tempLine = '{:4s}wire\t[{:^d}:0]\t{:s}{:d};'.format(' ', outRData['width']-1, outRData['name'], i)
            self.__tcamRtlWrapLine.append(tempLine)
        
        self.insertBlankLine(1)
        # * create instances
        for i in range(self._currConfig['tcamBlocks']):
            # * dut definition instantiation
            tempLine = '{:4s}{:s} {:s}_dut{:d} ('.format(' ', self._currConfig['instanceName'], self._currConfig['instanceName'], i)
            self.__tcamRtlWrapLine.append(tempLine)
            # * port instantiations
            for j in range(len(ports)):
                # * append N for signal vtb_addr1
                if ports[j]['name'] == 'in_addr':
                    tempLine = '{:8s}.{:<12s}({:>12s})'.format(' ', ports[j]['name'], 'vtb_addr'+str(i))
                elif ports[j]['name'] == 'out_pma':
                    tempLine = '{:8s}.{:<12s}({:>12s}{:d})'.format(' ', 'out_rdata', 'out_rdata',i)
                else:
                    tempLine = '{:8s}.{:<12s}({:>12s})'.format(' ', ports[j]['name'], ports[j]['name'])
                # * add a , for N-1 ports in definition
                if j != len(ports) - 1:
                    tempLine += ','            
                self.__tcamRtlWrapLine.append(tempLine)
            tempLine = '{:4s}{:s}'.format(' ', ');')
            self.__tcamRtlWrapLine.append(tempLine)
    
    
    def insertAndGates(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        outRData = self._currConfig['wireOutRData']['name']
        
        # * create wire/s for intermediate AND gate outputs
        for i in range(self._currConfig['tcamBlocks']-1):
            tempLine = '{:4s}wire\t[{:^d}:0]\t{:s}{:d};'.format(' ', self._currConfig['wireOutRData']['width']-1, 'out_andgate', i)
            self.__tcamRtlWrapLine.append(tempLine)
        
        # * create final AND gate output wire
        tempLine = '{:4s}wire\t[{:^d}:0]\t{:s};'.format(' ', self._currConfig['wireOutRData']['width']-1, 'out_andgate')
        self.__tcamRtlWrapLine.append(tempLine)
        
        # * create and gate instances with proper cascading
        for i in range(self._currConfig['tcamBlocks']-1):
            if i == 0:
                # First AND gate: out_rdata0 & out_rdata1 -> out_andgate0
                tempLine = '{:4s}and_gate andgate_dut{:d} (.out_data(out_andgate{:d}), .in_dataA({:>s}{:d}), .in_dataB({:>s}{:d}));' \
                .format(' ', i, i, outRData, i, outRData, i+1)
            elif i == self._currConfig['tcamBlocks'] - 2:
                # Last AND gate: out_andgate1 & out_rdata3 -> out_andgate (final)
                tempLine = '{:4s}and_gate andgate_dut{:d} (.out_data(out_andgate), .in_dataA(out_andgate{:d}), .in_dataB({:>s}{:d}));' \
                .format(' ', i, i-1, outRData, i+1)
            else:
                # Middle AND gates: out_andgate{i-1} & out_rdata{i+1} -> out_andgate{i}
                tempLine = '{:4s}and_gate andgate_dut{:d} (.out_data(out_andgate{:d}), .in_dataA(out_andgate{:d}), .in_dataB({:>s}{:d}));' \
                .format(' ', i, i, i-1, outRData, i+1)
            self.__tcamRtlWrapLine.append(tempLine)
    
    
    def insertPriorityEncoder(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        module = [
            '{:4s}priority_encoder_64x6 priority_encoder_dut0('.format(' '),
            '{:8s}.in_data  (out_andgate  ),'.format(' '),
            '{:8s}.out_data (out_pma      )'.format(' '),
            '{:4s});'.format(' ')
        ]
        for line in module:
            self.__tcamRtlWrapLine.append(line)
        
        # Add debug code to monitor address mapping
        self.insertBlankLine(1)
        debug_code = [
            '{:4s}// Debug code to monitor address mapping'.format(' '),
            '{:4s}always @(posedge in_clk) begin'.format(' '),
            '{:8s}if (!in_csb) begin  // Only print when chip is selected'.format(' '),
            '{:12s}$display("=== TCAM Address Debug ===");'.format(' '),
            '{:12s}$display("Input address: %h", in_addr);'.format(' '),
            '{:12s}$display("in_web: %b", in_web);'.format(' '),
            '{:12s}$display("Block 0 search addr = %b (%h)", in_addr[6:0], in_addr[6:0]);'.format(' '),
            '{:12s}$display("Block 1 search addr = %b (%h)", in_addr[13:7], in_addr[13:7]);'.format(' '),
            '{:12s}$display("Block 2 search addr = %b (%h)", in_addr[20:14], in_addr[20:14]);'.format(' '),
            '{:12s}$display("Block 3 search addr = %b (%h)", in_addr[27:21], in_addr[27:21]);'.format(' '),
            '{:12s}$display("vtb_addr0 = %h", vtb_addr0);'.format(' '),
            '{:12s}$display("vtb_addr1 = %h", vtb_addr1);'.format(' '),
            '{:12s}$display("vtb_addr2 = %h", vtb_addr2);'.format(' '),
            '{:12s}$display("vtb_addr3 = %h", vtb_addr3);'.format(' '),
            '{:12s}$display("out_pma = %h", out_pma);'.format(' '),            
            '{:12s}$display("=========================");'.format(' '),
            '{:8s}end'.format(' '),
            '{:4s}end'.format(' '),
            '{:4s}'.format(' ')
        ]
        for line in debug_code:
            self.__tcamRtlWrapLine.append(line)
        
        self.insertBlankLine(1)
        tempLine = 'endmodule'
        self.__tcamRtlWrapLine.append(tempLine)
    
    
    def generateWrapper(self, timeUnit, timePrecision):
        """
        what does this func do ?
        input args:
        return val:
        """
        self.insertTimeScale(timeUnit, timePrecision)
        self.insertBlankLine(1)
        
        self.insertModuleDefinition()
        self.insertBlankLine(1)
        
        self.insertComment('memory block selection for write logic')
        self.insertBlockSelect()
        self.insertBlankLine(1)
        
        self.insertComment('logic for write mask')
        self.insertWriteMask()
        self.insertBlankLine(1)
        
        self.insertComment('logic for write addresses')
        self.insertAwAddr()
        self.insertBlankLine(1)
        
        self.insertComment('address mux for all N blocks (selects between read or write addresses)')
        self.insertVtbAddr()
        self.insertBlankLine(1)
        
        self.insertComment('TCAM memory block instances')
        self.insertTcamInstances()
        self.insertBlankLine(1)
        
        self.insertComment('AND gate instantiations')
        self.insertAndGates()
        self.insertBlankLine(1)
        
        self.insertComment('Priority Encoder instantiations')
        self.insertPriorityEncoder()
        self.insertBlankLine(1)
    
    
    def copyRtlBlocks(self):
        for file in self.__rtlBlocks:
            srcPath = os.path.join(self.prjWorkDir, 'compiler/lib/tcam_block_rtl', file)
            dstPath = os.path.join(self.prjWorkDir, self.tcamMemWrapperRTLFolderPath, file)
            shutil.copy(srcPath, dstPath)



# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================

def printVerbose(verbose,msg):
    if verbose:
        print(str(msg))

def printDebug(debug,msg):
    if debug:
        print(str(msg))
