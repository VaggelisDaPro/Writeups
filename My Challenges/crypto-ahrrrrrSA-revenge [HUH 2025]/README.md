# **AhrrrrSA - Revenge** Writeup

| Challenge | AhrrrrSA - Revenge |
| :------- | :----- |
| Difficulty | Medium |
| Category | Crypto |

# Challenge Overview
The pirate tried encrypting the treasure's location with RSA... That didn't go as planned. Now the pirate doesn't know which location has the treasure!!

# Code Analysis
We are given the following code:
```py
from Crypto.Util.number import getPrime, GCD, bytes_to_long

C1_TEXT = b"REDACTED"
C2_TEXT = b"REDACTED"
C3_TEXT = b"REDACTED"

e = 65537
p = getPrime(512)
q = getPrime(512)
r = getPrime(512)
k = getPrime(128)
N1 = p * q
N2 = p * r
N3 = p * q * r

c1 = pow(bytes_to_long(C1_TEXT), e, N1)
c2 = pow(bytes_to_long(C2_TEXT), e, N2)
c3 = pow(bytes_to_long(C3_TEXT), e, N3)

with open('output.txt', 'w') as f:
    f.write(f"N1 = {N1}\n")
    f.write(f"N2 = {N2}\n")
    f.write(f"c1 = {c1}\n")
    f.write(f"c2 = {c2}\n")
    f.write(f"c3 = {c3}")
```

## What it does:
The code produces 3 primes, `p`, `q` and `r` like the original challenge. `N1`, `N2` and `N3` are calculated and used for encrypting the 3 ciphertexts.
$$\text{N1} = p * q$$
$$\text{N2} = p * r$$
$$\text{N3} = p * q * r$$

Importantly, `N3` is **never provided**.

# Vulnerability
**BUT** because `N1` and `N2` share the prime `p` we can compute (like the original challenge):
```py
p = gcd(N1, N2)
```
And from there we can calculate:
```py
q = N1 / p
r = N2 / p
# and once we know both p and q
N3 = p * q * r
```

Here's a solver script:
```py
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
```

# Flag
```
flag{p1r4tes_p1rat3s_p1rat3_s0ftw4r3}
```