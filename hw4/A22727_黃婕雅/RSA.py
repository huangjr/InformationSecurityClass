import random, math, sys
import doctest, Rsa

# use easy method to check prime
def IsPrime(n):
    '''
    >>> IsPrime(192)
    True
    '''
    upperbound = int(math.sqrt(n))

    for i in range(2, upperbound + 1):
        if n % i == 0: return False
    return True

# use miller rabin test to check if n is prime, do k times in miller rabin test to enhence the accuracy
def miller_rabin(n, k):
    '''
    >>> miller_rabin(192, 4)
    True
    '''
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
        # for i in range(self.n, 2, -1):
        #     if i * self.e % self.phi_n == 1:
        #         self.d = i
        #         break

def Square_and_Multiply(message_num, e, n):
    '''
    >>> Square_and_Multiply(5, 10, 13)
    12
    '''
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

if __name__ == "__main__":
    # doctest.testmod(Rsa)

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

