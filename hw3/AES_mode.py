#!/usr/bin/env python

from Crypto.Cipher import AES
from PIL import Image
import sys, os

def data_generator(pixs, number):
    data = []
    for pix in pixs:
        data.append(pix) 
        if len(data) == number:
            yield bytes(data)
            data = []
    # padding
    if len(data) != 0:
        yield pad(bytes(''.join( str(x) for x in data), encoding = 'utf-8'), number)

def pad(text, num):
    padding = num - (len(text) % num)
    return text + bytes([padding] * padding)

def prepare(file, text):
    key = bytes(text, encoding = "utf8")
    ppmPicture = "./" + file + ".ppm"
    im = Image.open("./" + file)
    im.save(ppmPicture)
    f = open("./" + file + ".ppm",'rb').read()
    ppm_type, size, max_color, pixs = f.split(b'\n', 3)

    # for AES_ECB_MODE
    cipher_ECB = AES.new(pad(key, 16), AES.MODE_ECB) 
    f_ECB = open("./" + file + "_aes_ECB.ppm", "wb")
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

    ppmPicture = "./" + file + "_aes_ECB.ppm"
    im = Image.open(ppmPicture)
    im.save("./" + file + "_aes_ECB.jpg", 'JPEG')

    # for AES_CBC_MODE
    iv = os.urandom(16)
    cipher_CBC = AES.new(pad(key, 16), AES.MODE_CBC, iv) 
    f_CBC = open("./" + file + "_aes_CBC.ppm", "wb")
    f_CBC.write(ppm_type)
    f_CBC.write(b'\n')
    f_CBC.write(size)
    f_CBC.write(b'\n')
    f_CBC.write(max_color)
    f_CBC.write(b'\n')

    for data in data_generator(pixs, 16): 
        try :
            ciphertext = cipher_CBC.encrypt(data)
        except:
            print(data)
        f_CBC.write(bytes(ciphertext))
    f_CBC.close()

    ppmPicture = "./" + file + "_aes_CBC.ppm"
    im = Image.open(ppmPicture)
    im.save("./" + file + "_aes_CBC.jpg" , 'JPEG')


if __name__ == "__main__":
    filename = sys.argv[1]
    key = sys.argv[2]
    if os.path.exists('./'+filename) is not True: print('No file, please put the picture file in the directory')
    else: prepare(filename , key)
