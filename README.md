# 10_days

## Decryption

The decryption algorithm can be simplified as follows:
```
from Crypto.Util.number import *
from functools import reduce
import random

def rI(b, mod):
    return getRandomNBitInteger(b) + mod

def cP(a, b, m):
    return a ** m + b

def gP():
    while True:
        a = rI(2048 // 4, 1)
        r = rI(16, random.randint(1, 3))
        p = a**4 + r
        if isPrime(p):
            return (p, r)

def sm():
    e = 65537
    p, a = gP(4)
    q, b = gP(4)
    n = p * q
    return e, n, p, q, a, b
# m=4
def encrypt():
    e, n, p, q, a, b = sm()
    with open("password.txt", "rb") as f:
        password = f.read().strip()
    mLng = bytes_to_long(password)
    c = pow(mLng, e, n)
    with open("out.txt", "w") as out:
        out.write(f"n = {n}\n")
        out.write(f"e = {e}\n")
        out.write(f"c = {c}\n")
        out.write(f"secret1 = {a}\n")
        out.write(f"secret2 = {b}\n")

encrypt()
```

What's happening here is that this RSA is implemented as follows:<br>

N = p * q<br>
p = a^4 + r_1<br>
q = b^4 + r_2<br>



So here a and b are 512 bit and r_1 and r_2 are 16 bit.<br>
What's being returned in the `out.txt` are the values of n, e, c, secret1 and secret 2. secret_1 and secret_2 that are being returned as a and b are actually r_1 and r_2. <br>
Ignoring the values of r_1 and r_2 compared to a^4 and b^4 (16 bit compared to 2048 bit integer), we can approximate N = (a\*b)^4.<br>
Taking S to be equal to the fourth root of N, i.e., `S=N^(1/4)`, and expanding N.<br>

We start with $N = p \cdot q = (a^4 + r_1)(b^4 + r_2)$.<br>

Expanding: $N = (ab)^4 + a^4 r_2 + b^4 r_1 + r_1 r_2$.<br>

Let $S = a \cdot b$.<br>

Then we can form the polynomial: $r_2 X^2 - \bigl(N - S^4 - r_1 r_2\bigr) X + r_1 S^4 = 0$<br>

Now we solve for X, and the fourth of the root as `X = a^4`. <br>
Then we have obtained a from which we can get p as `p = a^4 + r_1` and r_1 is already known. Then we obtain q from `N // p`. Then we get `phi(N) = (p-1)(q-1)`. From there we obtain d as `d\*e = 1 modulo(phi(N))`, from `d = e^-1 modulo(phi(N))`.<br>
Then we can obtain the decrypted message as `m = c^d modulo(N)`.<br>
Then convert the obtained long integer into ascii (utf-8).<br>

Attached in the `scripts` folder is the decryption script as `decrypt.txt`.<br>
