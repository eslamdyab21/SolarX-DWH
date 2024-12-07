import logging
import logging.config


def setup_logging(default_level=logging.INFO, log_file="dwh.log"):
    """Set up logging configuration."""
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": "INFO",
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "standard",
                "level": "DEBUG",
                "filename": log_file,
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": default_level,
        }
    }

    logging.config.dictConfig(log_config)
