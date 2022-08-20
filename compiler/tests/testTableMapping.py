from compiler.src.tableMapping import TableMapping
from unittest import TestCase
import pandas as pd
import numpy as np
import yaml
import glob
import os
import pytest

# ===========================================================================================
# ======================================= Begin Class =======================================
# ===========================================================================================

class testTableMapping(TestCase):
    
    def setUp(self):
        self.tm = TableMapping()
        self.verb = 0
        self.debug = 0
    
    
    @ pytest.mark.testTableMapping
    @ pytest.mark.testGetPrjDir
    def testGetPrjDir(self):
        # * ----- actual output
        actualVal = self.tm.getPrjDir(self.verb)
        # * ----- expected output
        expectedVal = os.getcwd()
        # * ----- assertion
        # print('\n',actualVal)
        # print('',expectedVal)
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in prj dir path')
    
    
    @ pytest.mark.testTableMapping
    @ pytest.mark.testGetYAMLFilePath
    def testGetYAMLFilePath(self):
        # * ----- actual output
        self.tm.getPrjDir(self.verb)
        actualVal = self.tm.getYAMLFilePath(self.verb)
        # * ----- expected output
        expectedVal = os.path.join(self.tm.prjWorkDir,'compiler/configs/tcamTables.yaml')
        # * ----- assertion
        # print('\n',actualVal)
        # print('',expectedVal)
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in TCAM table YAML file path')
    
    
    @ pytest.mark.testTableMapping
    @ pytest.mark.testReadYAML
    def testReadYAML(self):
        # * ----- actual output
        self.tm.getPrjDir(self.verb)
        self.tm.getYAMLFilePath(self.verb)
        actualVal = self.tm.readYAML(self.tm.tcamTableConfigsFilePath,self.verb)
        # * ----- expected output
        with open('compiler/configs/tcamTables.yaml','r') as file:
            expectedVal = yaml.full_load(file)
        # * ----- assertion
        # print('\n',actualVal)
        # print('',expectedVal)
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in reading TCAM table YAML config file')
    
    
    @ pytest.mark.testTableMapping
    @ pytest.mark.testGetTCAMConfig
    def testGetTCAMConfig(self):
        # * ----- actual output
        self.tm.getPrjDir(self.verb)
        self.tm.getYAMLFilePath(self.verb)
        self.tm.readYAML(self.tm.tcamTableConfigsFilePath,self.verb)
        actualVal = list(self.tm._tcamTableConfigs.keys())
        # * ----- expected output
        with open('compiler/configs/tcamTables.yaml','r') as file:
            fileData = yaml.full_load(file)
            expectedVal = list(fileData.keys())
        # * ----- assertion
        # print('\n',actualVal)
        # print('',expectedVal)
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in total number of TCAM table YAML configs')
    
    
    @ pytest.mark.testTableMapping
    @ pytest.mark.testGetTCAMTableFilePath
    def testGetTCAMTableFilePath(self):
        actualVal = list()
        expectedVal = list()
        # * ----- actual output
        self.tm.getPrjDir(self.verb)
        self.tm.getYAMLFilePath(self.verb)
        self.tm.readYAML(self.tm.tcamTableConfigsFilePath,self.verb)
        actualTcamConfName = list(self.tm._tcamTableConfigs.keys())
        for conf in actualTcamConfName:
            actualVal.append(self.tm.getTCAMTableFilePath(conf,self.verb))
        # * ----- expected output
        for expectRelXlsxPath in glob.iglob('compiler/lib/*.xlsx',recursive=True):
            expectAbsXlsxPath = os.path.join(self.tm.prjWorkDir,expectRelXlsxPath)
            expectedVal.append(expectAbsXlsxPath)
        # * ----- assertion
        actualVal.sort()
        expectedVal.sort()
        # print('\n',actualVal)
        # print('',expectedVal)
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in total number of Xlsx TCAM table maps')
    
    
    @ pytest.mark.testTableMapping
    @ pytest.mark.testReadTCAMTable
    def testReadTCAMTable(self):
        actualTcamTableShape = list()
        expectTcamTableShape = list()
        # * ----- actual output
        self.tm.getPrjDir(self.verb)
        self.tm.getYAMLFilePath(self.verb)
        self.tm.readYAML(self.tm.tcamTableConfigsFilePath,self.verb)
        for conf in self.tm._tcamTableConfigs:
            self.tm.getTCAMConfig(conf)
            self.tm.getTCAMTableFilePath(conf,self.verb)
            [rows, cols] = self.tm.readTCAMTable(self.verb)
            tempDict = {'config': conf,'rows': rows,'cols': cols}
            actualTcamTableShape.append(tempDict)
        actualVal = sorted(actualTcamTableShape, key=lambda x: x['config'])
        # * ----- expected output
        for expectRelXlsxPath in glob.iglob('compiler/lib/*.xlsx',recursive=True):
            expectAbsXlsxPath = os.path.join(self.tm.prjWorkDir,expectRelXlsxPath)
            expectAbsTcamConfig = os.path.basename(expectAbsXlsxPath).replace('.xlsx','')
            expectTcamTable = pd.read_excel(expectAbsXlsxPath, skiprows=2, index_col=None, engine='openpyxl')
            tempDict = {'config': expectAbsTcamConfig,'rows': expectTcamTable.shape[0],'cols': expectTcamTable.shape[1]}
            expectTcamTableShape.append(tempDict)
        expectedVal = sorted(expectTcamTableShape, key=lambda x: x['config'])
        # * ----- assertion
        # print('\n',actualVal)
        # print('',expectedVal)
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in TCAM table map rows and columns')
    
    
    @ pytest.mark.testTableMapping
    @ pytest.mark.testGetSRAMTableDim
    def testGetSRAMTableDim(self):
        actualSramTableShape = list()
        expectSramTableShape = list()
        # * ----- actual output
        self.tm.getPrjDir(self.verb)
        self.tm.getYAMLFilePath(self.verb)
        self.tm.readYAML(self.tm.tcamTableConfigsFilePath,self.verb)
        for conf in self.tm._tcamTableConfigs:
            self.tm.getTCAMConfig(conf)
            self.tm.getTCAMTableFilePath(conf,self.verb)
            self.tm.readTCAMTable(self.verb)
            [sramRows, sramCols] = self.tm.getSRAMTableDim(self.verb)
            conf = conf.replace('tcam','sram')
            tempSramDict = {'config': conf,'rows': sramRows,'cols': sramCols}
            actualSramTableShape.append(tempSramDict)
        actualVal = sorted(actualSramTableShape, key=lambda x: x['config'])
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
        # * ----- assertion
        # print('\n',actualVal)
        # print('',expectedVal)
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in SRAM table map rows and columns')
    
    
    @ pytest.mark.testTableMapping
    @ pytest.mark.testGenSRAMTable
    def testGenSRAMTable(self):
        pass
    
    
    @ pytest.mark.testTableMapping
    @ pytest.mark.testCreateSRAMTableDir
    def testCreateSRAMTableDir(self):
        # * ----- actual output
        self.tm.getPrjDir(self.verb)
        actualVal = os.path.join(self.tm.prjWorkDir,'sramTables')
        # * ----- expected output
        expectedVal = os.path.join(os.getcwd(),'sramTables')
        # * ----- assertion
        # print('\n',actualVal)
        # print('',expectedVal)
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in SRAM table map directory')
    
    
    @ pytest.mark.testTableMapping
    @ pytest.mark.testSplitRowsAndCols
    def testSplitRowsAndCols(self):
        actualVal = 0
        expectedVal = 4
        # * ----- actual output
        actualTcamRows = list()
        actualTcamCols = list()
        actualSramRows = list()
        actualSramCols = list()
        self.tm.getPrjDir(self.verb)
        self.tm.getYAMLFilePath(self.verb)
        self.tm.readYAML(self.tm.tcamTableConfigsFilePath,self.verb)
        for conf in self.tm._tcamTableConfigs:
            self.tm.getTCAMConfig(conf)
            self.tm.getTCAMTableFilePath(conf,self.verb)
            self.tm.readTCAMTable(self.verb)
            self.tm.getSRAMTableDim(self.verb)
            [tempTcamRows, tempTcamCols, tempSramRows, tempSramCols] = self.tm.splitRowsAndCols(self.debug)
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
        # print('\n',actualVal)
        # print('',expectedVal)
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in TCAM and SRAM row and column vectors')
    
    
    @ pytest.mark.testTableMapping
    @ pytest.mark.testGenerateSRAMSubStr
    def testGenerateSRAMSubStr(self):
        pass
    
    
    @ pytest.mark.testTableMapping
    @ pytest.mark.testMapTCAMtoSRAM
    def testMapTCAMtoSRAM(self):
        pass
    
    
    @ pytest.mark.testTableMapping
    @ pytest.mark.testWriteSRAMtoXlsx
    def testWriteSRAMtoXlsx(self):
        actualSramTablePath = list()
        expectedSramTablePath = list()
        # * ----- actual output
        self.tm.getPrjDir(self.verb)
        self.tm.getYAMLFilePath(self.verb)
        self.tm.readYAML(self.tm.tcamTableConfigsFilePath,self.verb)
        for conf in self.tm._tcamTableConfigs:
            self.tm.getTCAMConfig(conf)
            self.tm.getTCAMTableFilePath(conf,self.verb)
            self.tm.readTCAMTable(self.verb)
            self.tm.getSRAMTableDim(self.verb)
            self.tm.genSRAMTable(self.verb)
            self.tm.createSRAMTableDir(self.verb)
            self.tm.splitRowsAndCols(self.debug)
            self.tm.generateSRAMSubStr(self.verb,self.debug)
            self.tm.mapTCAMtoSRAM(self.verb, self.debug)
            self.tm.writeSRAMtoXlsx()
            actualSramTablePath.append(self.tm.sramTableXlsxFilePath)
        actualVal = actualSramTablePath
        # * ----- expected output
        sramTableDir = os.path.join(os.getcwd(),'sramTables')
        with open('compiler/configs/tcamTables.yaml','r') as file:
            fileOut = yaml.full_load(file)
        tcamTableConf = list(fileOut.keys())
        for conf in tcamTableConf:
            conf = conf.replace('tcam','sram') + '.xlsx'
            filePath = os.path.join(sramTableDir,conf)
            expectedSramTablePath.append(filePath)
        expectedVal = expectedSramTablePath
        # * ----- assertion
        # print('\n',actualVal)
        # print('',expectedVal)
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in SRAM xlsx file paths')
    
    
    @ pytest.mark.testTableMapping
    @ pytest.mark.testWriteSRAMtoHtml
    def testWriteSRAMtoHtml(self):
        actualSramTablePath = list()
        expectedSramTablePath = list()
        # * ----- actual output
        self.tm.getPrjDir(self.verb)
        self.tm.getYAMLFilePath(self.verb)
        self.tm.readYAML(self.tm.tcamTableConfigsFilePath,self.verb)
        for conf in self.tm._tcamTableConfigs:
            self.tm.getTCAMConfig(conf)
            self.tm.getTCAMTableFilePath(conf,self.verb)
            self.tm.readTCAMTable(self.verb)
            self.tm.getSRAMTableDim(self.verb)
            self.tm.genSRAMTable(self.verb)
            self.tm.createSRAMTableDir(self.verb)
            self.tm.splitRowsAndCols(self.debug)
            self.tm.generateSRAMSubStr(self.verb,self.debug)
            self.tm.mapTCAMtoSRAM(self.verb, self.debug)
            self.tm.writeSRAMtoHtml()
            actualSramTablePath.append(self.tm.sramTableHtmlFilePath)
        actualVal = actualSramTablePath
        # * ----- expected output
        sramTableDir = os.path.join(os.getcwd(),'sramTables')
        with open('compiler/configs/tcamTables.yaml','r') as file:
            fileOut = yaml.full_load(file)
        tcamTableConf = list(fileOut.keys())
        for conf in tcamTableConf:
            conf = conf.replace('tcam','sram') + '.html'
            filePath = os.path.join(sramTableDir,conf)
            expectedSramTablePath.append(filePath)
        expectedVal = expectedSramTablePath
        # * ----- assertion
        # print('\n',actualVal)
        # print('',expectedVal)
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in SRAM html file paths')
    
    
    @ pytest.mark.testTableMapping
    @ pytest.mark.testWriteSRAMtoJson
    def testWriteSRAMtoJson(self):
        actualSramTablePath = list()
        expectedSramTablePath = list()
        # * ----- actual output
        self.tm.getPrjDir(self.verb)
        self.tm.getYAMLFilePath(self.verb)
        self.tm.readYAML(self.tm.tcamTableConfigsFilePath,self.verb)
        for conf in self.tm._tcamTableConfigs:
            self.tm.getTCAMConfig(conf)
            self.tm.getTCAMTableFilePath(conf,self.verb)
            self.tm.readTCAMTable(self.verb)
            self.tm.getSRAMTableDim(self.verb)
            self.tm.genSRAMTable(self.verb)
            self.tm.createSRAMTableDir(self.verb)
            self.tm.splitRowsAndCols(self.debug)
            self.tm.generateSRAMSubStr(self.verb,self.debug)
            self.tm.mapTCAMtoSRAM(self.verb, self.debug)
            self.tm.writeSRAMtoJson()
            actualSramTablePath.append(self.tm.sramTableJsonFilePath)
        actualVal = actualSramTablePath
        # * ----- expected output
        sramTableDir = os.path.join(os.getcwd(),'sramTables')
        with open('compiler/configs/tcamTables.yaml','r') as file:
            fileOut = yaml.full_load(file)
        tcamTableConf = list(fileOut.keys())
        for conf in tcamTableConf:
            conf = conf.replace('tcam','sram') + '.json'
            filePath = os.path.join(sramTableDir,conf)
            expectedSramTablePath.append(filePath)
        expectedVal = expectedSramTablePath
        # * ----- assertion
        # print('\n',actualVal)
        # print('',expectedVal)
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in SRAM json file paths')
    
    
    @ pytest.mark.testTableMapping
    @ pytest.mark.testWriteSRAMtoTxt
    def testWriteSRAMtoTxt(self):
        actualSramTablePath = list()
        expectedSramTablePath = list()
        # * ----- actual output
        self.tm.getPrjDir(self.verb)
        self.tm.getYAMLFilePath(self.verb)
        self.tm.readYAML(self.tm.tcamTableConfigsFilePath,self.verb)
        for conf in self.tm._tcamTableConfigs:
            self.tm.getTCAMConfig(conf)
            self.tm.getTCAMTableFilePath(conf,self.verb)
            self.tm.readTCAMTable(self.verb)
            self.tm.getSRAMTableDim(self.verb)
            self.tm.genSRAMTable(self.verb)
            self.tm.createSRAMTableDir(self.verb)
            self.tm.splitRowsAndCols(self.debug)
            self.tm.generateSRAMSubStr(self.verb,self.debug)
            self.tm.mapTCAMtoSRAM(self.verb, self.debug)
            self.tm.writeSRAMtoTxt()
            actualSramTablePath.append(self.tm.sramTableTxtFilePath)
        actualVal = actualSramTablePath
        # * ----- expected output
        sramTableDir = os.path.join(os.getcwd(),'sramTables')
        with open('compiler/configs/tcamTables.yaml','r') as file:
            fileOut = yaml.full_load(file)
        tcamTableConf = list(fileOut.keys())
        for conf in tcamTableConf:
            conf = conf.replace('tcam','sram') + '.txt'
            filePath = os.path.join(sramTableDir,conf)
            expectedSramTablePath.append(filePath)
        expectedVal = expectedSramTablePath
        # * ----- assertion
        # print('\n',actualVal)
        # print('',expectedVal)
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in SRAM txt file paths')


# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================


if __name__ == '__main__':
    # * run all test cases
    unittest.main()