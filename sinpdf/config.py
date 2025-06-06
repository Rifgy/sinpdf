import configparser
import os
from typing import Any


class ConfigReader:
    def __init__(self, filename):
        self.filename = filename
        self.config = configparser.ConfigParser()

        # create INI if not exist
        if not os.path.exists(self.filename):
            self.create_default_config()

        self.config.read(self.filename)

    def create_default_config(self) -> None:
        """
        Create INI file with defaults value's

        :rtype: None
        """
        self.config['Default'] = {
            'WSize': 900,
            'HSize': 500,
            'FontName': 'Arial',
            'FontSize': 12
        }
        self.config['ScanOpt'] = {
            'BaseName': 'results.db',
            'BasePath': '',
            'LimitToScanPages': 3,
            'GetMetaFromPdf': True
        }
        self.config['BaseFiles'] = {
            'Db1': '',
        }

        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)

    def get(self, section, option) -> str | None:
        """
        Get value from section

        :param section:
        :param option:
        :return:
        """
        try:
            return self.config.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            if __name__ == "__main__":
                print(f"Error get: {e}")
            return None

    def get_int(self, section: object, option: object) -> int | None:
        """
        Get INT value from INI

        :param section:
        :param option:
        :return:
        """
        value = self.get(section, option)
        return int(value) if value is not None else None

    def get_flost(self, section: object, option: object) -> float | None:
        """
        Get FLOAT value from INI

        :param section:
        :param option:
        :return:
        """
        value = self.get(section, option)
        return float(value) if value is not None else None

    def get_bool(self, section: object, option: object) -> bool:
        """
        Get BOOL value from INI

        :param section:
        :param option:
        :return:
        """
        value = self.get(section, option)
        return True if value.lower() in ['true', '1', 'yes']  else False

    def get_dict(self, section: str) -> dict[Any, Any]:
        """
        Get DICT value in INI

        :param section:  Section name
        :return: Section option(s)
        :rtype: dict[Any, Any]
        """
        settings_dict = {}
        if section in self.config:
            settings = self.config[section]
            for option in settings:
                settings_dict[option] = settings[option]
            return settings_dict
        else:
            if __name__ == "__main__":
                print(f"Section {section} not found.")
                return dict()
            else:
                return dict()

if __name__ == "__main__":
    '''
    ini_file_path = 'config.ini'
    config_reader = ConfigReader(ini_file_path)
    DB_LIST = config_reader.get_dict('BaseFiles')
    if DB_LIST:
        for key, value in DB_LIST.items():
            print(f"{key} = {value}")
    '''
    pass

