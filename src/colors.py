from enum import Enum


class Colors(Enum):
    """
    Set standard unicode used by program.
    """
    # =================================== #
    #             TEXT COLORS
    # =================================== #
    DEFAULT   = '\033[0m'     # Default White.                                ( WHITE )
    INFO      = '\033[92m'    # Used to print the banner.                     ( GREEN )
    WARNING   = '\033[93m'    # Used when something need to be specified.     ( YELLOW )
    ERROR     = '\033[91m'    # Used when some error encountered.             ( RED )

    # =================================== #
    #           TEXT FORMATTING
    # =================================== #
    BOLD      = '\033[1m'     # Used when some error encountered.
    UNDERLINE = '\033[4m'     # Used when something need to be specified.
