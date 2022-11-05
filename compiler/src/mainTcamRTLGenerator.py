from tcamRtlGenerator import * 
import argparse
import os
os.system('clear')

def new_main():
    # create logs dir if it doesnt exist
    pwd=os.getcwd()
    logsDirPath = os.path.join(pwd, 'logs')
    if os.path.exists(logsDirPath) is False:
        os.makedirs('logs')
    # create rtl dir if it doesnt exist
    pwd=os.getcwd()
    logsDirPath = os.path.join(pwd, 'tcam_mem_rtl')
    if os.path.exists(logsDirPath) is False:
        os.makedirs('tcam_mem_rtl')

    # set arguments for OpenTCAM RTL Generator
    parser = argparse.ArgumentParser(prog='OpenTCAM RTL Wrapper Generator',
                                    usage='%(prog)s [options] path',
                                    description='TCAM memory wrapper generator',
                                    epilog='Python framework for generating configurable SRAM based TCAM memories')
    # list of all possible args for OpenTCAM
    parser.add_argument('-twconf','--tcamWrapConfig',
                        type=str,default='tcamMemWrapper_64x28',metavar='',required=True,nargs='?',help='name of specific TCAM mem wrapper config')
    parser.add_argument('-tunit','--timeunit',
                        type=str,default='1ns',metavar='',required=False,nargs='?',help='specify timeunit scale')
    parser.add_argument('-tprecision','--timeprecision',
                        type=str,default='100ps',metavar='',required=False,nargs='?',help='specify timeprecision scale')
    parser.add_argument('-d','--debug',
                        type=int,default=0,metavar='',required=False,nargs='?',help='print debugging mode')
    parser.add_argument('-v','--verbose',
                        type=int,default=0,metavar='',required=False,nargs='?',help='print verbose mode')
    arg = parser.parse_args()
    
    # ====================================================== code main body    
    
    # class objects
    trwg1=TcamRtlWrapperGenerator()
    
    # get project dir
    trwg1.getPrjDir(arg.verbose)
    # get tcam table config yaml file path
    trwg1.getYAMLFilePath(arg.verbose)
    # read tcam table config yaml file
    trwg1.readYAML(trwg1.tcamMemWrapperConfigsFilePath, arg.verbose)
    # print all tcam configs
    if arg.debug:
        trwg1.printYAML(arg.debug)
    if arg.tcamWrapConfig:
        # get specific tcam config from yaml file
        tempConfig = trwg1.getTCAMWrapperConfig(arg.tcamWrapConfig)
        # print specific tcam config
        print(json.dumps(tempConfig, indent=4))
    # create rtl dir for specific tcam mem wrap config
    trwg1.createWrapConfigDir(arg.tcamWrapConfig, arg.verbose)
    # create top wrapper file for specific tcam mem wrap config
    trwg1.createWrapConfigFile(arg.tcamWrapConfig)
    # generate wrapper
    trwg1.generateWrapper(arg.timeunit, arg.timeprecision)
    # print wrapper in sv
    trwg1.printWrapper()
    # copy respective RTL file in tcam config folder
    trwg1.copyRtlBlocks()



if __name__ == '__main__':
    new_main()