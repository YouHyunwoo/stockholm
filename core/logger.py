import os
import datetime

from colorama import Fore, Back, Style



class Logger:

    LOG = 0
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4
    FATAL = 5

    WORD = ['LOG', 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL']

    def __init__(self, level=0, verbose=False, silent=False, file=None, file_level=0):
        self.level = level
        self.verbose = verbose
        self.silent = silent

        self.file = None
        self.file_level = None
        self.file_io = None

        self.open(file, file_level)

    def __log(self, level, message, description=''):
        level = 0 if level >= len(Logger.WORD) else max(0, level)

        if level == Logger.DEBUG:
            color = Fore.BLUE
        elif level == Logger.INFO:
            color = Fore.GREEN
        elif level == Logger.WARN:
            color = Fore.YELLOW
        elif level == Logger.ERROR:
            color = Fore.RED
        elif level == Logger.FATAL:
            color = Back.RED + Fore.BLACK
        else:
            color = ''

        level_word = Logger.WORD[level]
        message = message

        log = '[{}] {}'.format(level_word, message)

        if self.verbose and len(description) > 0:
            log += '\n{}'.format(description)

        if level >= self.file_level and self.file_io is not None:
            self.file_io.write(log + '\n')
            self.file_io.flush()

        if level >= self.level:
            colored_level_word = color + level_word + Style.RESET_ALL
            colored_message = color + message + Style.RESET_ALL

            colored_log = '[{}] {}'.format(colored_level_word, colored_message)

            if self.verbose and len(description) > 0:
                colored_log += '\n  {}'.format(description)

            if not self.silent:
                print(colored_log)

    def log(self, message, desciption=''):
        self.__log(Logger.LOG, message, desciption)

    def debug(self, message, description=''):
        self.__log(Logger.DEBUG, message, description)

    def info(self, message, description=''):
        self.__log(Logger.INFO, message, description)

    def warn(self, message, description=''):
        self.__log(Logger.WARN, message, description)

    def error(self, message, description=''):
        self.__log(Logger.ERROR, message, description)

    def fatal(self, message, description=''):
        self.__log(Logger.FATAL, message, description)

    def open(self, file, file_level):
        if self.file_io is not None:
            self.close()

        self.file = file
        self.file_level = file_level

        os.makedirs(os.path.dirname(file), exist_ok=True)
        self.file_io = None if file is None else open(file, 'a')

        if self.file_io is not None:
            now = datetime.datetime.now()
            self.file_io.write('\n\n\nstart logging: {}\n'.format(now))

    def close(self):
        self.file_io.close()
