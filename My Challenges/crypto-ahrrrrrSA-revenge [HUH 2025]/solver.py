# python
from math import gcd

e = 65537

with open('output.txt') as f:
    data = f.read().splitlines()
vals = {k.strip(): int(v.strip()) for line in data for k, v in [line.split('=', 1)]}

N1 = vals.get('N1')
N2 = vals.get('N2')
c1 = vals.get('c1')
c2 = vals.get('c2')
c3 = vals.get('c3')

p = gcd(N1, N2)
q = N1 // p
r = N2 // p
N3 = p * q * r  # reconstructed

def decrypt(c, n, primes):
    if c is None:
        return None
    phi = 1
    for pr in primes:
        phi *= (pr - 1)
    d = pow(e, -1, phi)
    m = pow(c, d, n)
    return m.to_bytes((m.bit_length() + 7) // 8, 'big')

if c1 is not None:
    print(decrypt(c1, N1, (p, q)))
if c2 is not None:
    print(decrypt(c2, N2, (p, r)))
if c3 is not None:
    print(decrypt(c3, N3, (p, q, r)))