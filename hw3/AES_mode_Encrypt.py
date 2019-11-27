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

def XOR(text, iv):
    # text_h = text.hex()
    # iv_h = iv.hex()
    data = ""
    for a,b in zip(text, iv):
        c = format(a^b, '#04x')
        data += c[2:]
    cText = bytes.fromhex(data)
    return cText

def prepare(file, text):
    key = bytes(text, encoding = "utf8")
    ppmPicture = "./" + file.split(".")[0] + ".ppm"
    im = Image.open("./" + file)
    im.save(ppmPicture)
    f = open(ppmPicture,'rb').read()
    ppm_type, size, max_color, pixs = f.split(b'\n', 3)

    # #### for AES_ECB_MODE
    # cipher_ECB = AES.new(pad(key, 16), AES.MODE_ECB) 
    # f_ECB = open("./" + file.split(".")[0] + "_Encrypt_ECB.ppm", "wb")
    # f_ECB.write(ppm_type)
    # f_ECB.write(b'\n')
    # f_ECB.write(size)
    # f_ECB.write(b'\n')
    # f_ECB.write(max_color)
    # f_ECB.write(b'\n')
    
    # for data in data_generator(pixs, 16):
    #     try:
    #         ciphertext = cipher_ECB.encrypt(data)
    #     except:
    #         print(data)
    #     f_ECB.write(bytes(ciphertext))
    # f_ECB.close()

    # ppmPicture = "./" + file.split(".")[0] + "_Encrypt_ECB.ppm"
    # im = Image.open(ppmPicture)
    # im.save("./" + file.split(".")[0] + "_Encrypt_ECB.jpg", 'JPEG')

    # #### for AES_CBC_MODE
    # # iv should be explicit defined
    # iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    # # cipher_CBC = AES.new(pad(key, 16), AES.MODE_CBC, iv) # here should use ECB mode, iv=key?
    # f_CBC = open("./" + file.split(".")[0] + "_Encrypt_CBC.ppm", "wb")
    # f_CBC.write(ppm_type)
    # f_CBC.write(b'\n')
    # f_CBC.write(size)
    # f_CBC.write(b'\n')
    # f_CBC.write(max_color)
    # f_CBC.write(b'\n')

    # for data in data_generator(pixs, 16): 
    #     try :
    #         ciphertext = CBC_encrypt(data, key, iv)
    #         iv = ciphertext
    #     except:
    #         print(data)
    #     f_CBC.write(bytes(ciphertext))
    # f_CBC.close()

    # ppmPicture = "./" + file.split(".")[0] + "_Encrypt_CBC.ppm"
    # im = Image.open(ppmPicture)
    # im.save("./" + file.split(".")[0] + "_Encrypt_CBC.jpg" , 'JPEG')

    #### for AES_DIY_MODE
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    f_DIY = open("./" + file.split(".")[0] + "_Encrypt_DIY.ppm", "wb")
    f_DIY.write(ppm_type)
    f_DIY.write(b'\n')
    f_DIY.write(size)
    f_DIY.write(b'\n')
    f_DIY.write(max_color)
    f_DIY.write(b'\n')

    stack = bubbleStack.BubbleStack(int(math.log(len(pixs), 2)))
    for data in data_generator(pixs, 32): 
        try :
            ciphertext, new_iv = DIY_encrypt(data, key, iv)
            stack.push(new_iv)
            iv = stack.pop()
        except:
            print(data,'WRONG')
        f_DIY.write(bytes(ciphertext))
    f_DIY.close()

    ppmPicture = "./" + file.split(".")[0] + "_Encrypt_DIY.ppm"
    im = Image.open(ppmPicture)
    im.save("./" + file.split(".")[0] + "_Encrypt_DIY.jpg" , 'JPEG')

def DIY_encrypt(text, key, iv):
    a = text.hex()[:len(text.hex())//2]
    b = text.hex()[len(text.hex())//2:]
    cipher_ECB = AES.new(pad(key, 16), AES.MODE_ECB)
    a_c = cipher_ECB.encrypt(bytes.fromhex(a))
    b_c = cipher_ECB.encrypt(bytes.fromhex(b))
    a_cipher = XOR(a_c, iv)
    b_cipher = XOR(b_c, iv)
    new_iv = XOR(a_cipher, b_cipher)
    return a_cipher + b_cipher, new_iv

def iv(blockList):
    '''
    test docstring:
    >>> blocks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
    >>> iv(blocks)
    [1, 2, 0, 7, 1, 2, 4, 11, 1, 2, 8, 15, 9, 10, 12, 19, 1, 2]
    '''
    # iv is a two dimensional array, when every a layer has two element, element inside would be xor
    # togather, and then store into one higher layer, the height would be soooo long.
    stack = BubbleStack(int(math.log(len(blockList), 2)))
    current_iv = 0
    for i in range(0,len(blockList)-1,2):
        a = blockList[i] ^ current_iv
        b = blockList[i+1] ^ current_iv
        image.append(a)
        image.append(b)
        stack.push(a^b)
        current_iv = stack.pop()
    return image



if __name__ == "__main__":
    filename = sys.argv[1]
    key = sys.argv[2]
    if os.path.exists('./'+filename) is not True: print('No file, please put the picture file in the directory')
    else: prepare(filename , key)
