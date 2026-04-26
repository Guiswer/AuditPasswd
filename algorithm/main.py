import os, sys
from core.generator import generate_random_password, calculate_entropy
from core.auditor import check_pwned_api
from core.crypto import encrypt_data, decrypt_data
from core.i18n import get_messages

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_PATH = os.path.join(BASE_DIR, "data", "vault.bin")

def print_manual_table():
    """Restaura a tabelinha bonita do Guia de Comandos."""
    print("\n" + "="*45)
    print(f"{'CLI ARGUMENTS GUIDE':^45}")
    print("="*45)
    print(f" {'-g':<5} | {'--generate':<12} | {'New password':<20}")
    print(f" {'-a':<5} | {'--audit':<12} | {'Check HIBP Leaks':<20}")
    print(f" {'-s':<5} | {'--save':<12} | {'Encrypt & Save':<20}")
    print(f" {'-r':<5} | {'--retrieve':<12} | {'Open vault':<20}")
    print(f" {'-l n':<5} | {'--length n':<12} | {'Set length (ex: -l 32)':<20}")
    print("="*45)

def execute_logic(flags, msg, current_pwd=None):
    pwd = current_pwd
    length = 24

    if "-l" in flags:
        try: length = int(flags[flags.index("-l") + 1])
        except: pass

    if "-g" in flags:
        pwd = generate_random_password(length)
        print(f"\n{msg['label_gen']}: {pwd}")
        print(f"{msg['label_ent']}: {calculate_entropy(pwd)} bits")

    if "-a" in flags:
        if not pwd: print("[!] Error: -g required.")
        else:
            print(msg['audit_start'])
            leaks = check_pwned_api(pwd)
            if leaks == 0: print(msg['status_clean'])
            elif leaks > 0: print(msg['status_leaked'].format(leaks))

    if "-r" in flags:
        if not os.path.exists(VAULT_PATH):
            print(msg['err_no_vault'])
        else:
            master = input(msg['master_prompt'])
            print(msg['audit_start']) # Reutilizando feedback visual
            with open(VAULT_PATH, "rb") as f:
                for i, line in enumerate(f, 1):
                    dec = decrypt_data(line.strip(), master)
                    # Uso do .get() por segurança extra
                    lbl = msg.get('label_pwd', 'Password')
                    err = msg.get('err_decrypt', 'Error')
                    print(f"  [{i}] {lbl}: {dec}" if dec else f"  [{i}] {err}")
    
    return pwd

def save_flow(pwd, msg):
    if not pwd: return
    master = input(msg['master_prompt'])
    blob = encrypt_data(pwd, master)
    os.makedirs(os.path.dirname(VAULT_PATH), exist_ok=True)
    with open(VAULT_PATH, "ab") as f:
        f.write(blob + b"\n")
    print(msg['save_success'])

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n[Select Language] en, es, ptbr | 0. Exit")
        lang_choice = input("> ").strip().lower()
        if lang_choice == "0": break
        msg = get_messages(lang_choice)

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(msg['top_menu'])
            print(msg['mode_inter'])
            print(msg['mode_cmd'])
            print(msg['mode_back'])
            
            mode = input(msg['choice_prompt'])
            if mode == "0": break

            if mode in ["1", "2"]:
                last_pwd = None
                while True:
                    if mode == "1":
                        print(msg['menu_title'])
                        print(msg['menu_gen'])
                        print(msg['menu_ret'])
                        print(msg['menu_back'])
                        op = input(msg['choice_prompt'])
                        if op == "0": break
                        flags = ["-g", "-a"] if op == "1" else ["-r"]
                    else:
                        print_manual_table()
                        cmd = input(msg['manual_prompt'])
                        if cmd == "0": break
                        flags = cmd.split()

                    last_pwd = execute_logic(flags, msg, last_pwd)

                    if "-g" in flags:
                        while True:
                            sub_op = input(msg['post_gen_menu'])
                            if sub_op == "1":
                                save_flow(last_pwd, msg)
                                break
                            elif sub_op == "2":
                                last_pwd = execute_logic(["-g", "-a"], msg)
                                continue
                            elif sub_op == "0": break
                    
                    if "-r" in flags or mode == "2":
                        input("\n[Enter]...")
                    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()