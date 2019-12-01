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
        >>> miller_rabin(47)
        True
        '''
        # transformation to x-1= 2^n x r
        m = x-1
        while(x%2 != 0):
            m = int(r/2)
        # choose a number from x-1, can be random
        a = random.randint(2, x-1)
        # compute b=a^m mod x
        b = (a**m) % x
        if(b != 1 & b != (x-1))

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