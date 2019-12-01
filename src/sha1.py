# Prithu Pareek - Created 11/30/19
# Implementation of SHA1 Hash Function

import codecs
import binascii

# All originally written code, but basic sha1 agorithm based on https://www.youtube.com/watch?v=kmHojGMUn0Q
def hash(inputStr):

	# make sure the item is a string
	if type(inputStr) != str:
		raise ValueError("Input type must be string.")

	# take input string and turn it into a list of charecters
	inputStrList = list(inputStr)

	# convert the charecters in the list to their ascii values
	asciiList = [ord(char) for char in inputStrList]

	# convert ascii to binary (8 bit)
	binaryList = [decToBin(n, padding=8) for n in asciiList]

	# join all chars together and append a 1
	joinedBinary = "".join(binaryList) + '1'

	# pad the number with 0s until there are 448 chars
	while len(joinedBinary) % 512 != 448:

		joinedBinary = joinedBinary + '0'

	# get the len of ascii list, convert to binary, and pad until 64 chrs
	asciiLenBin = decToBin(len(asciiList))

	asciiLenBin = pad(asciiLenBin, 64, mode='pre')

	joinedBinary += asciiLenBin

	# split into 512 char chunks
	chunks = [joinedBinary[i*512: (i+1)*512] for i in range(0, len(joinedBinary)//512)]

	splitChunks = []

	# split chunks into 16, 32-bit subchunks
	for chunk in chunks:

		chunk = [chunk[i*32: (i+1)*32] for i in range(0, len(chunk)//32)]

		splitChunks.append(chunk)

	# generate 64 more 32-bit words for each chunk using bitwise operations
	# loop starting at last every time, bc len of list increases each iteration
	for j in range(len(splitChunks)):
		for i in range(16, 80):

			# grab 4 words to perform xor on
			word1 = splitChunks[j][i - 3]
			word2 = splitChunks[j][i - 8]
			word3 = splitChunks[j][i - 14]
			word4 = splitChunks[j][i - 16]

			# perform xor operations to generate new binary
			xor1 = binaryXOR(word1, word2, padding=32)
			xor2 = binaryXOR(word3, xor1, padding=32)
			xor3 = binaryXOR(word4, xor2, padding=32)

			# add padding
			xor3 = pad(xor3, 32, mode='pre')

			# add to the splitChunks list at the right position
			splitChunks[j].append(xor3)

	# initialize some variables
	a = h0 = '11010101010101110001010111101101'
	b = h1 = '01101000011111010010010100110101'
	c = h2 = '11001011011100000000110101100100'
	d = h3 = '01010001111101010001000011101000'
	e = h4 = '11110000111111101111110010111001'

	# loop through all the small chunks
	for i in range(0, len(splitChunks)):
		for j in range(0, 80):

			# perform bitwise operations on a,b,c,d,e based on j
			if j < 20:
				bANDc = binaryAND(b, c, padding=32)
				NOTb = binaryNOT(b, padding=32)
				notbANDd = binaryAND(NOTb, d, padding=32)
				f = binaryOR(bANDc, notbANDd, padding=32)
				k = '01001000000110011110100000110010'
			elif 20 < j < 40:
				bXORc = binaryXOR(b, c, padding=32)
				f = binaryXOR(bXORc, d, padding=32)
				k = '01001111001011001000010100011001'
			elif 40 < j < 60:
				bANDc = binaryAND(b, c, padding=32)
				bANDd = binaryAND(b, d, padding=32)
				cANDd = binaryAND(c, d, padding=32)
				f = binaryOR(binaryOR(bANDc, bANDd, padding=32), cANDd, padding=32)
				k = '00001001101111000111110100101011'
			else:
				bXORc = binaryXOR(b, c, padding=32)
				f = binaryXOR(bXORc, d, padding=32)
				k = '00001001000000000001101110100111'

			splitChunk = splitChunks[i][j]
			tempA = binaryAdd(binaryLeftRotate(a, 5, padding=32), f, padding=32)
			tempB = binaryAdd(tempA, e, padding=32)
			tempC = binaryAdd(tempB, k, padding=32)
			temp = binaryAdd(tempC, splitChunk, padding=32)

			temp = temp[:32]
			e = d
			d = c
			c = binaryLeftRotate(b, 30, padding=32)
			b = a
			a = temp

			h0 = binaryAdd(h0, a, padding=32)[:32]
			h1 = binaryAdd(h1, b, padding=32)[:32]
			h2 = binaryAdd(h2, c, padding=32)[:32]
			h3 = binaryAdd(h3, d, padding=32)[:32]
			h4 = binaryAdd(h4, e, padding=32)[:32]

	# convert the final h values to hex
	h0 = hex(int(h0, 2))
	h1 = hex(int(h1, 2))
	h2 = hex(int(h2, 2))
	h3 = hex(int(h3, 2))
	h4 = hex(int(h4, 2))

	# concatenate the hex strings and remove 0x from them
	hashString = (h0 + h1 + h2 + h3 + h4).replace("0x", "")

	return hashString

# helper function, converts decimal to binary, can specify how many bits the result will have if the output is less
def decToBin(n, padding=None):

	binary = bin(n)[2:]

	if padding != None:
		binary = pad(binary, padding)

	return binary


# exclusive or bitwise operation helper function
def binaryXOR(valueA, valueB, padding=None):

	# XOR value a and b
	binary = decToBin(int(valueA, 2) ^ int(valueB, 2), padding)

	return binary

def binaryAND(valueA, valueB, padding=None):
	
	binary = decToBin(int(valueA, 2) & int(valueB, 2), padding)

	return binary

def binaryOR(valueA, valueB, padding=None):
	
	binary = decToBin(int(valueA, 2) | int(valueB, 2), padding)

	return binary

def binaryNOT(valueA, padding=None):
	
	binary = ''

	for i in valueA:

		if i == '0':
			binary += '1'
		elif i == '1':
			binary += '0'

	binary = pad(binary, padding)

	return binary

def binaryLeftRotate(valueA, shift, padding):

	# shift left, and then or with the shift right to replace the 0s that are added when shifting left
	binary = decToBin((int(valueA,2) << shift) | (int(valueA, 2) >> (padding - shift)), padding)

	return binary

def binaryAdd(valueA, valueB, padding):

	# shift left, and then or with the shift right to replace the 0s that are added when shifting left
	binary = decToBin((int(valueA,2) + int(valueB,2)), padding)

	return binary


def pad(value, padding, mode='pre'):

	while len(value) < padding:

		if mode == 'pre':
			value = '0' + value
		elif mode == 'post':
			value = value + '0'

	return value
