import pandas as pd
from docx import Document
import os

def replace_de_char(st):
    # see https://unicode-table.com/en/alphabets/german/
    st = st.replace("\u201e", "")
    st = st.replace("\u201c", "")
    st = st.replace("\u00C4", "Ä")
    st = st.replace("\u00e4", "ä")
    st = st.replace("\u00D6", "Ö")
    st = st.replace("\u00F6", "ö")
    st = st.replace("\u00DC", "Ü")
    st = st.replace("\u00FC", "ü")
    st = st.replace("\u1E0E", "ẞ")
    st = st.replace("\u00DF", "ß")
    return st


def remove_chars(st):
    char_rmv = ["--", "\t", "     ", "      "]
    for char in char_rmv:
        st = st.replace(char, " ")

    st = replace_de_char(st)
    return st


def get_files(dir):
    res = []
    for file_path in os.listdir(dir):
        # check if current file_path is a file
        if os.path.isfile(os.path.join(dir_path, file_path)):
            # add filename to list
            f_in = dir_path + file_path
            res.append(file_path)
    return res


def process_file(file_path):
    from docx.api import Document
    document = Document(file_path)
    table = document.tables[0]
    data = [file_path]
    for i, row in enumerate(table.rows):
        x = 0
        for cell in row.cells:
            x += 1
            # if x == 1:
            #     print(cell.text, end="")
            if x == 2:
                text = cell.text.rstrip()
                if text == "":
                    text = "N.N."
                data.append(text)
                x = 0
    return data


if __name__ == '__main__':
    dir_path = r'../data/courses/zqm_modul/de/'
    res = get_files(dir_path)

    count = 0
    m = []
    for i in res:
        if i.startswith((".", "~")):  # ignore anyfile that start with "." or "~"
            continue
        count += 1
        dat = process_file(dir_path + i)
        m.append(dat)

    for i in m:
        print(i)
