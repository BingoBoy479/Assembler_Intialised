Assmenler_output=[]
testline="."
while True:
    try:
        testline=input()
        Assmenler_output.append(testline)
    except EOFError:
        break
# while(testline!=""):
#         testline=input()
#         Assmenler_output.append(testline)
for i in range(len(Assmenler_output)):
    if Assmenler_output[i]=='':
        Assmenler_output.pop(i)
register_access={'000': 0, '001': 0, '010': 0, '011': 0, '100': 0, '101': 0, '110': 0, '111': '0000000000000000'}
data={}
varaddress=[]
for a in range(len(Assmenler_output)):
    g=list(format(a,'08b'))
    g.pop(0)
    li=''
    for i in g:
        li=li+i
    data[li]=Assmenler_output[a]
    a=a-1
for i in Assmenler_output:
    a=i[0:5]
    if a=='00101' or a=='00100':
        data[i[9:16]]=0
        varaddress.append(i[9:16])
en=len(data)+len(Assmenler_output)-1
while en<128:
    g=list(format(en,'08b'))
    g.pop(0)
    li=''
    for i in g:
        li=li+i
    if li!='0000000':    
        data[li]=format(0,'017b')[1:]
    en=en+1
program_mem={}
for i in range(len(Assmenler_output)):
    program_mem[i]=Assmenler_output[i]
pc=0
TypeA=['00000','00001','00110','01010','01011','01100']
TypeB=['00010','01000','01001']
TypeC=['00011','00111','01101','01110']
TypeD=['00100','00101']
TypeE=['01111','11100','11101','11111']
#Type A instructions
def add(a,b,c,reg_dict):
    reg_dict[a]=reg_dict[b]+reg_dict[c]
    if reg_dict[a]>65535:
        bo=reg_dict['111']
        bo=list(bo)
        bo[-4]='1'
        reg_dict['111']=''
        for i in bo:
            reg_dict['111']=reg_dict['111']+i
        reg_dict[a]=0
    else:
        reg_dict['111']=reg_dict['111'][:12]+'0000'
def sub(a,b,c,reg_dict):
    reg_dict[a]=reg_dict[b]-reg_dict[c]
    if reg_dict[a]<0:
        bo=reg_dict['111']
        bo=list(bo)
        bo[-4]='1'
        reg_dict['111']=''
        for i in bo:
            reg_dict['111']=reg_dict['111']+i
        reg_dict[a]=0
    else:
        reg_dict['111']=reg_dict['111'][:12]+'0000'
def mul(a,b,c,reg_dict):
    reg_dict[a]=reg_dict[b]*reg_dict[c]
    if reg_dict[a]>65535:
        bo=reg_dict['111']
        bo=list(bo)
        bo[-4]='1'
        reg_dict['111']=''
        for i in bo:
            reg_dict['111']=reg_dict['111']+i
        reg_dict[a]=0
    else:
        reg_dict['111']=reg_dict['111'][:12]+'0000'
def xor(a,b,c,reg_dict):
    reg_dict[a]=reg_dict[b]^reg_dict[c]
def Or(a,b,c,reg_dict):
    reg_dict[a]=reg_dict[b]|reg_dict[c]
def And(a,b,c,reg_dict):
    reg_dict[a]=reg_dict[b]&reg_dict[c]
#type B instructions
def movi(a,b,reg_dict):
    reg_dict[a]=int(b,2)
def rs(a,b,reg_dict):
    i=format(reg_dict[a],'017b')
    i=i[1:]
    l=(-1)*(int(b,2))
    i=i[:l]
    while len(i)!=16:
        i='0'+i
    reg_dict[a]=int(i,2)
def ls(a,b,reg_dict):
    i=format(reg_dict[a],'017b')
    i=i[1:]
    l=(int(b,2))
    i=i[l:]
    while len(i)!=16:
        i=i+'0'
    reg_dict[a]=int(i,2)
#Type C instructions
def mov(a,b,reg_dict):
    if isinstance(reg_dict[b],int):
        reg_dict[a]=reg_dict[b]
    else:
        reg_dict[a]=int(reg_dict[b],2)
        if b=='111':
            reg_dict[b]=reg_dict[b][:12]+'0000'
def div(a,b,reg_dict):
    if reg_dict[b]!=0:
        reg_dict['000']=reg_dict[a]//reg_dict[b]
        reg_dict['001']=reg_dict[a]%reg_dict[b]
    else:
        bo=reg_dict['111']
        bo=list(bo)
        bo[-4]='1'
        reg_dict['111']=''
        for i in bo:
            reg_dict['111']=reg_dict['111']+i
        reg_dict['000'],reg_dict['001']=0
def Not(a,b,reg_dict):
    li=list(format(reg_dict[b],'017b')[1:])
    for i in range(len(li)):
        if li[i]=='0':
            li[i]='1'
        else:
            li[i]='0'
    ou=''
    for i in range(len(li)):
        ou=ou+li[i]
    reg_dict[a]=int(ou,2)
def Cmp(a,b,reg_dict):
    if int(reg_dict[a])<int(reg_dict[b]):
        bo=reg_dict['111']
        bo=list(bo)
        bo[-3]='1'
        reg_dict['111']=''
        for i in bo:
            reg_dict['111']=reg_dict['111']+i
    if reg_dict[a]==reg_dict[b]:
        bo=reg_dict['111']
        bo=list(bo)
        bo[-1]='1'
        reg_dict['111']=''
        for i in bo:
            reg_dict['111']=reg_dict['111']+i
    else:
        bo=reg_dict['111']
        bo=list(bo)
        bo[-2]='1'
        reg_dict['111']=''
        for i in bo:
            reg_dict['111']=reg_dict['111']+i
#Type D instruction
def st(a,b,reg_dict,data):
    if reg_dict[a] is int:
        data[b]=format(reg_dict[a],'017b')[1:]
    else:
        data[b]=format(reg_dict[a],'017b')[1:]
def ld(a,b,reg_dict,data):
    if type(data[b]) == int:
        reg_dict[a]=data[b]
    else:
        print(type(data[b]))
        reg_dict[a]=int(data[b],2)
#Type E instructions
def jmp(a,plc,reg_dict):
    plc=int(a,2)
    boi=reg_dict['111']
    return plc
def jlt(a,plc,reg_dict):
    if reg_dict['111'][-3]=='1':
        plc=int(a,2)
        return plc
    else:
        return plc+1
def jgt(a,plc,reg_dict):
    if reg_dict['111'][-2]=='1':
        plc=int(a,2)
        return plc
    else:
        return plc+1
def je(a,plc,reg_dict):
    if reg_dict['111'][-1]=='1':
        plc=int(a,2)
        return plc
    else:
        return plc+1
opcode_function={'00000': add, '00001': sub, '00010': movi, '00011': mov, '00100': ld, '00101': st, '00110': mul, '00111': div, '01000': rs, '01001': ls, '01010': xor, '01011': Or, '01100': And, '01101': Not, '01110': Cmp, '01111': jmp, '11100': jlt, '11101': jgt, '11111': je}
while program_mem[pc][:5]!='11010':
    if program_mem[pc][:5] in TypeA:
        print(format(pc,'08b')[1:],end=' ')
        print('      ',end=' ')
        a=program_mem[pc][7:10]
        b=program_mem[pc][10:13]
        c=program_mem[pc][13:16]
        opcode_function[program_mem[pc][:5]](a,b,c,register_access)
        for i in register_access.keys():
            if i!='111':
                print(format(register_access[i],'017b')[1:],end=' ')
            else:
                print(register_access['111'])
                register_access['111']=register_access['111'][:12]+'0000'
        pc+=1
    if program_mem[pc][:5] in TypeB:
        print(format(pc,'08b')[1:],end=' ')
        print('      ',end=' ')
        a=program_mem[pc][6:9]
        b=program_mem[pc][9:16]
        opcode_function[program_mem[pc][:5]](a,b,register_access)
        for i in register_access.keys():
            if i!='111':
                print(format(register_access[i],'017b')[1:],end=' ')
            else:
                register_access['111']=register_access['111'][:12]+'0000'
                print(register_access['111'])
        pc+=1
    if program_mem[pc][:5] in TypeC:
        print(format(pc,'08b')[1:],end=' ')
        print('      ',end=' ')
        a=program_mem[pc][10:13]
        b=program_mem[pc][13:16]
        opcode_function[program_mem[pc][:5]](a,b,register_access)
        for i in register_access.keys():
            if i!='111':
                print(format(register_access[i],'017b')[1:],end=' ')
            else:
                print(register_access['111'])
                if program_mem[pc][:5]!='01110':
                    register_access['111']=register_access['111'][:12]+'0000'

        pc+=1
    if program_mem[pc][:5] in TypeD:
        print(format(pc,'08b')[1:],end=' ')
        print('      ',end=' ')
        a=program_mem[pc][6:9]
        b=program_mem[pc][9:16]
        opcode_function[program_mem[pc][:5]](a,b,register_access,data)
        for i in register_access.keys():
            if i!='111':
                print(format(register_access[i],'017b')[1:],end=' ')
            else:
                register_access['111']=register_access['111'][:12]+'0000'
                print(register_access['111'])
        pc+=1
    if program_mem[pc][:5] in TypeE:
        print(format(pc,'08b')[1:],end=' ')
        print('      ',end=' ')
        a=program_mem[pc][9:16]
        pc=opcode_function[program_mem[pc][:5]](a,pc,register_access)
        for i in register_access.keys():
            if i!='111':
                print(format(register_access[i],'017b')[1:],end=' ')
            else:
                register_access['111']=register_access['111'][:12]+'0000'
                print(register_access['111'])

print(format(pc,'08b')[1:],end=' ')
print('      ',end=' ')
for i in register_access.keys():
    if i!='111':
        print(format(register_access[i],'017b')[1:],end=' ')
    else:
        register_access['111']=register_access['111'][:12]+'0000'
        print(register_access['111'])
for i in varaddress:
    if type(data[i])==int:
        data[i]=format(data[i],'017b')[1:]
    else:
        data[i]=data[i]
co=0
for i in data.keys():
    print(data[i])
    co+=1
if co!=128:
    pl=128-co
    for i in range(0,pl):
        print('0000000000000000')