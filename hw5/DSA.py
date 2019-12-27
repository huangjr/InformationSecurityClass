# generation
'''
p= 2^1023<p<2^1024
q= divisor of (p-1) in 2^159<q<2^160
a= a^q = 1 (mod p)= h^((p-1)/q) (mod p)
b= a^d (mod p)
d= 0<d<q

kpub=(p,q,a,b)
kpr=(d)
'''

# signature
'''
ke=random(0,q) <-- temporary value
signature=(r,s)
r=(a^ke mod p) mod q
s=(sha(x)+d*r)ke^-1 mod q
'''

# verification
'''
w=s^-1 mod q
u1=w*sha(x)mod q
u2=w*r mod q
v=(a^uq * b^u2 mod p) mod q

if v=r mod q --> signature is valid
else invalid
'''

if __name__ == "__main__":
    '''
    keygen {length}
    sign {message}
    verify {message}
    '''
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