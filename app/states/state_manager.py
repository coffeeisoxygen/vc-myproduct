from pathlib import Path

from app.utils.logger import get_logger
from app.config.settings import SettingManager
from app.config.constant import DEFAULT_CONFIG_NAME
from app.states.state_hardware import HardwareState
from app.states.state_otodb import OtoDBState
from app.events.event_manager import event_manager

logger = get_logger("state.manager")

class AppState:
    """
    Kelas utama untuk mengelola state global aplikasi seperti:
    - Hardware ID
    - Database
    - Otomax
    - Serial Port
    """

    def __init__(self, config_path: str | Path):
        """
        Inisialisasi AppState
        """
        logger.debug(f"Initializing AppState with config: {config_path}")
        self.config_manager = SettingManager(Path(config_path))
        self.hardware_state = HardwareState(self.config_manager)
        self.otodb_state = OtoDBState(self.config_manager)

        self.is_hardware_valid = self.hardware_state.is_valid
        self.is_db_connected = self.otodb_state.is_connected

        self._oto_constring = self.config_manager.get("DATABASE", "oto_db_url", "")

    @property
    def is_valid(self) -> bool:
        """Check apakah seluruh komponen state valid"""
        return self.is_hardware_valid

    @property
    def oto_constring(self) -> str:
        """Mendapatkan koneksi string Otomax"""
        return self._oto_constring or ""

    def reload_config(self):
        """Reload konfigurasi dari file"""
        self.config_manager.reload()
        self._oto_constring = self.config_manager.get("DATABASE", "oto_db_url", "")
        self.hardware_state = HardwareState(self.config_manager)
        self.is_hardware_valid = self.hardware_state.is_valid

    @staticmethod
    def validate_hardware(config_manager: SettingManager) -> bool:
        """
        Validasi hardware ID dengan event untuk GUI jika invalid
        """
        if not HardwareState.check_hardware(config_manager):
            logger.warning("Hardware ID invalid! Emitting hardware_invalid event.")
            # Emit event instead of directly calling UI
            event_manager.emit("hardware_invalid")

            config_manager.reload()

            if not HardwareState.check_hardware(config_manager):
                logger.error("Hardware ID masih invalid. Aplikasi tidak bisa dijalankan.")
                return False

        logger.info("Hardware verification passed.")
        return True

    @staticmethod
    def validate_otoconstring(config_manager: SettingManager) -> bool:
        """
        Validasi koneksi string Otomax dengan event untuk GUI jika invalid
        """
        constring = config_manager.get("DATABASE", "oto_db_url", "")

        if not constring:
            logger.warning("Otomax connection string invalid! Emitting database_config_needed event.")
            # Emit event instead of directly calling UI
            event_manager.emit("database_config_needed")

            config_manager.reload()
            constring = config_manager.get("DATABASE", "oto_db_url", "")

            if not constring:
                logger.error("Otomax connection string masih invalid. Aplikasi tidak bisa dijalankan.")
                return False

        logger.info("Otomax connection string verification passed.")
        return True

    @staticmethod
    def initialize_app(config_path=None):
        """
        Entry point inisialisasi awal AppState dan validasi konfigurasi.
        """
        config_path = config_path or DEFAULT_CONFIG_NAME
        logger.info(f"Initializing application with config: {config_path}")

        config_manager = SettingManager(Path(config_path))

        # Validasi hardware
        if not AppState.validate_hardware(config_manager):
            return None

        app_state = AppState(config_path)

        # Check database connection
        if not app_state.oto_constring:
            logger.warning("Otomax belum dikonfigurasi! Emitting database_config_needed event.")
            event_manager.emit("database_config_needed")
            app_state.reload_config()

            if not app_state.oto_constring:
                logger.error("Otomax connection string masih invalid setelah reload. Aplikasi tidak bisa dijalankan.")
                return None
