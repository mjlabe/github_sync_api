import logging
import os
import sys
from configparser import ConfigParser
from distutils.util import strtobool


parser = ConfigParser()
parser.read("settings.ini")

settings = {section: dict(parser.items(section)) for section in parser.sections()}

try:
    log_level = logging.getLevelName(
        os.environ.get("LOG_LEVEL") or settings.get("environment", {}).get("log_level", "ERROR"))
except ValueError as error:
    raise (
        ValueError(
            f"Setting 'log_level' improperly configured; must be INFO, DEBUG, WARNING, or ERROR: {error}"
        )
    ) from error

try:
    log_to_file = strtobool(os.environ.get("LOG_TO_FILE") or settings.get("environment", {}).get("log_to_file", "False"))
    print("LOG TO FILE", log_to_file, log_level)
    if log_to_file:
        logging.basicConfig(
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler("log.txt"),
            ],
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:
        logging.basicConfig(
            handlers=[
                logging.StreamHandler(sys.stdout),
            ],
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
except ValueError as error:
    raise (
        ValueError(
            f"Setting 'log_to_file' improperly configured; must be boolean: {error}"
        )
    ) from error

if not settings.get("repos"):
    raise (NotImplementedError("No repos are defined in settings"))

if token := os.environ.get("TOKEN") or settings.get("secrets", {}).get(
    "token"
):
    settings["secrets"]["token"] = token
else:
    raise (NotImplementedError("GitHub token is not defined in settings"))
