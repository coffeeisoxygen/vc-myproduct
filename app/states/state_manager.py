from pathlib import Path

from app.utils.logger import get_logger
from app.utils import generate_pc_serial
from app.config.settings import SettingManager

logger = get_logger("state.manager")

class AppState:
    """
    Kelas untuk mengelola state aplikasi secara keseluruhan.

    Kelas ini bertugas mengelola semua state aplikasi termasuk:
    - Konfigurasi aplikasi (settings.ini)
    - Hardware ID dan verifikasinya
    - Koneksi ke database aplikasi (SQLite)
    - Koneksi ke database Otomax

    AppState berperan sebagai point of access tunggal ke seluruh state aplikasi
    dan menjamin konsistensi antara berbagai komponen aplikasi.
    """

    def __init__(self, config_path: str | Path):
        """
        Inisialisasi AppState.

        Args:
            config_path: Path ke file konfigurasi
        """
        logger.debug(f"Initializing AppState with config: {config_path}")

        # Inisialisasi manager konfigurasi
        self.config_manager = SettingManager(Path(config_path))

        # Inisialisasi state hardware (serial PC)
        self._init_hardware_state()

        # Inisialisasi koneksi database aplikasi dan Otomax
        self._init_database_connections()

    def _init_hardware_state(self):
        """Inisialisasi state hardware dan serial PC"""
        # Generate hardware ID
        self.serial_key = generate_pc_serial()

        # Set hardware_id jika belum ada di konfigurasi
        if not self.config_manager.get("Hardwareid", "hardware_id"):
            logger.info("Setting hardware ID for first time")
            self.config_manager.set("Hardwareid", "hardware_id", self.serial_key.decode())

    def _init_database_connections(self):
        """Inisialisasi koneksi database aplikasi dan Otomax"""
        # Koneksi string Otomax (dienkripsi dalam konfigurasi)
        self._oto_constring = self.config_manager.get("DATABASE", "oto_db_url", "")

        # Inisialisasi koneksi database akan dibuat di kelas terpisah
        self.db_connected = False
        self.oto_connected = False

    @property
    def oto_constring(self) -> str:
        """Mendapatkan koneksi string Otomax"""
        return self._oto_constring or ""

    def set_oto_connection(self, connection_string: str) -> bool:
        """
        Set connection string untuk database Otomax.

        Args:
            connection_string: String koneksi ke database Otomax

        Returns:
            bool: True jika berhasil disimpan
        """
        try:
            # Simpan ke konfigurasi (enkripsi bisa ditambahkan di sini)
            self.config_manager.set("DATABASE", "oto_db_url", connection_string)
            self._oto_constring = connection_string
            return True
        except Exception as e:
            logger.error(f"Failed to set Otomax connection: {e}")
            return False

    def reload_config(self):
        """Reload konfigurasi dari file"""
        self.config_manager.reload()
        self._oto_constring = self.config_manager.get("DATABASE", "oto_db_url", "")
