<div align="center">
    <img src="./images/opentcam_logo.jpg">
    <!-- <img src="./images/opentcam_logo.svg"> -->
</div>

<!-- insert badges here -->
<!-- python -->
<!-- license -->
<!-- commits -->
<!-- PRs -->
<!-- forks -->

# OpenTCAM
An open-source Ternary Content Addressable Memory (TCAM) compiler.

## What is OpenTCAM?
<!-- introduction -->
OpenTCAM is an open source Python framework that can be used to create the design (RTL) and layouts (GDS-II) of a customizable SRAM-based TCAM memory to use in FPGA and ASIC designs respectively. 

Currently the compilers are using SRAMs generated from OpenRAM Compiler, but the idea is to make a generalized compiler for any SRAM-based TCAM. The idea is to utilize 36KB BRAM blocks of FPGAs and OpenRAM generated 1Kb SRAM blocks (using sky130 nm PDKs) for ASIC to mimic any size of TCAM.

## Documentation
<!-- links to documentation and FAQ -->
<!-- We have created a detailed presentation that serves as our documentation (for now). Take a look at it [here](). -->
Currently in the making. For now refer to this README.

## How to Install
The OpenTCAM compiler requires [Python3](https://www.python.org/downloads/), [Pip3](https://pypi.org/) and [MAKE](https://www.gnu.org/software/make/) inorder to run properly:

### Linux/Debian (Ubuntu)
-   Install all pre-requisites softwares using the following commands:
    ```bash
    sudo apt install -y git make python3 python3-pip python3-venv
	sudo python3 -m pip install --user virtualenv 
    ```
-   If MAKE is already pre installed simply run the command:
    ```bash
    make install_dependencies
    ```

<!-- ### MacOS
-   Make sure you have [Homebrew](https://brew.sh/) installed.
-   Install using the following command:
    ```bash
    brew install python3
    ``` -->

## How to Use
### 1.  Basic Setup
<!-- explain how to create virtual environments -->
- To setup and build the python virtual environment required for running the compiler simply run the following command in the project directory. It will automatically setup and install all the required pip packages.
    ```bash
    make opentcam_venv
    ```

### 2.  Virtual Environment Basics
<!-- explain how to use virtual environments -->
**NOTE:** All commands mentioned below require the use virtual environment created in the previous step. The virtual environment needs to be activated everytime before use and deactivated when done.
1.  Activate virtual environment: 
    ```bash
    source .pyVenvOpenTcam/bin/activate
    ```
2.  Deactivate virtual environment:
    ```bash
    deactivate
    ```
To learn more about what are python virtual environments and how they work click [here](https://realpython.com/python-virtual-environments-a-primer/).

### 3.  Generating TCAM Memories
<!-- explain how to run and simulate the opentcam code -->
-   Generate TCAM -> SRAM table map:
    ```bash
	make tablemap \
	TCAMCONFIG=tcamTableX \ # tcam table config name here X=1,2,..
    EXCEL=1/0 \             # generate SRAM table map as excel file
    HTML=1/0 \              # generate SRAM table map as html file
    JSON=1/0 \              # generate SRAM table map as json file
    TXT=1/0 \               # generate SRAM table map as text file
    DEBUG=1/0 \             # debugging on/off
    VERBOSE=1/0             # verbosity on/off    
	```

### 4.  Unit Tests
<!-- explain how to run and simulate the opentcam tests -->
Unit tests are an important part of regression testing to ensure that the code still functions as expected after making changes to the code and helps ensure code stability.

Use the following commands:
-   Run a specific test:
    ```bash
    make rununittest MARKER=test_name
    ```
-   Run all tests of a specific test class:
    ```bash
    make rununittest MARKER=test_class_name
    ```
-   Run all regression tests:
    ```bash
    make runregression
    ```
-   Display all test markers:
    ```bash
    make testmarkers
    ```

### 5.  Code Coverage
<!-- explain how to run and simulate code coverage -->
Used to gauge the effectiveness of tests. It can show which parts of your code are being exercised by tests, and which are not.
-   To generate code coverage simply run the command:
    ```bash
    make coverage
    ```
A report will be created in the folder `coverage_html`. Simply open the file `coverage_html/index.html` in the web browser of your choice to view a detailed coverage report.

### 6.  CleanUp
-   Clean all files including tables, bins, logs generated:
    ```bash
    make cleanall
    ```
-   Clean everything including virtual environment/s. Make sure to deactivate any or all virtual environment/s.
    ```bash
    make deepclean
    ```

## Get Involved
-   Report bugs by submitting [GitHub Issues](https://github.com/merledu/OpenTcam/issues).
-   Develop new features (see [how to contribute](https://github.com/merledu/OpenTcam/master/CONTRIBUTING.md)).
-   Submit code/fixes using a [Github Pull Request](https://github.com/merledu/OpenTcam/pulls).

## License
-   OpenTCAM is licensed under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Contributors & Acknowledgements
<!-- -   [Dr. Ali Ahmed](https://github.com/aliahmedphd) is the -->
<!-- -   [Usman Siddique](https://github.com/usman1515) is the  -->
<!-- -   [Sajjad Ahmed](https://github.com/sajjadahmed677) is the -->

<!-- If I forgot to add you, please let me know! -->