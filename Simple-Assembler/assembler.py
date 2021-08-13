import sys

# f = open('code.txt')

# Dividing the instructions into various types
type_A = {'add': '00000', 'sub': '00001', 'mul': '00110', 'xor': '01010', 'or': '01011', 'and': '01100'}

type_B = {'rs': '01000', 'ls':'01001', 'mov_i': '00010'}

type_C = {'div':'00111', 'not': '01101', 'cmp':'01110', 'mov_r': '00011'}

type_D = {'ld': '00100', 'st':'00101'}

type_E = {'jmp':'01111', 'jlt': '10000', 'jgt': '10001', 'je': '10010'}

type_F = {'hlt': '10011'}

instruct = ['add','sub','mul','xor','or','and','rs','ls','mov','div','not','cmp','ld','st','jmp','jlt','jgt','je','hlt']

register = ['R0','R1','R2','R3','R4','R5','R6']

#{var_name : [address(binary), value]}
var_dic = {}

#{label_name : address(decimal))}
labels = {}

#In order: code -> hlt
#{address(decimal) : entire instruction(string)}
#for labels, the label name is not included
line_dic = {}

# stores line no of instructions present in line_dic
code_line = []

# output list
bin_file = []

def pre_parse():
	var_temp = []
	
	address = 0
	line_no = 0
	halt = False
	var_end = False

	for line in sys.stdin:
		line_no +=1

		if line == "\n":
			continue

		words = line.split()
		if halt == True:
			print(str(line_no) + ": Syntax Error: hlt instuction must be given in the end.")
			quit()

		if var_end == True and words[0] == "var":
			print(str(line_no) + ": Syntax Error: All variables must be declared at the beginning")
			quit()

		if words[0] == "var":

			if words[1] in var_temp:
				print(str(line_no) + ": Syntax Error: 2 or more variables cannot have the same name.")
				quit()

			elif words[1] in labels.keys():
				print(str(line_no) + ": Syntax Error: Variables and labels can't have the same name.")
				quit()

			elif words[1] in instruct:
				print(str(line_no) + ": Syntax Error: Mnemonic of the instructions cannot be used as variables")
				quit()

			else:
				var_temp.append(words[1])
		
		elif words[0][-1] == ":":
			var_end = True
			if words[0][:-1] in var_temp:
				print(str(line_no) + ": Syntax Error: Variables and labels can't have the same name.")
				quit()

			elif words[0][:-1] in labels.keys():
				print(str(line_no) + ": Syntax Error: 2 or more labels cannot have the same name.")
				quit()

			elif words[0][:-1] in instruct:
				print(str(line_no) + ": Syntax Error: Mnemonic of the instructions cannot be used as labels")
				quit()

			else:
				labels[words[0][:-1]] = address
				if(line[-1] == "\n"):
					line_dic[address] = line[len(words[0])+1:-1]
				else:
					line_dic[address] = line[len(words[0])+1:]

			if len(words)>1 and words[1] == 'hlt':
				var_end = True
				halt = True

			address += 1

		else:
			if words[0] == "hlt":
				var_end = True
				halt = True

			var_end = True
			if(line[-1] == "\n"):
				line_dic[address] = line[:-1]
			else:
				line_dic[address] = line
			
			address +=1
		
		if words[0] != "var":
			code_line.append(line_no)

	if halt == False:
		print(str(line_no) + ": Syntax Error: The last instruction should be hlt.")
		quit()

	for v in var_temp:
		var_dic[v] = [address, 0]
		address += 1

	if(address>257):
		print("Error: Number of instructions exceed 256")
		quit()


def parse_A(instruction, words):
	opcode = type_A[instruction]

	if((words[1][0] == 'R' and words[2][0] == 'R' and words[3][0] == 'R') == 0):
		print(str(code_line[pc]) + ': Invalid syntax: Type B instruction cannot be interpreted in this way')
		quit()

	r1 = int(words[1][1])
	bin_r1 = '{0:03b}'.format(r1)

	r2 = int(words[2][1])
	bin_r2 = '{0:03b}'.format(r2)

	r3 = int(words[3][1])
	bin_r3 = '{0:03b}'.format(r3)

	code = opcode + '00' + bin_r1 + bin_r2 + bin_r3

	bin_file.append(code)
	
def parse_B(instruction, words):
	opcode = type_B[instruction]

	if((words[1][0] == 'R' and words[1][1].isdecimal() and words[2][0] == '$' and words[2][1:].isdecimal()) == 0):
		print(str(code_line[pc]) + ': Invalid syntax: Type B instruction cannot be interpreted in this way')
		quit()

	# Limits for immediate values
	if words[2][0] == '$':
			immediate = int(words[2][1:])
			if immediate < 0 or immediate > 255:
				print(str(code_line[pc]) + ": Immediate value out of bounds (0 -> 255)")
				quit()


	r1 = int(words[1][1])
	bin_r1 = '{0:03b}'.format(r1)

	imm = int(words[2][1:])
	bin_imm = '{0:08b}'.format(imm)

	code = opcode + bin_r1 + bin_imm

	bin_file.append(code)

def parse_C(instruction, words):
	opcode = type_C[instruction]

	if((words[1][0] == 'R' and words[1][1].isdecimal() and words[2][0] == 'R' and (words[2][1].isdecimal()) == 0 and words[2] != 'FLAGS')):
		print(str(code_line[pc]) + ': Invalid syntax: Type C instruction cannot be interpreted in this way')
		quit()

	r1 = int(words[1][1])
	bin_r1 = '{0:03b}'.format(r1)

	if words[2] == 'FLAGS':
		r2 = 'FLAGS'
		
		bin_r2 = '111'

	else:
		r2 = int(words[2][1])
		bin_r2 = '{0:03b}'.format(r2)

	code = opcode + '00000' + bin_r1 + bin_r2
	
	bin_file.append(code)

def parse_D(instruction, words):
	opcode = type_D[instruction]

	if((words[1][0] == 'R' and words[1][1].isdecimal()) == 0):
		print(str(code_line[pc]) + ': Invalid syntax: Type D instruction cannot be interpreted in this way')
		quit()

	if(words[2] in labels.keys()):
		print(str(code_line[pc]) + ': Syntax Error: Labels cannot be used as variables.')
		quit()

	if(words[2] not in var_dic.keys()):
		print(str(code_line[pc]) + ': Variable ' + words[2] + ' is not defined')
		quit()

	r1 = int(words[1][1])
	bin_r1 = '{0:03b}'.format(r1)

	bin_mem = '{0:08b}'.format(var_dic[words[2]][0])

	code = opcode + bin_r1 + bin_mem 

	bin_file.append(code)

def parse_E(instruction, words):
	opcode = type_E[instruction]

	if(words[1] in var_dic.keys()):
		print(str(code_line[pc]) + ': Syntax Error: Variables cannot be used as labels.')
		quit()

	if((words[1] in labels.keys()) == 0):
		print(str(code_line[pc]) + ': Syntax Error: The label ' + words[1] + ' is not defined.')
		quit()

	jmploc = labels[words[1]]

	bin_mem = '{0:08b}'.format(jmploc)

	code = opcode + '000' + bin_mem 
	bin_file.append(code)	
	
def parse_F(instruction):
	opcode = type_F[instruction]
	code = opcode + '0'*11
	bin_file.append(code)

pre_parse()

for pc in range(len(line_dic.keys())):
	words = line_dic[pc].split()

	if words[0] in type_A:
		
		if words[1] == "FLAGS" or words[2] == "FLAGS" or words[3] == "FLAGS":
			print(str(code_line[pc]) + ": Syntax Error: Illegal use of FLAGS register") 
			quit()

		if words[1] not in register or words[2] not in register or words[3] not in register:
			print(str(code_line[pc]) + ": Syntax Error: Register name does not exist.")
			quit()

		instruction = words[0]
		parse_A(instruction, words)

	elif words[0] in type_B:
		if words[1] == "FLAGS":
			print(str(code_line[pc]) + ": Syntax Error: Illegal use of FLAGS register") 
			quit()
		
		if words[1] not in register:
			print(str(code_line[pc]) + ": Syntax Error: Register name does not exist.")
			quit()

		instruction = words[0]
		parse_B(instruction, words)

	elif words[0] in type_C:
		if words[1] == "FLAGS" or words[2] == "FLAGS":
			print(str(code_line[pc]) + ": Syntax Error: Illegal use of FLAGS register") 
			quit()

		if words[1] not in register or words[2] not in register:
			print(str(code_line[pc]) + ": Syntax Error: Register name does not exist.")
			quit()

		instruction = words[0]
		parse_C(instruction, words)

	elif words[0] in type_D:
		if words[1] == "FLAGS":
			print(str(code_line[pc]) + ": Syntax Error: Illegal use of FLAGS register") 
			quit()

		if words[1] not in register:
			print(str(code_line[pc]) + ": Syntax Error: Register name does not exist.")
			quit()

		instruction = words[0]
		parse_D(instruction, words)

	elif words[0] in type_E:
		instruction = words[0]
		pc = parse_E(instruction, words)

	elif words[0] in type_F:
		instruction = words[0]
		pc = parse_F(instruction)

	elif words[0] == 'mov':
		if words[2][0] == '$':
			if words[1] not in register:
				print(str(code_line[pc]) + ": Syntax Error: Register name does not exist.")
				quit()
			instruction = 'mov_i'
			parse_B(instruction, words)

		else:
			if (words[1] not in register and words[1] != "FLAGS") or (words[2] not in register and words[2] != "FLAGS"):
				print(str(code_line[pc]) + ": Syntax Error: Register name does not exist.")
				quit()

			instruction = 'mov_r'
			parse_C(instruction, words)
	else:
		print(str(code_line[pc]) + ": " + words[0] + ': ' + "Invalid instruction!!")
		quit()
	
print(*bin_file, sep = '\n')
