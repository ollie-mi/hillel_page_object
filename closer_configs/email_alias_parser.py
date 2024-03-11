from globals import dir_globals
from config_parsers.config_email_alias_parser import ConfigEmailAliasParser


class CloserEmailAlias(ConfigEmailAliasParser):
    """ Parses config with email alias"""

    def __init__(self):
        super().__init__(dir_globals.CLOSER_EMAIL_ALIAS_CONFIG)
