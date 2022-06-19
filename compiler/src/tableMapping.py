import logging
import yaml
import json
import sys
import os

class tableMapping:
    # ----------------------------------------------------------------- Variables
    def __init__(self):
        # public vars
        self.prjWorkDir = str()
        self.tcamTableFilePath = str()
        # protected vars
        self._tcamTableConfigs = dict()
        # private vars
        
        # logging config
        logging.basicConfig(level=logging.DEBUG, filename='./logs/tableMapping.log',
                            format='%(asctime)s | %(filename)s | %(funcName)s | %(levelname)s | %(lineno)d | %(message)s')
    
    # ----------------------------------------------------------------- Functions
    def getPrjDir(self):
        """
        what does this func do ?
        """
        self.prjWorkDir=os.getcwd()
        logging.info('Project working dir: ' + self.prjWorkDir)
        return self.prjWorkDir
    
    
    def getYAMLFile(self):
        """
        what does this func do ?
        """
        # get tcamTables config file path
        tempPath = os.path.join(self.prjWorkDir,'compiler/configs/tcamTables.yaml')
        if os.path.isfile(tempPath) is True:
            self.tcamTableFilePath = tempPath
            logging.info('Config File FOUND: ' + self.tcamTableFilePath)
            return self.tcamTableFilePath
        else:
            logging.info('Config File NOT FOUND: ' + self.tcamTableFilePath)
            # return self.tcamTableFilePath
            sys.exit('TCAM table config File NOT FOUND')
    
    
    def readYAMLFile(self,filePath):
        """
        what does this func do ?
        """
        with open(filePath) as file:
            self._tcamTableConfigs=yaml.full_load(file)
        # print(json.dumps(self._tcamTableConfigs,indent=4))
        # print(yaml.dump(self._tcamTableConfigs,sort_keys=False,default_flow_style=False))
        return self._tcamTableConfigs
    
    
    def printYAMLFile(self):
        """
        what does this func do ?
        """
        print(json.dumps(self._tcamTableConfigs,indent=4))
        # print(yaml.dump(self._tcamTableConfigs,sort_keys=False,default_flow_style=False))
        logging.info('Printed TCAM table configs')
