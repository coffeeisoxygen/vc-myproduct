from app.utils.logger import get_logger
from app.events.event_manager import event_manager
from app.gui import (
    safe_show_hardware_form,
    safe_show_database_form,
    safe_show_serial_port_form,
)

logger = get_logger("controller.gui")

class GUIController:
    def __init__(self):
        self.register_event_handlers()

    def register_event_handlers(self):
        """Register event handlers untuk berbagai event dari state manager"""
        event_manager.subscribe("hardware_invalid", self.handle_hardware_invalid)
        event_manager.subscribe("database_config_needed", self.handle_database_config_needed)
        event_manager.subscribe("serial_config_needed", self.handle_serial_config_needed)

    def handle_hardware_invalid(self):
        """Handler untuk event hardware invalid"""
        logger.info("Handling hardware_invalid event - showing hardware form")
        safe_show_hardware_form()

    def handle_database_config_needed(self):
        """Handler untuk event database configuration needed"""
        logger.info("Handling database_config_needed event - showing database form")
        safe_show_database_form()

    def handle_serial_config_needed(self):
        """Handler untuk event serial configuration needed"""
        logger.info("Handling serial_config_needed event - showing serial port form")
        safe_show_serial_port_form()

# Create singleton instance
gui_controller = GUIController()
