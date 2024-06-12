import sqlite3

def get_learning_obj_en(db_file):
    """
    :param db_file: database file location
    :return: list with learning objectives
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    statement = 'SELECT learning_obj FROM zqm_module_en'
    cursor.execute(statement)
    records = cursor.fetchall()
    learning_obj = []
    for row in records:
        learning_obj.append([row[0]])
    conn.close()

    return learning_obj


def get_course_by_instructor(db_file, name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    query = "SELECT * FROM zqm_module_en WHERE instructor LIKE ?"
    cursor.execute(query, ('%' + name + '%',))
    records = cursor.fetchall()
    instructor = []
    for row in records:
        instructor.append([row[1]])
    conn.close()
    return instructor


def get_course_general(db_file, name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    query = "SELECT * FROM zqm_module_en WHERE title LIKE ?"
    cursor.execute(query, ('%' + name + '%',))
    records = cursor.fetchall()
    title = []
    for row in records:
        title.append([row[:]])
    conn.close()
    return records
