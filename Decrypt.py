#!/usr/bin/env python

# caesar

def Caesar_decrypt(Key,Ciphertext):  
    tempt= []
    new_tempt = []
    key = int(Key)
    plaintext = ""
    alphabet = {'a':'1','b':'2','c':'3','d':'4','e':'5','f':'6','g':'7','h':'8', 'i':'9','j':'10','k':'11','l':'12','m':'13','n':'14','o':'15','p':'16','q':'17',
    'r':'18','s':'19','t':'20','u':'21','v':'22','w':'23','x':'24','y':'25','z':'26'}

    ciphertext = Ciphertext.lower()

    for l in ciphertext:
        tempt.append(alphabet[l])

    for t in tempt:
        t = (int(t) - key) % 26
        new_tempt.append(t)


    for n in new_tempt:
        for a,b in alphabet.items():
            if n == int(b): plaintext = plaintext + a

    return plaintext.lower()         


# playfair

def Playfair_decrypt(Key,Ciphertext):

    key = Key.lower()
    combine = key + 'abcdefghijklmnopqrstuvwxyz'
    combine = combine.replace('i','j')

    new_order = []
    for l in combine:
        if l not in new_order:
            new_order.append(l)

    puzzle_map = {}    
    #  x is row列 and y is column行
    for x in range(1,6):
        for y in range(1,6):
            puzzle_map[x,y] = new_order[5*(x - 1) + y - 1]

    new_ciphertext = []
    Ciphertext = Ciphertext.replace('I','J')

    for char in Ciphertext:
        if len(new_ciphertext) % 2 == 0:
            new_ciphertext.append(char)
        else:
            if char == new_ciphertext[-1]: 
                if char != 'X': new_ciphertext.append('X') 
                else: new_ciphertext.append('Q')
            new_ciphertext.append(char)

    if len(new_ciphertext) % 2 == 1: new_ciphertext.append('X')

    reverse_puzzle = {k: v for v,k in puzzle_map.items()}

    plaintext = ''

    for i in range(0,len(new_ciphertext),2):
        x1, y1 = reverse_puzzle[new_ciphertext[i].lower()]
        x2, y2 = reverse_puzzle[new_ciphertext[i+1].lower()]
        if x1 == x2: 
            pre_x1 = x1  
            pre_x2 = x2  
            pre_y1 = y1 - 1
            pre_y2 = y2 - 1
            if pre_y1 == 0: pre_y1 = 5
            if pre_y2 == 0: pre_y2 = 5
        elif y1 == y2:
            pre_y1 = y1  
            pre_y2 = y2  
            pre_x1 = x1 - 1
            pre_x2 = x2 - 1
            if pre_x1 == 0: pre_x1 = 5
            if pre_x2 == 0: pre_x2 = 5
        else:
            pre_x1 = x1 
            pre_x2 = x2
            pre_y1 = y2
            pre_y2 = y1

        plaintext += puzzle_map[pre_x1,pre_y1] + puzzle_map[pre_x2,pre_y2]

    return plaintext


# vernam
def Vernam_decrypt(Key,Ciphertext):
    plaintext = ''
    ciphertext = Ciphertext.lower()
    key = Key.lower()
    lenth = len(key)

    for i in range(len(ciphertext)):
        key += chr( ((ord(ciphertext[i])-95)^(ord(key[i])-97)) +97)


    # for i in range(len(ciphertext)):
    #     plaintext += chr( ((ord(ciphertext[i])-97)^(ord(key[i])-97)) +97)
    #     # plaintext += chr(((ord(ciphertext[i]-97)^(ord(key[i]-97))+97)

    # return plaintext.lower()
    plaintext = key[lenth:].lower()
    return plaintext

#row transposition

def Row_decrypt(Key,Ciphertext):
    result = []
    key = Key
    ciphertext = Ciphertext
    basic_amount = int(len(ciphertext) / len(key))
    extra_amount = len(ciphertext) % len(key)
    for i in range(extra_amount):
        result.append(ciphertext[:basic_amount + 1])
        ciphertext = ciphertext[basic_amount + 1:]

    for i in range(len(key) - extra_amount):
        result.append(ciphertext[:basic_amount])
        ciphertext = ciphertext[basic_amount:]

    result = [a for a in map(list,result)]
    # return result
    sort_result = []

    for i,char in enumerate(key):
        sort_result.insert(int(char)-1, result[i])

    # return sort_result
    plaintext = ''
    for x in range(len(sort_result[0])):
        try:
            for y in range(len(sort_result)):
                plaintext += sort_result[y][x]
        except:      
            pass

    return plaintext.lower()


# rail fence
def RailFence_decrypt(Key,Ciphertext):
    plaintext = ''
    ciphertext = Ciphertext
    key = int(Key)
    puzzle = [["" for i in range(len(ciphertext))] for j in range(key)]
    num = ''
    for i in range(key):
        num += str(i)
    for i in reversed(range(key-1)):
        num += str(i)
    order = num[:-1]
    repeat = int(len(ciphertext)/ len(order) + 1)
    order *= repeat
    row = list(zip(ciphertext,order))

    for i in range(len(ciphertext)):
        puzzle[int(row[i][1])][i] = row[i][0]
    column = len(ciphertext)

    for i in range(key):
        for j in range(column):
            if puzzle[i][j] != '':
                puzzle[i][j] = ciphertext[0]
                ciphertext = ciphertext[1:]

    for i in range(column):
        for j in range(key):
            if puzzle[j][i] != '': 
                plaintext += puzzle[j][i].lower()
                
    return plaintext.lower()








import sys

Method = sys.argv[1]
Key = sys.argv[2]
Ciphertext = sys.argv[3]

if Method == 'caesar': print(Caesar_decrypt(Key,Ciphertext))
if Method == 'playfair': print(Playfair_decrypt(Key,Ciphertext))
if Method == 'vernam': print(Vernam_decrypt(Key,Ciphertext))
if Method == 'row': print(Row_decrypt(Key,Ciphertext))
if Method == 'rail_fence': print(RailFence_decrypt(Key,Ciphertext))