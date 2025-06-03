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

    def get(self, section, option):
        """Получить значение из конфигурации."""
        try:
            return self.config.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            print(f"Ошибка: {e}")
            return None

    def get_int(self, section, option):
        """Получить целочисленное значение из конфигурации."""
        value = self.get(section, option)
        return int(value) if value is not None else None

    def get_flost(self, section, option):
        """Получить действительное значение из конфигурации."""
        value = self.get(section, option)
        return float(value) if value is not None else None

    def get_bool(self, section, option):
        """Получить логическое значение из конфигурации."""
        value = self.get(section, option)
        return True if value.lower() in ['true', '1', 'yes']  else False

        # Пример использования

config_reader = ConfigReader('config.ini')

APP_FONT = config_reader.get('Default', 'FontName')
APP_FONTSIZE = config_reader.get_int('Default', 'FontSize')
BASE_NAME = config_reader.get('ScanOpt', 'BaseName')
BASE_PATH = config_reader.get('ScanOpt', 'BasePath')
LIMIT_TO_SCAN_PAGE = config_reader.get_int('ScanOpt', 'LimitToScanPages')
GET_META_FROM_PDF = config_reader.get_bool('ScanOpt', 'GetMetaFromPdf')

'''
if __name__ == "__main__":
    print(f'APP_FONT: {APP_FONT}, type:{type(APP_FONT)}')
    print(f'APP_FONTSIZE: {APP_FONTSIZE}, type:{type(APP_FONTSIZE)}')
    print(f'BASE_NAME: {BASE_NAME}, type:{type(BASE_NAME)}')
    print(f'BASE_PATH: {BASE_PATH}, type:{type(BASE_PATH)}')
    print(f'LIMIT_TO_SCAN_PAGE: {LIMIT_TO_SCAN_PAGE}, type:{type(LIMIT_TO_SCAN_PAGE)}')
    print(f'GET_META_FROM_PDF: {GET_META_FROM_PDF}, type:{type(GET_META_FROM_PDF)}')

'''

