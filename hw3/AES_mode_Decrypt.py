#!/usr/bin/env python
from Crypto.Cipher import AES
from PIL import Image
import AES_mode_Decrypt, doctest, bubbleStack, math, os, sys
from PIL import ImageFile
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

def data_generator_2(pixs, number):     # return a pair of blocks
    '''
    # test docstring
    >>> image = b'a;lskdjfoiaefkddsfdssfks'
    >>> data_generator_2(image, 8)
    [b'a;lskdjf',b'oiaefkdd']
    '''
    segment = []
    for block in data_generator(pixs, number):
        if(len(segment)<2):
            segment.append(block)
        else: 
            yield segment
            segment = []
    

def pad(text, num):
    padding = num - (len(text) % num)
    return text + bytes([padding] * padding)

def xor(a,b):
    '''
    xor function for bytes operation, a,b should both be bytes type
    '''
    data = ""
    # second xor text with iv
    for a1,b1 in zip(a, b):
    # make the string in 0x00 form, or some informaiton would lose
        c = format(a1^b1, '#04x')
        data += c[2:]
    pText = bytes.fromhex(data)
    return pText

def CBC_decrypt(text, key, iv):
    cipher_ECB = AES.new(pad(key, 16), AES.MODE_ECB)
    # first decrypt
    pText = cipher_ECB.decrypt(text)
    data = ""
    # second xor text with iv
    for a,b in zip(pText, iv):
        # make the string in 0x00 form, or some informaiton would lose
        c = format(a^b, '#04x')
        data += c[2:]
    pText = bytes.fromhex(data)
    # encrypt text with key in ECB mode
    # return text for next round's iv
    return pText

def prepare(file, text):
    key = bytes(text, encoding = "utf8")
    ppmPicture = "./" + file.split(".")[0] + ".ppm"
    im = Image.open("./" + file)
    im.save(ppmPicture)
    f = open(ppmPicture,'rb').read()
    ppm_type, size, max_color, pixs = f.split(b'\n', 3)
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    

    #### for AES_ECB_MODE
    f = open("./" + file.split(".")[0] + "_Encrypt_ECB.ppm",'rb').read()
    cipher_ECB = AES.new(pad(key, 16), AES.MODE_ECB) 
    f_ECB = open("./" + file.split(".")[0] + "_Decrypt_ECB.ppm", "wb")
    f_ECB.write(ppm_type)
    f_ECB.write(b'\n')
    f_ECB.write(size)
    f_ECB.write(b'\n')
    f_ECB.write(max_color)
    f_ECB.write(b'\n')
    
    for data in data_generator(pixs, 16):
        try:
            ciphertext = cipher_ECB.decrypt(data)   # only change to decrypt
        except:
            print(data)
        f_ECB.write(bytes(ciphertext))
    f_ECB.close()

    ppmPicture = "./" + file.split(".")[0] + "_Decrypt_ECB.ppm"
    im = Image.open(ppmPicture)
    im.save("./" + file.split(".")[0] + "_Decrypt_ECB.jpg", 'JPEG')

    # #### for AES_CBC_MODE
    # f = open("./" + file.split(".")[0] + "_Encrypt_CBC.ppm",'rb').read()
    # ppm_type, size, max_color, pixs = f.split(b'\n', 3)
    # # iv should be explicit defined
    # iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    # f_CBC = open("./" + file.split(".")[0] + "_Decrypt_CBC.ppm", "wb")
    # f_CBC.write(ppm_type)
    # f_CBC.write(b'\n')
    # f_CBC.write(size)
    # f_CBC.write(b'\n')
    # f_CBC.write(max_color)
    # f_CBC.write(b'\n')

    # for data in data_generator(pixs, 16): 
    #     try :
    #         plaintext = CBC_decrypt(data, key, iv)
    #         iv = data
    #     except:
    #         print(data)
    #     f_CBC.write(bytes(plaintext))
    # f_CBC.close()

    # ppmPicture = "./" + file.split(".")[0] + "_Decrypt_CBC.ppm"
    # im = Image.open(ppmPicture)
    # im.save("./" + file.split(".")[0] + "_Decrypt_CBC.jpg" , 'JPEG')

    # for AES_DIY_MODE
    f = open("./" + file.split(".")[0] + "_Encrypt_DIY.ppm",'rb').read()
    ppm_type, size, max_color, pixs = f.split(b'\n', 3)
    # iv should be explicit defined
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    f_CBC = open("./" + file.split(".")[0] + "_Decrypt_DIY.ppm", "wb")
    f_CBC.write(ppm_type)
    f_CBC.write(b'\n')
    f_CBC.write(size)
    f_CBC.write(b'\n')
    f_CBC.write(max_color)
    f_CBC.write(b'\n')

    # stack for store iv, and generate iv
    stack = bubbleStack.BubbleStack(int(math.log(int(len(pixs)/16), 2)))

    for data_couple in data_generator_2(pixs, 16):
        try :
            #xor togather
            print(data_couple)
            next_iv = xor(data_couple[0], data_couple[1])
            #store into stack
            stack.push(next_iv)
            #xor with iv
            p1 = xor(data_couple[0], iv)
            p2 = xor(data_couple[1], iv)
            #decrypt with AES
            plaintext = cipher_ECB.decrypt(p1) + cipher_ECB.decrypt(p2)
            iv = stack.pop()
        except:
            print(data,)
        f_CBC.write(bytes(plaintext))
    f_CBC.close()

    ppmPicture = "./" + file.split(".")[0] + "_Decrypt_DIY.ppm"
    im = Image.open(ppmPicture)
    im.save("./" + file.split(".")[0] + "_Decrypt_DIY.jpg" , 'JPEG')



if __name__ == "__main__":
    filename = sys.argv[1]
    key = sys.argv[2]
    # doctest.testmod(AES_mode_Decrypt)
    if os.path.exists('./'+filename) is not True: print('No file, please put the picture file in the directory')
    else: prepare(filename , key)
