# HW2_說明文件_Encrypt

----
## 分工
隨班附讀 a22727    黃婕雅 Encrypt  
四材料四 B10504028 林哲豪 Decrypt  


## 環境
MacOS Sierra 10.12.6.  Python 3 

## Decrypt 程式說明

### hexToBinary(hex)    
>Input: 'afafafafafafafaf'  
>Output: '1010111110101111101011111010111110101111101011111010111110101111'  

用來從16進位轉換成2進位

```python
def hexToBinary(hex):
    return bin(int(hex, 16))[2:].zfill(64)
```
### keyShift(c, d, round_number)   
>Input: '10000', '01000', 1   
>Output: '0000110000'  

key的部分依據不同回合，左移不同的位置，第1,2,9,16回合往左移一位，原本第一位的數字移到最後，其他回合左移二位，原本第一,二位的數字移到最後  

```python
def keyShift(c, d, round_number):   
    c1 = []
    d1 = []
    if round_number is 1 or round_number is 2 or round_number is 9 or round_number is 16:
        # print('1 right')
        c1 = c[1:] + c[0:1]
        d1 = d[1:] + d[0:1]
        return c1+d1
    else:
        # print('2 right') 
        c1 = c[2:] + c[0:2]
        d1 = d[2:] + d[0:2]
        return c1+d1
```
### Function(Right_32bit, round_key)   
>Input: ['1', '0', '0', '0', '0', '1', '1', '1', '0', '1', '0', '1', '0', '1', '0', '1', '1', '0', '0', '0', '0', '1', '1', '1', '0', '1', '0', '1', '0', '1', '0', '1'],  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ['0', '1', '0', '0', '1', '1', '1', '1', '0', '1', '1', '0', '1', '1', '0', '1', '0', '0', '1', '1', '0', '1', '0', '1','1', '0', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1']  

>Output: ['1', '0', '1', '1', '0', '0', '1', '1', '1', '1', '1', '0', '1', '0', '1', '0', '1', '1', '1', '1', '1', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0', '1']  

每一回合原本右半部的資料要做function的動作，其中function包含  
1. 32bits利用table E擴展成48bits  
2. 與每一回合的key做XOR  
3. 48bits分成八組，每六個一組放入Sbox查表  
4. 最後組出來的資料再去P查表，重新排位置  

```python
def Function(Right_32bit, round_key):
    r1 = [] 
    r1_48btis = []
    Expansion = permutateToTable(Right_32bit,E)
    for i, j in zip(Expansion,round_key):
        r1_48btis.append(int(i)^int(j))
    for n, i in enumerate(range(0, len(r1_48btis), 6)):
        r1.append(sBox(r1_48btis[i:i+6],n))
    r1_str = ''.join([char for char in r1])
    return permutateToTable(r1_str,P)
```

### sBox(six_bit, sbox_number)   
>Input: [0, 0, 1, 1, 0, 1], 1    
>Output: 1000  

前面做好的每六個一組的資料餵進sBox,並告知是要查第幾個sbox表，將第一個及最後一個合成row,中間四個合成column，去查sbox表，查完的數字再轉回2進位  

```python
def sBox(six_bit, sbox_number):
    row = str(six_bit[0]) + str(six_bit[-1])
    column = "".join([str(char) for char in six_bit[1:-1]])
    number = Sboxes[sbox_number][ int(row,2)*16 + int(column,2) ]
    return '{0:04b}'.format(number)
```

### permutateToTable(origin,table)   
>Input: 10001000011110110011100110010000, P
>Output: ['1', '0', '1', '1', '0', '1', '1', '0', '1', '1', '0', '0', '1', '0', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '1', '0', '1']  
  
將要重新排列組合的資料放進permutateToTable，並告知是要依照哪一個table做重新排列組合

```python
def permutateToTable(origin,table):
    afterTable = []
    for order in table:
        afterTable.append(origin[order - 1])
    return afterTable
```

### encrypt(key, plaintext)   
>Input: afafafafafafafaf, abcdef0123456789     
>Output: 4C30FC30FB2B0BFF   

先將16回合的keys製作出來，把key從16進位轉成2進位，再到PC1表查詢轉換過位置的樣子，而且此時會從64bits變成56bits,再將56bits拆成兩半各自為C及D,  
總共有16回合，將每一回合拆成兩半的C和D放進keyShift function裡，並告知是第幾回,每一回要位移的的數目並不相同,將每一回產生出的第一版key放進every_round_keys裡面,製作下一round的第一版key時,再將C及D更新,依此類推共生出16round的第一版keys,第一版的key會是C＋D的長度會是56bits,每一回合的key都還要丟到PC2重新排列組合變為48bits，再塞入every_round_keys_forFunc裡面,也就是最終版每一回合的key都儲存在裡面了  
<br/>
接著將plaintext做整理，將原來的16進位改成2進位, 並到IP查表後重新排列組合,切成兩半為L與R, 開始做Feistel Network, 總共有16回合，每一回合的R直接轉給下一回合input的L,而下一回合的R則是原本的R做function再與原本的L做XOR,也就是R1,再指給下一round新的一組L與R  
<br/>
最後一round的L與R,要左右交換後結合在一起,再到IP_INV查表重新排列組合,最後再把2進位轉回16進位,再換成大寫的形式輸出ciphertext    

```python
def encrypt(key, plaintext):
    Binary_key = hexToBinary(key)
    AfterPC1 = []
    AfterPC1 = permutateToTable(Binary_key,PC1)
    C = AfterPC1[:28]
    D = AfterPC1[28:]

    # make every round keys
    every_round_keys = []
    every_round_keys_forFunc = [['' for i in range(48)] for j in range(16)]
    for round_number in range(1, 16+1):
        every_round_keys.append(keyShift(C,D,round_number))
        C = every_round_keys[round_number - 1][:28]
        D = every_round_keys[round_number - 1][28:]
        every_round_keys_forFunc[round_number - 1] = permutateToTable(every_round_keys[round_number - 1],PC2)

    # prepare the plaintext
    Binary_plaintext = hexToBinary(plaintext)
    AfterIP = []
    AfterIP = permutateToTable(Binary_plaintext,IP)
    L = AfterIP[:32]
    R = AfterIP[32:]   

    # do the Feistel Network
    for round_number in range(1, 16+1):
        R1 = []
        for i, j in zip( L , Function(R, every_round_keys_forFunc[round_number - 1])):
            R1.append(str(int(i)^int(j)))
        L = R  
        R = R1

    # combine the last round 
    Final_64bit = [str(char) for char in (R+L)]
    AfterIP_INV = permutateToTable(Final_64bit,IP_INV)
    Ciphertext_binary = ''.join(AfterIP_INV)
    Ciphertext_hex = hex(int(Ciphertext_binary,2))[2:]
    Ciphertext = Ciphertext_hex.upper()
    return Ciphertext
```
### Command line 
>Input: ./EncryptDES.py afafafafafafafaf abcdef0123456789    
>Output: 4C30FC30FB2B0BFF  

進到目錄底下，就可以用command line 輸入執行檔名稱、key、plaintext就可以得到DES加密後的ciphertext     

```python
import sys

Key = sys.argv[1]
Plaintext = sys.argv[2]
# Plaintext = 'abcdef0123456789'
# Key = 'afafafafafafafaf'

if len(Key) != 16: print('Key\'s length is not 16')
elif len(Plaintext) != 16: print('Plaintext\'s length is not 16')
else : print(encrypt(Key,Plaintext))
```
