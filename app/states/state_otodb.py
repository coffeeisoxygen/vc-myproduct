# Module mengolal state database ke otomax

from app.utils.logger import get_logger
from app.config.settings import SettingManager
from app.events.event_manager import event_manager

logger = get_logger("state.otodb")

class OtoDBState:
    """
    Kelas untuk mengelola state koneksi database Otomax
    """

    def __init__(self, config_manager: SettingManager):
        """
        Inisialisasi OtoDBState

        Args:
            config_manager: Manager konfigurasi yang telah diinisialisasi
        """
        self.config_manager = config_manager
        self._connection_string = self.config_manager.get("DATABASE", "oto_db_url", "")
        self._is_connected = False

    @property
    def connection_string(self) -> str:
        """Mendapatkan connection string"""
        return self._connection_string or ""

    @property
    def is_connected(self) -> bool:
        """Cek apakah database terhubung"""
        return self._is_connected

    def validate(self) -> bool:
        """Validasi koneksi database"""
        if not self._connection_string:
            logger.warning("Connection string is empty")
            event_manager.emit("database_config_needed")
            return False

        # Di implementasi sebenarnya, tambahkan kode untuk test koneksi
        # dengan pyodbc atau library database lainnya

        return True

    def reload_config(self):
        """Reload konfigurasi dari file"""
        self.config_manager.reload()
        self._connection_string = self.config_manager.get("DATABASE", "oto_db_url", "")
