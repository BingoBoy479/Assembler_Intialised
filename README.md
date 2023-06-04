# Assembler_Intialised
CO Project  group:B-40 institue -IIIT-D yr-2023:

Assembler:- 
The provided code reads an assembly code which is inputed in the terminal, performs various checks on the code for syntax errors and semantic correctness, and generates binary machine code as output in terminal.
 
 The program_data_mem_allocator function takes the lines of the assembly code, processes them, and separates program memory and data memory instructions. It returns dictionaries prog_mem and data_mem, which store the instructions and their corresponding memory addresses.These two functions were made by Naitik(2022308)

The linechecker function checks each line of the assembly code for syntax and semantic errors based on predefined rules. It returns an error message if any error is found.

The binary_gen function generates the binary machine code for each line of the assembly code based on the opcode dictionary and other data structures.

The code then initializes dictionaries and lists for opcode mappings, register information, and label information. It iterates over the assembly code lines, checks for syntax and semantic errors using the linechecker function, and generates binary machine code using the binary_gen function. Finally, it prints the output to the terminal.This portion of the code was made by Shivankar Srijan Singh(2022479)
