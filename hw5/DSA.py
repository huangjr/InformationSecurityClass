import hashlib, acc_RSA, DSA_gen_sig

def generation():
    '''
    input: plaintext
    output: p q a b d 
    p= 2^1023<p<2^1024
    q= divisor of (p-1) in 2^159<q<2^160
    a=> a^q = 1 (mod p) => h^((p-1)/q) (mod p)
    b= a^d (mod p)
    d= 0<d<q

    kpub=(p,q,a,b)
    kpr=(d)
    '''
    # import from partner
    dsa_gen_sig = DSA_gen_sig.DSA_gen()
    p,q,a,b,d = dsa_gen_sig.generation(1024, 160)
    return (p,q,a,b,d)

def signature(plaintext,p,q,a,b,d):
    '''
    input: plaintext p q a b
    output: r s
    ke=random(0,q) <-- temporary value
    signature=(r,s)
    r=(a^ke mod p) mod q
    s=(sha(x)+d*r)ke^-1 mod q
    '''
    # import from partner
    dsa_gen_sig = DSA_gen_sig.DSA_gen()
    r,s = dsa_gen_sig.signature(plaintext,p,q,a,b,d)
    return (r,s)

def verification(x,r,s,a,b,p,q):
    '''
    input: x r s a b p q
    output: True or False
    w=s^-1 mod q
    u1=w*sha(x)mod q
    u2=w*r mod q
    v=(a^u1 * b^u2 mod p) mod q

    if v=r mod q --> signature is valid
    else invalid
    >>> verification(b'26',3,4,59,29,20,5)
    True
    '''
    acc_rsa=acc_RSA.QuickRSA()
    shaX = int(hashlib.sha1(bytes(x, encoding = "utf8")).hexdigest(), 16)
    w=acc_rsa.multiplicative_inverse(s,q)
    u1=(w*shaX)%q
    u2=(w*r)%q
    v=((pow(a,u1,p)*pow(b,u2,p))%p)%q
    if v==r:
        return True
    else:
        return False

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
    # doctest.testmod(DSA) # no test for now
    bcolors=bcolors.bcolors()
    while 1:
        print("Welcome to DSA program:")
        print(">g, generate public key and private key")
        print(">s, signature")
        print(">v, verification")
        print(">x, exit")
        option=input(">>> ")
        # key generation
        if option=='g':
            try:
                p,q,a,b,d=generation()
                print(bcolors.OKBLUE + "Here is your key information, store in wallet or paper, don't tell others your private key" + bcolors.ENDC)
                print("p= ",p)
                print("q= ",q)
                print("a= ",a)
                print("b= ",b)
                print("d= ",d)
            except TypeError: 
                print(bcolors.WARNING + "Warning: Please enter an string, don't do anything stupid." + bcolors.ENDC)
        # signature
        elif option=='s':
            print(">p")
            p=input(">>> ")
            print(">q")
            q=input(">>> ")
            print(">a")
            a=input(">>> ")
            print(">b")
            b=input(">>> ")
            print(">d")
            d=input(">>> ")
            print(">plaintext")
            plaintext=input(">>> ")
            try:
                r,s=signature(plaintext,int(p),int(q),int(a),int(b),int(d))
                print(bcolors.OKBLUE + "Here is your signature" + bcolors.ENDC)
                print('r= ',r)
                print('s= ',s)
            except TypeError:
                print(bcolors.WARNING + "Warning: Please enter the right type of private key, don't do anything stupid." + bcolors.ENDC)
            except ValueError:
                print(bcolors.WARNING + "Warning: Please enter the right type of private key, don't do anything stupid." + bcolors.ENDC)
        # signature verification
        elif option=='v':
            print(">p")
            p=input(">>> ")
            print(">q")
            q=input(">>> ")
            print(">a")
            a=input(">>> ")
            print(">b")
            b=input(">>> ")
            print(">r")
            r=input(">>> ")
            print(">s")
            s=input(">>> ")
            print(">plaintext")
            plaintext=input(">>> ")
            # take an integer as input
            try:
                result = verification(plaintext,int(r),int(s),int(a),int(b),int(p),int(q))
                if result==True:
                    print(bcolors.OKGREEN + "Verification Success ", bcolors.ENDC)
                else:
                    print(bcolors.WARNING + "Verification Fail ", bcolors.ENDC)
            except TypeError:
                print(bcolors.WARNING + "Warning: Please enter the right type of plaintext, don't do anything stupid." + bcolors.ENDC)
            except ValueError:
                print(bcolors.WARNING + "Warning: Please enter the right type of key, don't do anything stupid." + bcolors.ENDC)
        elif option=='x':
            print(bcolors.OKBLUE + "~~See you~~" + bcolors.ENDC)
            exit()