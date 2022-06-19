# from textwrap import indent
from tabulate import tabulate
import pandas as pd
import logging
import yaml
import json
import sys
import os

# ===========================================================================================
# ======================================= Begin Class =======================================
# ===========================================================================================

class tableMapping:
    # ----------------------------------------------------------------- Variables
    def __init__(self):
        # public vars
        self.prjWorkDir                 = str()
        self.tcamTableConfigsFilePath   = str()
        self.tcamTableXlsxFilePath      = str()
        # protected vars
        self._tcamTableConfigs  = dict()
        self._tcamTableMap      = pd.DataFrame
        # private vars
        self.__tcamQueryStrLen  = int()
        self.__tcamSubStrLen    = int()
        self.__tcamTotalSubStr  = int()
        self.__tcamPotMatchAddr = int()
        
        
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
        input args:
        return val:
        """
        # get tcamTables config file path
        tempPath = os.path.join(self.prjWorkDir,'compiler/configs/tcamTables.yaml')
        if os.path.isfile(tempPath) is True:
            self.tcamTableConfigsFilePath = tempPath
            logging.info('TCAM table config File FOUND: ' + self.tcamTableConfigsFilePath)
            return self.tcamTableConfigsFilePath
        else:
            logging.info('TCAM table config file NOT FOUND: ' + self.tcamTableConfigsFilePath)
            # return self.tcamTableConfigsFilePath
            sys.exit('TCAM table config file NOT FOUND')
    
    
    def readYAMLFile(self,filePath):
        """
        what does this func do ?
        input args:
        return val:
        """
        with open(filePath) as file:
            self._tcamTableConfigs=yaml.full_load(file)
        # print(json.dumps(self._tcamTableConfigs,indent=4))
        # print(yaml.dump(self._tcamTableConfigs,sort_keys=False,default_flow_style=False))
        return self._tcamTableConfigs
    
    
    def printYAMLFile(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        print(json.dumps(self._tcamTableConfigs,indent=4))
        # print(yaml.dump(self._tcamTableConfigs,sort_keys=False,default_flow_style=False))
        logging.info('Printed TCAM table configs')
    
    
    def getTCAMTable(self,tcamConfig):
        """
        what does this func do ?
        input args:
        return val:
        """
        # look for specific tcam config in compiler/configs/tcamTables.yaml
        if tcamConfig in self._tcamTableConfigs.keys():
            print(json.dumps(self._tcamTableConfigs[tcamConfig], indent=4))
            logging.info('Required TCAM Config [' + tcamConfig + '] FOUND')
            
            # find the specific tcam table map in compiler/lib/
            tempPath = os.path.join(self.prjWorkDir,'compiler/lib/'+tcamConfig+'.xlsx')
            if os.path.isfile(tempPath) is True:
                self.tcamTableXlsxFilePath = tempPath
                logging.info('TCAM table map XLSX file FOUND: ' + self.tcamTableXlsxFilePath)
                return self.tcamTableXlsxFilePath
            else:
                logging.info('TCAM table map XLSX file NOT FOUND: ' + self.tcamTableXlsxFilePath)
                sys.exit('TCAM table config file NOT FOUND')
        else:
            logging.info('TCAM Config [' + tcamConfig + '] NOT FOUND')
            sys.exit('Required TCAM table config ', tcamConfig,' NOT FOUND')
    
    
    # def readTCAMTable(self):
    #     """
    #     what does this func do ?
    #     input args:
    #     return val:
    #     """
    #     self._tcamTableMap = pd.read_excel(self.tcamTableXlsxFilePath, header=0 ,engine='openpyxl')
    #     # print(mytable)
    #     # print(type(mytable))
    
    
    
    
    # # print a table from excel or html file
    # def displayDF(self,dataFrame):
    #     """
    #     what does this func do ?
    #     input args:
    #     return val:
    #     """
    #     print(tabulate(dataFrame,headers='keys',tablefmt='github'))