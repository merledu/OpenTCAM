from tableMapping import *
import logging
import argparse
import os

def main():
    # create logs dir if it doesnt exist
    pwd=os.getcwd()
    logsDirPath = os.path.join(pwd,'logs')
    if os.path.exists(logsDirPath) is False:
        os.makedirs('logs')
    
    # set arguments for OpenTCAM
    parser = argparse.ArgumentParser(prog='OpenTCAM',
                                    usage='%(prog)s [options] path',
                                    description='TCAM memory generator',
                                    epilog='Python framework for generating configurable SRAM based TCAM memories')
    # list of all possible args for OpenTCAM
    parser.add_argument('-tconf','--tcamConfig',
                        type=str,default='tcamTable2',metavar='',required=True,nargs='?',help='name of specific TCAM table config')
    parser.add_argument('-d','--debug',
                        type=int,default=0,metavar='',required=False,nargs='?',help='print debugging mode')
    parser.add_argument('-v','--verbose',
                        type=int,default=0,metavar='',required=False,nargs='?',help='print verbose mode')
    myargs = parser.parse_args()
    
    # ====================================================== code main body    
    
    # class objects
    tm1=TableMapping()
    
    # get project dir
    tm1.getPrjDir()
    # get tcam table config yaml file path
    tm1.getYAMLFilePath()
    # read tcam table config yaml file
    tm1.readYAML(tm1.tcamTableConfigsFilePath)
    # print all tcam configs
    if myargs.debug:
        tm1.printYAML()
    if myargs.tcamConfig:
        # get specific tcam config from yaml file
        tempConfig = tm1.getTCAMConfig(myargs.tcamConfig)
        # print specific tcam config
        if myargs.verbose:
            print(json.dumps(tempConfig, indent=4))
        # get tcam table map file path
        tm1.getTCAMTableFilePath(myargs.tcamConfig)
    # read tcam table map file
    tm1.readTCAMTable()
    # print tcam table map
    if myargs.verbose:
        tm1.printDF(tm1._tcamTable)
    # calculate sram table dimensions
    tm1.getSRAMTableDim()
    # create sram table dataframe
    tm1.genSRAMTable()
    # print empty sram table map
    if myargs.debug:
        tm1.printDF(tm1._sramTable)
    # create sram table map excel file
    tm1.createSRAMExcel()
    # read various params and map the tcam table to sram table
    tm1.splitRowsAndCols()
    tm1.mapTCAMtoSRAM()
    # print updated sram table
    if myargs.verbose:
        tm1.printDF(tm1._sramTable)
    # write sram table map to excel file
    tm1.createSRAMExcel()



if __name__ == '__main__':
    main()