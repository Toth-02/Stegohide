from PIL import Image
from errors import TooLongTextError, TooShortTextError, ExtensionError, EncodeError
import sys
import os


class Steganography:

    READ_DATA        = 0b00000001
    WRITE_DATA       = 0b11111110

    END_STEP_DATA    = 0b01000000
    END_CHECK_ENCODE = 0b11000000

    CHAR_DIMENSION   = 0b00001000

    ENCODE_SIGNATURE = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

    IMAGE_EXT = ('.jpg', '.jpeg', '.png')

    def __init__(self, fp: str) -> None:

        if not fp.strip().endswith(Steganography.IMAGE_EXT):
            raise ExtensionError

        self.__image = Image.open(fp).convert('RGBA')

        self.__pixels = list(self.__image.getdata())
        self.__width, self.__height = self.__image.size
        self.__size = self.__width * self.__height

        self.__max_char = round((self.__size / Steganography.CHAR_DIMENSION)) - \
                          round(Steganography.END_STEP_DATA / Steganography.CHAR_DIMENSION) - \
                          round(Steganography.END_CHECK_ENCODE / Steganography.CHAR_DIMENSION) - 1

        self.__step = None

        self.__outfile = Steganography.__output_file_name(os.path.split(fp)[-1])

    def encode(self, text: str) -> None:

        bin_text = Steganography.__get_bin(text)

        self.__step = self.__best_step(len(bin_text))

        bin_text = (Steganography.END_STEP_DATA - len(bin(self.__step)[2:])) * '0' + bin(self.__step)[2:] + \
                   bin(Steganography.ENCODE_SIGNATURE)[2:] + bin_text

        self.__write_meta_data(bin_text, 0, Steganography.END_STEP_DATA)

        self.__write_meta_data(bin_text, Steganography.END_STEP_DATA, Steganography.END_CHECK_ENCODE)

        for i, j in zip(range(Steganography.END_CHECK_ENCODE, self.__size, self.__step), 
                        range(Steganography.END_CHECK_ENCODE, len(bin_text))):
            self.__pixels[i] = (
                                self.__pixels[i][0],                                                     # R
                               (self.__pixels[i][1] & Steganography.WRITE_DATA) | int(bin_text[j]),      # G
                                self.__pixels[i][2],                                                     # B
                                self.__pixels[i][3]                                                      # A
            )

        output = Image.new("RGBA", (self.__width, self.__height))
        output.putdata(self.__pixels)
        output.save(self.__outfile)

    def decode(self) -> str:

        self.__step, signature = self.__read_meta_data()

        if signature != Steganography.ENCODE_SIGNATURE:
            raise EncodeError

        raw = self.__read_raw()

        recovered = ''
        init = 0
        for last in range(init + Steganography.CHAR_DIMENSION, len(raw), Steganography.CHAR_DIMENSION):
            current_char = chr(int(raw[init:last], 2))

            if current_char == '\0':
                break

            recovered += current_char
            init = last

        return recovered

    def __read_raw(self) -> str:

        return ''.join(
            [str(self.__pixels[i][1] & Steganography.READ_DATA) for i in range(Steganography.END_CHECK_ENCODE,
                                                                               self.__size,
                                                                               self.__step
                                                                               )
             ]
        )

    def __write_meta_data(self, data: str, start: int, end: int) -> None:

        for i in range(start, end):
            self.__pixels[i] = (
                                self.__pixels[i][0],                                                     # R
                               (self.__pixels[i][1] & Steganography.WRITE_DATA) | int(data[i]),          # G
                                self.__pixels[i][2],                                                     # B
                                self.__pixels[i][3]                                                      # A
            )

    def __read_meta_data(self) -> tuple:

        return (
            int(''.join([str(self.__pixels[i][1] & Steganography.READ_DATA) for
                        i in range(0, Steganography.END_STEP_DATA)]), 2),
            int(''.join([str(self.__pixels[i][1] & Steganography.READ_DATA) for
                        i in range(Steganography.END_STEP_DATA, Steganography.END_CHECK_ENCODE)]), 2)
        )

    def __best_step(self, text_len: int) -> int:

        return round(self.__size / text_len)

    def get_max_char(self):
        return self.__max_char

    def get_out_file(self):
        return self.__outfile

    @staticmethod
    def __output_file_name(name: str) -> str:

        ext = '.' + name.split('.')[-1]
        return name.replace(ext, '-output.png')

    @staticmethod
    def sanitize_text(text: str) -> str:

        return ''.join(filter(lambda char: 32 <= ord(char) < 127, text))

    @staticmethod
    def __get_bin(text: str) -> str:

        return ''.join(
            [(Steganography.CHAR_DIMENSION - len(bin(ord(char))[2:])) * '0' + bin(ord(char))[2:] for char in text]
        )
