import unittest
from compiler.src.tableMapping import *
from unittest import TestCase
import logging
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
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in YAML file path')
    
    
    def testReadYAML(self):
        self.tm.getYAMLFilePath()
        actualVal = self.tm.readYAML(self.tm.tcamTableConfigsFilePath)
        self.assertEqual(type(actualVal),dict)

# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================


if __name__ == '__main__':
    # * run all test cases
    unittest.main()
    # unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='logs'))