import acc_RSA, random, math
import hashlib

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

def primeFactors(n): 
    prime_list = []
    # Print the number of two's that divide n 
    while n % 2 == 0: 
        # prime_list.append(2), 
        n = n / 2
          
    # n must be odd at this point 
    # so a skip of 2 ( i = i + 2) can be used 
    for i in range(3,int(math.sqrt(n))+1,2): 
          
        # while i divides n , print i ad divide n 
        while n % i== 0: 
            prime_list.append(i), 
            n = n / i 
              
    # Condition if n is a prime 
    # number greater than 2 
    if n > 2: 
        prime_list.append(n) 
    return prime_list

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

class DSA_gen:
    # generation
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


    # signature
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


if __name__ == "__main__":
    dsa_gen = DSA_gen()
    p, q, a, b, d = dsa_gen.generation(1024, 160)
    message = 'amy'
    r, s = dsa_gen.signature(message, p, q, a, b, d)
    print(r, s)
