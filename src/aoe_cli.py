import logging

class ColoredFormatter(logging.Formatter):
    yellow = "[33;20m"
    red = "[31;20m"
    blue = "[34;20m"
    reset = "[0m"
    format_str = "%(asctime)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: format_str,
        logging.INFO: blue + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: red + format_str + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Setup root logger with custom color formatter
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(ColoredFormatter())
logger.addHandler(ch)

from aoe_ir.cli import main

if __name__ == "__main__":
    main()
