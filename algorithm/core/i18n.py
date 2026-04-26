# core/i18n.py

LANGUAGES = {
    "ptbr": {
        "top_menu": "\n=== MENU DE MODO ===",
        "mode_inter": "1. Modo Interativo (Wizard)",
        "mode_cmd": "2. Prompt de Comandos (Manual)",
        "mode_back": "0. Voltar para Seleção de Idioma",
        "menu_title": "\n--- OPERAÇÕES DO COFRE ---",
        "menu_gen": "1. Gerar e Auditar",
        "menu_ret": "2. Recuperar Tudo",
        "menu_back": "0. Voltar",
        "choice_prompt": "[>] Opção: ",
        "manual_prompt": "[>] Flags (ex: -g -a) ou 0 p/ voltar: ",
        "post_gen_menu": "\n[1] Salvar | [2] Gerar outra | [0] Voltar",
        "master_prompt": "[>] Master Password: ",
        "label_gen": "[+] Senha",
        "label_ent": "[+] Entropia",
        "label_pwd": "Senha",  # CHAVE CORRIGIDA
        "audit_start": "[*] Consultando vazamentos...",
        "status_clean": "[✓] Status: Limpa",
        "status_leaked": "[!] STATUS: Vazou {} vezes.",
        "save_success": "[✓] Salvo com sucesso!",
        "err_no_vault": "[!] Erro: Cofre não encontrado.",
        "err_decrypt": "Erro: Chave incorreta.",
        "exit_msg": "Encerrando..."
    },
    "en": {
        "top_menu": "\n=== MODE MENU ===",
        "mode_inter": "1. Interactive Mode (Wizard)",
        "mode_cmd": "2. Command Prompt (Manual)",
        "mode_back": "0. Back to Language Selection",
        "menu_title": "\n--- VAULT OPERATIONS ---",
        "menu_gen": "1. Generate and Audit",
        "menu_ret": "2. Retrieve All",
        "menu_back": "0. Back",
        "choice_prompt": "[>] Option: ",
        "manual_prompt": "[>] Enter flags (e.g. -g -a) or 0 to back: ",
        "post_gen_menu": "\n[1] Save | [2] Generate another | [0] Back",
        "master_prompt": "[>] Master Password: ",
        "label_gen": "[+] Password",
        "label_ent": "[+] Entropy",
        "label_pwd": "Password", # CHAVE CORRIGIDA
        "audit_start": "[*] Checking leaks...",
        "status_clean": "[✓] Status: Clean",
        "status_leaked": "[!] STATUS: Leaked {} times.",
        "save_success": "[✓] Saved successfully!",
        "err_no_vault": "[!] Error: Vault not found.",
        "err_decrypt": "Error: Incorrect key.",
        "exit_msg": "Exiting..."
    },
    "es": {
        "top_menu": "\n=== MENÚ DE MODO ===",
        "mode_inter": "1. Modo Interactivo (Wizard)",
        "mode_cmd": "2. Símbolo del Sistema (Manual)",
        "mode_back": "0. Volver a Selección de Idioma",
        "menu_title": "\n--- OPERACIONES DE BÓVEDA ---",
        "menu_gen": "1. Generar y Auditar",
        "menu_ret": "2. Recuperar Todo",
        "menu_back": "0. Volver",
        "choice_prompt": "[>] Opción: ",
        "manual_prompt": "[>] Flags (ej: -g -a) o 0 para volver: ",
        "post_gen_menu": "\n[1] Guardar | [2] Generar otra | [0] Volver",
        "master_prompt": "[>] Contraseña Maestra: ",
        "label_gen": "[+] Contraseña",
        "label_ent": "[+] Entropía",
        "label_pwd": "Contraseña", # CHAVE CORRIGIDA
        "audit_start": "[*] Consultando filtraciones...",
        "status_clean": "[✓] Estado: Limpio",
        "status_leaked": "[!] ESTADO: Filtrado {} veces.",
        "save_success": "[✓] ¡Guardado con éxito!",
        "err_no_vault": "[!] Error: Bóveda no encontrada.",
        "err_decrypt": "Error: Llave incorrecta.",
        "exit_msg": "Saliendo..."
    }
}

def get_messages(lang):
    return LANGUAGES.get(lang, LANGUAGES["en"])