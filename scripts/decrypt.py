import math
from Crypto.Util.number import long_to_bytes, inverse

def main():
    # Reading the inputs file-by-file
    for i in range(1, 49): # Total 48 files from out1 to out48
        filename = f"./outs/out{i}.txt"
        try:
            with open(filename, "r") as f:
                data = f.read()
        except:
            print(f"File {filename} not found")
            continue

        n = None
        e = None
        c = None
        secret1 = None
        secret2 = None
        lines = data.splitlines()
        for line in lines:
            if line.startswith("n = "):
                n = int(line.split("=")[1].strip())
            elif line.startswith("e = "):
                e = int(line.split("=")[1].strip())
            elif line.startswith("c = "):
                c = int(line.split("=")[1].strip())
            elif line.startswith("secret1 = "):
                secret1 = int(line.split("=")[1].strip())
            elif line.startswith("secret2 = "):
                secret2 = int(line.split("=")[1].strip())
        
        if n is None or e is None or c is None or secret1 is None or secret2 is None:
            print(f"Missing data in {filename}")
            continue
        # File data/input parsed
        S = math.isqrt(math.isqrt(n))
        S4 = S**4
        C = n - S4 - secret1 * secret2
        D = C**2 - 4 * secret2 * secret1 * S4
        root_D = math.isqrt(D)
        if root_D**2 != D:
            continue

        X1 = None
        X2 = None
        if (C + root_D) % (2 * secret2) == 0:
            X1 = (C + root_D) // (2 * secret2)
        if (C - root_D) % (2 * secret2) == 0: 
            X2 = (C - root_D) // (2 * secret2)
        
        a = None
        for X in [X1, X2]:
            if X is None or X <= 0:
                continue
            a_candidate = math.isqrt(math.isqrt(X))
            if a_candidate**4 == X:
                a = a_candidate
                break
            if (a_candidate + 1)**4 == X: # Adjusting for errors
                a = a_candidate + 1
                break
        
        if a is None:
            continue
        # a found
        p = a**4 + secret1 
        if n % p != 0:
            continue # p found
        q = n // p # q found
        phi = (p - 1) * (q - 1) # phi(N) found
        d = inverse(e, phi) # private exponent (d) found
        m = pow(c, d, n) # message decrypted
        try:
            password = long_to_bytes(m).decode('utf-8') # converting message from long to ascii
            print(f"Password found in {filename}: {password}")
            continue
        except:
            continue
    
    print("Password not found in any file.")

if __name__ == "__main__":
    main()