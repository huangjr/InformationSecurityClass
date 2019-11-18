from Crypto.Cipher import AES
from PIL import Image
import sys, os

# def data_generator(information, block_num):
#     info = []
#     for x in information:
#         info.append(x)
#         if len(info) == block_num:
#             yield bytes(info)
#             info = []
#     # padding        
#     if len(info) != 0:
#         info.extend([0]*(block_num-len(info)))
#         yield bytes(info)

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

# for AES_ECB_MODE
size = 32
key = b'iloveyou'
ppmPicture = "./penguin.ppm"
im = Image.open("./penguin.jpg")
im.save(ppmPicture)
cipher_ECB = AES.new(pad(key, 16), AES.MODE_ECB) 
f = open("./penguin.ppm",'rb').read()
ppm_type, size, max_color, pixs = f.split(b'\n', 3)
f = open("./penguin_aes_ECB.ppm", "wb")
f.write(ppm_type)
f.write(b'\n')
f.write(size)
f.write(b'\n')
f.write(max_color)
f.write(b'\n')
   

for data in data_generator(pixs, size): 
    ciphertext = cipher_ECB.encrypt(data)
    f.write(bytes(ciphertext))
f.close()

# for AES_CBC_MODE
iv = os.urandom(16)
cipher_CBC = AES.new(pad(key, 16), AES.MODE_CBC, iv) 
f = open("./penguin.ppm",'rb').read()
f = open("./penguin_aes_CBC.ppm", "wb")
f.write(ppm_type)
f.write(b'\n')
f.write(size)
f.write(b'\n')
f.write(max_color)
f.write(b'\n')

for data in data_generator(pixs, size): 
    ciphertext = cipher_CBC.encrypt(data)
    f.write(bytes(ciphertext))
f.close()
