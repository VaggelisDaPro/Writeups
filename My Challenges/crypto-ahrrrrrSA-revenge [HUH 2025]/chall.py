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
    