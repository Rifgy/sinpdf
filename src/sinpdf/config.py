import configparser
import os

FntName = 'SansSerif'
FntSize = 12
BdName = 'results.db'
PgToLoad = 5

def write_config_file(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    with open(config_file, 'w') as configfile:
        config.write(configfile)

def config_read():
    config_file = 'config.ini'
    config = configparser.ConfigParser()

    # create and save file if not exist
    if not os.path.exists(config_file):
        # Add section and parameters
        config['DEFAULT'] = {
            'FontName': 'SansSerif',
            'FontSize': '12'
        }
        config['Database'] = {
            'BaseName': 'results.db',
            'PageToDbLoad': '3'
        }
        # write file
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    else:
        config.read(config_file)
        # Чтение значений из секций
        FntName = config['DEFAULT']['FontName']
        FntSize = config['DEFAULT'].getint('FontSize')
        BdName = config['Database']['BaseName']
        PgToLoad = config['Database'].getint('PageToDbLoad')

    # Запись новых значений
    write_config_file(config_file)

if __name__ == '__main__':
    pass