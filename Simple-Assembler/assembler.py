import sys

f = open('code.txt')

# Dividing the instructions into various types
type_A = {'add': '00000', 'sub': '00001', 'mul': '00110', 'xor': '01010', 'or': '01011', 'and': '01100'}

type_B = {'rs': '01000', 'ls':'01001', 'mov_i': '00010'}

type_C = {'div':'00111', 'not': '01101', 'cmp':'01110', 'mov_r': '00011'}

type_D = {'ld': '00100', 'st':'00101'}

type_E = {'jmp':'01111', 'jlt': '10000', 'jgt': '10001', 'je': '10010'}

type_F = {'hlt': '10011'}

#{var_name : [address(binary), value]}
var_dic = {}

#{label_name : address(decimal))}
labels = {}

#In order: code -> hlt
#{address(decimal) : entire instruction(string)}
#for labels, the label name is not included
line_dic = {}

reg_dic = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 'FLAGS': 0}

def reset():
	reg_dic['FLAGS'] = 0

def pre_parse():
	var_temp = []
	
	address = 0
	for line in f:
		if line == "\n":
			continue
		words = line.split()

		if words[0] == "var":

			if words[1] in var_temp:
				print("Syntax Error: 2 or more variables cannot have the same name.")
				quit()

			elif words[1] in labels.keys():
				print("Syntax Error: Variables and labels can't have the same name.")
				quit()

			else:
				var_temp.append(words[1])

		elif words[0][-1] == ":":
			
			if words[0][:-1] in var_temp:
				print("Syntax Error: Variables and labels can't have the same name.")
				quit()

			elif words[0][:-1] in labels.keys():
				print("Syntax Error: 2 or more variables cannot have the same name.")
				quit()

			else:
				labels[words[0][:-1]] = address
				if(line[-1] == "\n"):
					line_dic[address] = line[len(words[0])+1:-1]
				else:
					line_dic[address] = line[len(words[0])+1:]
			address += 1

		else:
			if(line[-1] == "\n"):
				line_dic[address] = line[:-1]
			else:
				line_dic[address] = line
			
			address +=1

	for v in var_temp:
		var_dic[v] = [address, 0]
		address += 1

	if(address>257):
		print("Error: Number of instructions exceed 256")
		quit()


#add overflows flag for add and subtract
def parse_A(instruction, words):
	opcode = type_A[instruction]

	if((words[1][0] == 'R' and words[2][0] == 'R' and words[3][0] == 'R') == 0):
		print('Invalid syntax: Type A instruction cannot be interpreted in this way')
		quit()

	r1 = int(words[1][1])
	bin_r1 = '{0:03b}'.format(r1)

	r2 = int(words[2][1])
	bin_r2 = '{0:03b}'.format(r2)

	r3 = int(words[3][1])
	bin_r3 = '{0:03b}'.format(r3)

	code = opcode + '00' + bin_r1 + bin_r2 + bin_r3
	#add
	if(opcode == '00000'):
		reg_dic[r1] = reg_dic[r2] + reg_dic[r3]
	
	#subtract
	elif(opcode == '00001'):
		reg_dic[r1] = reg_dic[r2] + reg_dic[r3]
		
	#multiply
	elif(opcode == '00110'):
		reg_dic[r1] = reg_dic[r2] + reg_dic[r3]
    	
	#bitwise XOR
	elif(opcode == '01010'):
		reg_dic[r1] = reg_dic[r2] + reg_dic[r3]

	#bitwise OR
	elif(opcode == '01011'):
		reg_dic[r1] = reg_dic[r2] + reg_dic[r3]

	#bitwise AND
	elif(opcode == '01100'):
		reg_dic[r1] = reg_dic[r2] + reg_dic[r3]

	print(code)
	
#done
def parse_B(instruction, words):
	opcode = type_B[instruction]

	if((words[1][0] == 'R' and words[1][1].isdecimal() and words[2][0] == '$' and words[2][1:].isdecimal()) == 0):
		print('Invalid syntax: Type B instruction cannot be interpreted in this way')
		quit()

	r1 = int(words[1][1])
	bin_r1 = '{0:03b}'.format(r1)

	imm = int(words[2][1:])
	bin_imm = '{0:08b}'.format(imm)

	code = opcode + bin_r1 + bin_imm

	#right shift
	if(opcode == '01000'):
		reg_dic[r1] = reg_dic[r1] >> imm
	#left shift
	elif(opcode == '01001'):
		reg_dic[r1] = reg_dic[r1] << imm
	#mov_i
	elif(opcode == '00010'):
		reg_dic[r1] = imm
	print(code)

#divide,compare done; invert tbd
def parse_C(instruction, words):
	opcode = type_C[instruction]

	if((words[1][0] == 'R' and words[1][1].isdecimal() and words[2][0] == 'R' and words[2][1].isdecimal()) == 0):
		print('Invalid syntax: Type B instruction cannot be interpreted in this way')
		quit()

	r1 = int(words[1][1])
	bin_r1 = '{0:03b}'.format(r1)

	r2 = int(words[2][1])
	bin_r2 = '{0:03b}'.format(r2)

	code = opcode + '00000' + bin_r1 + bin_r2

	#move_r
	if(opcode == '00011'):
		reg_dic[r1] = reg_dic[r2]
	#divide: r0 = quotient, r1 = remainder
	elif(opcode == '00111'):
		reg_dic[0] = reg_dic[r1] // reg_dic[r2]
		reg_dic[1] = reg_dic[r1] % reg_dic[r2]
	#invert - 8 bits or 16?
	elif(opcode == '01101'):
		reg_dic[r1] = '{0:016b}'.format(~int(reg_dic[r2][8:], 2))
	#compare
	elif(opcode == '01110'):
		if (reg_dic[r1] < reg_dic[r2]) :
			reg_dic['FLAGS'] = 4
		elif (reg_dic[r1] > reg_dic[r2]) :
			reg_dic['FLAGS'] = 2
		elif (reg_dic[r1] == reg_dic[r2]) :
			reg_dic['FLAGS'] = 1
	print(code)

#check how memory addresses are given in assembly ->  AS LABELS

def parse_D(instruction, words):
	opcode = type_D[instruction]

	if((words[1][0] == 'R' and words[1][1].isdecimal() and words[2] in var_dic.keys()) == 0):
		print('Invalid syntax: Type D instruction cannot be interpreted in this way')
		quit()

	r1 = int(words[1][1])
	bin_r1 = '{0:03b}'.format(r1)

	bin_mem = '{0:08b}'.format(var_dic[words[2]][0])

	code = opcode + bin_r1 + bin_mem #check binary memory
	#load
	if(opcode == '00100'):
		reg_dic[r1] = var_dic[words[2]][1]
	#store
	if(opcode == '00101'):
		var_dic[words[2]][1] = reg_dic[r1]
	print(code)
#done

def parse_E(instruction, words, pc):
	opcode = type_E[instruction]

	if((words[1] in labels.keys()) == 0):
		print('Invalid syntax: Type E instruction cannot be interpreted in this way')
		quit()

	jmploc = labels[words[1]]

	bin_mem = '{0:08b}'.format(jmploc)

	code = opcode + '000' + bin_mem #check binary memory
	print(code)

	#unconditional jump
	if(opcode == '01111'):
		reset()
		return jmploc-1
	#jump if less than
	elif(opcode == '10000' and reg_dic['FLAGS'] == 4):
		reset()
		return jmploc-1
	#jump if greater than
	elif(opcode == '10001' and reg_dic['FLAGS'] == 2):
		reset()
		return jmploc-1
	#jump if equal
	elif(opcode == '10010' and reg_dic['FLAGS'] == 1):
		reset()
		return jmploc-1
	return pc
	
def parse_F(instruction, words):
	opcode = type_F[instruction]
	pc = int(1000)
	code = opcode + '0'*11
	print(code)
	return pc

pre_parse()

print(labels, line_dic)
pc = 0
while pc < len(line_dic.keys()):
	words = line_dic[pc].split()

	if words[0] in type_A:
		instruction = words[0]
		parse_A(instruction, words)

	elif words[0] in type_B:
		instruction = words[0]
		parse_B(instruction, words)

	elif words[0] in type_C:
		instruction = words[0]
		parse_C(instruction, words)

	elif words[0] in type_D:
		instruction = words[0]
		parse_D(instruction, words)

	elif words[0] in type_E:
		instruction = words[0]
		pc = parse_E(instruction, words, pc)

	elif words[0] in type_F:
		instruction = words[0]
		pc = parse_F(instruction, words)

	elif words[0] == 'mov':
		if words[2][0] == '$':
			instruction = 'mov_i'
			parse_B(instruction, words)

		else:
			instruction = 'mov_r'
			parse_C(instruction, words)
	else:
		print(words[0] + ': ' + "Invalid instruction name!!")
		quit()
	pc = pc + 1
print(reg_dic)