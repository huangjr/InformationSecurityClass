# a22727_HW3_report
## ECB
all of the blocks encrypted with the same key, think there could be some parallel mechanism to do this in order to get higher performance.
My partner write the code of ECB.
這個部份是我的隊友做的,我隊友也做了block generator
## CBC
the cipherText of the previous block cipher become the next block's key.
I finish this by just modify some line of encryption code, but basically all of the CBC mode encryption is programmed by me.
這個部分我用了隊友的block generator來做,但主要是以下的程式碼比較複雜,因為資料要先轉成int型態,才能進行xor運算,然後又要再轉成bytes型態,才能做加密  
首先宣告一個ECB mode的AES cipher,其實應該要從頭到尾都用同一個cipher,而不是每一次都從新宣告一個,這樣做很沒有效率,但是因為我想要把所有跟加密有關的東西都放在同一個function裡面,所以也只好這麼做
```python=
def CBC_encrypt(text, key, iv):
    cipher_ECB = AES.new(pad(key, 16), AES.MODE_ECB)
```
接下來做把iv和plaintext做xor運算,因為從bytes中取出的資料就己經是int類型了,所以就直接做xor運算,但有些算出來的結果會是0x01這種的,而他的零會被直接忽略變成0x1,所以我們用上了format()來強制數字的變成0x01,這樣在最後轉成bytes型態時才不會發生問題。    
'#04x'的意義,#代表我們要對int操作,format()會按照最後一個參數分別在字串最前面加上0d,0x,0b等等;0是後綴字;4代表的是最後字串的總長度,0x加上我們要的另外兩個數字,所以長度是4;x就是說我們要轉的是hexadicimal 16進位的數字,所以會在最前面加上0x。
```python=
    data = ""
    for a,b in zip(text, iv):
        c = format(a^b, '#04x')
```
接著就是把數字的部分取出來,轉成bytes型態,最後對他進行加密就完成了。
```python=
        data += c[2:]
    cText = bytes.fromhex(data)
    cText = cipher_ECB.encrypt(cText)
    return cText
```
下面是對於block的操作部分
首先用data_generator,從block裡面依次取出16個字元
```python=
for data in data_generator(pixs, 16): 
    try :
```
接著拿iv來對ciphertext進行解密
```python=
        plaintext = CBC_decrypt(data, key, iv)
```
然後拿目前的cipherText當下一次的iv
```python=
        iv = data
```
如果以上的操作有失敗的話,就把cipherText給印出來.
```python=
    except:
        print(data)
```
如果沒有例外發生的話,就把解密的結果給寫到檔案中,但這裡其實有一個怪怪的地方,就是如果上面的操作發生意外的
```python=
    f_CBC.write(bytes(plaintext))
```
如果所有的檔案都寫完了,就把檔案給關掉
```python=
f_CBC.close()

```
## DIY
I aims to invent an protocol that can quickly generate cipherText with parallel execution. Maybe generate the key once and use for all the data in the recent time.
I came up with a concept that use a tree structure to build the initial value, which is a little complicate and maybe difficult to implement, but it is a start.
![](https://i.imgur.com/XoHPuDu.png)
which a tree is created from leaves, the first ciphertext of first two block generate the initail value for 3 and 4 block, and the ciphertext of 3 and 4 xor togather and xor togather with 1 and 2, and do this thing recursively until the last block is encrypt.
The decryption do the same thing. Decrypt and use iv to get the second initial value, and recursively doing so until the last block.
The benefit of this algorithm is it provide another layer of diffusion, which all of the block has the information of all previous block.
