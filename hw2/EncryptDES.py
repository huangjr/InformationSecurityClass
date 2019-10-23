#!/usr/bin/env python

PC1 = (
    57, 49, 41, 33, 25, 17, 9,
    1,  58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27,
    19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7,  62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29,
    21, 13, 5,  28, 20, 12, 4
)

PC2 = (
    14, 17, 11, 24, 1,  5,
    3,  28, 15, 6,  21, 10,
    23, 19, 12, 4,  26, 8,
    16, 7,  27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
)

IP = (
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
)

E  = (
    32, 1,  2,  3,  4,  5,
    4,  5,  6,  7,  8,  9,
    8,  9,  10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
)

Sboxes = {
    0: (
        14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
        0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
        4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
        15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13
    ),
    1: (
        15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
        3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
        0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
        13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9 
    ),
    2: (
        10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
        13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
        13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
        1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12 
    ),
    3: (
        7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
        13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
        10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
        3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14
    ),
    4: (
        2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
        14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
        4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
        11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3
    ),
    5: (
        12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
        10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
        9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
        4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13
    ),
    6: (
        4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
        13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
        1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
        6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12
    ),
    7: (
        13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
        1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
        7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
        2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11
    )
}

P = (
    16,  7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11, 4,  25
)

IP_INV = (
    40,  8, 48, 16, 56, 24, 64, 32,
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25
)

# hex to binary
def hexToBinary(hex):
    return bin(int(hex, 16))[2:].zfill(64)

# key need to left shift and it depends its round
def keyShift(c, d, round_number):   
    c1 = []
    d1 = []
    if round_number is 1 or round_number is 2 or round_number is 9 or round_number is 16:
        c1 = c[1:] + c[0:1]
        d1 = d[1:] + d[0:1]
        return c1+d1
    else:
        c1 = c[2:] + c[0:2]
        d1 = d[2:] + d[0:2]
        return c1+d1

# after transfering to IP, we split them half and put right-hand side into the Function
def Function(Right_32bit, round_key):
    r1 = [] 
    r1_48btis = []
    Expansion = permutateToTable(Right_32bit,E)
    for i, j in zip(Expansion,round_key):
        r1_48btis.append(int(i)^int(j))
    for n, i in enumerate(range(0, len(r1_48btis), 6)):
        r1.append(sBox(r1_48btis[i:i+6],n))
    r1_str = ''.join([char for char in r1])
    return permutateToTable(r1_str,P)

# check sbox table
def sBox(six_bit, sbox_number):
    row = str(six_bit[0]) + str(six_bit[-1])
    column = "".join([str(char) for char in six_bit[1:-1]])
    number = Sboxes[sbox_number][ int(row,2)*16 + int(column,2) ]
    return '{0:04b}'.format(number)

# permutate to table
def permutateToTable(origin,table):
    afterTable = []
    for order in table:
        afterTable.append(origin[order - 1])
    return afterTable

# encrypt DES 
def encrypt(key, plaintext):
    Binary_key = hexToBinary(key)
    AfterPC1 = []
    AfterPC1 = permutateToTable(Binary_key,PC1)
    C = AfterPC1[:28]
    D = AfterPC1[28:]

    # make every round keys
    every_round_keys = []
    every_round_keys_forFunc = [['' for i in range(48)] for j in range(16)]
    for round_number in range(1, 16+1):
        every_round_keys.append(keyShift(C,D,round_number))
        C = every_round_keys[round_number - 1][:28]
        D = every_round_keys[round_number - 1][28:]
        every_round_keys_forFunc[round_number - 1] = permutateToTable(every_round_keys[round_number - 1],PC2)

    # prepare the plaintext
    Binary_plaintext = hexToBinary(plaintext)
    AfterIP = []
    AfterIP = permutateToTable(Binary_plaintext,IP)
    L = AfterIP[:32]
    R = AfterIP[32:]   

    # do the Feistel Network
    for round_number in range(1, 16+1):
        R1 = []
        for i, j in zip( L , Function(R, every_round_keys_forFunc[round_number - 1])):
            R1.append(str(int(i)^int(j)))
        L = R  
        R = R1

    # combine the last round 
    Final_64bit = [str(char) for char in (R+L)]
    AfterIP_INV = permutateToTable(Final_64bit,IP_INV)
    Ciphertext_binary = ''.join(AfterIP_INV)
    Ciphertext_hex = hex(int(Ciphertext_binary,2))[2:]
    Ciphertext = Ciphertext_hex.upper()
    return '0x' + Ciphertext


import sys

Key = sys.argv[1]
Plaintext = sys.argv[2]
# Plaintext = '0xabcdef0123456789'
# Key = '0xafafafafafafafaf'

if len(Key) != 18: print('Key\'s length is not hex')
elif len(Plaintext) != 18: print('Plaintext\'s length is not hex')
else : print(encrypt(Key[2:],Plaintext[2:]))



