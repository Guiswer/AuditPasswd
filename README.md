# AuditPasswd
SecPass é uma ferramenta de linha de comando (CLI) desenvolvida em Python para a geração, auditoria e armazenamento seguro de credenciais. O projeto foca em três pilares fundamentais da segurança da informação: Criptografia Forte, Privacidade de Dados e Análise Matemática de Entropia.


## Funcionalidades
Geração Segura: Utiliza CSPRNG (Gerador de Números Pseudo-Aleatórios Criptograficamente Seguro) para garantir a imprevisibilidade das senhas.

Cálculo de Entropia: Avaliação matemática em tempo real da força da senha em bits.

Auditoria via HIBP: Integração com a API Have I Been Pwned utilizando K-Anonymity (o hash da senha nunca sai da máquina).

Cofre Criptografado: Armazenamento binário protegido por Fernet (AES-256) com derivação de chave robusta.

Internacionalização (i18n): Suporte completo para Português (PT-BR), Inglês (EN) e Espanhol (ES).

Interface Dual: Modo Interativo (Wizard) para usuários casuais e Prompt de Comandos para operações rápidas.
---
## Arquitetura de Segurança
### Este projeto foi construído seguindo recomendações do NIST e OWASP:
1. Criptografia e Derivação de Chave
Para proteger o cofre (vault.bin), não utilizamos a senha mestre diretamente como chave. Implementamos Key Stretching via PBKDF2 (Password-Based Key Derivation Function 2):

Algoritmo: HMAC-SHA256.

Iterações: 600.000 (superior ao padrão recomendado para mitigar ataques de força bruta offline).

Salt: 16 bytes aleatórios gerados por os.urandom para cada registro, impedindo ataques de Rainbow Tables.

2. Privacidade e K-Anonymity
Ao verificar se uma senha vazou, o SecPass utiliza o protocolo de K-Anonymity. Apenas os 5 primeiros caracteres do hash SHA-1 são enviados à API. O confronto final do hash completo é feito localmente, garantindo que o servidor remoto nunca saiba qual senha está sendo consultada.

3. Entropia de Shannon
A força da senha é calculada com base no espaço de busca (R) e comprimento (L), utilizando a fórmula:
H = L * log2(R)

Isso fornece uma métrica objetiva da dificuldade teórica de quebra da credencial em bits de entropia.

   
# Instalação
### Clonando o repositório:
git clone https://github.com/Guiswer/AuditPasswd

### Instalando as dependências (é necessário possuir o pip):
pip install -r requirements.txt

### Depois das instalações, execute o main.py com o python.
Exemplo: python{versão} main.py


### Comandos do modo manual:
-g [Extenso: --generate]: Gera uma nova senha.
-l [Extenso: --length]: Define o comprimento para 32 caracteres.
-a [Extenso: --audit]: Realiza a auditoria de vazamento.
-s [Extenso: --save]: Salva a senha no cofre.
-r [Extenso: --retrieve]: Recupera e descriptografa as senhas do cofre.

### Exemplo de comando encadeado:
[>] Comando: -g -a -s -l 24
[>] Comando extenso: --generate --audit --save --length 24
[>] Comando mescla: -g --audit --save -l 24

### Utilizar na ordem:
Gerar -> Auditar -> Salvar -> Comprimento
