import base64
import hashlib
import os
import uuid

from cryptography.fernet import Fernet


# === SERIAL (KUNCI BERBASIS HARDWARE) ===
def generate_pc_serial():
    """
    Generates a unique, hashed, and base64-encoded serial key based on the system's hardware and environment information.
    The serial key is derived from the system's UUID, CPU information, and OS information.
    It is hashed using SHA-256 and then encoded in a URL-safe base64 format to ensure compatibility
    with cryptographic libraries like Fernet.
    Returns:
        bytes: A 32-byte URL-safe base64-encoded serial key.
    """
    system_uuid = str(uuid.getnode())
    cpu_info = os.getenv("PROCESSOR_IDENTIFIER", "unknown_cpu")
    os_info = os.getenv("OS", "unknown_os")

    raw_serial = f"{system_uuid}-{cpu_info}-{os_info}"
    hashed_serial = hashlib.sha256(raw_serial.encode()).digest()

    # Harus 32-byte key base64, karena Fernet
    return base64.urlsafe_b64encode(hashed_serial[:32])


# === ENCRYPT & DECRYPT ===
def encrypt(text: str) -> str:
    """
    Encrypts the given text using a hardware-based key.

    Args:
        text (str): The plaintext string to be encrypted.

    Raises:
        ValueError: If encryption fails due to an invalid key or other issues.

    Returns:
        str: The encrypted string (token) in base64 format.
    """
    key = generate_pc_serial()
    try:
        fernet = Fernet(key)
        return fernet.encrypt(text.encode()).decode()
    except Exception as e:
        raise ValueError(f"Encryption failed: {e}")


def decrypt(token: str) -> str:
    """Decrypts the given token using a hardware-based key.

    Args:
        token (str): The encrypted string (token) to be decrypted.

    Raises:
        ValueError: If decryption fails due to an invalid key or other issues.

    Returns:
        str: The decrypted plaintext string.
    """
    key = generate_pc_serial()
    try:
        fernet = Fernet(key)
        return fernet.decrypt(token.encode()).decode()
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")
