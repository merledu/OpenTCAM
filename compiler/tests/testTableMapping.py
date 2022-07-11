import unittest
from compiler.src.tableMapping import *
from unittest import TestCase, expectedFailure
import logging
import yaml
import os

# ===========================================================================================
# ======================================= Begin Class =======================================
# ===========================================================================================

class TestTableMapping(TestCase):
    
    def setUp(self):
        self.tm = TableMapping()
    
    
    def testGetPrjDir(self):
        actualVal = self.tm.getPrjDir()
        expectedVal = os.getcwd()
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in prj dir path')
    
    
    def testGetYAMLFilePath(self):
        actualVal = self.tm.getYAMLFilePath()
        expectedVal = os.path.join(self.tm.prjWorkDir,'compiler/configs/tcamTables.yaml')
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in TCAM table YAML file path')
    
    
    def testReadYAML(self):
        self.tm.getYAMLFilePath()
        actualVal = self.tm.readYAML(self.tm.tcamTableConfigsFilePath)
        self.assertEqual(type(actualVal),dict,msg='MISMATCH in TCAM table YAML config data')
    
    
    def testGetTCAMConfig(self):
        self.tm.getYAMLFilePath()
        self.tm.readYAML(self.tm.tcamTableConfigsFilePath)
        actualVal = self.tm._tcamTableConfigs.keys()
        with open('compiler/configs/tcamTables.yaml','r') as file:
            fileData = yaml.full_load(file)
        expectedVal = fileData.keys()
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in TCAM table YAML config keys')

# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================


if __name__ == '__main__':
    # * run all test cases
    unittest.main()
    # unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='logs'))