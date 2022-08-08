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
    conn = sqlite3.connect(HERE + '/ranking_list_test.db')
    cursor = conn.cursor()
    sql = '''create table mydb(
    rank INTEGER,
    id  text,
    score  INTEGER,
    date text
     )
    '''
    cursor.execute(sql)
    cursor.close()
    conn.close()
    print("新建表")
def insert_data(tb,id,score,date):
    if(is_have(tb,id)):
        print('此id已注册！')
        return
    else:
        conn = sqlite3.connect(HERE + '/ranking_list_test.db')
        cursor = conn.cursor()
        # sql=" insert into " + tb + '''(id,score,date)
        # values
        # (?,?,?)
        # '''
        sql = "insert into "+ tb +" (id,score,date) values (?,?,?); "
        cursor.execute(sql,(id,score,date,))

        sql = " update " + tb + " set rank = ( "
        sql +=" with  AA2 AS ( "
        sql +="select count(*) as num,a1.ROWID "
        sql +="from " + tb + " a1, " + tb + " b1 "
        sql +="where a1.score < b1.score "
        sql +="group by a1.ROWID) "
        sql +="select ifnull(AA2.num,0)+1 as rankPlus /*, c1.**/ "
        sql +=" from " + tb + " c1 "
        sql +="left join AA2 on  AA2.ROWID = c1.ROWID "
        sql +="where c1.ROWID = " + tb + ".ROWID "
        sql +=") where score <= ? ; "
        cursor.execute(sql,(score,))

        sql ="select * from " + tb + " ; "
        cursor.execute(sql)

        conn.commit()

        cursor.close()
        conn.close()
        print('插入数据成功！')
def list_mydb(tb):
    conn=sqlite3.connect(HERE + '/ranking_list_test.db')
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
    conn=sqlite3.connect(HERE + '/ranking_list_test.db')
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
    conn = sqlite3.connect(HERE + '/ranking_list_test.db')
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
        conn=sqlite3.connect(HERE + '/ranking_list_test.db')
        cursor = conn.cursor()
        sql = "update " + tb + " set score=? , date=? where id=?"
        cursor.execute(sql,(score,date,id,))
        conn.commit()
        cursor.close()
        conn.close()
        print('修改数据成功')

def is_have(tb,id):
    conn=sqlite3.connect(HERE + '/ranking_list_test.db')
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
    conn=sqlite3.connect(HERE + '/ranking_list_test.db')
    cursor = conn.cursor()
    sql = " select * from " + tb + " order by score desc limit 10 "
    results = cursor.execute(sql)
    results_all = results.fetchall()
    print('当前分数排名如下：')
    for r in results_all:
        print(r)
    cursor.close()
    conn.close()
    # print(pd.DataFrame(results_all, columns=["rank", "id", "score", "timestamp"]).to_json(orient="records"))
    return pd.DataFrame(results_all, columns=["id", "score", "timestamp"]).to_json(orient="records")

if __name__ == '__main__':
    ndate = time.strftime('%Y-%m-%d %H:%M:%S')
    insert_data('mydb','Jacob',60,ndate)
    # search_mydb('mydb','Lim')
    # del_data('mydb','Lihua')
    # list_mydb('mydb')
    # update('mydb','Sam','85',ndate)
    # list_mydb('mydb')
    listByScore('mydb')
    # searchRanking('mydb','Lim')
    # create_table()
