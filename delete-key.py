import PyKCS11

""" O que este script faz:
1. Encontra objetos no token com o tipo de chave CKO_SECRET_KEY (chaves simétricas).
2. Filtra os objetos com base no LABEL ou ID fornecido.
3. Apaga a chave correspondente usando session.destroyObject(obj).
4. Exibe uma mensagem informando que a chave foi apagada ou se nenhuma chave foi encontrada para ser apagada com o filtro fornecido. 
"""

# Inicializar a biblioteca PKCS#11
pkcs11 = PyKCS11.PyKCS11Lib()
pkcs11.load("/usr/lib/softhsm/libsofthsm2.so")  # Certifique-se de que o caminho está correto

# Abrir a sessão
slot = pkcs11.getSlotList(tokenPresent=True)[0]
print(f"🔑 Slot encontrado: {slot}")
session = pkcs11.openSession(slot, PyKCS11.CKF_SERIAL_SESSION | PyKCS11.CKF_RW_SESSION)
session.login("1234")

def apagar_chave(filtro_label=None, filtro_id=None):
    if not filtro_label and not filtro_id:
        print("⚠️ Nenhum filtro definido. A operação foi cancelada por segurança.")
        return

    # Encontrar todas as chaves no token
    objects = session.findObjects([
        (PyKCS11.CKA_CLASS, PyKCS11.CKO_SECRET_KEY)
    ])

    if not objects:
        print("⚠️ Nenhuma chave encontrada no token.")
        return

    chave_apagada = False

    for obj in objects:
        try:
            atributos = session.getAttributeValue(obj, [
                PyKCS11.CKA_LABEL,
                PyKCS11.CKA_ID
            ])
            label = atributos[0]
            obj_id = atributos[1]
        except PyKCS11.PyKCS11Error:
            continue  # Ignora objetos com atributos inacessíveis

        # Verificar se ambos os filtros coincidem
        if (filtro_label is not None and label != filtro_label) or \
           (filtro_id is not None and obj_id != filtro_id):
            continue

        # Apagar a chave
        print(f"🔴 Apagando chave com LABEL: {label} e ID: {obj_id}")
        session.destroyObject(obj)
        chave_apagada = True

    if not chave_apagada:
        print("⚠️ Nenhuma chave encontrada com os filtros fornecidos.")

# Apagar apenas se LABEL for "file-key" e ID for (194, 144, 186, 175)
apagar_chave(filtro_label="file-key", filtro_id=(136, 12, 245, 218))

session.logout()
session.closeSession()
# Ou apagar chaves com um ID específico
# apagar_chave(filtro_id="algum_id")
