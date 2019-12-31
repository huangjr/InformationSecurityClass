# a22727_HW5_report 
## 分工
除了作業內容所寫的三個部分，還增加一個主程式，用來做與使用者互動的部分。  
<pre>
* key generation     A22727_黃婕雅
* signature          A22727_黃婕雅  
* verification       B10504028_林哲豪  
* main program       B10504028_林哲豪 
</pre>  

## 建置環境  
MacOS Sierra 10.12.6. Python 3  

## 操作方式與執行過程截圖
* 執行DSA.py檔  

  指令：
  > python DSA.py  
  
  執行結果：  
  ![Imgur](https://i.imgur.com/ECxvXRZ.png) 
  g指key generation, s指signature, v指verification, x指exit離開，使用者可以輸入要執行的英文字母。  
  
* g (產生公鑰p,q,a,b與私鑰d)  

  指令： 
  > g    
  
  執行結果：  
  ![Imgur](https://i.imgur.com/eOQMb66.png)
  產生出DSA的p, q, a, b, d，等等簽章與認證時使用。  
  
* s (簽章)  

  指令： 
  > s    
  
  執行結果：  
  ![Imgur](https://i.imgur.com/Afae6f5.png)
  輸入s，系統會問使用者p, q, a,b , d，使用者根據前面g得到的p, q, a, b, d，一項項複製上去，最後再打上自己預定的message，也就是系統顯示的plaintext，這裏我們輸入ntust，會得到r與s，如下圖。  
  ![Imgur](https://i.imgur.com/FdoC9SP.png)  
  
* v (認證)  

  指令： 
  > v    
  
  執行結果：  
  ![Imgur](https://i.imgur.com/DVosEQQ.png)
  輸入v，系統會問使用者p, q, a, b, d, plaintext，我們一樣依上面的數據一項項輸入，最後系統會顯示認證有沒有成功，成功會顯示True。    
  ![Imgur](https://i.imgur.com/wZIWbSD.png)  
  
* x (離開系統)  

  指令： 
  > x    
  
  執行結果：  
  ![Imgur](https://i.imgur.com/lo1bywl.png)
  輸入x，系統會顯示See you，然後離開。  
  
## 程式碼解說  

### Class DSA_gen    

DSA_gen的class寫在DSA_gen_sig.py檔裡面，這樣主程式只要call該class就可以直接使用裡面的function。 寫在DSA_gen的class裡有兩個function，一個是generation,另一個是signature

* key generation  
	* find q  
負責產生DSA需要的公鑰p, q, a, b與私鑰d，一開始需要給定參數，告知需要的p與q長度，通常設定p為1024，q為160。發現先找出q再去找p程式碼會跑比較快，所以先找q，利用上個作業的miller_rabin測試法，random一個長度為160 bits的q去miller_rabin的function做質數測試，測試的次數固定為4，通過4次就認定該數字是質數。  
	* find p   
	找到q後再去找p，由p的條件知道q是p-1的質因數，因此表示q*x = p-1，我們random一個長度為1024-160長度的數字x，這是為了讓p有符合1024 bits的條件，random x完後將x乘上q加1，去看看p是不是質數，若p為質數，則符合上述條件。  
    * find a, b, d  
	網路查詢發現可以將h固定為2，將h=2代入a的公式，又已知p與q，則可以得到a。d的條件是在1到q-1之間，因此就從中randon一個數字d，又已知a, d, p，再代入b的公式，得到b。

```python
    def generation(self, p_bit_length, q_bit_length):
        quickrsa = acc_RSA.QuickRSA()

        p_bit_length = p_bit_length
        q_bit_length = q_bit_length


        # find q
        q = random.getrandbits(q_bit_length)
        while miller_rabin(q, 4) != True:
            q = random.getrandbits(q_bit_length)

        # find p
        x = random.getrandbits(p_bit_length - q_bit_length)
        p = x * q + 1
        while miller_rabin(p, 4) != True:
            x = random.getrandbits(p_bit_length - q_bit_length)
            p = x * q + 1

        # fix h = 2, find a
        h = 2
        k = (p - 1) // q
        a = pow(h, k, p) 

        # find d and b
        d = random.randint(1, q-1)
        b = pow(a, d, p)

        return p, q, a, b, d
```  

* signature        
	* find r, s   
將前面取得的DSA公私鑰以及任意訊息message代入signature的公式，再代入公式前，需要先找出ke以及他在q下的乘法反元素，利用前個作業的modInverse function，找出乘法反元素。作業敘述需要用sha1算出message hash完的數字，我們利用內建的hashlib算出，因為輸入的message需要先轉成bytes，算出的數字用hexdigest翻成16進位，之後再轉成10進位再代入公式，得到r與s。

```python
    def signature(self, message, p, q, a, b, d):

        # find ke
        ke = random.randint(1, q-1)
        ke_inverse = modInverse(ke, q)

        # find sha(message) = m
        m = int(hashlib.sha1(bytes(message, encoding = "utf8")).hexdigest(), 16)

        # find r
        r = pow(a, ke, p) % q

        # find s
        s = (m + d*r)*ke_inverse % q

        return r, s
```

## 困難與心得  
  * 程式碼跑太久, 已改善  
  
  一開始寫DSA的Class, 先計算出p， 再去求q，發現這樣做程式碼要跑很久，因為q必須是p-1的質因數，卡在這邊很久，很難有符合的q，要是質數又要符合160 bits還要是p-1的因數，因為跑太久無法從p推出q，那之後的a, b, d都無法產生，後來跟partner討論到這一個問題，partner給了很好的意見，讓我先從q找起，再去推p，這樣程式碼的速度快很多，求到DSA的公私鑰(p, q, a, b, d)後，再做signature簽章的部分也是代公式求出，只是做sha1的hash要符合使用的格式，需要轉一下輸入的message成bytes，output也需要再轉一次讓他變成十進位再代入公式。
 
