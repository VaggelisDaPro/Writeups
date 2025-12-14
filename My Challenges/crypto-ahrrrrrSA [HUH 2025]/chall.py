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