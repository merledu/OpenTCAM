import logging
import yaml
import json
import sys
import os
import re

# ===========================================================================================
# ======================================= Begin Class =======================================
# ===========================================================================================

class TcamRtlGenerator:
    # * ----------------------------------------------------------------- Variables
    def __init__(self):
        # * ------------------- public vars
        self.prjWorkDir = str()
        self.tcamTableConfigsFilePath = str()
        self.tcamTableConfigsFileName = str()

        # * ------------------- protected vars
        self._tcamTableConfigs  = dict()

        # * ------------------- private vars
        self.__tcamQueryStrLen  = int()
        
        # * logging config
        logging.basicConfig(level=logging.DEBUG, filename='./logs/tcamRtlGenerator.log',
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
        tempPath = os.path.join(self.prjWorkDir,'compiler/configs/tcamTables.yaml')
        if os.path.isfile(tempPath) is True:
            self.tcamTableConfigsFilePath = tempPath
            self.tcamTableConfigsFileName = os.path.basename(tempPath)
            logging.info('"FOUND": TCAM table config file path: {:<s}'.format(self.tcamTableConfigsFilePath))
            printVerbose(verbose,'"FOUND": TCAM table config file path: {:<s}'.format(self.tcamTableConfigsFilePath))
            return self.tcamTableConfigsFilePath
        else:
            logging.error('"NOT FOUND": TCAM table config file path: {:<s}'.format(self.tcamTableConfigsFilePath))
            sys.exit('"NOT FOUND": TCAM table config file path: {:<s}'.format(self.tcamTableConfigsFilePath))
    
    
    def readYAML(self,filePath,verbose):
        """
        what does this func do ?
        input args:
        return val:
        """
        with open(filePath) as file:
            self._tcamTableConfigs=yaml.full_load(file)
        # print(json.dumps(self._tcamTableConfigs,indent=4))
        # print(yaml.dump(self._tcamTableConfigs,sort_keys=False,default_flow_style=False))
        logging.info('Read TCAM table config file: {:<s}'.format(self.tcamTableConfigsFilePath))
        printVerbose(verbose,'Read TCAM table config file: {:<s}'.format(self.tcamTableConfigsFilePath))
        return self._tcamTableConfigs









# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================

def printVerbose(verbose,msg):
    if verbose:
        print(str(msg))

def printDebug(debug,msg):
    if debug:
        print(str(msg))
