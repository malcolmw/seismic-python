import logging


def get_logger(name):
    return (logging.getLogger(name))


def configure_logger(name, logfile, verbose=False):
    '''
    A utility function to configure logging.
    '''
    if verbose is True:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if level == logging.DEBUG:
        formatter = logging.Formatter(fmt='%(asctime)s::%(levelname)s::'\
                '%(funcName)s()::%(lineno)d:: '\
                '%(message)s',
                datefmt="%Y%jT%H:%M:%S")
    else:
        formatter = logging.Formatter(fmt='%(asctime)s::%(levelname)s:: '\
                '%(message)s',
                datefmt="%Y%jT%H:%M:%S")
    if logfile is not None:
        file_handler = logging.FileHandler(logfile)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
