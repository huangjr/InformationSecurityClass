import random

class QuickRSA:
    def miller_rabin(self, x):
        '''
        test whether x is a composite or has the probability to be a prime
        return False when x has an composite witness
        return True when x has no composite witness
        7 times should this test carried out
        >>> quickRSA=QuickRSA()
        >>> quickRSA.miller_rabin(48)
        False
        >>> quickRSA.miller_rabin(47)
        True
        '''
        # transformation to x-1= 2^n x r
        m = x-1
        k = 0
        while((m%2) == 0):
            m = m // 2
            k = k+1
        # choose a number from x-1, can be random
        a = random.randrange(2, x-2)
        # compute b=a^m mod x
        b = pow(a,m,x)
        if(b != 1 and b != (x-1)):
            i=1
            while(i<k and b!=(x-1)):
                b= pow(b,2,x)
                if b==1: 
                    return False
                i=i+1
            if(b!=(x-1)): 
                return False
        return True

    def multiply_and_square(self, x, exponent, n):
        '''
        accelerate method of exponent
        public key "e" was default to 2^16+1
        >>> quickRSA=QuickRSA()
        >>> x = 2
        >>> exponent = 17
        >>> quickRSA.multiply_and_square(x, exponent,20)
        12
        '''
        # translate the exponent to binary array, which is a str object
        exponent = bin(exponent)
        y=x
        for a in exponent[3:]:
            # square on every round: y=y^2 mod n
            y=pow(y,2,n)
            # mutiply on exponent[i] = 1: y=x*y mod n
            if a=='1':
                y=(y*x)%n
        return y

    def crt_Decrypt(self, d,p,q,y):
        '''
        p and q only know to the one have private key, so we use the information of p and q to shorten the decryption time.
        d=private key, p,q=large prime, y=cipherText
        calculate y^d=x(mod pxq)
        >>> quickRSA=QuickRSA()
        >>> chr(quickRSA.crt_Decrypt(43937,277,443,17300))
        2
        >>> chr(quickRSA.multiply_and_square(17300,43937,122711))
        2
        '''
        # transformation: x to xq and xp
        n=p*q
        xp = y%p
        xq = y%q
        # modular exponentiation: compute xp^dp mod p, xq^dq mod q, both eqaul N
        dp = d%(p-1)
        dq = d%(q-1)
        yp = self.multiply_and_square(xp,dp,p)
        yq = self.multiply_and_square(xq,dq,q)
        # inverse transportation
        cp= self.multiplicative_inverse(q, p)
        cq= self.multiplicative_inverse(p, q)
        x = (q*cp*yp+ p*cq*yq)%n
        return x

    def primality(self, suspicious, security_coefficient):
        '''
        determine the primality with x time of miller_rabin test
        '''
        result=True
        for a in range(security_coefficient):
            result=result*self.miller_rabin(suspicious)
        return (result,suspicious)

    def find_prime(self, number_of_bits, security_coefficient):
        '''
        find a prime number that is x bits wide
        large number_of_bits and security_coefficient result in long execution time
        '''
        finded = False
        while not finded:
            r=random.getrandbits(number_of_bits)
            while r%2 != 1:
                # if the random number is an even, then it's useless
                r=random.getrandbits(number_of_bits)
            result=self.primality(r, security_coefficient)
            finded=result[0]
        return result[1]

    def multiplicative_inverse(self, a, m):
        '''
        find the multiplicative inverse of x on the base of n:y
        x must be a prime
        x*y = 1 mod n, k*n+1=x*y, 
        >>> quickRSA=QuickRSA()
        >>> quickRSA.multiplicative_inverse(71,200)
        31
        '''
        m0 = m 
        y = 0
        x = 1
    
        if (m == 1) : 
            return 0
    
        while (a > 1) : 
            q = a // m 
    
            t = m 
    
            m = a % m 
            a = t 
            t = y 

            y = x - q * y 
            x = t 
        if (x < 0) : 
            x = x + m0 
    
        return x

if __name__ == "__main__":
    import acc_RSA, doctest
    doctest.testmod(acc_RSA)
    # find_prime()