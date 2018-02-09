import sys
import logging

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"


COLORS = {
    'DEBUG': BLUE,
    'INFO': GREEN,
    'WARNING': YELLOW,
    'CRITICAL': MAGENTA,
    'ERROR': RED
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
