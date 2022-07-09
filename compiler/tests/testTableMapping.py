from compiler.src.tableMapping import *
import HtmlTestRunner
import unittest
import logging
import os

# ===========================================================================================
# ======================================= Begin Class =======================================
# ===========================================================================================

class TestTableMapping(unittest.TestCase):
    
    def testGetPrjDir(self):
        actual = TableMapping.getPrjDir(self)
        expected = os.getcwd()
        self.assertEqual(actual,expected,msg='MISMATCH in prj dir path')


# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================


if __name__ == '__main__':
    # * run all test cases
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='logs'))