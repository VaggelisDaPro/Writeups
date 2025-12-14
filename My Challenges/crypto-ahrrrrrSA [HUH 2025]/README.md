# **AhrrrrSA** Writeup

| Challenge | AhrrrrSA |
| :------- | :----- |
| Difficulty | Easy |
| Category | Crypto |

# Challenge Overview
The pirate tried encrypting the treasure's location with RSA... That didn't go as planned.

# Code Analysis
We are given the following code:
```py
from Crypto.Util.number import getPrime, GCD, bytes_to_long

FLAG = b"flag{REDACTED}"
DECOY = b"REDACTED"

e = 65537
p = getPrime(256)
q = getPrime(256)
r = getPrime(256)

N1 = p * q
N2 = p * r

cflag = pow(bytes_to_long(FLAG), e, N1)
cdecoy = pow(bytes_to_long(DECOY), e, N2)

with open('output.txt', 'w') as f:
    f.write(f"N1 = {N1}\n")
    f.write(f"N2 = {N2}\n")
    f.write(f"cflag = {cflag}\n")
    f.write(f"cdecoy = {cdecoy}\n")
```

## What it does:
It generates 3 primes, `p`, `q` and `r` all of which are used in the creation of `N1` and `N2` which are then used to create `cflag` and `cdecoy` respectively. These values are written to `output.txt`.

# Vulnerability
The vulnerability here is the fact that `N1` and `N2` both use `p` to be calculated, meaning that it can easily be recovered with **greatest common divisor** (`gcd()` function).

Here's a solver script:
```py
from Crypto.Util.number import GCD, inverse, long_to_bytes

e = 65537

# take the values from output.txt
with open('output.txt') as f:
    data = f.read()
def parse(name):
    for line in data.splitlines():
        if line.startswith(name):
            return int(line.split('=',1)[1].strip())
    raise ValueError(name + " not found")

N1 = parse("N1")
N2 = parse("N2")
cflag = parse("cflag")

p = GCD(N1, N2)
q = N1 // p

phi = (p - 1) * (q - 1)
d = inverse(e, phi)

m = pow(cflag, d, N1)
print(long_to_bytes(m))
```

# Flag
```
flag{p1r4t3s_h4t3_rsa!!}
```