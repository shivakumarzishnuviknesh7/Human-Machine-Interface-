import logging
import datetime
from include.utils import *


def name_log_file(folder):
    log_name = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    dir_logs = folder
    if not exist(dir_logs):
        create_directory(dir_logs)

    log_file = dir_logs+log_name+".log"
    return log_file


def initialize_logger(folder, level):
    """
    Function to initialise the logger
    :param folder: log folder
    :param level: logger level e.g. debug
    :return: logger handler including messaging formatting
    """
    log_file = name_log_file(folder)
    logger = logging.getLogger()
    logger.setLevel(level)

    # create console handler
    console_level = level
    handler = logging.StreamHandler()
    handler.setLevel(console_level)
    formatter = logging.Formatter("["+level+"]- %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler
    handler = logging.FileHandler(log_file, "w")
    handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s ["+level+"]- %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
