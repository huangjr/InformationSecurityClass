# a22727_HW3_report
## ECB
ECB的程式碼寫在prepare的function裡面，如下：  
```python
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
原圖如下：  
![](https://i.imgur.com/Bvd2YQA.jpg)  
ECB加密過後的圖案如下：  
![](https://i.imgur.com/xUPlaEh.jpg)

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

CBC加密過後的圖案如下：(原圖與ECB的原圖相同)  
![](https://i.imgur.com/SPKPvIu.jpg)

  
## DIY
DIY的程式碼寫在prepare的function裡面，如下： 
```python=
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
            # iv = ciphertext  
            stack.push(new_iv)
            iv = stack.pop()
            
        except:
            print(data,'WRONG')
        f_DIY.write(bytes(ciphertext))
    f_DIY.close()

    ppmPicture = "./" + file.split(".")[0] + "_Encrypt_DIY.ppm"
    im = Image.open(ppmPicture)
    im.save("./" + file.split(".")[0] + "_Encrypt_DIY.jpg" , 'JPEG')
```
這段DIY的程式碼是照著ECB的code做修改，唯一的差別是DIY中間的串流是自己寫的，每次的block不是用之前的16而是用32bytes，所以在try下的程式碼，寫了一個DIY_encrypt的function如下：
```python
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
```
我們每一個block的加密方式是從原圖中取32bytes，再拆成兩半分別是a,b，a,b各自先做AES的ECB加密，加密的key就跟其他加密法的key都一樣，只是各自加密完後，再各自跟iv做XOR，XOR的function如下圖，因為後面一直用到XOR，所以寫個function呼叫比較快，程式碼也會比較清楚，兩邊與iv作完XOR的兩半各自為a_cipher與b_cipher，這兩半最後會加在一起變成32bytes再傳出去寫進_Encrypt_DIY.ppm檔案裡，變成加密過後的檔案，但是新的iv會是a_cipher與b_cipherXOR下的產物，傳給下一輪的block變成新的iv，把資訊帶給下一輪，有點像是CBC的概念，但是最特別的是他並不是完全複製CBC的概念，因為我們將產生出的iv放進一個BubbleStack裡面，他是一個tree，並不是每一輪的block都是拿到上一輪兩半ciphertextXOR後的新iv，下面會配合圖片詳細敘述。
```python
def XOR(a, b):
    # text_h = text.hex()
    # iv_h = iv.hex()
    data = ""
    for a1,b1 in zip(a, b):
        c = format(a1^b1, '#04x')
        data += c[2:]
    cText = bytes.fromhex(data)
    return cText
```
以下是我們iv產生的流程圖
![](https://i.imgur.com/nO0ggAc.png)





爸

