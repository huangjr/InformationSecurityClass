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
        data.extend([0]*(32 - len(data)))
        yield bytes(data)

def pad(text, num):
    padding = num - (len(text) % num)
    return text + bytes([padding] * padding)


size = 32
key = b'11111111'
ppmPicture = "./penguin.ppm"
im = Image.open("./penguin.jpg")
im.save(ppmPicture)
f = open("./penguin.ppm",'rb').read()
ppm_type, size, max_color, pixs = f.split(b'\n', 3)


# for AES_ECB_MODE
cipher_ECB = AES.new(pad(key, 16), AES.MODE_ECB) 
f_ECB = open("./penguin_aes_ECB.ppm", "wb")
f_ECB.write(ppm_type)
f_ECB.write(b'\n')
f_ECB.write(size)
f_ECB.write(b'\n')
f_ECB.write(max_color)
f_ECB.write(b'\n')
   
for data in data_generator(pixs, size):
    ciphertext = cipher_ECB.encrypt(data)
    f_ECB.write(bytes(ciphertext))
f_ECB.close()

# for AES_CBC_MODE
iv = os.urandom(16)
cipher_CBC = AES.new(pad(key, 16), AES.MODE_CBC, iv) 
f_CBC = open("./penguin.ppm",'rb').read()
f_CBC = open("./penguin_aes_CBC.ppm", "wb")
f_CBC.write(ppm_type)
f_CBC.write(b'\n')
f_CBC.write(size)
f_CBC.write(b'\n')
f_CBC.write(max_color)
f_CBC.write(b'\n')

for data in data_generator(pixs, size): 
    ciphertext = cipher_CBC.encrypt(data)
    f_CBC.write(bytes(ciphertext))
f_CBC.close()
