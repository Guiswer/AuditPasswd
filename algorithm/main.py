import os, sys
from core.generator import generate_random_password, calculate_entropy
from core.auditor import check_pwned_api
from core.crypto import encrypt_data, decrypt_data
from core.i18n import get_messages

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_PATH = os.path.join(BASE_DIR, "data", "vault.bin")

def print_manual_table():
    """Restores the CLI Arguments Guide table."""
    print("\n" + "="*45)
    print(f"{'CLI ARGUMENTS GUIDE':^45}")
    print("="*45)
    print(f" {'-g':<5} | {'--generate':<12} | {'New password':<20}")
    print(f" {'-a':<5} | {'--audit':<12} | {'Check HIBP Leaks':<20}")
    print(f" {'-s':<5} | {'--save':<12} | {'Encrypt & Save':<20}")
    print(f" {'-r':<5} | {'--retrieve':<12} | {'Open vault':<20}")
    print(f" {'-l n':<5} | {'--length n':<12} | {'Set length (ex: -l 32)':<20}")
    print("="*45)

def save_flow(pwd, msg):
    """Saves the password with duplicate check."""
    if not pwd: return False
    
    master = input(msg['master_prompt'])
    
    # 1. Check if it already exists in the vault
    if os.path.exists(VAULT_PATH):
        with open(VAULT_PATH, "rb") as f:
            for line in f:
                if not line.strip(): continue
                # If it decrypts and matches, block the saving process
                if decrypt_data(line.strip(), master) == pwd:
                    print(msg.get('err_duplicate', "[!] Duplicate found."))
                    return False
    
    # 2. Save if it is unique
    blob = encrypt_data(pwd, master)
    os.makedirs(os.path.dirname(VAULT_PATH), exist_ok=True)
    with open(VAULT_PATH, "ab") as f:
        f.write(blob + b"\n")
    print(msg['save_success'])
    return True

def execute_logic(flags, msg, current_pwd=None):
    """Executes the logic and returns the resulting password to maintain state."""
    pwd = current_pwd
    length = 24

    has_gen = "-g" in flags or "--generate" in flags
    has_audit = "-a" in flags or "--audit" in flags
    has_save = "-s" in flags or "--save" in flags
    has_ret = "-r" in flags or "--retrieve" in flags

    if "-l" in flags or "--length" in flags:
        try:
            idx = flags.index("-l") if "-l" in flags else flags.index("--length")
            length = int(flags[idx + 1])
        except: pass

    # Execution order: Generate -> Audit -> Save
    if has_gen:
        pwd = generate_random_password(length)
        print(f"\n{msg['label_gen']}: {pwd}")
        print(f"{msg['label_ent']}: {calculate_entropy(pwd)} bits")

    if has_audit:
        if not pwd: print("[!] Error: -g required.")
        else:
            print(msg['audit_start'])
            leaks = check_pwned_api(pwd)
            if leaks == 0: print(msg['status_clean'])
            elif leaks > 0: print(msg['status_leaked'].format(leaks))

    if has_save:
        if not pwd: print("[!] Error: Nothing to save.")
        else: save_flow(pwd, msg)

    if has_ret:
        if not os.path.exists(VAULT_PATH): print(msg['err_no_vault'])
        else:
            master = input(msg['master_prompt'])
            print(msg['decrypting'])
            with open(VAULT_PATH, "rb") as f:
                for i, line in enumerate(f, 1):
                    dec = decrypt_data(line.strip(), master)
                    lbl, err = msg.get('label_pwd', 'Pass'), msg.get('err_decrypt', 'Err')
                    print(f"  [{i}] {lbl}: {dec}" if dec else f"  [{i}] {err}")
    
    return pwd

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nWelcome! Select language / Selecione o idioma:")
        print("Options: en, es, ptbr | 0. Exit")
        lang_input = input("[>] Language: ").strip().lower()

        if lang_input == "0": break
        msg = get_messages(lang_input)

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
                        # In the Wizard, we generate and audit, but don't save automatically
                        flags = ["-g", "-a"] if op == "1" else ["-r"]
                    else:
                        print_manual_table()
                        cmd = input(msg['manual_prompt'])
                        if cmd == "0": break
                        flags = cmd.split()

                    last_pwd = execute_logic(flags, msg, last_pwd)

                    # Sub-menu logic
                    if ("-g" in flags or "--generate" in flags) and ("-s" not in flags and "--save" not in flags):
                        while True:
                            sub_op = input(msg['post_gen_menu'])
                            if sub_op == "1":
                                save_flow(last_pwd, msg)
                                break
                            elif sub_op == "2":
                                last_pwd = execute_logic(["-g", "-a"], msg)
                                continue
                            elif sub_op == "0": break
                    
                    if any(f in flags for f in ["-r", "--retrieve", "-s", "--save"]) or mode == "2":
                        input("\n[Enter]...")
                    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()