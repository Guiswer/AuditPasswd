import hashlib
import requests

def check_pwned_api(password):
    """
    Checks if the credential exists in leaked databases (HIBP).
    Uses K-Anonymity to preserve user privacy.
    """
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        # The suffix is returned in a list: SUFFIX:COUNT
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return int(count)
        return 0
    except requests.RequestException:
        return -1 # Server communication error