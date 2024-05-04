"""
"""

import os
import pandas as pd
import Levenshtein


def create_directory(directory):
    """
    Creates a directory
    @param directory: directory to be created
    @return: 0 if operation successful
    """
    try:
        os.makedirs(directory)
    except OSError as e:
        if not os.path.isdir(directory):
            raise e
    return 0


def exist(file_path):
    """
    Checks if a file path exist
    @param file_path: file path to check
    @return: true or false
    """
    if os.path.exists(file_path):
        return True
    else:
        return False


def open_file(file_path):
    """
    creates a file handler
    @param file_path: file to open
    @return:
    """
    file_handle = open(file_path, "w")
    return file_handle


def close_file(file_handle):
    """
    closes a file
    @param file_handle: file handler of file to close
    @return:
    """
    file_handle.close()
    return


def write_line(file_handle, line):
    """
    Write a file
    @param file_handle: file handler
    @param line:
    @return:
    """
    file_handle.write(line)
    return


def file2df(file_in):
    """
    Reads a comma separated file and returns a data frame
    :param file_in: csv data file
    :return: DataFrame: -1 if error
    """
    if not os.path.isfile(file_in) or not os.access(file_in, os.R_OK):
        print("Cannot locate file",)
        return -1

    data = pd.read_csv(file_in, header=0)
    # we deal with missing values here

    return data


def file_sanity_check(file_path):
    """
    This function does a basic check to ensure a file can be read
    and that does not have missing values.

    :param file_path: file_path
    :return: data frame; None if file has missing values
    """
    data = pd.read_csv(file_path, header=0)

    for index, row in data.iterrows():

        for i in row:
            if pd.isnull(i):
                # there are lots of ways to dealt with missing values (e.g. fillna, drop row, etc.)
                print("File contain missing values")
                return None

    return data


def csv2df(file_in):
    """
    Reads a comma separated file and returns a pandas data frame
    :param file_in: csv data file
    :return: DataFrame: -1 if error
    """
    if not os.path.isfile(file_in) or not os.access(file_in, os.R_OK):
        print("Cannot locate file", file_in)
        return -1

    data = pd.read_csv(file_in, header=0)
    # we deal with missing values here

    return data


def lang_context(conf, lang):
    context = []
    if lang == 'en':
        context.append(conf.get('ESCO_DB_EN'))
        context.append(conf.get('SBERT_TRAINED_MODEL_EN'))
    elif lang == 'de':
        context.append(conf.get('ESCO_DB_DE'))
        context.append(conf.get('SBERT_TRAINED_MODEL_DE'))

    return context


def get_normalised_edit_distance(s1, s2):
    edit_distance = Levenshtein.distance(s1, s2)
    dist = round((edit_distance / max(len(s1), len(s2))), 2)
    return edit_distance, dist


def edit_distance(s1, s2):
    edit, dis = get_normalised_edit_distance(s1.lower(), s2.lower())
    return edit, dis


