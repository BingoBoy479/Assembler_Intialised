def file_reader(file_name):
    with open(file_name, 'r') as file:
        content = file.readlines()
    return content
def program_data_mem_allocator(lines):
    prog_mem = {}
    data_mem = {}
    variables = []
    var_values = []  
    line_count = 0
    for line in lines:
        line = line.strip()
        if '\t' in line:
            line = line.replace('\t', ' ')
        if line == "":
            continue
        if line and line.startswith('var'):
            parts = line.split(' ')
            var_name = parts[1]
            var_value = int(parts[2]) if len(parts) > 2 else 0

            variables.append(var_name)
            var_values.append(var_value)  
        else:
            prog_mem[format(line_count, '08b')[-7:]] = line
            line_count += 1
    a = len(list(prog_mem.keys()))  
    for i in range(len(variables)):
        data_mem[variables[i]] = [format(a + i, '08b')[-7:], var_values[i]]  
    return prog_mem, data_mem