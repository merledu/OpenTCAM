from compiler.src.tableMapping import *
from unittest import TestCase
import pandas as pd
import numpy as np
import pytest
# import logging
import yaml
import glob
import os

# ===========================================================================================
# ======================================= Begin Class =======================================
# ===========================================================================================

class TestTableMapping(TestCase):
    
    def setUp(self):
        self.tm = TableMapping()
    
    
    def testGetPrjDir(self):
        # * ----- actual output
        actualVal = self.tm.getPrjDir()
        # * ----- expected output
        expectedVal = os.getcwd()
        # * ----- assertion
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in prj dir path')
    
    
    def testGetYAMLFilePath(self):
        # * ----- actual output
        self.tm.getPrjDir()
        actualVal = self.tm.getYAMLFilePath()
        # * ----- expected output
        expectedVal = os.path.join(self.tm.prjWorkDir,'compiler/configs/tcamTables.yaml')
        # * ----- assertion
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in TCAM table YAML file path')
    
    
    def testReadYAML(self):
        # * ----- actual output
        self.tm.getPrjDir()
        self.tm.getYAMLFilePath()
        actualVal = self.tm.readYAML(self.tm.tcamTableConfigsFilePath)
        # * ----- expected output
        with open('compiler/configs/tcamTables.yaml','r') as file:
            expectedVal = yaml.full_load(file)
        # * ----- assertion
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in reading TCAM table YAML config file')
    
    
    def testGetTCAMConfig(self):
        # * ----- actual output
        self.tm.getPrjDir()
        self.tm.getYAMLFilePath()
        self.tm.readYAML(self.tm.tcamTableConfigsFilePath)
        actualVal = list(self.tm._tcamTableConfigs.keys())
        # * ----- expected output
        with open('compiler/configs/tcamTables.yaml','r') as file:
            fileData = yaml.full_load(file)
            expectedVal = list(fileData.keys())
        # * ----- assertion
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in total number of TCAM table YAML configs')
    
    
    def testGetTCAMTableFilePath(self):
        actualVal = list()
        expectedVal = list()
        # * ----- actual output
        self.tm.getPrjDir()
        self.tm.getYAMLFilePath()
        self.tm.readYAML(self.tm.tcamTableConfigsFilePath)
        actualTcamConfName = list(self.tm._tcamTableConfigs.keys())
        for conf in actualTcamConfName:
            actualVal.append(self.tm.getTCAMTableFilePath(conf))
        # * ----- expected output
        for expectRelXlsxPath in glob.iglob('compiler/lib/*.xlsx',recursive=True):
            expectAbsXlsxPath = os.path.join(self.tm.prjWorkDir,expectRelXlsxPath)
            expectedVal.append(expectAbsXlsxPath)
        # * ----- assertion
        actualVal.sort()
        expectedVal.sort()
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in total number of Xlsx TCAM table maps')
    
    
    def testReadTCAMTable(self):
        actualTcamTableShape = list()
        expectTcamTableShape = list()
        # * ----- actual output
        self.tm.getPrjDir()
        self.tm.getYAMLFilePath()
        self.tm.readYAML(self.tm.tcamTableConfigsFilePath)
        for conf in self.tm._tcamTableConfigs:
            self.tm.getTCAMConfig(conf)
            self.tm.getTCAMTableFilePath(conf)
            [rows, cols] = self.tm.readTCAMTable()
            tempDict = {'config': conf,'rows': rows,'cols': cols}
            actualTcamTableShape.append(tempDict)
        actualVal = sorted(actualTcamTableShape, key=lambda x: x['config'])
        # print(actualVal)
        # * ----- expected output
        for expectRelXlsxPath in glob.iglob('compiler/lib/*.xlsx',recursive=True):
            expectAbsXlsxPath = os.path.join(self.tm.prjWorkDir,expectRelXlsxPath)
            expectAbsTcamConfig = os.path.basename(expectAbsXlsxPath).replace('.xlsx','')
            expectTcamTable = pd.read_excel(expectAbsXlsxPath, skiprows=2, index_col=None, engine='openpyxl')
            tempDict = {'config': expectAbsTcamConfig,'rows': expectTcamTable.shape[0],'cols': expectTcamTable.shape[1]}
            expectTcamTableShape.append(tempDict)
        expectedVal = sorted(expectTcamTableShape, key=lambda x: x['config'])
        # print(expectedVal)
        # * ----- assertion
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in TCAM table map rows and columns')
    
    
    def testGetSRAMTableDim(self):
        actualSramTableShape = list()
        expectSramTableShape = list()
        # * ----- actual output
        self.tm.getPrjDir()
        self.tm.getYAMLFilePath()
        self.tm.readYAML(self.tm.tcamTableConfigsFilePath)
        for conf in self.tm._tcamTableConfigs:
            self.tm.getTCAMConfig(conf)
            self.tm.getTCAMTableFilePath(conf)
            self.tm.readTCAMTable()
            [sramRows, sramCols] = self.tm.getSRAMTableDim()
            conf = conf.replace('tcam','sram')
            tempSramDict = {'config': conf,'rows': sramRows,'cols': sramCols}
            actualSramTableShape.append(tempSramDict)
        actualVal = sorted(actualSramTableShape, key=lambda x: x['config'])
        # print(actualVal)
        # * ----- expected output
        with open('compiler/configs/tcamTables.yaml','r') as file:
            fileData = yaml.full_load(file)
        for key in fileData:
            sramRows = fileData[key]['totalSubStr'] * pow(2,fileData[key]['subStrLen'])
            sramCols = fileData[key]['potMatchAddr']
            conf = key.replace('tcam','sram')
            tempSramDict = {'config': conf,'rows': sramRows,'cols': sramCols}
            expectSramTableShape.append(tempSramDict)
        expectedVal = sorted(expectSramTableShape, key=lambda x: x['config'])
        # print(expectedVal)
        # * ----- assertion
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in SRAM table map rows and columns')
    
    
    def tesGenSRAMTable(self):
        pass
    
    
    def testCreateSRAMTableDir(self):
        # * ----- actual output
        self.tm.getPrjDir()
        actualVal = os.path.join(self.tm.prjWorkDir,'sramTables')
        # * ----- expected output
        expectedVal = os.path.join(os.getcwd(),'sramTables')
        # * ----- assertion
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in SRAM table map directory')
    
    
    def testSplitRowsAndCols(self):
        actualVal = 0
        expectedVal = 4
        # * ----- actual output
        actualTcamRows = list()
        actualTcamCols = list()
        actualSramRows = list()
        actualSramCols = list()
        self.tm.getPrjDir()
        self.tm.getYAMLFilePath()
        self.tm.readYAML(self.tm.tcamTableConfigsFilePath)
        for conf in self.tm._tcamTableConfigs:
            self.tm.getTCAMConfig(conf)
            self.tm.getTCAMTableFilePath(conf)
            self.tm.readTCAMTable()
            self.tm.getSRAMTableDim()
            [tempTcamRows, tempTcamCols, tempSramRows, tempSramCols] = self.tm.splitRowsAndCols()
            actualTcamRows.append(tempTcamRows)
            actualTcamCols.append(tempTcamCols)
            actualSramRows.append(tempSramRows)
            actualSramCols.append(tempSramCols)
        # * ----- expected output
        expectedTcamRows = list()
        expectedTcamCols = list()
        expectedSramRows = list()
        expectedSramCols = list()
        with open('compiler/configs/tcamTables.yaml','r') as file:
            fileData = yaml.full_load(file)
        for conf in fileData:
            qsl = fileData[conf]['queryStrLen']
            ssl = fileData[conf]['subStrLen']
            tss = fileData[conf]['totalSubStr']
            pma = fileData[conf]['potMatchAddr']
            tempTcamRows = np.arange(0,pma,1).tolist()
            tempTcamCols = np.arange(1,qsl+1,1).tolist()
            tempTcamColVec = np.array_split(tempTcamCols,tss)
            for i in range(len(tempTcamColVec)):
                tempTcamColVec[i] = tempTcamColVec[i].tolist()
            tempSramRows = np.arange(0,tss * 2**ssl,1).tolist()
            tempSramRowVec = np.array_split(tempSramRows,tss)
            for i in range(len(tempSramRowVec)):
                tempSramRowVec[i] = tempSramRowVec[i].tolist()
            tempSramCols = np.arange(0,pma+1,1).tolist()
            expectedTcamRows.append(tempTcamRows)
            expectedTcamCols.append(tempTcamColVec)
            expectedSramRows.append(tempSramRowVec)
            expectedSramCols.append(tempSramCols)
        # * ----- assertion
        if actualTcamRows == expectedTcamRows:
            actualVal += 1
        if actualTcamCols == expectedTcamCols:
            actualVal += 1
        if actualSramRows == expectedSramRows:
            actualVal += 1
        if actualSramCols == expectedSramCols:
            actualVal += 1
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in TCAM and SRAM row and column vectors')





# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================


if __name__ == '__main__':
    # * run all test cases
    unittest.main()
    # unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='logs'))