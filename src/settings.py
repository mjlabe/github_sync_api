import os
from configparser import ConfigParser


parser = ConfigParser()
parser.read("settings.ini")

settings = {section: dict(parser.items(section)) for section in parser.sections()}

if not settings.get("repos"):
    raise (NotImplementedError("No repos are defined in settings"))

token = os.environ.get("TOKEN") or settings.get("secrets", {}).get("token")

if not token:
    raise (NotImplementedError("GitHub token is not defined in settings"))

settings["secrets"]["token"] = token
