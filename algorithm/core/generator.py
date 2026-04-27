import secrets
import string
import math

def calculate_entropy(password):
    """
    Calculates the Shannon entropy of the password.
    
    Formula: $$H = L \cdot \log_2(R)$$
    Measures the theoretical resistance against offline brute-force attacks.
    """
    if not password:
        return 0
    
    pool = 0
    if any(c in string.ascii_lowercase for c in password): pool += 26
    if any(c in string.ascii_uppercase for c in password): pool += 26
    if any(c in string.digits for c in password): pool += 10
    if any(c in string.punctuation for c in password): pool += 32
    
    length = len(password)
    # H = L * log2(Pool)
    entropy = length * math.log2(pool) if pool > 0 else 0
    return round(entropy, 2)

def generate_random_password(length=24):
    """
    Generates random strings using the Operating System's 
    CSPRNG (Cryptographically Secure Pseudo-Random Number Generator).
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))