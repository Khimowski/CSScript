import configparser
import os

class configUtil:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    @staticmethod
    def readConfigFile(filePath : str, configType : str):
        filePath = os.path.join(configUtil.parent_dir, 'config', filePath)
        print(filePath)
        cfg = configparser.ConfigParser()
        cfg.read(filePath)
        print(cfg.items(configType))
        print(dict(cfg.items(configType)))
        return dict(cfg.items(configType))
