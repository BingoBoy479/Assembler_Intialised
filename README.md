# Assembler_Intialised
CO Project  group:B-40 institue -IIIT-D yr-2023:
The provided code seems to be an implementation of an assembler for a specific architecture or instruction set. It reads an assembly code file, performs various checks on the code for syntax errors and semantic correctness, and generates binary machine code as output.

The file_reader function reads the contents of a file and returns them as a list of lines.

The program_data_mem_allocator function takes the lines of the assembly code, processes them, and separates program memory and data memory instructions. It returns dictionaries prog_mem and data_mem, which store the instructions and their corresponding memory addresses.

The linechecker function checks each line of the assembly code for syntax and semantic errors based on predefined rules. It returns an error message if any error is found.

The binary_gen function generates the binary machine code for each line of the assembly code based on the opcode dictionary and other data structures.

The code then initializes dictionaries and lists for opcode mappings, register information, and label information. It iterates over the assembly code lines, checks for syntax and semantic errors using the linechecker function, and generates binary machine code using the binary_gen function. Finally, it writes the output to a file named "assembler_output.txt".

If there are any errors, they are written to the output file. Otherwise, the binary machine code is written to the output file.
