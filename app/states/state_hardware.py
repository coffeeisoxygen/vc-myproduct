from app.utils.logger import get_logger
from app.utils import generate_pc_serial
from app.config.settings import SettingManager

logger = get_logger("state.hardware")

class HardwareState:
    """
    Kelas untuk mengelola state hardware.

    Bertugas untuk:
    - Menyimpan dan memverifikasi hardware ID
    - Mengatur pembatasan akses berdasarkan hardware
    """

    def __init__(self, config_manager: SettingManager):
        """
        Inisialisasi HardwareState.

        Args:
            config_manager: Manager konfigurasi yang telah diinisialisasi
        """
        self.config_manager = config_manager
        self.serial_key = generate_pc_serial()
        self.is_valid = self._validate_hardware()

        # Simpan hardware ID jika belum ada
        if not self.get_stored_id():
            self._store_hardware_id()

    def _validate_hardware(self) -> bool:
        """
        Validasi apakah hardware ID sesuai dengan yang tersimpan.

        Returns:
            bool: True jika valid atau belum diset, False jika tidak sesuai
        """
        stored_id = self.get_stored_id()

        # Jika belum ada hardware ID tersimpan, anggap valid
        if not stored_id:
            return True

        # Verifikasi apakah serial yang tersimpan cocok dengan PC ini
        return stored_id == self.serial_key.decode()

    def get_stored_id(self) -> str:
        """
        Mendapatkan hardware ID yang tersimpan di konfigurasi.

        Returns:
            str: Hardware ID yang tersimpan atau string kosong jika belum ada
        """
        return self.config_manager.get("Hardwareid", "hardware_id", "") or ""

    def _store_hardware_id(self) -> bool:
        """
        Menyimpan hardware ID ke konfigurasi.

        Returns:
            bool: True jika berhasil disimpan
        """
        try:
            self.config_manager.set("Hardwareid", "hardware_id", self.serial_key.decode())
            logger.info("Hardware ID set for the first time")
            return True
        except Exception as e:
            logger.error(f"Failed to store hardware ID: {e}")
            return False
