import logging
import os

# ===========================================================================================
# ======================================= Begin Class =======================================
# ===========================================================================================

class TcamRtlGenerator:
    # * ----------------------------------------------------------------- Variables
    def __init__(self):
        # * ------------------- public vars
        self.prjWorkDir = str()

        # * ------------------- protected vars
        self._tcamTableConfigs  = dict()

        # * ------------------- private vars
        self.__tcamQueryStrLen  = int()
\
        # * logging config
        logging.basicConfig(level=logging.DEBUG, filename='./logs/tcamRtlGenerator.log',
                            format='%(asctime)s | %(filename)s | %(funcName)s | %(levelname)s | %(lineno)d | %(message)s')
    
    
    # # * ----------------------------------------------------------------- Functions
    # def getPrjDir(self,verbose):
    #     """
    #     what does this func do ?
    #     input args:
    #     return val:
    #     """
    #     self.prjWorkDir=os.getcwd()
    #     logging.info('Project working dir: {:<s}'.format(self.prjWorkDir))
    #     printVerbose(verbose,'Project working dir: {:<s}'.format(self.prjWorkDir))
    #     return self.prjWorkDir









# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================

def printVerbose(verbose,msg):
    if verbose:
        print(str(msg))

def printDebug(debug,msg):
    if debug:
        print(str(msg))
