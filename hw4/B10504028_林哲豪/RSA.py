import acc_RSA
# function declaration
def gcd(x, y):
    '''
    compute GCD of x,y
    but seems like it's useless here
    >>> gcd(100,50)
    50
    '''
    while(y): 
        x, y = y, x % y 
    return x

def multiplicative_inverse(x, n):
    '''
    find the multiplicative inverse of x on the base of n:y
    x*y = 1 mod n, k*n+1=x*y, 
    >>> multiplicative_inverse(9,10)
    9
    '''
    y=1
    while((x*y)%n != 1): y+=1
    return y

def key_generation(number_of_bit):
    '''
    generate a key of number_of_bit,return p,q,e,d,n
    >>> key_generation(20)
    0
    '''
    # find two large prime:p,q
    # this process can be accelerated with miller rabin primality test.
    # the size of integer type in python is unlimited, so we can do anything we want
    quickRSA = acc_RSA.QuickRSA()
    p = quickRSA.find_prime(number_of_bit,3)
    q = quickRSA.find_prime(number_of_bit,3)
    # compute n=pxq
    n=p*q
    # compute phi(n) = (p-1)x(q-1)
    phi_n=(p-1)*(q-1)
    # find e by gcd(e, phi(n)) = 1
    # public key was default set to 2*16+1, to provide fase encryption
    e = 2**16+1
    # find d by exd = 1 mod phi(n)
    d = multiplicative_inverse(e, phi_n)
    return (p,q,e,d,n)

def encryption(plaintext, e):
    # encryption:
    pass
    # plaintext**e mod n= ciphertext
    # the exponentiation can be accelerated with multiply and square

def decryption(ciphertext, d):
    # decryption:
    # decryption can be accelerate with CRT, because we have know the p,q
    pass
    # ciphertext**d mod n= plaintext
    # the exponentiation can be accelerated with multiply and square
    
if __name__ == "__main__":
    '''
    program entry point
    '''
    import doctest, RSA, acc_RSA
    doctest.testmod(RSA)
    # p,q,e,d,n=key_generation()