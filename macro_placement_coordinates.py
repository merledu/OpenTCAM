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

def macro_placement_cfg(sram_instance_names, tcam_instance_names):
    x, y = 100, 100
    dir = ['N', 'S', 'E', 'W']
    dir_index = 0
    for tcam_instance in tcam_instance_names:
        for sram_instance in sram_instance_names:
            print(f'{tcam_instance}.{sram_instance} {x} {y} {dir[dir_index]}')
            x = x + 400
            y = y + 500
            dir_index = (dir_index+1)%4

# Define the file path and module name
file_path = 'tcam_mem_rtl/tcamMemWrapper_64x28/top_tcam_64x28.sv'
search_module1 = 'sky130_sram_1kbyte_1rw1r_32x256_8'
search_module2 = 'tcam_32x28'

# Call the function and print the result
module_line1 = find_sram_module_line(file_path, search_module1)
print(module_line1)
module_line2 = find_tcam_module_line(file_path, search_module2)
print(module_line2)
sram_instance_names = sram_instance_name(module_line1)
print(sram_instance_names)
tcam_instance_names = tcam_instance_name(module_line2)
print(tcam_instance_names)
total_sram_instances = len(sram_instance_names)*len(tcam_instance_names)
print(total_sram_instances)
macro_placement_cfg(sram_instance_names, tcam_instance_names)