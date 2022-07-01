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
    
    # setup logging
    # logging.basicConfig(level=logging.DEBUG, filename='./logs/opentcam.log',
    #                     format='%(asctime)s | %(filename)s | %(funcName)s | %(levelname)s | %(lineno)d | %(message)s')
    
    # set arguments for class tableMapping
    parser = argparse.ArgumentParser(prog='OpenTCAM',
                                    usage='%(prog)s [options] path',
                                    description='TCAM memory generator',
                                    epilog='Happy Onboarding! Eat, Sleep, Code, Repeat')
    # list of all possible args for OpenTCAM
    parser.add_argument('-tconf','--tcamConfig',
                        type=str,default='tcamTable2',metavar='',required=True,nargs='?',help='name of specific TCAM table config')
    parser.add_argument('-d','--debug',
                        type=int,default=0,metavar='',required=False,nargs='?',help='print debugging mode')
    parser.add_argument('-v','--verbose',
                        type=int,default=0,metavar='',required=False,nargs='?',help='print verbose mode')
    myargs = parser.parse_args()
