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
        self.tm.getPrjDir()
        actualVal = self.tm.getYAMLFilePath()
        expectedVal = os.path.join(self.tm.getPrjDir(),'compiler/configs/tcamTables.yaml')
        self.assertEqual(actualVal,expectedVal,msg='MISMATCH in YAML file path')


# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================


if __name__ == '__main__':
    # * run all test cases
    unittest.main()
    # unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='logs'))