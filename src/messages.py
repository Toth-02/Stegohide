import sys
from colors import Colors
from time import sleep


class SystemMessages:
    @staticmethod
    def banner(term_width: int) -> None:
        """
        Simply print the logo centered for the current terminal.

        :return:
            Entire logo with right format.
        """

        # Center the logo.
        banner_rows = '\n'.join([' ' * round((term_width - len(row)) / 2) + row for row in [
            "███████╗████████╗███████╗ ██████╗  ██████╗ ██╗  ██╗██╗██████╗ ███████╗",
            "██╔════╝╚══██╔══╝██╔════╝██╔════╝ ██╔═══██╗██║  ██║██║██╔══██╗██╔════╝",
            "███████╗   ██║   █████╗  ██║  ███╗██║   ██║███████║██║██║  ██║█████╗  ",
            "╚════██║   ██║   ██╔══╝  ██║   ██║██║   ██║██╔══██║██║██║  ██║██╔══╝  ",
            "███████║   ██║   ███████╗╚██████╔╝╚██████╔╝██║  ██║██║██████╔╝███████╗",
            "╚══════╝   ╚═╝   ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝",
            "                                                         Coded by Thot"
        ]])

        print('\n\n{}{}{}\n\n\n'.format(Colors.INFO.value, banner_rows, Colors.DEFAULT.value))

    @staticmethod
    def op_menu() -> None:

        menu = '{}'.format("=" * 30) + '\n' + \
               '          OPERATIONS' + \
               '\n{}'.format("=" * 30) + '\n\n' +\
               '1) Encode text in image\n' + \
               '2) Decode text from image\n\n\n\n' + \
               '99) Exit\n\n'

        print(menu)

    @staticmethod
    def basic_warning(text: str) -> None:
        print('{}\n[WARNING] {}{}'.format(Colors.WARNING.value, text, Colors.DEFAULT.value))

    @staticmethod
    def hard_warning(text: str) -> None:
        print('{}{}\n[WARNING] {}{}'.format(Colors.WARNING.value, Colors.UNDERLINE.value, text, Colors.DEFAULT.value))

    @staticmethod
    def error(text: str) -> None:
        print('{}{}\n[ERROR] {}{}\n'.format(Colors.ERROR.value, Colors.BOLD.value, text, Colors.DEFAULT.value))
        SystemMessages.exit()

    @staticmethod
    def complete(text: str) -> None:
        print('{}{}\n\n\n[COMPLETED] {}{}\n'.format(Colors.INFO.value, Colors.BOLD.value, text, Colors.DEFAULT.value))
        SystemMessages.exit(Colors.INFO.value)

    @staticmethod
    def info(text: str) -> None:
        sys.stdout.write('{}{}{} {}'.format(Colors.INFO.value, Colors.BOLD.value, text, Colors.DEFAULT.value))

    @staticmethod
    def clear_line() -> None:
        sys.stdout.write('\r{}'.format(" " * 40))

    @staticmethod
    def exit(exit_color=Colors.ERROR.value) -> None:

        exit_code = 0 if exit_color == Colors.INFO.value else -1

        print()

        for sec in range(3, -1, -1):
            sleep(1)
            SystemMessages.clear_line()

            if not sec:
                sys.stdout.write('\r{}{}Exiting...{}'.format(exit_color,
                                                             Colors.BOLD.value,
                                                             Colors.DEFAULT.value)
                                 )
                sys.stdout.flush()
                print()
                sys.exit(exit_code)

            sys.stdout.write('\r{}{}[EXIT] in {} {}.{}'.
                             format(exit_color,
                                    Colors.BOLD.value, sec,
                                    'seconds' if sec > 1 else 'second',
                                    Colors.DEFAULT.value)
                             )
            sys.stdout.flush()


class PrettyMessage:
    def __init__(self):
        self.need_run = True

    def message(self, msg, color, time_step=0.1, iteration=500) -> None:
        """
        Make wait time a bit more good.

        :WARNING:
            Controlled by need_run.

        :param msg:
            Message to be printed.

        :param color:
            Color used in print.

        :param time_step:
            Time in seconds for each iteration.

        :param iteration:
            Number of total iteration if no block.
        """

        part = '|/-\\'

        i = 0

        while self.need_run and i < iteration:
            sleep(time_step)
            sys.stdout.write('\r{}[ {} ] {}{}'.format(color, part[i % 4], msg, Colors.DEFAULT.value))
            sys.stdout.flush()
            i += 1

        SystemMessages.clear_line()
        print('\r{}[+] {}{}'.format(color, msg.replace('ing', 'ed').replace('...', '!'), Colors.DEFAULT.value))
