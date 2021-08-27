import sys
import matplotlib.pyplot as plt
import numpy as np

# Dividing the instructions into various types
type_A = {'00000', '00001', '00110', '01010', '01011', '01100'}

type_B = {'01000', '01001', '00010'}

type_C = {'00111', '01101', '01110', '00011'}

type_D = {'00100', '00101'}

type_E = {'01111', '10000', '10001', '10010'}

type_F = {'10011'}


reg_dic = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 'FLAGS': 0}
# FLAGS: E = 1, G = 2, L = 4, V = 8

Mem_dic = {}

f = open("code.txt")

counter = 0

def registerOutput(pc):
    print('{0:08b}'.format(pc), end = " ")
    for line in (reg_dic.keys()):
        print(format(reg_dic[line], '016b'), end = " ")
    print()
    cycle_list.append(cycle)
    mem_list.append(pc);

def flagReset():
    reg_dic['FLAGS'] = 0

for line in sys.stdin:
# for line in f:
    if line[0:5] == '10011':
        Mem_dic[counter] = line
    else:
        Mem_dic[counter] = line[0:-1]
    counter += 1

programCounter = 0

# cycle is for the bonus q
cycle = 0
cycle_list = []
mem_list = []

while programCounter < len(Mem_dic.keys()):

    line = Mem_dic[programCounter]

    opcode = line[0:5]

    #check for type_a
    if opcode in type_A:
        r1 = int(line[7:10], 2)

        r2 = int(line[10:13], 2)

        r3 = int(line[13:16], 2)

        #add
        if(opcode == '00000'):
            reg_dic[r1] = reg_dic[r2] + reg_dic[r3]
            #Overflow for addition
            if reg_dic[r1] > 65535:
                reg_dic[r1] = reg_dic[r1] % (256*256)
                reg_dic['FLAGS'] = 8
            else:
                flagReset()
        #subtract
        elif(opcode == '00001'):
            reg_dic[r1] = reg_dic[r2] - reg_dic[r3]

            #Overflow for subtraction
            if reg_dic[r1] < 0:
                reg_dic[r1] = reg_dic[r1] % (256*256)
                reg_dic['FLAGS'] = 8
            else:
                flagReset()
        #multiply
        elif(opcode == '00110'):
            reg_dic[r1] = reg_dic[r2] * reg_dic[r3]

            #Overflow for Multiplication
            if reg_dic[r1] > 65535:
                reg_dic[r1] = reg_dic[r1] % (256*256)
                reg_dic['FLAGS'] = 8
            else:
                flagReset()
            
        #bitwise XOR
        elif(opcode == '01010'):
            reg_dic[r1] = reg_dic[r2] ^ reg_dic[r3]
            flagReset()

        #bitwise OR
        elif(opcode == '01011'):
            reg_dic[r1] = reg_dic[r2] | reg_dic[r3]
            flagReset()

        #bitwise AND
        elif(opcode == '01100'):
            reg_dic[r1] = reg_dic[r2] & reg_dic[r3]
            flagReset()

        registerOutput(programCounter)

    #check for Type_B
    elif opcode in type_B:
        r1 = int(line[5:8], 2)

        imm = int(line[8:16], 2)

        #right shift
        if(opcode == '01000'):
            reg_dic[r1] = reg_dic[r1] >> imm
            flagReset()

        #left shift
        elif(opcode == '01001'):
            reg_dic[r1] = (reg_dic[r1] << imm) % (256*256)
            flagReset()

        #mov_i
        elif(opcode == '00010'):
            reg_dic[r1] = imm
            flagReset()

        registerOutput(programCounter)

    #check for Type_C
    elif opcode in type_C:
        r1 = int(line[10:13], 2)

        r2 = int(line[13:16], 2)

        if(r1 == 7):
            r1 = 'FLAGS'
        if(r2 == 7):
            r2 = 'FLAGS'

        #move_r
        if(opcode == '00011'):
            reg_dic[r1] = reg_dic[r2]
            flagReset()

        #divide: r0 = quotient, r1 = remainder
        elif(opcode == '00111'):
            temp1 = reg_dic[r1] // reg_dic[r2]
            temp2 = reg_dic[r1] % reg_dic[r2]
            reg_dic[0] = temp1
            reg_dic[1] = temp2
            flagReset()

        #invert - 8 bits or 16? --> TBD
        elif(opcode == '01101'):
            print(reg_dic[r1], reg_dic[r2])
            # reg_dic[r1] = '{0:016b}'.format(~int(reg_dic[r2][8:], 2))
            reg_dic[r1] = ~(reg_dic[r2])
            flagReset()

        #compare
        elif(opcode == '01110'):
            if (reg_dic[r1] < reg_dic[r2]) :
                reg_dic['FLAGS'] = 4
            elif (reg_dic[r1] > reg_dic[r2]) :
                reg_dic['FLAGS'] = 2
            elif (reg_dic[r1] == reg_dic[r2]) :
                reg_dic['FLAGS'] = 1

        registerOutput(programCounter)

    #check for Type_D
    elif opcode in type_D:
        r1 = int(line[5:8], 2)

        mem = int(line[8:16], 2)

        if opcode == '00100':
            if mem in Mem_dic.keys():
                reg_dic[r1] = int(Mem_dic[mem],2)

            else:
                reg_dic[r1] = 0

        elif opcode == '00101':   
            Mem_dic[mem] = '0'*8 + '{0:08b}'.format(reg_dic[r1])

        cycle_list.append(cycle)
        mem_list.append(mem)

        flagReset()
        registerOutput(programCounter)

    
    #check for Type_E
    elif opcode in type_E:
        # mem = int(line[8:16], 2)
        mem = line[8:16]

        #unconditional jump
        if opcode == '01111':
            programCounter = int(mem, 2) - 1

        #jump if less than
        elif opcode == '10000':
            if reg_dic['FLAGS'] == 4:
                programCounter = int(mem, 2) - 1
        
        #jump if greater than
        elif opcode == '10001':
            if reg_dic['FLAGS'] == 2:
                programCounter = int(mem, 2) - 1
        
        #jump if equal
        elif opcode == '10010':
            if reg_dic['FLAGS'] == 1:
                programCounter = int(mem, 2) - 1

        flagReset()
        registerOutput(programCounter)

    elif opcode in type_F:
        flagReset()
        registerOutput(programCounter)
        programCounter = 1000

    programCounter += 1
    cycle += 1

lines = 0
for i in Mem_dic.values():
    lines +=1
    print(i)

for i in range(256-lines):
    print('0'*16)

#Plotting for the bonus
x = np.array(cycle_list)
y = np.array(mem_list)

plt.xlabel("Cycle number")
plt.ylabel("Memory Address")
plt.scatter(x, y, color = 'red')
plt.savefig('bonus.png')