import configparser
import os

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
            'FontName': 'Arial',
            'FontSize': 12
        }
        self.config['ScanOpt'] = {
            'BaseName': 'result.db',
            'BasePath': '',
            'LimitToScanPages': 3,
            'GetMetaFromPdf': True
        }

        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)
        print(f'Файл {self.filename} был создан с начальными значениями.')

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

    def get_dict(self, section: object):
        # Словарь для хранения опций
        settings_dict = {}

        # Получаем секцию 'Settings'
        if section in self.config:
            settings = self.config[section]
            # Присваиваем опции переменным в словаре
            for option in settings:
                settings_dict[option] = settings[option]
            return settings_dict
        else:
            print(f"Секция {section} не найдена.")
            return None

'''
if __name__ == "__main__":
    '''
    ini_file_path = 'config.ini'
    config_reader = ConfigReader(ini_file_path)

    DB_LIST = config_reader.get_dict('BaseFile')

    if DB_LIST:
        # Выводим все опции и их значения
        for key, value in DB_LIST.items():
            print(f"{key} = {value}")
    '''
    pass
'''
