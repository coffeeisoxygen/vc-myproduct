from app.run import run_application
from app.utils.logger import get_logger

# Get logger
logger = get_logger("main")


def main():
    """Main entry point for the application"""
    logger.info("Starting vc-myproduct application")

    # Run the application
    app_state = run_application()

    # Your application's main loop or logic would go here
    logger.info("Application initialized successfully")


if __name__ == "__main__":
    main()
