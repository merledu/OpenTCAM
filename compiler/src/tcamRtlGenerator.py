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
        # self.__inputWMask       = int()
        # self.__inputAddress     = int()
        # self.__outputReadData   = int()
        # self.__blockSelect      = int()
        
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
        # * insert comment in code
        tempLine = '{:<4s}// {:<s}'.format(' ', comment)
        self.__tcamRtlWrapLine.append(tempLine)
        logging.info('Added comment {:s} in: {:<s}'.format(comment, self._topWrapperFileName))
    
    
    def insertBlankLine(self, blankLines):
        for i in range(blankLines):
            tempLine = ''
            self.__tcamRtlWrapLine.append(tempLine)
        logging.info('Added {:d} line space definition in: {:<s}'.format(blankLines, self._topWrapperFileName))
    
    
    def printWrapper(self):
        with open(self.tcamMemWrapperRTLFilePath, 'w') as file1:
            for line in self.__tcamRtlWrapLine:
                file1.write(line + '\n')
        file1.close()
    
    
    def insertTimeScale(self, timeUnit, timePrecision):
        tempLine = '`timescale ' + str(timeUnit).replace(' ','') + '/' + str(timePrecision).replace(' ','')
        self.__tcamRtlWrapLine.append(tempLine)
        logging.info('Added timescale in: {:<s}'.format(self._topWrapperFileName))
    
    
    def insertModuleDefinition(self):
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
        vtbAddr = self._currConfig['wireVtbAddr']
        
        # * create wire/s for vtb_addr
        for i in range(self._currConfig['tcamBlocks']):
            tempLine = '{:4s}wire\t[{:^d}:0]\t{:s}{:d};'.format(' ', vtbAddr['width']-1, vtbAddr['name'], i)
            self.__tcamRtlWrapLine.append(tempLine)
        
        # assign vtb_addr1 = in_web ? {1'b0, in_addr[6:0]}   : aw_addr1;
        # * create assign statements
        for i in range(self._currConfig['tcamBlocks']):
            lsb = 7 * i
            msb = lsb + 6
            tempLine1 = '{:4s}assign {:<s}{:d} = '.format(' ', vtbAddr['name'], i)
            tempLine2 = "{:s} ? {:s} 1'b0, {:s}[{:>3d}:{:>3d}]{:s} : {:s}{:d};" \
            .format(self._currConfig['ports'][2]['name'], '{', self._currConfig['ports'][4]['name'], msb, lsb, ' }', self._currConfig['wireAwAddr']['name'], i)
            tempLine = tempLine1 + tempLine2
            self.__tcamRtlWrapLine.append(tempLine)







    def generateWrapper(self, timeUnit, timePrecision):
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

# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================

def printVerbose(verbose,msg):
    if verbose:
        print(str(msg))

def printDebug(debug,msg):
    if debug:
        print(str(msg))
