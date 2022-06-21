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
        self._tcamTableConfigs          = dict()
        self._tempTcamTableConfig       = dict()
        self._tcamTableMap              = pd.DataFrame
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
    
    
    def getYAMLFilePath(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        # get tcamTables config file path
        tempPath = os.path.join(self.prjWorkDir,'compiler/configs/tcamTables.yaml')
        if os.path.isfile(tempPath) is True:
            self.tcamTableConfigsFilePath = tempPath
            logging.info('"FOUND": TCAM table config file path: ' + self.tcamTableConfigsFilePath)
            return self.tcamTableConfigsFilePath
        else:
            logging.info('"NOT FOUND": TCAM table config file path: ' + self.tcamTableConfigsFilePath)
            sys.exit('"NOT FOUND": TCAM table config file')
    
    
    def readYAML(self,filePath):
        """
        what does this func do ?
        input args:
        return val:
        """
        with open(filePath) as file:
            self._tcamTableConfigs=yaml.full_load(file)
        # print(json.dumps(self._tcamTableConfigs,indent=4))
        # print(yaml.dump(self._tcamTableConfigs,sort_keys=False,default_flow_style=False))
        logging.info('Read TCAM table config file: ' + self.tcamTableConfigsFilePath)
        return self._tcamTableConfigs
    
    
    def printYAML(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        print(json.dumps(self._tcamTableConfigs,indent=4))
        # print(yaml.dump(self._tcamTableConfigs,sort_keys=False,default_flow_style=False))
        logging.info('Printed TCAM table configs')
    
    
    def getTCAMTableFilePath(self,tcamConfig):
        """
        what does this func do ?
        input args:
        return val:
        """
        # look for specific tcam config in compiler/configs/tcamTables.yaml
        if tcamConfig in self._tcamTableConfigs.keys():
            self._tempTcamTableConfig = self._tcamTableConfigs[tcamConfig]
            print(json.dumps(self._tempTcamTableConfig, indent=4))
            logging.info('"FOUND" Required TCAM Config [' + tcamConfig + ']')
            # find the specific tcam table map in compiler/lib/
            tempPath = os.path.join(self.prjWorkDir,'compiler/lib/'+tcamConfig+'.xlsx')
            if os.path.isfile(tempPath) is True:
                self.tcamTableXlsxFilePath = tempPath
                logging.info('"FOUND" TCAM table map XLSX file path: ' + self.tcamTableXlsxFilePath)
                return self.tcamTableXlsxFilePath
            else:
                logging.info('"NOT FOUND": TCAM table map XLSX file path: ' + self.tcamTableXlsxFilePath)
                sys.exit('"NOT FOUND": TCAM table config file')
        else:
            logging.info('"NOT FOUND": TCAM Config [' + tcamConfig + ']')
            sys.exit('"NOT FOUND": Required TCAM table config ', tcamConfig)
    
    
    def printDF(self,dataFrame):
        """
        what does this func do ?
        input args:
        return val:
        """
        print('\n')
        print(tabulate(dataFrame,headers='keys', showindex=False, disable_numparse=True, tablefmt='github'),'\n')
        logging.info('Printed dataframe')
    
    
    def readTCAMTable(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        # store tcam table in dataframe
        self._tcamTableMap = pd.read_excel(self.tcamTableXlsxFilePath, skiprows=2, index_col=None, engine='openpyxl')
        # get num of rows and col from tcam table
        tcamTableRows = self._tcamTableMap.shape[0]
        tcamTableCols = self._tcamTableMap.shape[1]
        # compare row/col of tcam table with respective yaml config
        if (tcamTableRows == self._tempTcamTableConfig['potMatchAddr'] and 
            tcamTableCols - 1 == self._tempTcamTableConfig['queryStrLen']):
            logging.info('"MATCH FOUND": TCAM table map rows == TCAM table YAML config potMatchAddr')
            logging.info('"MATCH FOUND": TCAM table map cols == TCAM table YAML config queryStrLen')
            return [tcamTableRows, tcamTableCols]
        else:
            logging.info('"MATCH NOT FOUND": TCAM table map rows != TCAM table YAML config potMatchAddr')
            logging.info('"MATCH NOT FOUND": TCAM table map cols != TCAM table YAML config queryStrLen')
            sys.exit('"MATCH NOT FOUND": MISMATCH in TCAM table map and YAML config rows/cols')
    
    
    # parseTCAMTable
    # createSRAMTable
    # genSRAMTable
    # printTableExcel
    # printTableCsv
    
    

