import acc_RSA
# function declaration
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
    while(p == q):
        q = quickRSA.find_prime(int(number_of_bit/2),3)
    # compute n=pxq
    n=p*q
    # compute phi(n) = (p-1)x(q-1)
    phi_n=(p-1)*(q-1)
    # public key was default set to 2*16+1, to provide fast encryption--short private key
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
    # plaintext**e mod n= ciphertext
    # the exponentiation can be accelerated with multiply and square
    quickRSA=acc_RSA.QuickRSA()
    ciphertext = quickRSA.multiply_and_square(plaintext,e,n)
    return ciphertext

def decryption(d, p, q, ciphertext):
    '''
    Using crt accelerated decryption method defaultly
    '''
    # decryption:
    # decryption can be accelerate with CRT, because we have know the p,q
    # ciphertext**d mod n= plaintext
    # the exponentiation can be accelerated with multiply and square
    quickRSA=acc_RSA.QuickRSA()
    plainText = quickRSA.crt_Decrypt(d,p,q,ciphertext)
    return plainText
    
if __name__ == "__main__":
    '''
    program entry point, to interact with this program use the following command
    '''
    import doctest, RSA, acc_RSA, bcolors
    # doctest.testmod(RSA) # no test for now
    bcolors=bcolors.bcolors()
    while 1:
        print("Welcome to RSA program:")
        print(">g, generate public key and private key")
        print(">e, encrypt")
        print(">d, decrypt")
        print(">x, exit")
        option=input(">>> ")
        if option=='g':
            print(">how many bits do you want?")
            number_of_bits=input(">>> ")
            try:
                p,q,e,d,n=key_generation(int(number_of_bits))
                print(bcolors.OKBLUE + "Here is your key information, store in wallet or paper, don't tell others your private key" + bcolors.ENDC)
                print("p=",p)
                print("q=",q)
                print("e=",e)
                print("d=",d)
                print("n=",n)
            except: 
                print(bcolors.WARNING + "Warning: Please enter an interger, don't do anything stupid." + bcolors.ENDC)
        elif option=='e':
            print(">public key")
            e=input(">>> ")
            print(">n=?")
            n=input(">>> ")
            print(">plaintext")
            plaintext=input(">>> ")
            try:
                ciphertext=''
                for char in plaintext:
                    # convert plaintext to ascii code
                    ciphertext=ciphertext+str(encryption(int(e),int(n),ord(char)))+" "
                # ouput an decimal integer
                print("Your cipherText= ", ciphertext)
            except:
                print(bcolors.WARNING + "Warning: Please enter the right public key, don't do anything stupid." + bcolors.ENDC)
        elif option=='d':
            print(">private key")
            d=input(">>> ")
            print(">p=?")
            p=input(">>> ")
            print(">q=?")
            q=input(">>> ")
            print(">ciphertext")
            ciphertext=input(">>> ")
            # take an integer as input
            try:
                ciphertext=ciphertext.split(" ")
                plaintext=''
                for char in ciphertext:
                    plaintext=plaintext+chr(decryption(int(d),int(p),int(q),int(char)))
                    # convert plaintext from integer to ascii to str
                print(bcolors.OKGREEN + "Your plaintext= ", plaintext + bcolors.ENDC)
            except:
                print(bcolors.WARNING + "Warning: Please enter the right private key, don't do anything stupid." + bcolors.ENDC)
        elif option=='x':
            print(bcolors.OKBLUE + "~~See you~~" + bcolors.ENDC)
            exit()