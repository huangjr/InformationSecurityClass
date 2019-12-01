# function declaration
def gcd(x, y):
    '''
    compute GCD of x,y
    >>> gcd(100,50)
    50
    '''
    while(y): 
        x, y = y, x % y 
    return x

def mutiplicative_invert(x, n):
    '''
    find the multiplicative invert of x on the base of n
    '''
    pass

def miller_rabin(x):
    '''
    test whether x is a composite or has the probability to be a prime
    return False when x has an composite witness
    return True when x has no composite witness
    7 times should this test carried out
    >>> miller_rabin(48)
    False
    >>> miller_rabin(47)
    True
    '''

def multiply_and_square(x, exponent):
    '''
    accelerate method of exponent
    public key "e" was default to 2^16+1
    >>> x = 2
    >>> exponent = 17
    >>> multiply_and_square(x, exponent)
    562949953421312
    '''
    # translate the exponent to binary array, which is a str object
    exponent = bin(exponent)
    y=x
    for a in exponent[2:]:
        # square on every round: y=y^2 mod n
        y=y**2
        # mutiply on exponent[i] = 1: y=x*y mod n
        if a=='1':
            y=y*x
    return y

# find two large prime:p,q
# this process can be accelerated with miller rabin primality test.
# the size of integer type in python is unlimited, so we can do anything we want

# compute n=pxq

# compute phi(n) = (p-1)x(q-1)

# find e by gcd(e, phi(n)) = 1

# find d by exd = 1 mod phi(n)

# encryption:

# plaintext**e mod n= ciphertext
# the exponentiation can be accelerated with multiply and square

# decryption:
# decryption can be accelerate with CRT, because we have know the p,q

# ciphertext**d mod n= plaintext
# the exponentiation can be accelerated with multiply and square

# main function
if __name__ == "__main__":
    import doctest, RSA
    doctest.testmod(RSA)