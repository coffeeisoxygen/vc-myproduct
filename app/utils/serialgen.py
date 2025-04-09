import base64
import hashlib
import os
import uuid

from cryptography.fernet import Fernet


# === SERIAL (KUNCI BERBASIS HARDWARE) ===
def generate_pc_serial():
    system_uuid = str(uuid.getnode())
    cpu_info = os.getenv("PROCESSOR_IDENTIFIER", "unknown_cpu")
    os_info = os.getenv("OS", "unknown_os")

    raw_serial = f"{system_uuid}-{cpu_info}-{os_info}"
    hashed_serial = hashlib.sha256(raw_serial.encode()).digest()

    # Harus 32-byte key base64, karena Fernet
    return base64.urlsafe_b64encode(hashed_serial[:32])


# === ENCRYPT & DECRYPT ===
def encrypt(text: str) -> str:
    key = generate_pc_serial()
    fernet = Fernet(key)
    return fernet.encrypt(text.encode()).decode()


def decrypt(token: str) -> str:
    key = generate_pc_serial()
    fernet = Fernet(key)
    return fernet.decrypt(token.encode()).decode()
