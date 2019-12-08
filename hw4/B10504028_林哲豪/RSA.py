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
    p = quickRSA.find_prime(int(number_of_bit/2),3)
    q = quickRSA.find_prime(int(number_of_bit/2),3)
    # compute n=pxq
    n=p*q
    # compute phi(n) = (p-1)x(q-1)
    phi_n=(p-1)*(q-1)
    # ax+by=ax+my, ax+my=1=ax(mod m), we can use extended gcd to find x and y, x is the multiplicative inverse.
    # public key was default set to 2*16+1, to provide fast encryption
    e = pow(2,16)+1
    # find d by exd = 1 mod phi(n)
    # find e by gcd(e, phi(n)) = 1, for e an phi_n are coprime, we can use the EGCD algorithm
    d = quickRSA.multiplicative_inverse(e, phi_n)
    return (p,q,e,d,n)

def encryption(e, n, plaintext):
    '''
    encrypt plaintext with e:public key, n:given
    '''
    # encryption:
    quickRSA = acc_RSA.QuickRSA()
    ciphertext = quickRSA.multiply_and_square(plaintext, e, n)
    return ciphertext
    # plaintext**e mod n= ciphertext
    # the exponentiation can be accelerated with multiply and square

def decryption(d, p, q, ciphertext):
    '''
    Using crt accelerated decryption method defaultly
    '''
    # decryption:
    # decryption can be accelerate with CRT, because we have know the p,q
    quickRSA = acc_RSA.QuickRSA()
    plainText = quickRSA.crt_Decrypt(d, p, q, ciphertext)
    return plainText
    # ciphertext**d mod n= plaintext
    # the exponentiation can be accelerated with multiply and square
    
if __name__ == "__main__":
    '''
    program entry point, to interact with this program use the following command
    '''
    import doctest, RSA, acc_RSA
    # doctest.testmod(RSA) # no test for now
    while 1:
        print("Welcome to RSA program:")
        print(">g, generate public key and private key")
        print(">e, encrypt")
        print(">d, decrypt")
        print(">x, exit")
        option=input(">>>")
        if option=='g':
            print(">how many bits do you want?")
            number_of_bits=input(">>>")
            p,q,e,d,n=key_generation(int(number_of_bits))
            print("p=",p)
            print("q=",q)
            print("e=",e)
            print("d=",d)
            print("n=",n)
        elif option=='e':
            print(">public key")
            e=input(">>>")
            print(">n=?")
            n=input(">>>")
            print(">plaintext")
            plaintext=input(">>>")
            plainText=''
            # convert plaintext to ascii code
            for chr in plaintext:
                plainText+=str(hex(ord(chr)))[2:]
            ciphertext=encryption(int(e),int(n),int(plainText,16))
            print("Your cipherText= ", ciphertext)
        elif option=='d':
            print(">private key")
            d=input(">>>")
            print(">p=?")
            p=input(">>>")
            print(">q=?")
            q=input(">>>")
            print(">ciphertext")
            ciphertext=input(">>>")
            cipherText=''
            for chr in ciphertext:
                cipherText+=str(hex(ord(chr)))[2:]
            plainText=str(decryption(int(d),int(p),int(q),int(cipherText,16)))
            # convert plaintext from integer to ascii to str
            plainText=hex(int(plainText,16))[2:]
            print(plainText)
            plainText=bytes.fromhex(plainText).decode("utf8")
            print("Your plaintext= ", plainText)
        elif option=='x':
            print(">see you")
            exit()