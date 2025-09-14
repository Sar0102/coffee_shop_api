import logging
import os


class LoggerConfig:
    LOG_LEVEL = int(os.getenv("LOGGING_LEVEL", logging.INFO))

    @classmethod
    def setup_logger(cls) -> None:
        logger_ = logging.getLogger()
        logger_.setLevel(cls.LOG_LEVEL)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(cls.LOG_LEVEL)

        for handler in logger_.handlers[:]:
            logger_.removeHandler(handler)

        formatter = None

        if not any(isinstance(h, logging.StreamHandler) for h in logger_.handlers):
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        if formatter:
            console_handler.setFormatter(formatter)
            logger_.addHandler(console_handler)

        logger_.info("Logger configured")
