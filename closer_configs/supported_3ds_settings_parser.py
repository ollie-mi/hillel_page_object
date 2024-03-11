from globals import dir_globals
from config_parsers.config_3ds_settings_parser import Config3dsSettingsParser


class Closer3dsSettings(Config3dsSettingsParser):
    """ Parses config with 3ds settings for supported card"""

    def __init__(self):
        super().__init__(dir_globals.CLOSER_3DS_SETTINGS_CONFIG)
