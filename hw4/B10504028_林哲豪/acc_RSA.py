import random

class QuickRSA:
    def miller_rabin(x):
        '''
        test whether x is a composite or has the probability to be a prime
        return False when x has an composite witness
        return True when x has no composite witness
        7 times should this test carried out
        >>> QuickRSA.miller_rabin(48)
        False
        >>> QuickRSA.miller_rabin(49)
        False
        '''
        # transformation to x-1= 2^n x r
        m = x-1
        k=0
        while(m%2 != 0):
            m = int(m/2)
            k+=1
        # choose a number from x-1, can be random
        a = random.randint(2, x-1)
        # compute b=a^m mod x
        b = (a**m) % x
        if(b != 1 & b != (x-1)):
            i=1
            while(i<k & b!=(x-1)):
                b=(b**2)%x
                if b==1: return False
                i=i+1
            if(b!=(x-1)): return False
        return True

    def multiply_and_square(x, exponent):
        '''
        accelerate method of exponent
        public key "e" was default to 2^16+1
        >>> x = 2
        >>> exponent = 17
        >>> QuickRSA.multiply_and_square(x, exponent)
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
    def crt_Decrypt(p,q,y,N):
        '''
        p and q only know to the one have private key, so we use the information of p and q to shorten the decryption time.
        '''
        # transformation: x to xq and xp
        xq = x%q
        xp = x%p
        # modular exponentiation: compute xp^dp mod p, xq^dq mod q
        
        # inverse transportation
    def primality(security_coefficient):
        '''
        determine the primality with x time of miller_rabin test
        '''
        result=True
        for a in range(security_coefficient):
            result=result*QuickRSA.miller_rabin(r)
        return (result,r)

    def find_prime(number_of_bits, security_coefficient):
        '''
        find a prime number that is x bits wide
        large number_of_bits and security_coefficient result in long execution time
        '''
        r=random.getrandbits(number_of_bits)
        finded= False
        while not finded:
            result=primality(security_coefficient)
            finded=result[0]
        return result[1]

if __name__ == "__main__":
    import acc_RSA, doctest
    doctest.testmod(acc_RSA)
    # find_prime()