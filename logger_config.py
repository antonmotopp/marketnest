from loguru import logger
import sys

def setup_logger():
    logger.remove()
    logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                                  "<level>{level: <8}</level> | "
                                  "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                                  "<level>{message}</level>",
               colorize=True)

    logger.add("app/logs/app.log", rotation="1 week", retention="1 month", encoding="utf-8")
    return logger
