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
        self._serial_key = None  # Lazy loading untuk menghemat resources

        # Status validasi
        self._is_valid = None

    @property
    def serial_key(self):
        """
        Mendapatkan serial key PC saat ini (lazy loading).

        Returns:
            bytes: Serial key dalam bentuk bytes
        """
        if self._serial_key is None:
            self._serial_key = generate_pc_serial()
        return self._serial_key

    @property
    def is_valid(self) -> bool:
        """
        Memeriksa apakah hardware ID valid.

        Returns:
            bool: True jika valid, False jika tidak
        """
        if self._is_valid is None:
            self._is_valid = self.validate()
        return self._is_valid

    def validate(self) -> bool:
        """
        Validasi apakah hardware ID sesuai dengan yang tersimpan.

        Jika hardware ID belum ada di konfigurasi, akan disimpan.

        Returns:
            bool: True jika valid atau berhasil disimpan, False jika tidak sesuai
        """
        stored_id = self.get_stored_id()

        # Jika belum ada hardware_id tersimpan, simpan dan return valid
        if not stored_id:
            logger.info("No hardware ID found, storing new ID")
            return self._store_hardware_id()

        # Verifikasi apakah serial yang tersimpan cocok dengan PC ini
        is_matching = stored_id == self.serial_key.decode()

        if not is_matching:
            logger.warning("Hardware ID verification failed!")

        return is_matching

    def get_stored_id(self) -> str:
        """
        Mendapatkan hardware ID yang tersimpan di konfigurasi.

        Returns:
            str: Hardware ID yang tersimpan atau string kosong jika belum ada
        """
        return self.config_manager.get("Hardwareid", "hardware_id", "") or ""

    def _store_hardware_id(self) -> bool:
        """
        Menyimpan hardware ID saat ini ke konfigurasi.

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

    @classmethod
    def check_hardware(cls, config_manager: SettingManager) -> bool:
        """
        Metode kelas untuk memeriksa hardware ID tanpa membuat instance.

        Args:
            config_manager: Manager konfigurasi yang telah diinisialisasi

        Returns:
            bool: True jika hardware ID valid atau belum diset, False jika tidak sesuai
        """
        # Buat instance sementara dan validasi
        hw_state = cls(config_manager)
        return hw_state.is_valid
