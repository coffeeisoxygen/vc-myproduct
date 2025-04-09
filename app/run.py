from pathlib import Path

from app.states import AppState  # Perubahan import
from app.utils.logger import get_logger
from app.utils import generate_pc_serial
from app.config.settings import SettingManager
from app.config.constant import DEFAULT_CONFIG_NAME

logger = get_logger("app")


def verify_hardware_id(config_manager: SettingManager) -> bool:
    """
    Verifikasi hardware ID pada settings dengan PC saat ini.

    Args:
        config_manager: Manager konfigurasi yang telah diinisialisasi

    Returns:
        bool: True jika hardware ID valid atau belum diset, False jika tidak sesuai
    """
    current_serial = generate_pc_serial()
    stored_hardware_id = config_manager.get("Hardwareid", "hardware_id")

    # Jika belum ada hardware_id, kita anggap valid (akan diset nanti)
    if not stored_hardware_id:
        return True

    # Verifikasi apakah hardware_id sesuai dengan PC saat ini
    return stored_hardware_id == current_serial.decode()


def initialize_app(config_path=None):
    """
    Initialize the application by checking for config files
    and creating them if they don't exist.

    Args:
        config_path: Optional path to config file. If None, uses default.

    Returns:
        AppState: Initialized application state or None if verification fails
    """
    if config_path is None:
        config_path = DEFAULT_CONFIG_NAME

    logger.info(f"Initializing application with config: {config_path}")

    # Cek apakah file konfigurasi ada
    config_exists = Path(config_path).exists()
    if not config_exists:
        logger.info(f"Config file not found, will create with defaults: {config_path}")

    # Inisialisasi setting manager dahulu
    config_manager = SettingManager(Path(config_path))

    # Verifikasi hardware ID
    if not verify_hardware_id(config_manager):
        logger.error("Hardware ID verification failed! Unauthorized device.")
        return None  # Atau raise exception

    # Hardware ID valid, create AppState (yang juga akan update hardware_id jika kosong)
    app_state = AppState(config_path)

    # Periksa connection string Otomax
    if not app_state.oto_constring:
        logger.warning(
            "No Otomax connection string configured! Please set up the connection."
        )
        # Here you would typically trigger a UI to get the connection string
    else:
        logger.info("Otomax connection string loaded successfully")

    return app_state


def run_application():
    """Main entry point to run the application"""
    app_state = initialize_app()

    if app_state is None:
        logger.error("Application failed to initialize due to hardware ID verification.")
        return

    # Start your application logic here
    logger.info("Application started")

    # Return AppState for testing purposes
    return app_state
