from compiler.src.tableMapping import *
from unittest import TestCase
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
        actualVal = self.tm.getYAMLFilePath()
        # * ----- expected output
        expectedVal = os.path.join(self.tm.prjWorkDir,'compiler/configs/tcamTables.yaml')
        # * ----- assertion
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in TCAM table YAML file path')
    
    
    def testReadYAML(self):
        # * ----- actual output
        self.tm.getYAMLFilePath()
        actualVal = self.tm.readYAML(self.tm.tcamTableConfigsFilePath)
        # * ----- expected output
        # * ----- assertion
        self.assertEqual(type(actualVal),dict,msg='MISMATCH in reading TCAM table YAML config file')
    
    
    def testGetTCAMConfig(self):
        # * ----- actual output
        self.tm.getYAMLFilePath()
        self.tm.readYAML(self.tm.tcamTableConfigsFilePath)
        actualVal = self.tm._tcamTableConfigs.keys()
        with open('compiler/configs/tcamTables.yaml','r') as file:
            fileData = yaml.full_load(file)
        # * ----- expected output
        expectedVal = fileData.keys()
        # * ----- assertion
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in total number of TCAM table YAML configs')
    
    
    def testGetTCAMTableFilePath(self):
        actualVal = list()
        expectedVal = list()
        # * ----- actual output
        self.tm.getYAMLFilePath()
        self.tm.readYAML(self.tm.tcamTableConfigsFilePath)
        tempTcamConfig = list(self.tm._tcamTableConfigs.keys())
        for i in range(len(tempTcamConfig)):
            actualVal.append(self.tm.getTCAMTableFilePath(tempTcamConfig[i]))
        # * ----- expected output
        for file in glob.iglob('compiler/lib/*.xlsx',recursive=True):
            expectedVal.append(file)
        # * ----- assertion
        actualVal.sort()
        expectedVal.sort()
        self.assertEqual(actualVal,expectedVal,msg='hello')

# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================


if __name__ == '__main__':
    # * run all test cases
    unittest.main()
    # unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='logs'))