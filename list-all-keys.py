from PyKCS11 import PyKCS11Lib, CKA_LABEL, CKA_ID, CKA_CLASS, CKA_KEY_TYPE
import PyKCS11

PKCS11_LIB = "/usr/lib/softhsm/libsofthsm2.so"  # adapta para o caminho correto
PIN = "1234"

pkcs11 = PyKCS11Lib()
pkcs11.load(PKCS11_LIB)

slot = pkcs11.getSlotList(tokenPresent=True)[0]
print(f"🔑 Slot encontrado: {slot}")
session = pkcs11.openSession(slot)
session.login(PIN)

# Listar todos os objetos
objects = session.findObjects()

print(f"🔎 Encontrados {len(objects)} objetos no token.")
print("=====================================")

if not objects:
    print(f"⚠️ Nenhum objeto encontrado no token.")
    session.logout()
    session.closeSession()
    exit()

print(f"🔎 Listando objetos no token. Slot: {slot}")
print("=====================================")

for obj in objects:
    attr_dict = {}
    for attr_type, attr_name in [
        (CKA_CLASS, "CLASS"),
        (CKA_KEY_TYPE, "KEY_TYPE"),
        (CKA_LABEL, "LABEL"),
        (CKA_ID, "ID")
    ]:
        try:
            value = session.getAttributeValue(obj, [attr_type])[0]
            attr_dict[attr_name] = value
        except PyKCS11.PyKCS11Error:
            attr_dict[attr_name] = "N/A"

    # Mostrar os dados
    print("🧾 Objeto:")
    for key, value in attr_dict.items():
        print(f"  {key}: {value}")
    print("-" * 30)

session.logout()
session.closeSession()
