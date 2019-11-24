#!/usr/bin/env python

from Crypto.Cipher import AES
from PIL import Image
import sys, os

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

def prepare(file, text):
    key = bytes(text, encoding = "utf8")
    ppmPicture = "./" + file.split(".")[0] + ".ppm"
    im = Image.open("./" + file)
    im.save(ppmPicture)
    f = open(ppmPicture,'rb').read()
    ppm_type, size, max_color, pixs = f.split(b'\n', 3)

    # for AES_ECB_MODE
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

    # for AES_CBC_MODE
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
