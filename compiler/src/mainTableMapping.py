"""
List of all pip packages imported
"""

import argparse
import json
import os

from tableMapping import TableMapping


def main():
    """
    main func for implementing py class TableMapping
    """
    # create logs dir if it doesn't exist
    pwd = os.getcwd()
    logsDirPath = os.path.join(pwd, "logs")
    if os.path.exists(logsDirPath) is False:
        os.makedirs("logs")

    # set arguments for OpenTCAM
    parser = argparse.ArgumentParser(
        prog="OpenTCAM",
        usage="%(prog)s [options] path",
        description="TCAM memory generator",
        epilog="Python framework for generating configurable SRAM based TCAM memories",
    )
    # list of all possible args for OpenTCAM
    parser.add_argument(
        "-tconf", "--tcamConfig", type=str, default="tcamTable2", metavar="", required=True, nargs="?", help="name of specific TCAM table config"
    )
    parser.add_argument("-excel", type=int, default=1, metavar="", required=False, nargs="?", help="print SRAM table map as xlsx")
    parser.add_argument("-html", type=int, default=0, metavar="", required=False, nargs="?", help="print SRAM table map as html")
    parser.add_argument("-json", type=int, default=0, metavar="", required=False, nargs="?", help="print SRAM table map as json")
    parser.add_argument("-txt", type=int, default=0, metavar="", required=False, nargs="?", help="print SRAM table map as txt")
    parser.add_argument("-d", "--debug", type=int, default=0, metavar="", required=False, nargs="?", help="print debugging mode")
    parser.add_argument("-v", "--verbose", type=int, default=0, metavar="", required=False, nargs="?", help="print verbose mode")
    arg = parser.parse_args()

    # ====================================================== code main body

    # class objects
    tm1 = TableMapping()

    # get project dir
    tm1.getPrjDir(arg.verbose)
    # get tcam table config yaml file path
    tm1.getYAMLFilePath(arg.verbose)
    # read tcam table config yaml file
    tm1.readYAML(tm1.tcamTableConfigsFilePath, arg.verbose)
    # print all tcam configs
    if arg.debug:
        tm1.printYAML(arg.debug)
    if arg.tcamConfig:
        # get specific tcam config from yaml file
        tempConfig = tm1.getTCAMConfig(arg.tcamConfig)
        # print specific tcam config
        print(json.dumps(tempConfig, indent=4))
        # get tcam table map file path
        tm1.getTCAMTableFilePath(arg.tcamConfig, arg.verbose)
    # read tcam table map file
    tm1.readTCAMTable(arg.verbose)
    # print tcam table map
    tm1.printDF(tm1.getTcamTableMap(), "TCAM Table Map")
    # calculate sram table dimensions
    tm1.getSRAMTableDim(arg.verbose)
    # create sram table dataframe
    tm1.genSRAMTable(arg.verbose)
    # print empty sram table map
    if arg.debug:
        tm1.printDF(tm1.getSramTableMap(), "Empty SRAM Table Map")
    # create sram tables dir
    tm1.createSRAMTableDir(arg.verbose)
    # read various params and map the tcam table to sram table
    tm1.splitRowsAndCols(arg.debug)
    # generate all possible combinations of sram addr
    tm1.isolateTCAMSearchQueries(arg.verbose, arg.debug)
    tm1.generateSRAMSubStr(arg.verbose, arg.debug)
    # map all possible tcam table addr to sram table
    tm1.mapTCAMtoSRAM(arg.verbose, arg.debug)
    # print updated sram table
    tm1.printDF(tm1.getSramTableMap(), "SRAM Table Map")
    # write sram table map to excel file
    if arg.excel:
        tm1.writeSRAMtoXlsx()
    # write sram table map to html file
    if arg.html:
        tm1.writeSRAMtoHtml()
    # write sram table map to json file
    if arg.json:
        tm1.writeSRAMtoJson()
    # write sram table map to txt file
    if arg.txt:
        tm1.writeSRAMtoTxt()


if __name__ == "__main__":
    main()
