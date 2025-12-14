from Crypto.Util.number import GCD, inverse, long_to_bytes

e = 65537

# read values from output.txt
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