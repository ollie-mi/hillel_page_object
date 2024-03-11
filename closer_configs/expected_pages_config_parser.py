from globals import dir_globals
from config_parsers.config_expected_pages_parser import ExpectedPagesConfigParser


class CloserExpectedPagesConfigParser(ExpectedPagesConfigParser):
    """ Parses config with expected pages
    Config example:
        domain: {
            'current_page': 'next_page'
        }
    """

    def __init__(self):
        super().__init__(dir_globals.CLOSER_EXPECTED_PAGES_CONFIG)
