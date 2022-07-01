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
OpenTCAM is an open source Python framework that can be used to create the design and layouts of a customizable TCAM memory to use in FPGA and ASIC designs. 
<!-- OpenTCAM supports integration in both commercial and open-source flows with both predictive and fabricable technologies. -->

## Documentation
<!-- links to documentation and FAQ -->
We have created a detailed presentation that serves as our documentation (for now). Take a look at it [here]().

## How to Install
The OpenTCAM compiler requires Python3 and Pip3 inorder to work:

### Linux/Debian (Ubuntu)
-   Install using the following command:
    ```bash
    sudo apt install python3 python3-pip python3-venv
    ```

### MacOS
-   Make sure you have [Homebrew](https://brew.sh/) installed.
-   Install using the following command:
    ```zsh
    brew install python3
    ```

### Basic Setup
- To setup and build the python virtual environment required for running the compiler simply run the following command in the project directory. It will automatically setup and install all the required pip packages.
    ```bash
    make setupvenv
    ```
-   To learn more about what are python virtual environments and how they work click [here](https://realpython.com/python-virtual-environments-a-primer/).

## Basic Usage
<!-- explain how to run and simulate the opentcam code -->
-   Activate virtual environment: `source .pyVenvOpenTcam/bin/activate`
-   Generate TCAM -> SRAM table map:
    ```bash
	make runopentcam \
	TCAMCONFIG=tcamTableX \     # tcam table config name here X=1,2,..
	DEBUG=1/0 \                 # debugging on/off
	VERBOSE=1/0 \               # verbosity on/off
    ```


-   Deactivate virtual environment: `deactivate`

## Unit Tests
<!-- explain how to run and simulate the opentcam tests -->
Regression testing performs a number of tests for all modules in OpenTCAM. From the unit test directory (`$OpenTCAM/compiler/tests`), use the following command:
-   Run all regression tests:
    ```bash
    ```
-   Run a specific test:
    ```bash
    ```
-   To set the verbosity add the `-v` flag:
    ```bash
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