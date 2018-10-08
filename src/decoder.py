import logging
from enum import Enum, auto


class Signal(Enum):
    """A single signal that has been processed by the machine learning algorithm"""
    SHORT = auto()
    LONG = auto()
    PAUSE_SHORT = auto()
    PAUSE_MEDIUM = auto()
    PAUSE_LONG = auto()


class State(Enum):
    """A state in a finite state machine that determines the transmitted code"""
    INITIAL = '-INITIAL-'
    ERROR = '-ERROR-'
    LETTER_A = 'A'
    """.-"""
    LETTER_B = 'B'
    """-..."""
    LETTER_C = 'C'
    """-.-."""
    LETTER_D = 'D'
    """-.."""
    LETTER_E = 'E'
    """."""
    LETTER_F = 'F'
    """..-."""
    LETTER_G = 'G'
    """--."""
    LETTER_H = 'H'
    """...."""
    LETTER_I = 'I'
    """.."""
    LETTER_J = 'J'
    """.---"""
    LETTER_K = 'K'
    """-.-"""
    LETTER_L = 'L'
    """.-.."""
    LETTER_M = 'M'
    """--"""
    LETTER_N = 'N'
    """-."""
    LETTER_O = 'O'
    """---"""
    LETTER_P = 'P'
    """.--."""
    LETTER_Q = 'Q'
    """--.-"""
    LETTER_R = 'R'
    """.-."""
    LETTER_S = 'S'
    """..."""
    LETTER_T = 'T'
    """-"""
    LETTER_U = 'U'
    """..-"""
    LETTER_V = 'V'
    """...-"""
    LETTER_W = 'W'
    """.--"""
    LETTER_X = 'X'
    """-..-"""
    LETTER_Y = 'Y'
    """-.--"""
    LETTER_Z = 'Z'
    """--.."""
    NUMBER_0 = '0'
    """-----"""
    NUMBER_1 = '1'
    """.----"""
    NUMBER_2 = '2'
    """..---"""
    NUMBER_3 = '3'
    """...--"""
    NUMBER_4 = '4'
    """....-"""
    NUMBER_5 = '5'
    """....."""
    NUMBER_6 = '6'
    """-...."""
    NUMBER_7 = '7'
    """--..."""
    NUMBER_8 = '8'
    """---.."""
    NUMBER_9 = '9'
    """----."""
    SPECIAL_CH = 'CH'
    """----"""
    SPECIAL_AE = 'Ä'
    """.-.-"""
    SPECIAL_OE = 'Ö'
    """---."""
    SPECIAL_UE = 'Ü'
    """..--"""
    SPECIAL_AMPERSAND = '&'
    """.-..."""
    SPECIAL_SPACE = auto()
    SPECIAL_DOT = auto()
    """.-.-.-"""


class Decoder:
    """
    A decoder for morse signals.
    """

    # All states:
    # DIT, DAH, "INITIAL", PAUSE_SHORT, PAUSE_MEDIUM, PAUSE_LONG

    __current_state = State.INITIAL
    __last_signal = Signal.PAUSE_LONG

    message = ''

    def __init__(self, _logger: logging.Logger):
        self.logger = _logger

    def decode(self, signal: Signal):
        """ Decode a morse stream step by step."""

        if (signal == Signal.SHORT or signal == Signal.LONG) and (
                self.__last_signal == Signal.SHORT or self.__last_signal == Signal.LONG):
            self.logger.info("ERROR! There has to be a pause in between two signals!")
            self.message += "(E!)"

        elif signal == Signal.SHORT:
            self.logger.info("DIT")
            self.__last_signal = Signal.SHORT
            self.__process_dit()
        elif signal == Signal.LONG:
            self.logger.info("DAH")
            self.__last_signal = Signal.LONG
            self.__process_dah()
        elif signal == Signal.PAUSE_SHORT:
            self.logger.info("PAUSE_SHORT")
            self.__last_signal = Signal.PAUSE_SHORT
            self.__process_short_pause()
        elif signal == Signal.PAUSE_MEDIUM:
            self.logger.info("PAUSE_MEDIUM")
            self.__last_signal = Signal.PAUSE_MEDIUM
            self.__process_medium_pause()
        elif signal == Signal.PAUSE_LONG:
            self.logger.info("PAUSE_LONG")
            self.__last_signal = Signal.PAUSE_LONG
            self.__process_long_pause()
        else:
            self.logger.info("ERROR!")

    def __process_dit(self):
        """ Process a short 'DIT' signal."""
        if self.__current_state == State.INITIAL:
            self.__current_state = State.LETTER_E
            self.logger.info("INITIAL -> E")
        elif self.__current_state == State.LETTER_E:
            self.__current_state = State.LETTER_I
            self.logger.info("E -> I")
        elif self.__current_state == State.LETTER_I:
            self.__current_state = State.LETTER_S
            self.logger.info("I -> S")
        elif self.__current_state == State.LETTER_S:
            self.__current_state = State.LETTER_H
            self.logger.info("S -> H")
        elif self.__current_state == State.LETTER_H:
            self.__current_state = State.NUMBER_5
            self.logger.info("H -> 5")

        elif self.__current_state == State.LETTER_T:
            self.__current_state = State.LETTER_N
            self.logger.info("T -> N")
        elif self.__current_state == State.LETTER_N:
            self.__current_state = State.LETTER_D
            self.logger.info("N -> D")
        elif self.__current_state == State.LETTER_D:
            self.__current_state = State.LETTER_B
            self.logger.info("D -> B")
        elif self.__current_state == State.LETTER_B:
            self.__current_state = State.NUMBER_6
            self.logger.info("B -> 6")

        elif self.__current_state == State.LETTER_M:
            self.__current_state = State.LETTER_G
            self.logger.info("M -> G")
        elif self.__current_state == State.LETTER_G:
            self.__current_state = State.LETTER_Z
            self.logger.info("G -> Z")
        elif self.__current_state == State.LETTER_Z:
            self.__current_state = State.NUMBER_7
            self.logger.info("Z -> 7")

        elif self.__current_state == State.LETTER_O:
            self.__current_state = State.SPECIAL_OE
            self.logger.info("O -> Ö")
        elif self.__current_state == State.SPECIAL_OE:
            self.__current_state = State.NUMBER_8
            self.logger.info("Ö -> 8")

        elif self.__current_state == State.SPECIAL_CH:
            self.__current_state = State.NUMBER_9
            self.logger.info("CH -> 9")

        elif self.__current_state == State.LETTER_A:
            self.__current_state = State.LETTER_R
            self.logger.info("A -> R")
        elif self.__current_state == State.LETTER_R:
            self.__current_state = State.LETTER_L
            self.logger.info("R -> L")
        elif self.__current_state == State.LETTER_L:
            self.__current_state = State.SPECIAL_AMPERSAND
            self.logger.info("L -> &")

        elif self.__current_state == State.LETTER_W:
            self.__current_state = State.LETTER_P
            self.logger.info("W -> P")

        elif self.__current_state == State.LETTER_U:
            self.__current_state = State.LETTER_F
            self.logger.info("U -> F")

        elif self.__current_state == State.LETTER_K:
            self.__current_state = State.LETTER_C
            self.logger.info("K -> C")

        else:
            self.__current_state = State.ERROR
            self.logger.info("ERROR")

    def __process_dah(self):
        """ Process a long 'DAH' signal."""
        if self.__current_state == State.INITIAL:
            self.__current_state = State.LETTER_T
            self.logger.info("INITIAL -> T")
        elif self.__current_state == State.LETTER_T:
            self.__current_state = State.LETTER_M
            self.logger.info("T -> M")
        elif self.__current_state == State.LETTER_M:
            self.__current_state = State.LETTER_O
            self.logger.info("M -> O")
        elif self.__current_state == State.LETTER_O:
            self.__current_state = State.SPECIAL_CH
            self.logger.info("O -> CH")
        elif self.__current_state == State.SPECIAL_CH:
            self.__current_state = State.NUMBER_0
            self.logger.info("CH -> 0")

        elif self.__current_state == State.LETTER_E:
            self.__current_state = State.LETTER_A
            self.logger.info("E -> A")
        elif self.__current_state == State.LETTER_A:
            self.__current_state = State.LETTER_W
            self.logger.info("A -> W")
        elif self.__current_state == State.LETTER_W:
            self.__current_state = State.LETTER_J
            self.logger.info("W -> J")
        elif self.__current_state == State.LETTER_J:
            self.__current_state = State.NUMBER_1
            self.logger.info("J -> 1")

        elif self.__current_state == State.LETTER_I:
            self.__current_state = State.LETTER_U
            self.logger.info("I -> U")
        elif self.__current_state == State.LETTER_U:
            self.__current_state = State.SPECIAL_UE
            self.logger.info("U -> Ü")
        elif self.__current_state == State.SPECIAL_UE:
            self.__current_state = State.NUMBER_2
            self.logger.info("Ü -> 2")

        elif self.__current_state == State.LETTER_S:
            self.__current_state = State.LETTER_V
            self.logger.info("S -> V")
        elif self.__current_state == State.LETTER_V:
            self.__current_state = State.NUMBER_3
            self.logger.info("V -> 3")

        elif self.__current_state == State.LETTER_H:
            self.__current_state = State.NUMBER_4
            self.logger.info("H -> 4")

        elif self.__current_state == State.LETTER_N:
            self.__current_state = State.LETTER_K
            self.logger.info("N -> K")
        elif self.__current_state == State.LETTER_K:
            self.__current_state = State.LETTER_Y
            self.logger.info("K -> Y")

        elif self.__current_state == State.LETTER_D:
            self.__current_state = State.LETTER_X
            self.logger.info("D -> X")

        elif self.__current_state == State.LETTER_G:
            self.__current_state = State.LETTER_Q
            self.logger.info("G -> Q")

        elif self.__current_state == State.LETTER_R:
            self.__current_state = State.SPECIAL_AE
            self.logger.info("R -> AE")

        else:
            self.__current_state = State.ERROR
            self.logger.info("ERROR")

    def __process_short_pause(self):
        """ Process a short pause."""
        self.logger.info("New signal")

    def __process_medium_pause(self):
        """ Process a medium pause."""
        self.message += self.__current_state.value
        self.__current_state = State.INITIAL
        self.logger.info("New character")

    def __process_long_pause(self):
        """ Process a long pause."""
        self.message += self.__current_state.value
        self.message += " "
        self.__current_state = State.INITIAL
        self.logger.info("New word")


if __name__ == "__main__":
    # create logger
    logger = logging.getLogger('decoder')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warning('warn message')
    # logger.error('error message')
    # logger.critical('critical message')

    decoder = Decoder(logger)
    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_LONG)

    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_MEDIUM)

    print("\n----------------------------------\n")
    print(decoder.message)

    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_MEDIUM)
    decoder.message = ""

    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_MEDIUM)

    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.SHORT)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_SHORT)
    decoder.decode(Signal.LONG)
    decoder.decode(Signal.PAUSE_LONG)

    print("\n----------------------------------\n")
    print(decoder.message)
