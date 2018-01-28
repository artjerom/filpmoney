# -*- coding: utf-8 -*-

import shelve
from SQLighter import SQLighter
from config import shelve_name, db_name

def count_rows():
    db = SQLighter(db_name)
    rowsnum = db.count_rows()
    with shelve.open(shelve_name) as storage:
        storage['rows_count'] = rowsnum

def get_rows_count():
    with shelve.open(shelve_name) as storage:
        rowsnum = storage['rows_count']
    return rowsnum

def set_user(id, amount):
    with shelve.open(shelve_name) as storage:
        storage[str(id)] = amount                    