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



# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================


if __name__ == '__main__':
    # * run all test cases
    unittest.main()
    # unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='logs'))