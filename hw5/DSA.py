import hashlib

def generation(plaintext):
    '''
    p= 2^1023<p<2^1024
    q= divisor of (p-1) in 2^159<q<2^160
    a= a^q = 1 (mod p)= h^((p-1)/q) (mod p)
    b= a^d (mod p)
    d= 0<d<q

    kpub=(p,q,a,b)
    kpr=(d)
    '''
    # import from partner
    
    # return p,q,a,b,d

def signature()
    '''
    ke=random(0,q) <-- temporary value
    signature=(r,s)
    r=(a^ke mod p) mod q
    s=(sha(x)+d*r)ke^-1 mod q
    '''

def verification(x,r,s,p,q):
    '''
    w=s^-1 mod q
    u1=w*sha(x)mod q
    u2=w*r mod q
    v=(a^u1 * b^u2 mod p) mod q

    if v=r mod q --> signature is valid
    else invalid
    >>> verification(26,59,29,20,5)
    True
    '''
    sha=hashlib.sha1()
    shaX=sha.update(x).hex()
    w=pow(s,-1,q)
    u1=(w*sha(x))%q
    u2=(w*r)%q
    v=((pow(a,u1)*pow(b,u2))%p)%q
    if v==r:
        return True


if __name__ == "__main__":
    '''
    keygen {length}
    sign {message}
    verify {message}
    '''
    '''
    program entry point, to interact with this program use the following command
    '''
    import doctest, DSA, acc_RSA, bcolors
    doctest.testmod(DSA) # no test for now
    bcolors=bcolors.bcolors()
    while 1:
        print("Welcome to DSA program:")
        print(">g, generate public key and private key")
        print(">s, signature")
        print(">v, verification")
        print(">x, exit")
        option=input(">>> ")
        if option=='g':
            print(">how many bits do you want?")
            number_of_bits=input(">>> ")
            try:
                p,q,a,b,d=key_generation()
                print(bcolors.OKBLUE + "Here is your key information, store in wallet or paper, don't tell others your private key" + bcolors.ENDC)
                print("p=",p)
                print("q=",q)
                print("a=",e)
                print("b=",d)
                print("d=",n)
            except: 
                print(bcolors.WARNING + "Warning: Please enter an interger, don't do anything stupid." + bcolors.ENDC)
        elif option=='s':
            print(">p")
            e=input(">>> ")
            print(">q")
            n=input(">>> ")
            print(">a")
            d=input(">>> ")
            print(">plaintext")
            plaintext=input(">>> ")
            try:
                r,s=signature()
            except:
                print(bcolors.WARNING + "Warning: Please enter the right public key, don't do anything stupid." + bcolors.ENDC)
        elif option=='v':
            print(">p=?")
            p=input(">>> ")
            print(">q=?")
            q=input(">>> ")
            print(">r=?")
            r=input(">>> ")
            print(">s=?")
            s=input(">>> ")
            print(">plaintext")
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