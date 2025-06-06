import PyKCS11

# Setup
pkcs11 = PyKCS11.PyKCS11Lib()
pkcs11.load("/usr/lib/softhsm/libsofthsm2.so")

slot = pkcs11.getSlotList(tokenPresent=True)[0]
session = pkcs11.openSession(slot, PyKCS11.CKF_SERIAL_SESSION | PyKCS11.CKF_RW_SESSION)
session.login("1234")

print(f"🔑 Slot encontrado: {slot}")

# Helper para decodificar LABEL
def safe_decode(val):
    if isinstance(val, bytes):
        return val.decode("utf-8")
    return val

# Listar chaves com filtros
def listar_chaves(filtro_label=None, filtro_id=None):
    if not filtro_label and not filtro_id:
        print("⚠️ Nenhum filtro definido. A operação foi cancelada por segurança.")
        return
    if filtro_label and not isinstance(filtro_label, str):
        print("⚠️ Filtro de LABEL deve ser uma string.")
        return
    if filtro_id and not isinstance(filtro_id, (list, tuple)):
        print("⚠️ Filtro de ID deve ser uma lista ou tupla.")
        return

    print("🔎 Objetos encontrados no token:")
    found = False

    for obj in session.findObjects([(PyKCS11.CKA_CLASS, PyKCS11.CKO_SECRET_KEY)]):
        try:
            label = session.getAttributeValue(obj, [PyKCS11.CKA_LABEL])[0]
            obj_id = session.getAttributeValue(obj, [PyKCS11.CKA_ID])[0]
            label_str = safe_decode(label)

            # Aplica filtros
            if filtro_label and label_str != filtro_label:
                continue
            if filtro_id and obj_id != filtro_id:
                continue

            # Mostra info
            found = True
            print("🧾 Objeto:")
            print(f"  LABEL: {label_str}")
            print(f"  ID: {obj_id}")
            print("-" * 30)
        except Exception as e:
            print(f"❌ Erro ao obter atributos: {e}")
            continue

    if not found:
        print("⚠️ Nenhum objeto encontrado com os filtros fornecidos.")

# ✅ Teste: substitui por um ID real, exemplo: (94, 114, 192, 113)
# listar_chaves(filtro_id=(94, 114, 192, 113))
# listar_chaves(filtro_label="file-key")
listar_chaves()

session.logout()
session.closeSession()
