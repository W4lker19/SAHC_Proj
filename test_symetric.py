import os
import random
import argparse
from Crypto.Util.Padding import pad, unpad
from PyKCS11 import *
from PyKCS11.LowLevel import CK_TRUE, CK_FALSE

# Constantes
SOFTHSM_LIB = "/usr/lib/softhsm/libsofthsm2.so"
USER_PIN = "1234"
KEY_LABEL = "file-key"
BLOCK_SIZE = 16

# Argumentos da linha de comandos
parser = argparse.ArgumentParser(description="Cifrar ou decifrar ficheiros com AES via HSM.")
parser.add_argument("modo", choices=["encrypt", "decrypt"], help="Modo de operação: encrypt ou decrypt")
parser.add_argument("ficheiro_entrada", help="Caminho do ficheiro de entrada")
parser.add_argument("ficheiro_saida", nargs="?", help="Caminho do ficheiro de saída (opcional)")
args = parser.parse_args()

# Inicializar PKCS#11 e sessão
pkcs11 = PyKCS11Lib()
pkcs11.load(SOFTHSM_LIB)
slot = pkcs11.getSlotList(tokenPresent=True)[0]
session = pkcs11.openSession(slot, CKF_SERIAL_SESSION | CKF_RW_SESSION)
session.login(USER_PIN)

# Criar ou obter chave AES
def get_or_create_aes_key(label: str):
    keys = session.findObjects([
        (CKA_LABEL, label),
        (CKA_CLASS, CKO_SECRET_KEY),
        (CKA_KEY_TYPE, CKK_AES),
    ])
    if keys:
        print("🔐 Chave existente encontrada.")
        return keys[0]

    random_id = list(random.randint(0, 2**32 - 1).to_bytes(4, byteorder="big"))
    key_template = [
        (CKA_CLASS, CKO_SECRET_KEY),
        (CKA_KEY_TYPE, CKK_AES),
        (CKA_LABEL, label),
        (CKA_ID, random_id),
        (CKA_TOKEN, CK_TRUE),
        (CKA_PRIVATE, CK_FALSE),
        (CKA_ENCRYPT, CK_TRUE),
        (CKA_DECRYPT, CK_TRUE),
        (CKA_VALUE_LEN, 32),  # 256-bit
    ]
    print(f"🆕 A criar nova chave com ID: {random_id}")
    return session.generateKey(key_template)

# Função para gerar nome único aleatório
def gerar_nome_unico(extensao):
    # Gera um número único aleatório com 6 dígitos
    nome_unico = random.randint(100000, 999999)
    return f"{nome_unico}{extensao}"

# Cifrar ficheiro
def encrypt_file(input_path, output_path, key):
    iv = os.urandom(BLOCK_SIZE)
    with open(input_path, "rb") as f:
        plaintext = f.read()

    # Obter e salvar a extensão do ficheiro
    file_ext = os.path.splitext(input_path)[1].lower()
    
    # Escrever o tamanho da extensão seguido pela própria extensão
    ext_len = len(file_ext).to_bytes(1, byteorder='big')  # 1 byte para o tamanho da extensão

    padded = pad(plaintext, BLOCK_SIZE)
    mechanism = Mechanism(CKM_AES_CBC, iv)
    ciphertext = session.encrypt(key, list(padded), mechanism)
    
    with open(output_path, "wb") as f:
        f.write(ext_len)  # Escreve o tamanho da extensão
        f.write(file_ext.encode('utf-8'))  # Escreve a extensão
        f.write(iv + bytes(ciphertext))

    print(f"🛡️ Ficheiro cifrado: {output_path}")

# Decifrar ficheiro
def decrypt_file(input_path, output_path, key):
    with open(input_path, "rb") as f:
        # Ler o tamanho da extensão (1 byte) e a extensão
        ext_len = int.from_bytes(f.read(1), byteorder='big')
        file_ext = f.read(ext_len).decode('utf-8')
        data = f.read()

    iv = data[:BLOCK_SIZE]
    ciphertext = data[BLOCK_SIZE:]
    mechanism = Mechanism(CKM_AES_CBC, iv)
    decrypted = session.decrypt(key, list(ciphertext), mechanism)
    unpadded = unpad(bytes(decrypted), BLOCK_SIZE)

    # Se não for especificado ficheiro de saída, manter o mesmo nome mas com a extensão correta
    if not output_path:
        # Substituir a extensão do ficheiro cifrado pela original
        output_path = os.path.splitext(input_path)[0] + file_ext

    with open(output_path, "wb") as f:
        f.write(unpadded)
    
    print(f"🔓 Ficheiro decifrado: {output_path}")

# Execução principal
aes_key = get_or_create_aes_key(KEY_LABEL)

if args.modo == "encrypt":
    output = args.ficheiro_saida or gerar_nome_unico(".enc")
    encrypt_file(args.ficheiro_entrada, output, aes_key)

elif args.modo == "decrypt":
    output = args.ficheiro_saida or None
    decrypt_file(args.ficheiro_entrada, output, aes_key)

# Encerrar sessão
session.logout()
pkcs11.closeAllSessions(slot)
