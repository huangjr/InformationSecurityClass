# a22727_HW3_report
## ECB
ECB的程式碼寫在prepare的function裡面，如下：  
```python=
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
```
這段ECB的程式碼是照著助教的code做修改，padding的方式也是複製助教上次給的程式碼，ECB的製作方式是用import AES，call AES裡面的MODE_ECB，我們開了一個＿Encrypt_ECB.ppm檔，將每一個block也就是16btyes的資料做ECB加密，中間使用data_generator的function將資料每16bytes也就是一個block一個block的方式yield出去作加密，為了方便除錯所以寫在try跟except裡面，若加密成功會再將加密完的block寫入＿Encrypt_ECB.ppm檔，最後全部完成後再將＿Encrypt_ECB.ppm檔轉乘jpg檔。  
data_generator的function如下：
```python
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
```
data是暫存規定數量number的list，當他儲存資料到達規定的number就會丟出去，並清空，讀取到最後面的資料有很大的機會是不滿規定的number數量，故用pad的function讓他到達到規定的數量，pad的function是複製助教pad的程式碼，就不放上來了。  
## CBC
CBC的程式碼寫在prepare的function裡面，如下：  
```python=
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
```
這段CBC的程式碼是照著ECB的code做修改，唯一的差別是CBC中間的串流要自己寫，不能call現成的程式碼，所以在try下的程式碼，寫了一個CBC_encrypt的function如下：  
```python=
 def CBC_encrypt(text, key, iv):
    cipher_ECB = AES.new(pad(key, 16), AES.MODE_ECB)
    data = ""
    for a,b in zip(text, iv):
        c = format(a^b, '#04x')
        # make the string:0x00 form, or some informaiton would lose
        data += c[2:]
    cText = bytes.fromhex(data)
    cText = cipher_ECB.encrypt(cText)
    return cText
    f_CBC = open("./" + file.split(".")[0] + "_Encrypt_CBC.ppm", "wb")
```
一開始的iv是寫死的，每一個block的資料都丟進CBC_encrypt作加密的動作，把原文跟iv做XOR，做完的東西再去做ECB加密，加密完的資料就是下一輪的iv。下一輪block會再重新call一次CBC_encrypt的function，此時丟進來的iv已經是上一輪加密完的密文，因此每次的iv都會不一樣。


  
## DIY
I aims to invent an protocol that can quickly generate cipherText with parallel execution. Maybe generate the key once and use for all the data in the recent time.
I came up with a concept that use a tree structure to build the initial value, which is a little complicate and maybe difficult to implement, but it is a start.
![](https://i.imgur.com/XoHPuDu.png)
which a tree is created from leaves, the first ciphertext of first two block generate the initail value for 3 and 4 block, and the ciphertext of 3 and 4 xor togather and xor togather with 1 and 2, and do this thing recursively until the last block is encrypt.
The decryption do the same thing. Decrypt and use iv to get the second initial value, and recursively doing so until the last block.
The benefit of this algorithm is it provide another layer of diffusion, which all of the block has the information of all previous block.
