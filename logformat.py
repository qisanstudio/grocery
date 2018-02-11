import sys
import logging

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"


COLORS = {
    'DEBUG': BLUE,
    'INFO': GREEN,
    'WARNING': YELLOW,
    'ERROR': RED,
    'CRITICAL': MAGENTA,
}


class ColorFormater(logging.Formatter):

    def get_color_levelname(self, levelname):
        LEVEL_COLOR_SEQ = COLOR_SEQ % (30 + COLORS[levelname])
        color_levelname = LEVEL_COLOR_SEQ + levelname + RESET_SEQ
        return color_levelname

    def format(self, record):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        record.levelname = self.get_color_levelname(record.levelname)

        s = self._fmt % record.__dict__
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            try:
                s = s + record.exc_text
            except UnicodeError:
                s = s + record.exc_text.decode(sys.getfilesystemencoding(),
                                               'replace')
        return s


def get_color_file_logger(name,
                          file_name='access.log',
                          level=logging.DEBUG,
                          fmt='%(levelname)-8s %(message)s'):
    # define logger
    logger = logging.getLogger(name)
    # set logger level
    logger.setLevel(logging.DEBUG)
    # add file handler to logger
    fh = logging.FileHandler(file_name)
    # set format
    formatter = ColorFormater(fmt)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger


if __name__ == '__main__':
    # define logger
    logger = logging.getLogger(__name__)
    # set logger level
    logger.setLevel(logging.DEBUG)
    # add file handler to logger
    fh = logging.FileHandler('access.log')
    fh.setLevel(logging.DEBUG)
    # set format
    formatter = ColorFormater('%(levelname)-8s %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
