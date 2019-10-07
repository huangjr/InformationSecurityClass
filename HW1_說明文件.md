# HW1_說明文件

----
## 分工
四材料四 B10504028 林哲豪 Encrypt  
隨班附讀 a22727    黃婕雅 Decrypt


## 環境
MacOS Sierra 10.12.6.  Python 3 

## Decrypt 程式說明

### 1. Caesar cipher    
>Input: ITDTZWGJXYFSYMJSQJYLT  
>Key: 5  
>Output: doyourbestandthenletgo  

tempt儲存原本的位置  
new_tempt儲存後來位移過後的位置  
plaintext 儲存原文  
alphabet 字母對應位置的字典  

```python
  tempt= []
  new_tempt = []
  key = int(Key)
  plaintext = ""
  alphabet = {'a':'1','b':'2','c':'3','d':'4','e':'5','f':'6','g':'7','h':'8', 'i':'9','j':'10','k':'11','l':'12','m':'13','n':'14','o':'15','p':'16','q':'17',
  'r':'18','s':'19','t':'20','u':'21','v':'22','w':'23','x':'24','y':'25','z':'26'}
```

將ciphertext的字對應到alphabet字典裡的數字得到原來的位置存到tempt裡  
   
   ```python
    for l in ciphertext:
        tempt.append(alphabet[l])
   ```
將位移後的數字存到new_tempt裡
   ```python
    for t in tempt:
        t = (int(t) - key) % 26
        new_tempt.append(t)
   ```
將new_tempt裡位置的數字對應到alphabet字典裡將字母傳出來給plaintext
   ```python
    for n in new_tempt:
        for a,b in alphabet.items():
            if n == int(b): plaintext = plaintext + a

    return plaintext.lower()   
   ```

### 2. Playfair cipher   
>Input: IDWPQSDFTUGUQLGKKFUFMW  
>Key: COMP  
>Output: doyourbestandthenletgo  

將key與abc...z串在一起，並將i取代為j，因為等等放入5*5的puzzle_map時，i與j共用一個位置  
```python
    combine = key + 'abcdefghijklmnopqrstuvwxyz'
    combine = combine.replace('i','j')
```
將剛剛combine字串有重複的字元刪掉並依序排入new_order裡面
```python
    new_order = []
    for l in combine:
        if l not in new_order:
            new_order.append(l)
```
用前面的new_order按順序一個個放入5*5的puzzle_map裡面
```python
    puzzle_map = {}    
    for x in range(1,6):
        for y in range(1,6):
            puzzle_map[x,y] = new_order[5*(x - 1) + y - 1]
```
進來的ciphertext如果有i必須換成j，因為puzzle裡面只有j的位置，而ij共用，因此會造成iloveyou還原時也會變成jloveyou
```python
    new_ciphertext = []
    Ciphertext = Ciphertext.replace('I','J')
```
進來的ciphertext需要兩兩一組看是否有重複，如果是偶數表示是兩兩一組裡的第一個字，可以直接放入new_ciphertext，
若奇數則表示是兩兩一組的第二個字，則要判斷跟前面加入的第一個字是不是同一個字，同一個字要加'X'進去，如果兩個字都是'X'則加'Q'
（不過助教表示測資不會有重複的字！）
```python
    for char in Ciphertext:
        if len(new_ciphertext) % 2 == 0:
            new_ciphertext.append(char)
        else:
            if new_ciphertext[-1] == char: 
                if char != 'X': new_ciphertext.append('X') 
                else: new_ciphertext.append('Q')
            new_ciphertext.append(char)
```
前面的puzzle_map的key是位置的x,y,而value是位置x,y對應的字母，因為等等要用字母找位置x,y，所以將puzzle_map的key和value反過來，變成reverse_puzzle，
key是字母, value是對應的位置x,y

```python
    reverse_puzzle = {k: v for v,k in puzzle_map.items()}
```
根據前面改造過後的new_ciphertext（I取代成J），兩兩一組放入reverse_puzzle字典裡查詢位置，有三種狀況，兩個字在同一條水平線，或是在同一垂直線上，
或是形成對角線，根據playfair規則還原，pre_x以及pre_y則是找回原來plaintext字母的位置，再放回reverse_puzzle裡找pre_x和pre_y對應的字母，加回plaintext裡

```python
    plaintext = ''

    for i in range(0,len(new_ciphertext),2):
        x1, y1 = reverse_puzzle[new_ciphertext[i].lower()]
        x2, y2 = reverse_puzzle[new_ciphertext[i+1].lower()]
        if x1 == x2: 
            pre_x1 = x1  
            pre_x2 = x2  
            pre_y1 = y1 - 1
            pre_y2 = y2 - 1
            if pre_y1 == 0: pre_y1 = 5
            if pre_y2 == 0: pre_y2 = 5
        elif y1 == y2:
            pre_y1 = y1  
            pre_y2 = y2  
            pre_x1 = x1 - 1
            pre_x2 = x2 - 1
            if pre_x1 == 0: pre_x1 = 5
            if pre_x2 == 0: pre_x2 = 5
        else:
            pre_x1 = x1 
            pre_x2 = x2
            pre_y1 = y2
            pre_y2 = y1

        plaintext += puzzle_map[pre_x1,pre_y1] + puzzle_map[pre_x2,pre_y2]

    return plaintext.lower()
```
### 3. Vernam cipher   
>Input: OIYLYHNOBQC~_FH}K_}LI  
>Key: TEC  
>Output: doyourbestandthenletgo  

因為key只有一小段，後面要接原來的plaintext內容，只好先key的第一個字與ciphertext的第一個字XOR算出字母再加回key後面，也就是plaintext的第一個字，
全部跑完後key就還原出來了，就等於key後面加上完整的plaintext，我們再將前面的key移掉還原成原文，會用95而不是97是因為partner加密後的值對應到
ASCII無法顯示，因此與partner討論過後改成換算時用95
```python
  def Vernam_decrypt(Key,Ciphertext):
      plaintext = ''
      ciphertext = Ciphertext.lower()
      key = Key.lower()
      lenth = len(key)

      for i in range(len(ciphertext)):
          key += chr( ((ord(ciphertext[i])-95)^(ord(key[i])-97)) +97)


      plaintext = key[lenth:]
      return plaintext.lower()
```

### 4. Row cipher   
>Input: ONGUTOYATRHOTEDSLBEEN  
>Key: 45362178  
>Output: doyourbestandthenletgo  

result拿來裝分割好的ciphertext（幾個字是一個column來的，同一個column來的放一起），split_numbers用來裝每一個column應該要有幾個字，
因為會有ciphertext的長度不能被key的長度整除，表示會有一些column多字，有一些column字比較少
```python
    result = []
    key = Key
    ciphertext = Ciphertext
    split_numbers = {}
```
用extra儲存有幾個column多出來，表示有幾個column有多出一個字，如果整除就表示每一個column有的字數都一樣用rows表示，
就直接將ciphertext拆成rows個一組，塞回result裡
若無法除盡，表示有column要多字，此時用rows表示多出字的column裡共有幾個字，而split_numbers用來記錄每一column應該要有的字數，因為不是整除，
表示column的字數不同，有的要多一個字，前面有用extra裝總共有幾個column要多字，而剩下的column字數就是rows-1，
確認好了split_numbers我們就得知每一個column應該要有的字數，else裡的最後一個迴圈就可以依照key也就是第幾個column去split_numbers查幾個字是一組的，
將ciphertext依照查出來的字數，一組拆好再塞回result裡，再換下一組

```python
    extra = len(ciphertext) % len(key)
    if extra == 0:
        rows = int(len(ciphertext)/len(key))
        for i in range(0, len(ciphertext), rows):
            result.append(ciphertext[i: i+rows])
    else:
        rows = int(len(Ciphertext)/len(key)) + 1
        for i in range(extra):
            split_numbers[i] = rows
        for i in range(extra, len(key)):
            split_numbers[i] = rows - 1
        for char in key:
            result.append(ciphertext[0:split_numbers[int(char) - 1]])
            ciphertext = ciphertext[split_numbers[int(char) - 1]:]
```
將result裡的字串都轉成list的格式：原本result= ['ABC','DEF','GH',...]變成->result= [['A','B','C'],['D','E','F'],['G','H'],...]

```python
   result = [a for a in map(list,result)]
```

將sort_result陣列建好，現在的result是順序沒被擺正的column，
我們依照key的順序將result裡的column還原成原本的樣子，用sort_result接收

```python
    sort_result = [["" for j in range(rows)] for i in range(len(key))]
    
    for i, char in enumerate(key):
        sort_result[int(char)-1] =  result[i]
```

將sort_result裡每一column的第一個字取出再來是每一個column的第二個字取出，依此類推還原出原本的plaintext，因為
有的column字比較多，有的column字比較少，所以會出錯，若遇到column字較少的，沒有這個值就直接pass掉
```python
    plaintext = ''
    for x in range(len(sort_result[0])):
        try:
            for y in range(len(sort_result)):
                plaintext += sort_result[y][x]
        except:      
            pass

    return plaintext.lower()
```

### 5. Rail fence cipher   
>Input: DYUBSATELTOOORETNHNEG  
>Key: 2  
>Output: doyourbestandthenletgo  

先將puzzle陣列建好，共有key個row，ciphertext長度個的column，num用來儲存重複的數字，拿來記錄每一個字的row位置，例如有key為3
則表示有3個row，他們依序會是012101210121....指row的位置，所以前面兩個迴圈會做出 num = 01210,而order就會是0121，
我們要讓每一個ciphertext都對應到一個row位置，就必續一直重複order到超過ciphertext的長度，最後再將ciphtertext跟row zip在一起，
row會變成[('A',0),('B',1),('C',2),('D',1),('E',0),('F',1),...]，我們知道每一個字對應到row的位置

```python
    puzzle = [["" for i in range(len(ciphertext))] for j in range(key)]
    num = ''
    for i in range(key):
        num += str(i)
    for i in reversed(range(key-1)):
        num += str(i)
    order = num[:-1]
    repeat = int(len(ciphertext)/ len(order) + 1)
    order *= repeat
    row = list(zip(ciphertext,order))
```
將前面建好的row放入puzzle裡，已經知道每一個字的row位置就依照ciphertext的順序去row找再放進puzzle，此時塞完，puzzle的位置已經呈現W的樣式，
但是塞進去的字母是錯的，塞進去的是ciphertext的字在不對的位置上，我們只是利用ciphertext建造puzzleW的樣式

```python
    for i in range(len(ciphertext)):
        puzzle[int(row[i][1])][i] = row[i][0]
```
column就是ciphertext的長度，變數設好比較方便，不用一直寫len(ciphertext),puzzle的陣列位置圖Ｗ做好了，只是裡面的字母是錯的，
因為ciphertext的順序是先給第一排row再給第二排row，我們就從第一排row開始讀取，不是空格就把ciphertext的字母塞進，當第一排塞完，
也表示ciphertext在第一排的字母都沒了，接著再做第二排，依此類推，正確的puzzle就會建好，裡面的位置是對的，對應的字母也會是對的

```python
    column = len(ciphertext)

    for i in range(key):
        for j in range(column):
            if puzzle[i][j] != '':
                puzzle[i][j] = ciphertext[0]
                ciphertext = ciphertext[1:]
```
當前面的正確puzzle有了，就可以從column一路讀取puzzle到最後，把plaintext串回來

```python
    for i in range(column):
        for j in range(key):
            if puzzle[j][i] != '': 
                plaintext += puzzle[j][i].lower()
                
    return plaintext.lower()
```
