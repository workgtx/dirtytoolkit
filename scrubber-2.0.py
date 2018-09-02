#!/usr/bin/python
import getdirty
import pushintodb
# from sqlalchemy import update
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.exc import IntegrityError
# from re import split
# import pdb
from tqdm import tqdm
import datetime

session = pushintodb.Session()


def boolify_f(__change):
    if __change == 'True':
        return True
    elif __change == 'False':
        return False
    else:
        pass


def unixtimestamp_to_postgres_f(__timestamp):
    __value = datetime.datetime.fromtimestamp(__timestamp)
    __postgrestimestamp = (__value.strftime('%Y-%m-%d %H:%M:%S+03'))
    return(__postgrestimestamp)


def comments_extr_lvl_0_f():
    f = open('mistakes.list', 'r')
    c2db = getdirty.Extractor('comments')
    cbar = tqdm(total=10389)
    for __id in f:
        cbar.update(1)
        c2db.index = int(__id)
        try:
            comments_extr_lvl_1_f(c2db)
        except Exception as e:
            print('Ошибка индекса в посте')
            pass
    cbar.close()


def comments_extr_lvl_1_f(c2db):
    try:
        c2db.comments_f()
    except Exception:
        pass
    c2db.maxvalue = 2000
    c2db.i = 0
    while c2db.i < c2db.maxvalue:
        try:
            comments_extr_lvl_2_f(c2db)
            comments_extr_lvl_3_f(c2db)
        except Exception:
            pass
        c2db.i += 1


def comments_extr_lvl_2_f(c2db):
    try:
        c2db.page = 1
        c2db.post = c2db.index
        c2db.index = c2db.comments[c2db.i][0]
    except Exception:
        pass
    try:
        c2db.commentvoters_f()
    except Exception as e:
        pass
    c2db.index = c2db.post


def comments_extr_lvl_3_f(c2db):
    try:
        db = pushintodb.Comments(
                c2db.index, c2db.comments[c2db.i][0],
                c2db.comments[c2db.i][1], c2db.comments[c2db.i][2],
                c2db.comments[c2db.i][3], c2db.comments[c2db.i][4],
                c2db.comments[c2db.i][5], c2db.comments[c2db.i][6],
                list(c2db.commentupvoters), list(c2db.commentdownvoters),
                boolify_f(c2db.comments[c2db.i][7]),
                boolify_f(c2db.comments[c2db.i][8]),
                boolify_f(c2db.comments[c2db.i][9]),
                boolify_f(c2db.comments[c2db.i][10]),
                unixtimestamp_to_postgres_f(int(c2db.comments[c2db.i][11])))
    except Exception as e:
        pass
    try:
        session.add(db)
        session.commit()
    except Exception as e:
        c2db.i = c2db.maxvalue
        session.close()
        pass


class Users():
    def __init__(self):
        self.per_page = 210

    def list_cycle_f(self):
        self.file = open('users.list', 'r')
        self = getdirty.Extractor('users')
        __bar = tqdm(total=29429)
        for __id in self.file:
            __bar.update(1)
            self.index = int(__id)
            try:
                self.votes_cycle_f()
            except Exception as e:
                print('Ошибка в имени пользователя')
                pass
        __bar.close()

    def votes_cycle_f(self):
        try:
            self.users_f()
        except Exception as e:
            print('Ошибка вызова функции \'getdirty.users_f()\',\
                    проверьте аргументы')
        self.maxvalue = 10000
        self.iter = 0
        self.a = False
        self.b = False
        while self.iter < self.maxvalue:
            try:
                self.userdata_to_db_f()
            except Exception as e:
                print('Ошибка вызова фунций записи userdata в БД')
        try:
            self.uservotes_to_db_f()
        except Exception:
            print('Ошибка вызова фунций записи uservotes в БД')

    def userdata_to_db_f(self):
        if self.a is False:
            try:
                self.userdataup = pushintodb.users(
                    self.userupvoters[self.iter][1],
                    self.userupvoters[self.iter][2],
                    self.userupvoters[self.iter][4],
                    self.userupvoters[self.iter][5],
                    self.userupvoters[self.iter][6],
                    boolify_f(self.userupvoters[self.iter][7]),
                    boolify_f(self.userupvoters[self.iter][8]),
                    boolify_f(self.userupvoters[self.iter][9]))
            except Exception:
                self.a = True
            try:
                session.add(self.userdataup)
                session.commit()
            except Exception:
                session.close()
        if self.b is False:
            try:
                self.userdatadown = pushintodb.users(
                        self.userdownvoters[self.iter][1],
                        self.userdownvoters[self.iter][2],
                        self.userdownvoters[self.iter][4],
                        self.userdownvoters[self.iter][5],
                        self.userdownvoters[self.iter][6],
                        boolify_f(self.userdownvoters[self.iter][7]),
                        boolify_f(self.userdownvoters[self.iter][8]),
                        boolify_f(self.userdownvoters[self.iter][9]))
            except Exception:
                self.b = True
            try:
                session.add(self.userdatadown)
                session.commit()
            except Exception:
                session.close()

    def uservotes_to_db_f(self):
        try:
            self.uservotes = pushintodb.UsersVotes(
                    self.index, self.userupvoters, self.downvoters)
        except Exception:
            print('Ошибка записи в БД')
        try:
            session.add(self.uservotes)
            session.commit()
        except Exception:
            session.close()


comments_extr_lvl_0_f()
