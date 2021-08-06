import sys

f = open('code.txt')

# Dividing the instructions into various types
type_A = {'add': '00000', 'sub': '00001', 'mul': '00110', 'xor': '01010', 'or': '01011', 'and': '01100'}

type_B = {'rs': '01000', 'ls':'01001', 'mov_i': '00010'}

type_C = {'div':'00111', 'not': '01101', 'cmp':'01110', 'mov_r': '00011'}

type_D = {'ld': '00100', 'st':'00101'}

type_E = {'jmp':'01111', 'jlt': '10000', 'jgt': '10001', 'je': '10010'}

type_F = {'hlt': '10011'}

def pre_parse():
	var = {}
	labels = {}
	lines = {}


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
	print(code)

def parse_B(instruction, words):
	opcode = type_B[instruction]

	if((words[1][0] == 'R' and words[1][1].isdecimal() and words[2][1:].isdecimal()) == 0):
		print('Invalid syntax: Type B instruction cannot be interpreted in this way')
		quit()

	r1 = int(words[1][1])
	bin_r1 = '{0:03b}'.format(r1)

	imm = int(words[2][1:])
	bin_imm = '{0:08b}'.format(imm)

	code = opcode + bin_r1 + bin_imm
	print(code)


def parse_C(instruction, words):
	opcode = type_C[instruction]

	if((words[1][0] == 'R' and words[1][1].isdecimal() and words[2][0] == 'R' and words[2][1].isdecimal()) == 0):
		print('Invalid syntax: Type B instruction cannot be interpreted in this way')
		quit()

	r1 = int(words[1][1])
	bin_r1 = '{0:03b}'.format(r1)

	r2 = int(words[2][1])
	bin_r2 = '{0:03b}'.format(r2)

	code = opcode + '00000' + bin_r1 + bin_r2;
	print(code)

#check how memory addresses are given in assembly ->  AS LABELS

def parse_D(instruction, words):
	opcode = type_D[instruction]

	if((words[1][0] == 'R' and words[1][1].isdecimal() and words[2] in labels) == 0):
		print('Invalid syntax: Type D instruction cannot be interpreted in this way')
		quit()

	r1 = int(words[1][1])
	bin_r1 = '{0:03b}'.format(r1)

	mem = int(labels[words[2]])
	bin_mem = '{0:08b}'.format(imm)

	code = opcode + bin_r1 + bin_mem #check binary memory
	print(code)

def parse_E(instruction, words):
	opcode = type_E[instruction]

	if((words[1] in labels) == 0):
		print('Invalid syntax: Type E instruction cannot be interpreted in this way')
		quit()

	mem = int(labels[words[1]])
	bin_mem = '{0:08b}'.format(imm)

	code = opcode + '000' + bin_mem #check binary memory
	print(code)

def parse_F(instruction, words):
	opcode = type_F[instruction]
	code = opcode + '0'*11
	print(code)


for line in f:
	words = line.split()

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
		parse_E(instruction, words)

	elif words[0] in type_F:
		instruction = words[0]
		parse_F(instruction, words)

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