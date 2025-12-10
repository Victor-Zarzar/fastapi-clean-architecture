import logging.config
from pathlib import Path

import yaml

from app.core.config import settings


# Logger main to wrap at the highest level of the application.
def setup_logger():
    config_path = Path(__file__).resolve().parent.parent.parent / "logger.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    log_level = settings.LOG_LEVEL.upper() if settings.LOG_LEVEL else "INFO"

    # Set levels dynamically
    config["root"]["level"] = log_level

    if "app" in config.get("loggers", {}):
        config["loggers"]["app"]["level"] = log_level

    if "console" in config.get("handlers", {}):
        config["handlers"]["console"]["level"] = log_level

    logging.config.dictConfig(config)


setup_logger()
logger = logging.getLogger("app")
