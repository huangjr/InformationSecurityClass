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
    import doctest, RSA, acc_RSA
    doctest.testmod(RSA)
    doctest.testmod(acc_RSA)