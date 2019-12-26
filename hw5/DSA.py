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
    import sys
    if sys.argv[]