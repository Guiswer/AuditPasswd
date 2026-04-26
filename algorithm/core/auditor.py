import hashlib
import requests

def check_pwned_api(password):
    """
    Verifica se a credencial consta em bancos de dados vazados (HIBP).
    Usa K-Anonymity para preservar a privacidade do usuário.
    """
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        # O sufixo é retornado em uma lista: SUFIXO:CONTAGEM
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return int(count)
        return 0
    except requests.RequestException:
        return -1 # Erro de comunicação com o servidor