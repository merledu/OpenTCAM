import os
import sys
import subprocess
import time

def find_sram_module_line(file_path, search_module):
    sram_lines=[]
    # Read the Verilog file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Search for the line containing the module name
    for line in lines:
        if search_module in line:
            if(line.strip()[0] != '/' and line.strip()[1] != '/'):
                sram_lines.append(line.strip())  # Append the line as a string without leading/trailing whitespace
    return sram_lines

def find_tcam_module_line(file_path, search_module):
    tcam_lines=[]
    # Read the Verilog file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Search for the line containing the module name
    for line in lines:
        if search_module in line:
            if(line.strip()[0] != '/' and line.strip()[1] != '/' and 'module' not in line):
                tcam_lines.append(line.strip())  # Append the line as a string without leading/trailing whitespace
    return tcam_lines

def sram_instance_name(sram_lines):
    sram_instance_names = []
    for line in sram_lines:
        str1 = line.split()[1]
        str1 = str1.split('(')[0]
        sram_instance_names.append(str1)  # Split the line and get the second word
    return sram_instance_names

def tcam_instance_name(tcam_lines):
    tcam_instance_names = []
    for line in tcam_lines:
        str1 = line.split()[1]
        str1 = str1.split('(')[0]
        tcam_instance_names.append(str1)  # Split the line and get the second word
    return tcam_instance_names

def macro_placement_cfg(sram_instance_names, tcam_instance_names, macro_margin, margin_index):
    sram_coordinates = []
    x, y = macro_margin[margin_index], macro_margin[margin_index]
    dir = ['N', 'S']
    dir_index = 0
    print("--------------------------------MACRO_PLACEMENT_CFG--------------------------------")
    with open('macro_placement.cfg', 'w') as file:
        for tcam_instance in tcam_instance_names:
            for sram_instance in sram_instance_names:
                sram_coordinates.append((tcam_instance, sram_instance, x, y, dir[dir_index]))
                print(f"{tcam_instance}.{sram_instance} {x} {y} {dir[dir_index]}")
                file.write(f'{tcam_instance}.{sram_instance} {x} {y} {dir[dir_index]}\n')
                y = y + 500 + macro_margin[margin_index]
                dir_index = (dir_index+1)%2
            x = x + 400 + macro_margin[margin_index]
            y = macro_margin[margin_index]
    return sram_coordinates


def area(sram_coordinates, macro_margin, margin_index):
    min_x = sram_coordinates[0][2]
    max_x = int(sram_coordinates[-1][2]) + 400
    min_y = sram_coordinates[0][3]
    max_y = int(sram_coordinates[-1][3]) + 500
    print("-----------------------------CORE_AREA-----------------------------")
    print(f'SRAM area Min x: {min_x}, Max x: {max_x}, Min y: {min_y}, Max y: {max_y}')
    print(f'Core area Min x: 0, Max x: {max_x+macro_margin[margin_index]}, Min y: 0, Max y:{max_y+macro_margin[margin_index]}')

def generate_pdn(sram_coordinates):
    print("-----------------------------FP_PDN_HOOKS-----------------------------")
    for i in range(len(sram_coordinates)):
        if(i != len(sram_coordinates)-1):
            print(f"{sram_coordinates[i][0]}.{sram_coordinates[i][1]} vccd1 vssd1,",end='')
        else:
            print(f"{sram_coordinates[i][0]}.{sram_coordinates[i][1]} vccd1 vssd1")

def wait_for_file(file_path):
    while not os.path.exists(file_path):
        time.sleep(1)  # Check every second

def capture_flow_output(command):
    arr = []
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    for line in process.stdout:
        print(line.strip())  # Process each line
        arr.append(line.strip())
    process.stdout.close()
    process.wait()
    return arr

def tag(arr):
    for line in arr:
        if('RUN' in line):
            index = line.find('RUN')
            return line[index:index+23]

def capture_error(arr):
    arr_e = []
    for line in arr:
        if('ERROR' in line):
            arr_e.append(line)
            return arr_e, 0
        else:
            return arr_e, 1

def error_handler(arr_e):
    return 0

# Define the file path and module name
file_path = '/home/vignesh/OpenLane/designs/designs/designs/ci/and_gate/src/top_tcam_64x28.sv'
search_module1 = 'sky130_sram_1kbyte_1rw1r_32x256_8'
search_module2 = 'tcam_32x28'
command = '../../../../../flow.tcl -interactive -file script1'

# Call the function and print the result
module_line1 = find_sram_module_line(file_path, search_module1)
# print(module_line1)
module_line2 = find_tcam_module_line(file_path, search_module2)
# print(module_line2)
sram_instance_names = sram_instance_name(module_line1)
# print(sram_instance_names)
tcam_instance_names = tcam_instance_name(module_line2)
# print(tcam_instance_names)
total_sram_instances = len(sram_instance_names)*len(tcam_instance_names)
print(total_sram_instances)
macro_margin = [50, 150, 250, 300]
margin_index = 0
x = 1
while(not x or margin_index != 2):
    sram_coordinates = macro_placement_cfg(sram_instance_names, tcam_instance_names, macro_margin, margin_index)
    # print(sram_coordinates)
    area(sram_coordinates, macro_margin, margin_index)
    generate_pdn(sram_coordinates)
    arr = capture_flow_output(command)
    print(tag(arr))
    arr_e, x = capture_error(arr)
    error_handler(arr_e)
    margin_index = margin_index + 1
