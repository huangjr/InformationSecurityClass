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
```python
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
```python
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
```python
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
第一輪的iv一開始也是寫死的，跟CBC相同，如上圖的IV0，藍色的圈圈是我們原圖的資料，每一個藍圈圈都是16bytes，兩個藍圈圈是一個block共32bytes，兩個藍圈圈會丟到上述的DIY_encrypt的function，此時第一輪放進DIY_encryptfunction的iv是IV0，作完DIY_encrypt後產生的new_iv會是上圖的紅圈1，這裡剛好就是IV1，也就是第二輪，第3藍圈圈與第4藍圈圈做DIY_encrypt的iv，因為我們儲存新iv的方式是放進一個stack裡面，這個stack是呼叫一個Class叫BubbleStack，程式碼如下，他讓每一輪的iv都是好幾輪的iv做merge，這裡我們的merge其實就是xor，也就是好幾輪的ciphertext的資訊會一路帶到好幾輪後，stack的功能則是他會依照樹的層級，幫忙merge新iv，例如第一輪的block經過DIY_encrypt產生出紅圈1，第二輪的block經過DIY_encrypt(這輪做DIY_encrypt是用IV1)產生出紅圈2，此時的紅圈1與紅圈2都是第一層，stack會將第一層的紅圈1及紅圈2做merge(我們是用xor的方式merge)產生出第三輪要用的IV2(也就是紅圈3)，做第三輪的block時(第5第6藍圈圈)，這輪做DIY_encrypt是用IV2，經過DIY_encrypt後產生出新的iv是紅圈4此時就是IV3，做第四輪時(第7第8藍圈圈)，做DIY_encrypt是用IV3，然後產生出紅圈5，紅圈5放進stack時會與紅圈4做merge，產生出紅圈6，而紅圈6又會與先前的紅圈3做merge產生出紅圈7也就是IV4給下一輪用，以此類推。  


stack流程如下(左邊是每一輪做完DIY_encrypt的產物以數字代表，也就是上圖的紅圈圈，灰色是stack，右邊的線是做DIY_encrypt)：
![](https://i.imgur.com/5RuZ1ra.png)

BubbleStack的Class程式碼如下：
```python
class BubbleStack:
    # constructor
    stack = []
    def __init__(self, size):
        self.stack = [None]*size
    # public operation:
    '''
    void push(value): put a value into the stack
    int pop():  get a value from the stack
    '''
    def push(self,data):
        '''
        push the iv into stack
        '''
        j=0
        new = data
        while(self.__get(j) != None):
            new = self.__merge(self.__get(j), new)
            j+=1
        self.__set(j, new)
        self.__clear(j)

    def pop(self):
        '''
        get the first value of stack
        '''
        j=0
        while(self.__get(j) == None):
            j+=1
        return self.__get(j)

    # private method
    def __merge(self,a,b):
        data = ""
        # second xor text with iv
        for a1,b1 in zip(a, b):
            # make the string in 0x00 form, or some informaiton would lose
            c = format(a1^b1, '#04x')
            data += c[2:]
        pText = bytes.fromhex(data)
        # encrypt text with key in ECB mode
        # return text for next round's iv
        return pText

    def __clear(self, index):
        j=0
        while(j < index):
            self.__set(j, None)
            j+=1

    def __get(self, index):
        return self.stack[index]

    def __set(self, index, value):
        self.stack[index] = value
```
我們自製的加密方法實作後發現效果並不是那麼好，如果大片的顏色相似，兩兩一組加密(一樣的key)又跟一樣的iv做XOR寫出來的加密東西會相似，雖然下一輪的IV有加上merge的部分，也就是跟stack裡上一次的iv做merge也就是XOR，並沒有把iv打亂，特別是在大片顏色一樣的地方，在做merge時，可能前組的iv跟下一組iv太類似，再做一次XOR有點會像似還原的狀況，這是我們想出來可能造成加密效果不好的原因，但是助教說只要加密方法看起來很酷就行，用tree的方式製造iv還滿特別的。 
DIY加密過後的圖片如下：(原圖與前組相同，都是hello_kitty.jpg)  
![](https://i.imgur.com/Sw45OQe.jpg)

