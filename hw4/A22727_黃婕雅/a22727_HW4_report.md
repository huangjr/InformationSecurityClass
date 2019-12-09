# a22727_HW4_report 

## 建置環境  
MacOS Sierra 10.12.6. Python 3  

## 操作方式與執行結果
* 初始化RSA的p與q長度  

  指令： (python ./Rsa.py init {bit長度})
  > python ./Rsa.py init 10  
  
  執行結果：  
  ![](https://i.imgur.com/8Nq2F8S.png)  
  第一行是印出bit的長度，第二,三行是p與q的數字以及執行過miller_rabin Test是否為prime的結果,第四,五行是e與d,第六行是印出gcd(e, phi_n)的結果,
  第七行是印出e*d % phi_n的結果，確認兩項都是1表示程式碼產生出來的e與d是正確的。第八行則是印出n的數字。上述的數字會用到後面指令的加解密。  
  
* RSA加密  

  指令： (python ./Rsa.py -e {plaintext} {n} {e})  
         設plaintext：SOS, n: 800881, e: 400439  
  > python ./Rsa.py -e SOS 800881 400439    
  
  執行結果：  
  ![](https://i.imgur.com/vdz7dwh.png)  
  印出ciphertext,這裡是㝳髵㝳,當init的bit數輸入較大時,用前面所產生出來的n以及e都會較大,在做完RSA加密後的數字也會變大,無法轉成可見字元,此時會印出
  加密後的數字,並用','相連,如下圖,先做初始化50個bit產生出n及e,再用來做加密：  
  ![](https://i.imgur.com/1OJTtI6.png)  
  此時的n為8968138575292343660932279537,e是4484069287646171830466139767,轉出來的三個加密數字6503239710066372034480909034,8593655076183664752095032237,6503239710066372034480909034
  太大,會用逗號的方式相連印出加密數字。  
  
* RSA解密  

  指令： (python ./Rsa.py -d {ciphertext} {p} {q} {d} {n})  
  設ciphertext：㝳髵㝳, p: 907, q: 883, d: 673367, n: 800881  
  > python ./Rsa.py -d 㝳髵㝳 907 883 673367 800881  
  
  執行結果：  
  ![](https://i.imgur.com/jerXjDI.png)  
  印出plaintext是SOS,與加密前的訊息一致。若ciphertext不是可見字元,而是加密後的數字,一樣可以當作解密的input,用上述的例子解密,如下圖： 
  
  > python ./Rsa.py -d 6503239710066372034480909034,8593655076183664752095032237,6503239710066372034480909034 63508718965969 141211139530273 3236007956662825865655592775 8968138575292343660932279537
  
  ![](https://i.imgur.com/RkrAb5v.png)   
  ciphertext是6503239710066372034480909034,8593655076183664752095032237,6503239710066372034480909034,而p是63508718965969, q是141211139530273, d是3236007956662825865655592775, n是8968138575292343660932279537
  
## 程式碼解說  

* RSA的Class  

寫了一個RSA的Class, 給定一個bit的長度, 會得到p, q, n, e, d, phi_n 這些與加密和解密需要用到的資訊。  

```python
class RSA():
    # bit is the length of p and q
    def __init__(self, bit):
        self.bit_length = bit
        self.p = random.getrandbits(self.bit_length)
        self.q = random.getrandbits(self.bit_length)

        # check if p and q are both prime and not 0, here we use miller_rabin function to check prime
        while self.p == 0 or miller_rabin(self.p, 4) == False:
            self.p = random.getrandbits(self.bit_length)
        while self.q == 0 or miller_rabin(self.q, 4) == False:
            self.q = random.getrandbits(self.bit_length)

        # get n
        self.n = self.p * self.q

        # get phi_n
        self.phi_n = ( self.p - 1 ) * ( self.q - 1 )

        # get e
        for i in range(self.n // 2 , 2, -1):
            if math.gcd(i, self.phi_n) == 1:
                self.e = i
                break

        # get d
        self.d = modInverse(self.e, self.phi_n)
```  

  * miller_rabin(n,k)做質數的測試      

其中RSA的Class, 會用到的function分別是miller_rabin(n,k)以及modInverse(a, m),程式碼有寫註解, miller_rabin這裡的測試次數設4, 
k越高則是質數的機會越高。  

```python
# use miller rabin test to check if n is prime, do k times in miller rabin test to enhence the accuracy
def miller_rabin(n, k):
    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    # to get s and r from the equation: n - 1 = 2**r*s 
    while s % 2 == 0:
        r += 1
        s //= 2
    # check n for k times
    for _ in range(k):
        a = random.randrange(2, n - 2)
        # x = a**s % n 
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        # to check x**2 % n from the equation: a**(s*2j) == n−1 (mod n), if not then n is not prime
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True
```

  * modInverse(a, m)尋找乘法反元素

在找d時用到的方法, 在phi_n下找e的乘法反元素, 心得遇到困難裡有說明因為當bit數變長後, 處理速度會很慢, 因此找d的方法改成用Euclidian algorithm。  

```python
# find a**-1 in mod m
def modInverse(a, m) : 
    m0 = m 
    y = 0
    x = 1  
    if (m == 1) : 
        return 0
    while (a > 1) :   
        # q is quotient 
        q = a // m 
        t = m   
        # m is remainder now, process 
        # same as Euclid's algo 
        m = a % m 
        a = t 
        t = y 
        # Update x and y 
        y = x - q * y 
        x = t 
    # Make x positive 
    if (x < 0) : 
        x = x + m0 
    return x
```

* RSA的初始化  

呼叫前面敘述的RSA Class, 下指令時給定一定長度的bit數, 得到相對應的RSA資訊, 如p, q, n, e, d, phi_n, 並顯示在畫面上。  

```python
    # initial the RSA, and give the length of p, q
    if sys.argv[1] == 'init':
        bit = sys.argv[2]
        rsa = RSA(int(bit))
        p = rsa.p
        q = rsa.q
        n = rsa.n
        e = rsa.e
        d = rsa.d

        print(rsa.bit_length, '=the length of bit for p and q')
        print(p, '=p', 'Is prime?', miller_rabin(p, 4))
        print(q, '=q', 'Is prime?', miller_rabin(q, 4))
        print(e, '=e')
        print(d, '=d')
        print('gcd(e, phi_n)=', math.gcd(e, rsa.phi_n))
        print('e*d % phi_n=', e*d % rsa.phi_n )
        print(n, '=n')

```


* RSA的加密  

程式碼裡有註解, 輸入的東西需要plaintext,n以及e, 但因加密過後的數字可能太大無法轉成可見字元, 若遇到該問題會在except裡印出加密過後的數字, 不然一律
皆在try裡印出加密過後的數字再轉成可見字元的樣式。  

```python
    # use RSA to encrypt, the input should be plaintext, n and e
    # the output is the ciphertext, if the number can transfer to acsii, then we can see the words
    # if the number cannot transfer to acsii, then we see the ciphered number 
    if sys.argv[1] == '-e':
        plaintext = sys.argv[2]
        n = int(sys.argv[3])
        e = int(sys.argv[4])
        ciphertext = []
        # encrypt the plaintext and transfer plaintext to ascii
        for num in [ord(char) for char in plaintext]:
            # ciphertext.append(num ** e % n)
            ciphertext.append(Square_and_Multiply(num, e, n))

        # get ciphertext
        try:
            print(''.join( [chr(number) for number in ciphertext] ))
        except:
            # if we cannot transfer the number to ascii
            print(','.join( [str(number) for number in ciphertext] ))
            print('number above is too large, cannot transfer to ascii')
```

  * 加解密都會用到Square_and_Multiply(message_num, e, n)  

利用Square_and_Multiply加快計算次方的速度, 程式碼如下, 每一輪到下一個bit時, 要先square, 若該bit是1再乘一次, 這樣會大幅降低要計算的次數, 
次方項會大大下降。

```python
def Square_and_Multiply(message_num, e, n):
    # transfer the exponent, 'e' to binary  
    H = bin(e)[2:] 
    # initial the first bit
    ciphertext_number = message_num

    # every round when we go to next bit, we square ourselves
    for i in range(1, len(H)):
        ciphertext_number = pow(ciphertext_number, 2, n)
        # if the bit is 1, we multiply 
        if int(H[i]) == 1:
            ciphertext_number = ciphertext_number * message_num % n
    return ciphertext_number
```

* RSA的解密  

輸入的input要有ciphertext, p, q, d, n, 但因加密過後的數字可能太大無法轉成可見字元, ciphertext有可能是一連串的數字用','連接, 此時會進入
try程式碼裡, 將加密過後的數字也就是ciphertext, 利用中國餘式定理解密, 但若是ciphtertext是正常的可見字元, 會進入except裡解密。

```python
    # use RSA to decrypt, the input should be ciphertext, p, q, d and n
    # the output is the plaintext
    # the input is ciphertext, it could be words or the ciphered numbers which is divided with ','
    if sys.argv[1] == '-d':
        ciphertext = sys.argv[2]
        p = int(sys.argv[3])
        q = int(sys.argv[4])
        d = int(sys.argv[5])
        n = int(sys.argv[6])
        plaintext = []
        
        # decrypt the ciphtertext and transfer ciphertext to ascii
        try:
            # if the number is too large for ascii, the format would be number,number,...
            for num in [int(char) for char in ciphertext.split(',')]:
                plaintext.append(Chinese_Remainder_Theorem(num, p, q, d, n))
        except:
            # the normal situation, the input is ascii
            for num in [ord(char) for char in ciphertext]:
                plaintext.append(Chinese_Remainder_Theorem(num, p, q, d, n))

        # get plaintext
        print(''.join( [chr(number) for number in plaintext] ))
```

  * 解密用到的Chinese_Remainder_Theorem
  
利用中國餘式定理讓解密的速度變快, 根據老師chap0809-part2的第10至12頁的內容寫出, 除此之外也同時可利用Square_and_Multiply讓跑次方的次數降低。  

```python
def Chinese_Remainder_Theorem(message_number, p, q, d, n):
    xp = message_number % p 
    xq = message_number % q
    dp = d % (p - 1)
    dq = d % (q - 1)
    yp = Square_and_Multiply(xp, dp, p)
    yq = Square_and_Multiply(xq, dq, q)
    cp = modInverse(q, p)
    cq = modInverse(p, q)
    # the equation from chinese_remainder_theorem
    x = (q * cp * yp + p * cq * yq) % n
    return x
```

## 困難與心得  
  * 程式碼跑太久  
  
  一開始寫RSA的Class, 計算出p, q, n, e, d都跑很快, 但是當init p跟q的長度到15以上，電腦開始跑不動, 每次測試都要等到好幾分鐘, 導致無法測試, 因次開始
  想原因, 分別將p, q, n, e, d註解起來, 測試是哪一段程式碼卡太久, 結果發現是在產生d的時候卡住, d是e在phi_n下的乘法反元素, 一開始我的找法很笨, 是從2開
  始一個一個測試看哪一個數字會跟e相乘後, 再mod phi_n會是1, 後來決定要改善找d的演算法, 上網查到一個方程式, 決定利用該方程式找d。
  
  * 數學不夠好
  
    * 用錯方程式找d  
  前面為了加快運算速度, 修改找d的演算法, 利用了一個數學方程式是 a**(p - 1) mod p ＝ 1, 因此可以推出 a * a**(p - 2) mod p = 1, 當下思考以為將
  a當作e, 那就可以快速找到d, d就是e的(p - 2)次方, 但是實作後, 發現如此找出來的d無法符合RSA的條件: e*d = 1 mod(phi_n), 這裡卡了一天吧，想不出來
  哪裡錯了, 覺得數學式子是對的吧, 後來才發現我們的RSA無法用該方法找到d, 因為上述的數學式子要成立, 必須符合p是prime, 但是我們的phi_n一定不會是prime,
  因為phi_n是 (p - 1) * (q - 1), 又p跟q都是prime, 質數除了2以外一定是奇數, 奇數減1一定是偶數, 兩個偶數相乘一定還是偶數, 不可能為質數, 該方法無效。
  
    * 找d用Euclidian algorithm以及Bézout’s Theorem   
  看了很久的數學公式, a = bq + r, 則gcd(a,b) = gcd(b,r), 又gcd(a,b)可以寫成 ax + by = gcd(a,b), 所以gcd(e,phi_n) = 1 可以寫成 
  e*x + phi_n*y = 1 mod(phi_n), 這樣就可以得到 e*x = 1 mod(phi_n), 此時可以用Euclidian algorithm找到 x, 也就是d。
  
    * 看不太懂The Chinese Remainder Theorem   
  雖然照抄老師在中國餘式定理pdf的演算法Chap0809-part2的第10頁到第12頁, 就可以實作找到y**d mod(n)下的結果, 少做了很多次方項後速度非常快一樣有用
  Square_and_Multiply的方法, 但是不是很懂𝑦 ≡ 𝑞×𝑐𝑝 ×𝑦𝑝+𝑝×𝑐𝑞 ×𝑦𝑞 mod𝑛 是怎麼出來的, 可能數學好一點就會看懂該公式如何來的,可以加快解密的速度。

  
