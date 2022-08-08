from curses import curs_set
import sqlite3
import os
from unittest import result
import time
import pandas as pd
from pyparsing import ExceptionWordUnicode
HERE = os.path.dirname(__file__)
# print(HERE)
def create_table():
    conn = sqlite3.connect(HERE + '/ranking_list.db')
    cursor = conn.cursor()
    sql = '''create table mydb(
    id  text,
    score  INTEGER,
    date text
     )
    '''
    cursor.execute(sql)
    cursor.close()
    cursor.close()
    print("新建表")
def insert_data(tb,id,score,date):
    if(is_have(tb,id)):
        # print('此id已注册！')
        update(tb,id,score,date)
        return True
    else:
        conn = sqlite3.connect(HERE + '/ranking_list.db')
        cursor = conn.cursor()
        sql=" insert into " + tb + '''(id,score,date)
        values
        (?,?,?)
        '''
        cursor.execute(sql,(id,score,date))
        conn.commit()

        cursor.close()
        conn.close()
        print('插入数据成功！')
        return True
def list_mydb(tb):
    conn=sqlite3.connect(HERE + '/ranking_list.db')
    cursor = conn.cursor()
    sql=" select * from " + tb
    results = cursor.execute(sql)
    results_all = results.fetchall()
    print('当前列表数据如下：')
    for r in results_all:
        print(r)
    cursor.close()
    conn.close()
    
def search_mydb(tb,id):
    conn=sqlite3.connect(HERE + '/ranking_list.db')
    cursor = conn.cursor()
    sql=" select * from " + tb +" where id = ?"
    results = cursor.execute(sql,(id,))
    results_all = results.fetchall()
    for r in results_all:
        print(r)
    cursor.close()
    conn.close()
    print('查询数据完毕！')
def del_data(tb,id):
    conn = sqlite3.connect(HERE + '/ranking_list.db')
    cursor = conn.cursor()
    sql="delete from " + tb + " where id=?"
    cursor.execute(sql,(id,))
    conn.commit()
    cursor.close()
    conn.close()
    print('删除数据成功！')
def update(tb,id,score,date):
    if(is_have(tb,id) == 0):
        print('无此id')
    else:
        conn=sqlite3.connect(HERE + '/ranking_list.db')
        cursor = conn.cursor()
        sql = "update " + tb + " set score=? , date=? where id=?"
        cursor.execute(sql,(score,date,id,))
        conn.commit()
        cursor.close()
        conn.close()
        print('修改数据成功')

def is_have(tb,id):
    conn=sqlite3.connect(HERE + '/ranking_list.db')
    cursor = conn.cursor()
    sql=" select * from " + tb +" where id = ?"
    results = cursor.execute(sql,(id,))
    results_all = results.fetchall()
    if results_all:
        return 1
    else:
        return 0
    
    cursor.close()
    conn.close()
    print('查询数据完毕')

def listByScore(tb):
    conn=sqlite3.connect(HERE + '/ranking_list.db')
    cursor = conn.cursor()
    sql = " select * from " + tb + " order by score desc limit 10"
    results = cursor.execute(sql)
    results_all = results.fetchall()
    print('当前分数前十名如下：')
    for r in results_all:
        print(r)
    cursor.close()
    conn.close()
    return (pd.DataFrame(results_all, columns=["id", "score", "timestamp"]).to_json(orient="records"))
    # return results_all

if __name__ == '__main__':
    # create_table()
    # ndate = time.strftime('%Y-%m-%d %H:%M:%S')
    # insert_data('mydb','Sam',9,ndate)
    # search_mydb('mydb','Lim')
    # del_data('mydb','Lihua')
    # list_mydb('mydb')
    # update('mydb','Sam','85',ndate)
    # list_mydb('mydb')
    listByScore('mydb')
    # searchRanking('mydb','Lim')