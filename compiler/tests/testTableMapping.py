from compiler.src.tableMapping import *
from unittest import TestCase
import pandas as pd
import logging
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
        # actualTcamConfCount = len(list(self.tm._tcamTableConfigs.keys()))
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






# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================


if __name__ == '__main__':
    # * run all test cases
    unittest.main()
    # unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='logs'))