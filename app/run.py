from app.utils.logger import get_logger
from app.states import AppState
from app.controllers.gui_controller import gui_controller  # Import controller

logger = get_logger("app")

def run_application():
    """Main entry point to run the application"""
    # Controller sudah diinisialisasi sebagai singleton

    app_state = AppState.initialize_app()

    if app_state is None:
        logger.error("Application failed to initialize due to hardware ID verification.")
        return

    # Start your application logic here
    logger.info("Application started")

    # Return AppState for testing purposes
    return app_state
