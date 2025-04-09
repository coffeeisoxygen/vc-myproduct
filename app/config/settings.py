import configparser
from pathlib import Path

from app.config.constant import DEFAULT_CONFIG_PATH

DEFAULT_INI_STRUCTURE = {
    "APP": {
        "ip": "127.0.0.1",
        "port": "8000",
    },
    "DATABASE": {
        "oto_db_url": "",
    },
    "Hardwareid": {
        "hardware_id": "",
    },
}

class SettingManager:
    def __init__(self, config_path: Path = DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.load_or_create_config()

    def load_or_create_config(self):
        if not self.config_path.exists():
            self.create_default_config()
        self.config.read(self.config_path)

    def create_default_config(self):
        for section, values in DEFAULT_INI_STRUCTURE.items():
            self.config[section] = values
        self.save()

    def save(self):
        with open(self.config_path, "w") as f:
            self.config.write(f)

    def get(self, section: str, key: str, fallback=None):
        return self.config.get(section, key, fallback=fallback)

    def set(self, section: str, key: str, value: str):
        if section not in self.config:
            self.config.add_section(section)
        self.config[section][key] = value
        self.save()

    def reload(self):
        self.config.read(self.config_path)

    def dump(self):
        for section in self.config.sections():
            print(f"[{section}]")
            for key, val in self.config[section].items():
                print(f"{key} = {val}")
