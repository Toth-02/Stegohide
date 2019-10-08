import os
import threading
from colors import Colors
from terminal import Terminal
from messages import SystemMessages, PrettyMessage
from steganography import Steganography
from enum import Enum
from errors import TooLongTextError, TooShortTextError, ExtensionError, EncodeError


class Operation(Enum):
    ENCODE = 1
    DECODE = 2

    EXIT  = 99


if __name__ == '__main__':

    try:
        clear_com = Terminal.get_clear_command()
        term_width, _ = Terminal.get_terminal_size()

        os.system(clear_com)
        SystemMessages.banner(term_width)

        print('\n\n\n\n')

        SystemMessages.hard_warning('Current working directory: {}\n'.format(os.getcwd()))

        try:
            image_path = input('[INSERT] Path of the image where you want to load: ')
            stego = Steganography(image_path)

        except (FileNotFoundError, AttributeError):
            SystemMessages.error('File not found!')

        except ExtensionError:
            SystemMessages.error('Extension not recognized for an image file!')

        os.system(clear_com)
        SystemMessages.banner(term_width)
        SystemMessages.op_menu()

        try:
            choice = int(input('{}stegohide{} > '.format(Colors.UNDERLINE.value, Colors.DEFAULT.value)))

            while not(choice == Operation.ENCODE.value or
                      choice == Operation.DECODE.value or
                      choice == Operation.EXIT.value):
                os.system(clear_com)
                SystemMessages.banner(term_width)
                SystemMessages.op_menu()
                choice = int(input('{}stegohide{} > '.format(Colors.UNDERLINE.value, Colors.DEFAULT.value)))

        except ValueError:
            SystemMessages.error('Wrong value!')

        if choice == Operation.ENCODE.value:

            os.system(clear_com)
            SystemMessages.banner(term_width)

            SystemMessages.hard_warning('File {} will be re-wrote if present...'.format(stego.get_out_file()))
            print('{}>>> Press ^C if you want to cancel the operation.{}'.format(Colors.WARNING.value,
                                                                                 Colors.DEFAULT.value))
            SystemMessages.basic_warning('You can write a max of {} character on this photo!\n\n'.format(
                stego.get_max_char()))

            text = input("[INSERT] Text you want to insert on photo: ")

            try:
                if not text:
                    raise TooShortTextError

                text = Steganography.sanitize_text(text) + '\0'

                if len(text) > (stego.get_max_char() + 1):
                    raise TooLongTextError

            except TooLongTextError:
                SystemMessages.error('Too long text for this file!')

            except TooShortTextError:
                SystemMessages.error('At least a character is required!')

            print('\n')

            meta_data = PrettyMessage()
            meta_data_printer = threading.Thread(target=meta_data.message,
                                                 args=("Encoding META-DATA...", Colors.INFO.value, 0.1, 15))
            meta_data_printer.start()
            meta_data_printer.join()
            del meta_data, meta_data_printer

            text_data = PrettyMessage()
            text_data_printer = threading.Thread(target=text_data.message,
                                                 args=("Encoding text in image...", Colors.INFO.value))
            text_data_printer.start()

            stego.encode(text)

            text_data.need_run = False
            text_data_printer.join()
            del text_data, text_data_printer

            SystemMessages.complete('{} {} writed with success!'.format(len(text),
                                                                        'character' if len(text) == 1 else 'characters')
                                    )

        elif choice == Operation.DECODE.value:

            try:
                text = stego.decode()

            except EncodeError:
                SystemMessages.error("You can't decode an image not encoded!")

            os.system(clear_com)
            SystemMessages.banner(term_width)

            meta_data = PrettyMessage()
            meta_data_printer = threading.Thread(target=meta_data.message,
                                                 args=("Decoding META-DATA...", Colors.INFO.value, 0.1, 20))
            meta_data_printer.start()
            meta_data_printer.join()
            del meta_data, meta_data_printer

            text_data = PrettyMessage()
            text_data_printer = threading.Thread(target=text_data.message,
                                                 args=("Decoding text in image...", Colors.INFO.value))
            text_data_printer.start()

            text_data.need_run = False
            text_data_printer.join()
            del text_data, text_data_printer

            SystemMessages.info('\n\n[DECODED] {} {}\n\n[TEXT]'.format(len(text),
                                                                       'character' if len(text) == 1 else 'characters'))

            print(text)

            SystemMessages.exit(Colors.INFO.value)

        elif choice == Operation.EXIT.value:
            SystemMessages.exit()

    except KeyboardInterrupt:
        print('\n')
        SystemMessages.exit()
