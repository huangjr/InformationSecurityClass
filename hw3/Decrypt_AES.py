from PIL import Image
from Crypto.Cipher import AES
import os, sys

"""
jpg to ppm-p3, p3 is easier to operate, while p6 is smaller
ppmPicture="./img/car.ppm"
im = Image.open("./img/car_jpg.jpg")
im.save(ppmPicture,"ppm")
"""

"""
ppm to jpg
ppmPicture = "./img/test.ppm"
im = Image.open(ppmPicture)
im.save('./img/test.jpg', "jpeg")
"""

# DES ECB mode: block:128 bits, key:128 bits
# encrypt image by 16 words
# collect 16 word from file
# declaration of ciphertext for the big block
def ECB(ciphertext, key):
    plaintext = ""
    cipher = AES.new(key, AES.MODE_ECB)
    # cut with a block of 16, the data is well block
    for a in range(int(len(ciphertext)/16)):
        # encrypt a block of 16 bytes or 128 bits
        plaintext += cipher.decrypt(ciphertext[a*16:a*16+16].encode("cp875"))
    unpad(plaintext)
    return plaintext


# AES CBC mode: block:128 bits, key:128 bits
# encrypt image by 16 words and feed the previous ciphertext as the next key
def CBC(ciphertext, iv, key):
    plaintext = ""
    cipher = AES.new(key, AES.MODE_ECB)
    # xor the first block with iv
    for a in range(int(len(ciphertext)/16)):
        if a==0:
            block = plaintext[0:a*16]^iv[:-1]
            plaintext + cipher.decrypt(block.encode("cp875"))
        else:
            block = ciphertext[a*16:a*16+16]^ciphertext[a*16-16:a*16]
            plaintext + cipher.decrypt(block.encode("cp875"))
    unpad(plaintext)
    return plaintext


# padding mechanism, fill the unfill character with the number of loss character.
# ex: lose 5:55555, lose 7:7777777 etc...
def pad(text):
    padding = 16 - (len(text))
    return text+bytes([padding]*padding)

def unpad(text):
    padding = text[-1]
    # -1 = last, suppose the last number was 5:0~-5, and the real data is in -6
    # this mechanism is genius
    return text[:-padding]

if __name__ == "__main__":
    # enter command like: python Decrypt_AES.py mode key file (initial value)
    # generate random key
    key = os.urandom(32)
    # recieve key from command line, key length = 32 bytes or 128 bits
    # key = sys.argv[2]
    filename = "./img/car.ppm"
    # filename = sys.argv[3]
    # iv = sys.argv[4]
    # intermediate ppm file
    ppmfile = "./tmp.ppm"
    im = Image.open(filename, 'r')
    im.save(ppmfile, "ppm")

    imgFile = open(ppmfile, "r", encoding="cp875")
    # can't decode the hex file->try P3, use cp875 and everything works!!
    lines = imgFile.readlines()
    # store the header of original file
    header = ""
    for i in range(2):
        header + lines[i]

    # encrypt the image
    ciphertext = lines[3]
    if sys.argv[1] == "ECB": plaintext = ECB(ciphertext, key)
    elif(sys.argv[1] == "CBC"): plaintext = CBC(ciphertext, iv, key)

    # generating the fileName.ppm file
    im = open(ppmfile, "x") # x refer to create mode
    im.write(header)
    im.write(plaintext)
    im.close()

    # saving to fileName.jpg file
    im = Image.open(ppmfile)
    im.save("./test.jpg", "jpeg")