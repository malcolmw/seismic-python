import logging

def initialize_logging(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # console handler
    ch = logging.StreamHandler()
    ch.setLevel(level=logging.INFO)
    fmtr = logging.Formatter("%(levelname)s::%(name)s:: %(message)s")
    ch.setFormatter(fmtr)
    logger.addHandler(ch)
    return logger

def add_file_handler(name, logfile, level=logging.DEBUG):
    logger = logging.getLogger(name)
    fh = logging.FileHandler(logfile)
    fh.setLevel(level=level)
    fmtr = logging.Formatter("%(asctime)s - %(levelname)s::%(name)s(%(lineno)s)"
                             ":: %(message)s",
                             datefmt="%Y-%m-%d %H:%M:%S")
    fh.setFormatter(fmtr)
    logger.addHandler(fh)

def set_level(name, level):
    logger = logging.getLogger(name)
    for handler in logger.handlers:
        handler.setLevel(level=level)

