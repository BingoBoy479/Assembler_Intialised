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
def linechecker(line,label_dict,called,data_memory,register_list,opcode):
    b=line.split(" ")
    c=b[0]
    d=c[:-1]    
    #general ourpose checker 
    if c not in opcode:
        if d not in label_dict.keys():
            return 'Typo in command name'
        if d in label_dict.keys():
            b.pop(0)
            c=b[0]
            if c==" ":
                b=b.strip(" ")
                c=[b[0]]
                if c not in opcode:
                    return 'Typo in command name'
                #error checker for Immediate value type instructions or B Type instructions 
                if '$' in b[-1]:
                    imm=int(b[-1][1:])
                    okay=['rs','ls','mov']
                    if imm>127:
                        return 'Illegal value of immediate'
                    if c not in okay:
                        return 'Illegal use of command'
                    if b[1] == 'R7' or b[1]=='FLAGS':
                        return 'Illegal use of flag register'
                    if b[1] not in register_list:
                        return 'Typo in register name'
                #error checker for A Type instructions 
                type_A_instructions=['add','sub','mul','xor','or','and']
                if len(b)==4:
                    if c in type_A_instructions:
                        if b[1]=='R7' or b[2]=='R7' or b[3]=='R7' or b[1]=='FLAGS' or b[2]=='FLAGS' or b[3]=='FLAGS':
                            return 'Illegal use of flag register'
                        if b[1] not in register_list or b[2] not in register_list or b[3] not in register_list:
                            return 'Typo in register name'
                else:
                    return 'general syntax error'
                #special error checker for mov reg1 reg2
                if '$' not in b[-1] and c=='mov':
                    if b[1]=='R7'or b[1]=='FLAGS':
                        return 'Illegal use of flag register'
                    if b[1] not in register_list:
                        return 'Typo in register name'
                    if b[2]!='FLAGS' and b[2] not in register_list:
                        return 'Typo in register name'
                #to check for illegal labels aka error checker for E type Instructions
                jump=['jmp','jlt','jgt','je']
                if c in jump:
                    declared_label=list(label_dict.keys())
                    called_label=list(called.keys())
                    for i in called_label:
                        if i not in declared_label:
                            return 'Illegal use of label'
                #error checker for D type instructions
                var_list=list(data_memory.keys())
                fla1=['FLAGS','R7']
                if c=='ld' or c=='st':
                    if b[-1] not in var_list:
                        return 'Variable not declared'
                    if b[-1] in var_list:
                        if b[1] in fla1 and c!="st":
                            return 'Illegal use of flag register'
                        if b[1] not in register_list and b[1] not in fla1:
                            return 'Typo in register name'
                    if b[1]in fla1 and c!='st':
                        return 'Illegal use of flag refister'
                    if b[1] not in register_list and b[2] not in fla1 and b[2] not in var_list:
                        print("llll")
                        return 'Typo in register name'
                #error checker for C type instruction
                type_X_instructions=['div','not','cmp']
                if c in type_X_instructions:
                    if b[1]=='R7'or b[2]=='R7':
                        return 'Illegal use of flag register'
                    if b[1] not in register_list or b[2] not in register_list:
                        return 'Typo in register name'
                if c not in opcode:
                    return 'Typo in command name'
    #error checker for Immediate value type instructions or B Type instructions 
    if '$' in b[-1]:
        try:
            imm=int(b[-1][1:])
            okay=['rs','ls','mov']
            if imm>127:
                return 'Illegal value of immediate'
            if c not in okay:
                return 'Illegal use of command'
            if b[1] == 'R7' or b[1]=='FLAGS':
                return 'Illegal use of flag register'
            if b[1] not in register_list:
                return 'Typo in register name'
        except:
            return 'genral syntax error'
    #error checker for A Type instructions 
    type_A_instructions=['add','sub','mul','xor','or','and']
    if len(b)==4:
        if c in type_A_instructions:
            if b[1]=='R7' or b[2]=='R7' or b[3]=='R7' or b[1]=='FLAGS' or b[2]=='FLAGS' or b[3]=='FLAGS':
                return 'Illegal use of flag register'
            if b[1] not in register_list or b[2] not in register_list or b[3] not in register_list:
                return 'Typo in register name'
    else:
        return ' genral syntax error'
    #special error checker for mov reg1 reg2
    if '$' not in b[-1] and c=='mov':
        if b[1]=='R7'or b[1]=='FLAGS':
            return 'Illegal use of flag register'
        if b[1] not in register_list :
            return 'Typo in register name'
        if b[2] not in register_list and b[2]!='FLAGS':
            return 'Typo in register name'
    #to check for illegal labels aka error checker for E type Instructions
    jump=['jmp','jlt','jgt','je']
    if c in jump:
        declared_label=list(label_dict.keys())
        called_label=list(called.keys())
        for i in called_label:
            if i not in declared_label:
                return 'Illegal use of label'
    #error checker for D type instructions
    var_list=list(data_memory.keys())
    fla1=['FLAGS','R7']
    if c=='ld' or c=='st':
        if b[-1] not in var_list:
            return 'Variable not declared'
        if b[-1] in var_list:
            if b[1] in fla1 and c!="st":
                return 'Illegal use of flag register'
            if b[1] not in register_list and b[1] not in fla1:
                return 'Typo in register name'
        if b[1]in fla1 and c!='st':
            return 'Illegal use of flag refister'
        if b[1] not in register_list and b[2] not in fla1 and b[2] not in var_list:
            print("llll")
            return 'Typo in register name'
    #error checker for C type instruction
    type_X_instructions=['div','not','cmp']
    if c in type_X_instructions:
        if b[1]=='R7'or b[2]=='R7':
            return 'Illegal use of flag register'
        if b[1] not in register_list or b[2] not in register_list:
            return 'Typo in register name'

def binary_gen(line,dec_dict,data_memory,reg_dict,opco_dict):
    b=line.split(" ")
    d=b[0][:-1]
    c=b[0]
    if d in dec_dict.keys():
        b.pop(0)
        c=b[0]
        if c=='mov':
            if '$' in b[-1]:
                imm=int(b[-1][1:])
                return opco_dict['mov']+'0'+reg_dict[b[1]][0]+format(imm,'07b')
            else:
                return opco_dict['mov1']+'00000'+reg_dict[b[1]][0]+reg_dict[b[2]][0]
        Type_A=['add','sub','mul','xor','and','or']
        if c in Type_A:
            return opco_dict[c]+'00'+reg_dict[b[1]][0]+reg_dict[b[2]][0]+reg_dict[b[3]][0]
        Type_B=['rs','ls']
        if c in Type_B:
            imm=int(b[-1][1:])
            return opco_dict[c]+"0"+reg_dict[b[1]][0]+format(imm,'07b')
        Type_C=['div','not','cmp']
        if c in Type_C:
            return opco_dict[c]+'00000'+reg_dict[b[1]][0]+reg_dict[b[2]][0]
        Type_D=['ld','st']
        if c in Type_D:
            return opco_dict[c]+'0'+reg_dict[b[1]][0]+data_memory[b[2]][0]
        Type_E=['jmp','jlt','jgt','je']
        if c in Type_E:
            return opco_dict[c]+'0000'+dec_dict[b[1]][0]      
    if c=='mov':
        if '$' in b[-1]:
            imm=int(b[-1][1:])
            return opco_dict['mov']+'0'+reg_dict[b[1]][0]+format(imm,'07b')
        else:
            return opco_dict['mov1']+'00000'+reg_dict[b[1]][0]+reg_dict[b[2]][0]
    Type_A=['add','sub','mul','xor','and','or']
    if c in Type_A:
        return opco_dict[c]+'00'+reg_dict[b[1]][0]+reg_dict[b[2]][0]+reg_dict[b[3]][0]
    Type_B=['rs','ls']
    if c in Type_B:
        imm=int(b[-1][1:])
        return opco_dict[c]+"0"+reg_dict[b[1]][0]+format(imm,'07b')
    Type_C=['div','not','cmp']
    if c in Type_C:
        return opco_dict[c]+'00000'+reg_dict[b[1]][0]+reg_dict[b[2]][0]
    Type_D=['ld','st']
    if c in Type_D:
        return opco_dict[c]+'0'+reg_dict[b[1]][0]+data_memory[b[2]][0]
    Type_E=['jmp','jlt','jgt','je']
    if c in Type_E:
        return opco_dict[c]+'0000'+dec_dict[b[1]][0]
    Type_F=['hlt']
    if c in Type_F:
        return opco_dict[c]+format(0,'011b')
lines=file_reader("assembly_code(1).txt")    
programme_memory,data_memory = program_data_mem_allocator(lines)
declared_label_dict = {}
for (i, j) in programme_memory.items():
    if ":" in j:
        a=j.split(" ")
        Label =a[0][:-1]
        j=" ".join(a[1:])
        declared_label_dict[Label] = [i, j]
called_label_list={}
for i,j in programme_memory.items():
    a=j.split(" ")
    jump=['jmp','jlt','jgt','je']
    if a[0] in jump:
        called_label_list[a[-1]]=i
register_dict={'R0':['000',0],'R1':['001',0],'R2':['010',0],'R3':['011',0],'R4':['100',0],'R5':['101',0],'R6':['110',0],'R7':['111',format(0,'016b')],'FLAGS':['111',format(0,'016b')]}
register_useable=['R0','R1','R2','R3','R4','R5','R6']
opcode_list=['add','sub','mov','mov1','ld','st','mul','div','rs','ls','xor','or','and','not','cmp','jmp','jlt','jgt','je','hlt']
opcode_dict={}
for i in range(len(opcode_list)-4):
    opcode_dict[opcode_list[i]]=format(i,"05b")
opcode_dict['jlt']='11100'
opcode_dict['jgt']='11101'
opcode_dict['je']='11111'
opcode_dict['hlt']='11010'
error=[]
#only checker outside line checker is the hlt checker
key=list(programme_memory.keys())
val=list(programme_memory.values())
last=programme_memory[key[-1]]
hlt_co=0
for j in val:    
    if 'hlt' in j:
        hlt_co=hlt_co+1
if hlt_co==0:
    error.append("hlt missing")
elif hlt_co>1:
    error.append("Genral Syntax error(Too many hlt's)")
elif hlt_co==1:
    if 'hlt' not in last:
        error.append("hlt not last element")    
#hlt checker ends here        
for i,j in programme_memory.items():
    if linechecker(programme_memory[i],declared_label_dict,called_label_list,data_memory,register_useable,opcode_list)!=None:
        error.append(i+":"+linechecker(programme_memory[i],declared_label_dict,called_label_list,data_memory,register_useable,opcode_list))
if len(error)!=0:
    error=set(error)
    with open("assembler_output.txt","w")as f:
        error=list(error)
        for i in range(len(error)):    
            f.write(error[i])
            f.write("\n")
    flag=""
else:
    #flag to check if everything is correct
    flag="Friday hai"
if flag=='Friday hai':
    #output writer
    with open("assembler_output.txt","w")as f:
        for j in programme_memory.values():
            f.write(binary_gen(j,declared_label_dict,data_memory,register_dict,opcode_dict))
            f.write("\n")
