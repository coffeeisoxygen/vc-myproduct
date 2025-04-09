from app.utils.logger import get_logger

# Dapatkan objek logger
logger = get_logger("main")


def main():
    print("Hello from vc-myproduct!")
    # Gunakan logger untuk mencatat pesan
    logger.info("Hello from vc-myproduct!")
    logger.debug("Ini pesan debug")
    logger.warning("Ini pesan peringatan")
    logger.error("Ini pesan error")
    logger.critical("Ini pesan kritis")


if __name__ == "__main__":
    main()
