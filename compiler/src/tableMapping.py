"""
List of all pip packages imported
"""

import difflib
import itertools
import json
import logging
import os
import re
import sys

import jellyfish
import numpy as np
import pandas as pd
import yaml
from tabulate import tabulate

# ===========================================================================================
# ======================================= Begin Class =======================================
# ===========================================================================================


class TableMapping:
    """
    Generates a golden model for a particular SRAM memory table map config
    using a respective TCAM memory table map and configs.
    """

    # * ----------------------------------------------------------------- Variables
    def __init__(self):
        """
        Constructor: Initializes all the class variables

        **Public Variables:**
        :param str prjWorkDir:                  current project working dir
        :param str sramTableDir:                abs path of SRAM table map folder
        :param str tcamTableConfigsFilePath:    abs path of TCAM table map config file
        :param str tcamTableConfigsFileName:    TCAM table map config file name
        :param str tcamTableXlsxFilePath:       abs path of TCAM table map XLSX file
        :param str tcamTableXlsxFileName:       TCAM table map XLSX file name
        :param str sramTableXlsxFilePath:       abs path of generated SRAM table map XLSX file
        :param str sramTableXlsxFileName:       SRAM table map XLSX file name
        :param str sramTableHtmlFilePath:       abs path of generated SRAM table map HTML file
        :param str sramTableHtmlFileName:       SRAM table map HTML file name
        :param str sramTableJsonFilePath:       abs path of generated SRAM table map JSON file
        :param str sramTableJsonFileName:       SRAM table map JSON file name
        :param str sramTableTxtFilePath:        abs path of generated SRAM table map TXT file
        :param str sramTableTxtFileName:        SRAM table map TXT file name

        **Protected Variables:**
        :param dict _tcamTableConfigs:      TCAM table map configs
        :param DataFrame _tcamTable:        TCAM table map
        :param DataFrame _sramTable:        SRAM table map
        :param DataFrame _tcamQSAddrTable:  TCAM table map query addr sub str
        :param DataFrame _sramQSAddrTable:  SRAM table map query addr sub str

        **Private Variables:**
        :param int __tcamQueryStrLen:   `queryStrLen` of a particular TCAM table config
        :param int __tcamSubStrLen:     `subStrLen` of a particular TCAM table config
        :param int __tcamTotalSubStr:   `totalSubStr` of a particular TCAM table config
        :param int __tcamPotMatchAddr:  `potMatchAddr` of a particular TCAM table config
        :param int __sramTableRows:     SRAM table map row count
        :param int __sramTableCols:     SRAM table map col count
        :param list __tcamRows:         TCAM table map row count vector
        :param list __tcamCols:         TCAM table map col count vector
        :param list __tcamColVec:       TCAM table map sub string address col count vector
        :param list __sramRows:         SRAM table map row count vector
        :param list __sramRowVec:       SRAM table map sub string address row count vector
        :param list __sramCols:         SRAM table map col count vector
        """
        # * ------------------- public vars
        self.prjWorkDir = ""
        self.sramTableDir = ""
        self.tcamTableConfigsFilePath = ""
        self.tcamTableConfigsFileName = ""
        self.tcamTableXlsxFilePath = ""
        self.tcamTableXlsxFileName = ""
        self.sramTableXlsxFilePath = ""
        self.sramTableXlsxFileName = ""
        self.sramTableHtmlFilePath = ""
        self.sramTableHtmlFileName = ""
        self.sramTableJsonFilePath = ""
        self.sramTableJsonFileName = ""
        self.sramTableTxtFilePath = ""
        self.sramTableTxtFileName = ""
        # * ------------------- protected vars
        self._tcamTableConfigs = {}
        self._tcamTable = pd.DataFrame
        self._sramTable = pd.DataFrame
        self._tcamQSAddrTable = pd.DataFrame
        self._sramQSAddrTable = pd.DataFrame
        # * ------------------- private vars
        self.__tcamQueryStrLen = 0
        self.__tcamSubStrLen = 0
        self.__tcamTotalSubStr = 0
        self.__tcamPotMatchAddr = 0
        self.__sramTableRows = 0
        self.__sramTableCols = 0
        self.__tcamRows = []
        self.__tcamCols = []
        self.__tcamColVec = []
        self.__sramRows = []
        self.__sramRowVec = []
        self.__sramCols = []
        # * logging config
        logging.basicConfig(
            level=logging.DEBUG,
            filename="./logs/tableMapping.log",
            format="%(asctime)s | %(filename)s | %(funcName)s | %(levelname)s | %(lineno)d | %(message)s",
        )

    # * ----------------------------------------------------------------- Functions
    def getPrjDir(self, verbose):
        """
        Obtain the absolute path of the current working directory.

        :param int verbose: print information in verbose mode.
        :return str: absolute path of the current project working directory.
        """
        self.prjWorkDir = os.getcwd()
        logging.info("Project working dir: %s", self.prjWorkDir)
        printVerbose(verbose, f"Project working dir: {self.prjWorkDir}")
        return self.prjWorkDir

    def getYAMLFilePath(self, verbose):
        """
        Obtain the absolute path of file tcamTables.yaml.

        :param int verbose: print information in verbose mode.
        :return str: absolute path of the current project working directory.
        """
        # * get tcamTables config file path
        tempPath = os.path.join(self.prjWorkDir, "compiler/configs/tcamTables.yaml")
        if os.path.isfile(tempPath) is True:
            self.tcamTableConfigsFilePath = tempPath
            self.tcamTableConfigsFileName = os.path.basename(tempPath)
            logging.info('"FOUND": TCAM table config file path: %s', self.tcamTableConfigsFilePath)
            printVerbose(verbose, f'"FOUND": TCAM table config file path: {self.tcamTableConfigsFilePath}')
            return self.tcamTableConfigsFilePath
        logging.error('"NOT FOUND": TCAM table config file path: %s', self.tcamTableConfigsFilePath)
        sys.exit(f'"NOT FOUND": TCAM table config file path: {self.tcamTableConfigsFilePath}')

    def readYAML(self, filePath, verbose):
        """
        Read a particular YAML config file

        :param str filePath: absolute path of file tcamTables.yaml.
        :param int verbose: print information in verbose mode.
        :return dict: dictionary containing all the TCAM table configs.
        """
        with open(filePath, encoding="utf-8") as file:
            self._tcamTableConfigs = yaml.full_load(file)
        # print(json.dumps(self._tcamTableConfigs,indent=4))
        # print(yaml.dump(self._tcamTableConfigs,sort_keys=False,default_flow_style=False))
        logging.info("Read TCAM table config file: %s", self.tcamTableConfigsFilePath)
        printVerbose(verbose, f"Read TCAM table config file: {self.tcamTableConfigsFilePath}")
        return self._tcamTableConfigs

    def printYAML(self, debug):
        """
        Print all present configs of a YAML file either in JSON or YAML style.

        :param int debug: print information in debug mode.
        """
        printDebug(debug, "Printing TCAM table configs")
        print(json.dumps(self._tcamTableConfigs, indent=4))
        # print(yaml.dump(self._tcamTableConfigs,sort_keys=False,default_flow_style=False))
        logging.info("Printed TCAM table configs")

    def getTCAMConfig(self, tcamConfig):
        """
        Check if a particular tcamTable config exists in file tcamTables.yaml. If found store the config params in vars.
        - **__tcamQueryStrLen:**    saves `queryStrLen`
        - **__tcamSubStrLen:**      saves `subStrLen`
        - **__tcamTotalSubStr:**    saves `totalSubStr`
        - **__tcamPotMatchAddr:**   saves `potMatchAddr`

        :param str tcamConfig: TCAM table config name e.g. tcamTableX
        :return dict: dictionary containing the respective table map config.
        """
        # * look for specific tcam config in compiler/configs/tcamTables.yaml
        if tcamConfig in self._tcamTableConfigs.keys():
            tempConfig = self._tcamTableConfigs[tcamConfig]
            # * save tcam config vars
            self.__tcamQueryStrLen = tempConfig["queryStrLen"]
            self.__tcamSubStrLen = tempConfig["subStrLen"]
            self.__tcamTotalSubStr = tempConfig["totalSubStr"]
            self.__tcamPotMatchAddr = tempConfig["potMatchAddr"]
            # * print specific tcam config
            # print(type(tempConfig))
            logging.info('"FOUND" Required TCAM Config [%s]', tcamConfig)
            print('"FOUND" Required TCAM Config [%s]', tcamConfig)
            logging.info("TCAM Config Data [%s] = %s", tcamConfig, tempConfig)
            return tempConfig
        logging.error('"NOT FOUND": TCAM Config [%s]', tcamConfig)
        sys.exit(f'"NOT FOUND": Required TCAM table config [{tcamConfig}]')

    def getTCAMTableFilePath(self, tcamConfig, verbose):
        """
        Obtain the absolute path of file **tcamTableX.xlsx** which represents the TCAM memory table map.

        :param str tcamConfig: TCAM table config name e.g. tcamTableX
        :param int verbose: print information in verbose mode.
        :return str: absolute path of the TCAM table mapping file.
        """
        # * find the specific tcam table map in compiler/lib/
        tempPath = os.path.join(self.prjWorkDir, "compiler/lib/" + tcamConfig + ".xlsx")
        if os.path.isfile(tempPath) is True:
            self.tcamTableXlsxFilePath = tempPath
            self.tcamTableXlsxFileName = os.path.basename(tempPath)
            logging.info('"FOUND" TCAM table map XLSX file path: %s', self.tcamTableXlsxFilePath)
            printVerbose(verbose, f'"FOUND" TCAM table map XLSX file path: {self.tcamTableXlsxFilePath}')
            return self.tcamTableXlsxFilePath
        logging.error('"NOT FOUND": TCAM table map XLSX file path: %s', self.tcamTableXlsxFilePath)
        sys.exit(f'"NOT FOUND": TCAM table map XLSX file path {self.tcamTableXlsxFilePath}')

    def printDF(self, dataFrame, heading):
        """
        Display the contents of a particular data frame.

        :param DataFrame dataFrame: particular data frame object.
        :param str heading: Title above data frame.
        """
        print("\n")
        print("Printing dataframe: %s", heading)
        print(tabulate(dataFrame, headers="keys", showindex=True, disable_numparse=True, tablefmt="github"), "\n")
        logging.info("Printing dataframe: %s", str(heading))

    def getTcamTableMap(self):
        """
        Getter function for the TCAM table map

        :return DataFrame: TCAM table map dataframe object
        """
        return self._tcamTable

    def getSramTableMap(self):
        """
        Getter function for the SRAM table map

        :return DataFrame: SRAM table map dataframe object
        """
        return self._sramTable

    def readTCAMTable(self, verbose):
        """
        Read the contents of a **tcamTableX.xlsx** TCAM memory table map as a data frame.

        :param int verbose: print information in verbose mode.
        :return int: list containing dimensions of TCAM table memory map.
        """
        # * store tcam table in dataframe
        self._tcamTable = pd.read_excel(self.tcamTableXlsxFilePath, skiprows=2, index_col=None, engine="openpyxl")
        # * get num of rows and col from tcam table
        tcamTableRows = self._tcamTable.shape[0]
        tcamTableCols = self._tcamTable.shape[1]
        # * compare row/col of tcam table with respective yaml config
        if tcamTableRows == self.__tcamPotMatchAddr and tcamTableCols - 1 == self.__tcamQueryStrLen:
            logging.info('"MATCH FOUND": TCAM table map rows == TCAM table YAML config potMatchAddr')
            printVerbose(verbose, '"MATCH FOUND": TCAM table map rows == TCAM table YAML config potMatchAddr')
            logging.info('"MATCH FOUND": TCAM table map cols == TCAM table YAML config queryStrLen')
            printVerbose(verbose, '"MATCH FOUND": TCAM table map cols == TCAM table YAML config queryStrLen')
            return [tcamTableRows, tcamTableCols]
        logging.error('"MATCH NOT FOUND": TCAM table map rows != TCAM table YAML config potMatchAddr')
        logging.error('"MATCH NOT FOUND": TCAM table map cols != TCAM table YAML config queryStrLen')
        sys.exit('"MATCH NOT FOUND": MISMATCH in TCAM table map and YAML config rows/cols')

    def getSRAMTableDim(self, verbose):
        """
        Generate the dimensions of the SRAM table map data frame using TCAM table map configs.

        :param int verbose: print information in verbose mode.
        :return int: list containing dimensions of SRAM table memory map.
        """
        self.__sramTableRows = self.__tcamTotalSubStr * pow(2, self.__tcamSubStrLen)
        self.__sramTableCols = self.__tcamPotMatchAddr
        logging.info("SRAM table rows [{%4d}] cols [{%4d}]", self.__sramTableRows, self.__sramTableCols)
        printVerbose(verbose, f"SRAM table rows [{self.__sramTableRows}] cols [{self.__sramTableCols}]")
        return [self.__sramTableRows, self.__sramTableCols]

    def genSRAMTable(self, verbose):
        """
        Create an empty SRAM table map data frame containing respective row addresses and column headings.

        :param int verbose: print information in verbose mode.
        """
        # * create temp vars
        sramTableAddrList = []
        sramColHeadings = []
        # * create row address
        for i in range(self.__tcamTotalSubStr):
            for j in range(2**self.__tcamSubStrLen):
                padding = "0" + str(self.__tcamSubStrLen) + "b"
                # sramTableAddrList.append(format(j, '#012b'))  # with 0b prefix
                sramTableAddrList.append(format(j, padding))  # without 0b prefix
            logging.info("Created [{%4d}] SRAM addresses from search query [{%4d}]", j + 1, i)
            printVerbose(verbose, f"Created [{j+1}] SRAM addresses from search query [{i}]")
        # * create col headings
        for k in reversed(range(self.__tcamPotMatchAddr)):
            heading = "D" + str(k)
            sramColHeadings.append(heading)
            logging.info("Created column heading %s", heading)
        # * gen empty m*n sram table
        self._sramTable = pd.DataFrame(index=np.arange(self.__sramTableRows), columns=np.arange(self.__sramTableCols))
        # * rename column headings
        self._sramTable.columns = sramColHeadings
        # * insert addr col at position 0
        self._sramTable.insert(0, "Addresses", sramTableAddrList, allow_duplicates=True)
        logging.info("Created empty [%d x %d] SRAM table", self._sramTable.shape[0], self._sramTable.shape[1])
        printVerbose(verbose, f"Created empty [{self._sramTable.shape[0]} x {self._sramTable.shape[1]}] SRAM table")

    def createSRAMTableDir(self, verbose):
        """
        Create a directory to store SRAM table maps in various formats.

        :param int verbose: print information in verbose mode.
        :return str: absolute path of the SRAM table map directory.
        """
        # * create sramTables dir if it doesn't exist
        self.sramTableDir = os.path.join(self.prjWorkDir, "sramTables")
        if os.path.exists(self.sramTableDir) is False:
            os.makedirs("sramTables")
            logging.info("Created sramTables dir: %s", self.sramTableDir)
            printVerbose(verbose, f"Created sramTables dir: {self.sramTableDir}")
        return self.sramTableDir

    def splitRowsAndCols(self, debug):
        """
        Create TCAM and SRAM table map row and column vectors based on TCAM table config parameters.

        :param int debug: print information in debug mode.
        :return list: list containing TCAM and SRAM row and column vectors.
        """
        # * store tcam and sram table in temp vars
        tcamDF = self._tcamTable
        sramDF = self._sramTable
        logging.info("TCAM table (r*c): %s", tuple(tcamDF.shape))
        logging.info("SRAM table (r*c): %s", tuple(sramDF.shape))
        # * create tcamRows vector
        self.__tcamRows = np.arange(0, self.__tcamPotMatchAddr, 1).tolist()
        logging.info("TCAM table row vector: %s", list(self.__tcamRows))
        printDebug(debug, f"TCAM table row vector: {*self.__tcamRows,}")
        # * create tcamCols vector
        self.__tcamCols = np.arange(1, self.__tcamQueryStrLen + 1, 1).tolist()
        logging.info("TCAM table col vector: %s", list(self.__tcamCols))
        printDebug(debug, f"TCAM table col vector: {*self.__tcamCols,}")
        # * create tcamColVec vector and split in equal pieces
        self.__tcamColVec = np.array_split(self.__tcamCols, self.__tcamTotalSubStr)
        for i in range(len(self.__tcamColVec)):
            self.__tcamColVec[i] = self.__tcamColVec[i].tolist()
            logging.info("TCAM table col split vector [%d]: %s", i, list(self.__tcamColVec[i]))
            printDebug(debug, f"TCAM table col split vector [{i}]: {self.__tcamColVec[i]}")
        # * create sramRows vector
        self.__sramRows = np.arange(0, self.__tcamTotalSubStr * 2**self.__tcamSubStrLen, 1).tolist()
        logging.info("SRAM table row vector: %s", list(self.__sramRows))
        printDebug(debug, f"SRAM table row vector: {self.__sramRows}")
        # * create sramRowVec vector and split in equal pieces
        self.__sramRowVec = np.array_split(self.__sramRows, self.__tcamTotalSubStr)
        for i in range(len(self.__sramRowVec)):
            self.__sramRowVec[i] = self.__sramRowVec[i].tolist()
            logging.info("SRAM table row split vector [%d]: %s", i, list(self.__sramRowVec[i]))
            printDebug(debug, f"SRAM table row split vector [{i}]: {self.__sramRowVec[i]}")
        # * create sramCols vector
        self.__sramCols = np.arange(0, self.__tcamPotMatchAddr + 1, 1).tolist()
        logging.info("SRAM table col vector: %s", list(self.__sramCols))
        printDebug(debug, f"SRAM table col vector: {self.__sramCols}")
        return [self.__tcamRows, self.__tcamColVec, self.__sramRowVec, self.__sramCols]

    def isolateTCAMSearchQueries(self, verbose, debug):
        """
        Create a data frame containing all the sub strings in original format from all the TCAM table search queries.

        :param int verbose: print information in verbose mode.
        :param int debug: print information in debug mode.
        """
        tcamDF = self._tcamTable
        count1 = 0
        self._tcamQSAddrTable = pd.DataFrame(columns=["TCAM Query Str Addr", "PMA", "QS col"])

        # * ----- add all original search queries in dataframe
        # * iterate through tcam table rows
        for row in range(len(tcamDF)):
            # * iterate through tcam table cols
            for col in range(len(self.__tcamColVec)):
                # * search and concat search query string address in tcam table
                tempAddr = [str(c) for c in list(tcamDF.iloc[row, self.__tcamColVec[col]])]
                tempAddr = "".join(tempAddr)
                # * append row in sqSubStrAddrDf data frame
                tempRow = [tempAddr, row, col]
                self._tcamQSAddrTable.loc[count1] = tempRow
                count1 += 1
                logging.info("TCAM Search Queries Table | Addr: %s | TCAM Row: %5d | Sub String Col: %5d |", tempAddr, row, col)
                printDebug(debug, f"TCAM Search Queries Table | Addr: {tempAddr} | TCAM Row: {row} | Sub String Col: {col} |")
        if verbose:
            self.printDF(self._tcamQSAddrTable, "Original TCAM Search Query Address Table")

    def generateSRAMSubStr(self, verbose, debug):
        """
        Generate all possible combinations of all sub strings from the original TCAM table search queries.

        :param int verbose: print information in verbose mode.
        :param int debug: print information in debug mode.
        """
        count2 = 0
        self._sramQSAddrTable = pd.DataFrame(columns=["SRAM Query Str Addr", "PMA", "QS col"])

        # * ----- find all possible alternatives for X based addr
        # * create array of N bit bin addresses
        queryStrBinAddrList = np.arange(2**self.__tcamSubStrLen).tolist()
        padding = "0" + str(self.__tcamSubStrLen) + "b"
        for item in queryStrBinAddrList:
            dec2Bin = format(item, padding)
            queryStrBinAddrList = queryStrBinAddrList[:item] + [dec2Bin] + queryStrBinAddrList[item + 1 :]
        logging.info("N bit bin addr list: %s", list(queryStrBinAddrList))
        logging.info("N bit bin addr list len: %d", len(queryStrBinAddrList))
        if verbose or debug:
            print("N bit bin addr list: %s", list(queryStrBinAddrList))
            print("N bit bin addr list len: %d", len(queryStrBinAddrList))

        # * get origSQ addr
        tempQSAddrList = self._tcamQSAddrTable["TCAM Query Str Addr"].to_list()
        tempQSPmaList = self._tcamQSAddrTable["PMA"].to_list()
        tempQSColList = self._tcamQSAddrTable["QS col"].to_list()

        printDebug(debug, f"Search Query addr list: {tempQSAddrList}")
        printDebug(debug, f"Search Query addr list len: {len(tempQSAddrList)}\n")
        # * map the 'bX in search queries to 0 and 1
        for (oldAddr, pma, qscol) in zip(tempQSAddrList, tempQSPmaList, tempQSColList):
            # * if 'bX in search query then find all possible alternatives and add in table
            if "x" in oldAddr:
                for newAddr in queryStrBinAddrList:
                    matching = jellyfish.damerau_levenshtein_distance(oldAddr, newAddr)
                    if matching == len(re.findall("x", oldAddr)):
                        printVerbose(
                            verbose,
                            f"count = {count2} | orig Search Query = {oldAddr} | " f"new Search Query = {newAddr} | matching ratio = {matching} |",
                        )
                        logging.info(
                            "count = %d | orig Search Query = %s | new Search Query = %s | matching ratio = %f |", count2, oldAddr, newAddr, matching
                        )
                        self._sramQSAddrTable.loc[count2] = [newAddr, pma, qscol]
                        count2 += 1
            # * else simply add search query in table as is
            else:
                printVerbose(verbose, f"count = {count2} | orig Search Query = {oldAddr} | new Search Query = {oldAddr} | matching ratio = {0} |")
                logging.info("count = %d | orig Search Query = %s | new Search Query = %s | matching ratio = %f |", count2, oldAddr, oldAddr, 0)
                self._sramQSAddrTable.loc[count2] = [oldAddr, pma, qscol]
                count2 += 1

        if verbose:
            self.printDF(self._sramQSAddrTable, "Original SRAM Search Query Address Table")

    def mapTCAMtoSRAM(self, verbose, debug):
        """
        Map all possible combinations of TCAM table map sub strings to SRAM table map sub strings.

        :param int verbose: print information in verbose mode.
        :param int debug: print information in debug mode.
        """
        sramDF = self._sramTable
        sramAddrList = self._sramQSAddrTable["SRAM Query Str Addr"].to_list()
        tcamRowList = self._sramQSAddrTable["PMA"].to_list()
        sramColList = self._sramQSAddrTable["QS col"].to_list()

        if len(tcamRowList) == len(sramColList):
            for (queryStr, pma, qsCol) in itertools.zip_longest(sramAddrList, tcamRowList, sramColList):
                # * create sram table subsections based on query str
                tempSRAMTable = sramDF.iloc[self.__sramRowVec[qsCol], self.__sramCols]
                logging.info("Search Query mapping portion: %d", qsCol)
                printDebug(debug, f"Search Query mapping portion: {qsCol}")
                # print(tabulate(tempSRAMTable,headers='keys',tablefmt='github'),'\n')
                # * find specific mapping cell in sram table
                rowIndex = tempSRAMTable.index[tempSRAMTable["Addresses"] == queryStr].to_list()[0]
                colIndex = len(self.__sramCols) - pma - 1
                # print('sram rowIndex: ',rowIndex,type(rowIndex))
                # print('sram colIndex: ',colIndex,type(colIndex))
                # * find specific entry
                oldSramTableEntry = sramDF.iloc[rowIndex, colIndex]
                # print(sramDF.iloc[rowIndex,colIndex])
                # * replace specific entry
                sramDF.iat[rowIndex, colIndex] = 1
                # * print before and after
                if verbose or debug:
                    logging.info("SRAM table cell [%d, %d] | Value = %s -> %s", rowIndex, colIndex, oldSramTableEntry, sramDF.iat[rowIndex, colIndex])
                    printDebug(debug, f"SRAM table cell [{rowIndex}, {colIndex}] | Value = {oldSramTableEntry} -> {sramDF.iat[rowIndex,colIndex]}")
            # * add zeros in empty cells
            sramDF = sramDF.fillna(0)
            self._sramTable = sramDF
        else:
            logging.error('"MATCH NOT FOUND": TCAM table rows != SRAM table cols config potMatchAddr')
            sys.exit('"MATCH NOT FOUND": MISMATCH in TCAM table map and YAML config rows/cols')

    def writeSRAMtoXlsx(self):
        """
        Generates an SRAM table map in XLSX format.

        :return str: absolute path of the SRAM table map `.xlsx` file.
        """
        # * create sram table file path and name
        self.sramTableXlsxFileName = os.path.basename(self.tcamTableXlsxFileName.replace("tcam", "sram"))
        self.sramTableXlsxFilePath = os.path.join(self.sramTableDir, self.sramTableXlsxFileName)
        # * create excel file in dir sramTables
        # writer = pd.ExcelWriter(self.sramTableXlsxFilePath,engine='xlsxwriter')
        # writer.save()
        # * apply formatting to dataframe
        self._sramTable.style.applymap(highlightCell).to_excel(
            excel_writer=self.sramTableXlsxFilePath, sheet_name=self.sramTableXlsxFileName, na_rep="", header=True, index=True, engine="openpyxl"
        )
        logging.info("Created SRAM table XLSX file: %s", self.sramTableXlsxFilePath)
        print("Created SRAM table XLSX file: %s", self.sramTableXlsxFilePath)
        return self.sramTableXlsxFilePath

    def writeSRAMtoHtml(self):
        """
        Generates an SRAM table map in HTML format.

        :return str: absolute path of the SRAM table map `.html` file.
        """
        # * create sram table file path and name
        self.sramTableHtmlFileName = os.path.basename(self.tcamTableXlsxFileName.replace("tcam", "sram").replace(".xlsx", ".html"))
        self.sramTableHtmlFilePath = os.path.join(self.sramTableDir, self.sramTableHtmlFileName)
        # * create html file in dir sramTables
        self._sramTable.to_html(self.sramTableHtmlFilePath, index=True, header=True, justify="center", classes="table table-stripped")
        logging.info("Created SRAM table HTML file: %s", self.sramTableHtmlFilePath)
        print("Created SRAM table HTML file: %s", self.sramTableHtmlFilePath)
        return self.sramTableHtmlFilePath

    def writeSRAMtoJson(self):
        """
        Generates an SRAM table map in JSON format.

        :return str: absolute path of the SRAM table map `.json` file.
        """
        # * create sram table file path and name
        self.sramTableJsonFileName = os.path.basename(self.tcamTableXlsxFileName.replace("tcam", "sram").replace(".xlsx", ".json"))
        self.sramTableJsonFilePath = os.path.join(self.sramTableDir, self.sramTableJsonFileName)
        # * create json file in dir sramTables
        self._sramTable.to_json(self.sramTableJsonFilePath, orient="index", indent=4)
        logging.info("Created SRAM table JSON file: %s", self.sramTableJsonFilePath)
        print("Created SRAM table JSON file: %s", self.sramTableJsonFilePath)
        return self.sramTableJsonFilePath

    def writeSRAMtoTxt(self):
        """
        Generates an SRAM table map in TXT format.

        :return str: absolute path of the SRAM table map `.txt` file.
        """
        # * create sram table file path and name
        self.sramTableTxtFileName = os.path.basename(self.tcamTableXlsxFileName.replace("tcam", "sram").replace(".xlsx", ".txt"))
        self.sramTableTxtFilePath = os.path.join(self.sramTableDir, self.sramTableTxtFileName)
        # * create txt file in dir sramTables
        myTable = tabulate(self._sramTable, headers="keys", showindex=True, disable_numparse=True, tablefmt="github")
        with open(self.sramTableTxtFilePath, "w", encoding="utf-8") as file:
            file.write(myTable)
        logging.info("Created SRAM table Txt file:  %s", self.sramTableTxtFilePath)
        print("Created SRAM table Txt file:  %s", self.sramTableTxtFilePath)
        return self.sramTableTxtFilePath


# ===========================================================================================
# ======================================== End Class ========================================
# ===========================================================================================


def printVerbose(verbose, msg):
    """
    Prints a string if verbose flag is active.

    :param int verbose: print information in verbose mode.
    :param str msg: Message to be printed in verbose mode.
    """
    if verbose:
        print(str(msg))


def printDebug(debug, msg):
    """
    Prints a string if debug flag is active.

    :param int debug: print information in debug mode.
    :param str msg: Message to be printed in debug mode.
    """
    if debug:
        print(str(msg))


def highlightCell(val):
    """
    Colors SRAM table map cells in XLSX file depending upon their value.

    :param int val: numerical value of a particular cell.
    :return str: cell background color code as a hex RBG value.
    """
    if val == 1:
        color = "#E5961A"
    elif val == 0:
        color = "#E4EA15"
    else:
        color = "#D8C05A"
    return f"background-color: {color}"
