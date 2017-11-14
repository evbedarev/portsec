import sqlite3
import os

def read_settings(par):
    list = []
    dir = os.path.abspath(os.curdir)
    base_name = dir + r'\android.sqlite'
    con = sqlite3.connect(base_name)
    cur = con.cursor()
    cur.execute(
                "select {} from {} where name_par='{}'".format('value', 'par', par)
            )
    res = cur.fetchall()
    for i in res:
        for j in i:
            list.append(j)
    cur.close()
    con.close()
    return(list)

    # noinspection PyUnreachableCode


def ins_to_db(par, val):
    list = []
    dir = os.path.abspath(os.curdir)
    base_name = dir + r'\android.sqlite'
    con = sqlite3.connect(base_name)
    cur = con.cursor()

    cur.execute(
         "delete from par where name_par='{}'".format(par)
    )
    con.commit()
    for i in val:
        print(i)
        cur.execute(
            "INSERT INTO 'main'.'par' ('name_par','value') VALUES ('{}','{}')".format(par, i)
        )
    con.commit()
    cur.close()
    con.close()