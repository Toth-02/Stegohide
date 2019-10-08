import os
from platform import platform


class Terminal:
    @staticmethod
    def get_clear_command() -> str:
        """
        Used to get the right clear command based on the running operative system.
        """
        running_os = platform()

        if 'Windows' in running_os:
            return 'cls'
        # Every other OS
        return 'clear'

    @staticmethod
    def get_terminal_size(fallback=(80, 24)) -> tuple:
        """
        Get the terminal size, reading from:
                0 - Standard Input
                1 - Standard Output
                2 - Standard Error

        :param fallback:
            Default value if all failed.

        :return:
            Tuple containing width and height of terminal.
        """

        for i in range(0, 3):
            try:
                columns, rows = os.get_terminal_size(i)
            except OSError:
                continue
            break
        else:  # All failed
            columns, rows = fallback
        return columns, rows
