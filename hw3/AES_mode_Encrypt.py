#!/usr/bin/env python

from Crypto.Cipher import AES
from PIL import Image
import sys, os, bubbleStack, math

def data_generator(pixs, number):
    data = []
    for pix in pixs:
        data.append(pix) 
        if len(data) == number:
            yield bytes(data)   # here would be execute every number time
            data = []           # clear the buffer
    # padding
    if len(data) != 0:
        yield pad(bytes(''.join( str(x) for x in data), encoding = 'utf-8'), number)

def pad(text, num):
    padding = num - (len(text) % num)
    return text + bytes([padding] * padding)

def CBC_encrypt(text, key, iv):
    cipher_ECB = AES.new(pad(key, 16), AES.MODE_ECB)
    # xor text with iv
    data = ""
    for a,b in zip(text, iv):
        c = format(a^b, '#04x')
        # make the string:0x00 form, or some informaiton would lose
        data += c[2:]
    cText = bytes.fromhex(data)
    # encrypt text with key in ECB mode
    cText = cipher_ECB.encrypt(cText)
    # return text for next round's iv
    return cText

def XOR(a, b):
    # text_h = text.hex()
    # iv_h = iv.hex()
    data = ""
    for a1,b1 in zip(a, b):
        c = format(a1^b1, '#04x')
        data += c[2:]
    cText = bytes.fromhex(data)
    return cText

def DIY_encrypt(text, key, iv):
    a = text.hex()[:len(text.hex())//2]
    # print(a, 'AAAA')
    b = text.hex()[len(text.hex())//2:]
    # print(b, 'BBBB')
    cipher_ECB = AES.new(pad(key, 16), AES.MODE_ECB)
    a_c = cipher_ECB.encrypt(bytes.fromhex(a))
    b_c = cipher_ECB.encrypt(bytes.fromhex(b))
    a_cipher = XOR(a_c, iv)
    # in order to ruin the order
    iv = XOR(bytes([c for t in zip(iv[1::2], iv[::2]) for c in t]),bytes([c for t in zip(text[1::2], text[::2]) for c in t]))
    b_cipher = XOR(b_c, iv)
    new_iv = XOR(a_cipher, b_cipher)
    return a_cipher + b_cipher, new_iv

def prepare(file, text):
    key = bytes(text, encoding = "utf8")
    ppmPicture = "./" + file.split(".")[0] + ".ppm"
    im = Image.open("./" + file)
    im.save(ppmPicture)
    f = open(ppmPicture,'rb').read()
    ppm_type, size, max_color, pixs = f.split(b'\n', 3)

    #### for AES_DIY_MODE
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    f_DIY = open("./" + file.split(".")[0] + "_Encrypt_DIY.ppm", "wb")
    f_DIY.write(ppm_type)
    f_DIY.write(b'\n')
    f_DIY.write(size)
    f_DIY.write(b'\n')
    f_DIY.write(max_color)
    f_DIY.write(b'\n')

    stack = bubbleStack.BubbleStack(int(math.log(len(pixs)/16, 2)))
    for data in data_generator(pixs, 32): 
        try :
            
            ciphertext, new_iv = DIY_encrypt(data, key, iv)
            ## if we use iv = ciphertext, then we cannot see the encrypted picture
            # iv = ciphertext  
            stack.push(new_iv)
            ## if we use iv = stack.pop(), then we can see the encrypted picture
            iv = stack.pop()
            
        except:
            print(data,'WRONG')
        f_DIY.write(bytes(ciphertext))
    f_DIY.close()

    ppmPicture = "./" + file.split(".")[0] + "_Encrypt_DIY.ppm"
    im = Image.open(ppmPicture)
    im.save("./" + file.split(".")[0] + "_Encrypt_DIY.jpg" , 'JPEG')


    #### for AES_ECB_MODE
    cipher_ECB = AES.new(pad(key, 16), AES.MODE_ECB) 
    f_ECB = open("./" + file.split(".")[0] + "_Encrypt_ECB.ppm", "wb")
    f_ECB.write(ppm_type)
    f_ECB.write(b'\n')
    f_ECB.write(size)
    f_ECB.write(b'\n')
    f_ECB.write(max_color)
    f_ECB.write(b'\n')
    
    for data in data_generator(pixs, 16):
        try:
            ciphertext = cipher_ECB.encrypt(data)
        except:
            print(data)
        f_ECB.write(bytes(ciphertext))
    f_ECB.close()

    ppmPicture = "./" + file.split(".")[0] + "_Encrypt_ECB.ppm"
    im = Image.open(ppmPicture)
    im.save("./" + file.split(".")[0] + "_Encrypt_ECB.jpg", 'JPEG')

    #### for AES_CBC_MODE
    # iv should be explicit defined
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    # cipher_CBC = AES.new(pad(key, 16), AES.MODE_CBC, iv) # here should use ECB mode, iv=key?
    f_CBC = open("./" + file.split(".")[0] + "_Encrypt_CBC.ppm", "wb")
    f_CBC.write(ppm_type)
    f_CBC.write(b'\n')
    f_CBC.write(size)
    f_CBC.write(b'\n')
    f_CBC.write(max_color)
    f_CBC.write(b'\n')

    for data in data_generator(pixs, 16): 
        try :
            ciphertext = CBC_encrypt(data, key, iv)
            iv = ciphertext
        except:
            print(data)
        f_CBC.write(bytes(ciphertext))
    f_CBC.close()

    ppmPicture = "./" + file.split(".")[0] + "_Encrypt_CBC.ppm"
    im = Image.open(ppmPicture)
    im.save("./" + file.split(".")[0] + "_Encrypt_CBC.jpg" , 'JPEG')


if __name__ == "__main__":
    filename = sys.argv[1]
    key = sys.argv[2]
    if os.path.exists('./'+filename) is not True: print('No file, please put the picture file in the directory')
    else: prepare(filename , key)