#!/usr/bin/python
import getdirty
import pushintodb
# from sqlalchemy import update
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.exc import IntegrityError
from re import split
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


def domains_into_db_f():
    d2db = getdirty.Extractor('domains', per_page=1)
    d2db.domains_f()
    d2db.per_page = 42
    copys = 0
    while d2db.page <= d2db.numofpages:
        i = 0
        d2db.domains_f()
        while i < d2db.per_page:
            try:
                db = pushintodb.Domains(
                  d2db.domains[i][0], d2db.domains[i][1],
                  d2db.domains[i][2], d2db.domains[i][3], d2db.domains[i][4],
                  d2db.domains[i][5], boolify_f(d2db.domains[i][6]), boolify_f
                  (d2db.domains[i][7]), d2db.domains[i][8], d2db.domains[i][9])
            except Exception:
                print('index error\n\n')
                i = d2db.per_page - 1
            session.add(db)
            try:
                session.commit()
            except Exception as e:
                session.close()
                copys += 1
                print(e)
            i += 1
        d2db.page += 1
        print(d2db.page)
        return(print(d2db.numofitems, copys))


def domain_name_from_db_f():
    domainslist = []
    for instanse in session.query(pushintodb.Domains)\
            .order_by(pushintodb.Domains.readers_count):
        domainslist.append(instanse.prefix)
    domainslist.reverse()
    return(domainslist)


def post_ids_from_db_f():
    idlist = []
    countlist = []
    for instanse in session.query(pushintodb.Posts)\
            .order_by(pushintodb.Posts.domain_id):
        idlist.append(instanse.post_id)
        countlist.append(instanse.comments_count)
    return(idlist, countlist)


def posts_extr_lvl_0_f():
    __domainlist = domain_name_from_db_f()
    p2db = getdirty.Extractor('posts')
    for __podsite in tqdm(__domainlist):
        p2db.index = __podsite
        p2db.page = 1
        posts_extr_lvl_1_f(p2db)


def posts_extr_lvl_1_f(p2db):
    try:
        while p2db.page <= 75:
            p2db.per_page = 42
            p2db.posts_f()
            p2db.i = 0
            posts_extr_lvl_2_f(p2db)
            p2db.page += 1
    except Exception:
        pass


def posts_extr_lvl_2_f(p2db):
    try:
        while p2db.i < p2db.per_page:
            p2db.tags = split(',', p2db.posts[p2db.i][11])
            posts_extr_lvl_4_f(p2db)
            posts_extr_lvl_3_f(p2db)
            p2db.i += 1
    except Exception:
        pass


def posts_extr_lvl_3_f(p2db):
    if int(p2db.posts[p2db.i][3]) > 1274740:
        try:
            db = pushintodb.Posts(
                p2db.posts[p2db.i][0],  p2db.posts[p2db.i][1],
                p2db.posts[p2db.i][2],  p2db.posts[p2db.i][3],
                p2db.posts[p2db.i][4], p2db.posts[p2db.i][5],
                p2db.posts[p2db.i][6], p2db.posts[p2db.i][7],
                p2db.posts[p2db.i][8], p2db.posts[p2db.i][9],
                p2db.posts[p2db.i][10], list(p2db.tags),
                p2db.postupvoters, p2db.postdownvoters,
                boolify_f(p2db.posts[p2db.i][12]),
                boolify_f(p2db.posts[p2db.i][13]),
                boolify_f(p2db.posts[p2db.i][14]),
                boolify_f(p2db.posts[p2db.i][15]),
                boolify_f(p2db.posts[p2db.i][16]),
                unixtimestamp_to_postgres_f(int(p2db.posts[p2db.i][17])))
        except Exception as z:
            pass
        try:
            session.add(db)
            session.commit()
        except Exception as e:
            session.close()
            pass
    else:
        p2db.page = 75
        p2db.i = 41


def posts_extr_lvl_4_f(p2db):
    p2db.mainpage = p2db.page
    p2db.page = 1
    p2db.podsite = p2db.index
    p2db.index = p2db.posts[p2db.i][3]
    try:
        p2db.postvoters_f()
    except Exception as e:
        p2db.postupvoters = []
        p2db.postdownvoters = []
        pass
    p2db.index = p2db.podsite
    p2db.page = p2db.mainpage
    p2db.per_page = 42
# i 6159
# def comments_extr_lvl_0_f():
#    f = open('filtered.list', 'r')
#    c2db = getdirty.Extractor('comments')
#    cbar = tqdm (total = 162200)
#    for __id in f:
#        cbar.update(1)
#        c2db.index = int(__id[:7])
#        c2db.comments_count = int(__id[8:-1])
#        try:
#            comments_extr_lvl_1_f(c2db)
#        except Exception as e:
#            print(e)
#            pass
#    cbar.close()


def comments_extr_lvl_0_f():
    f = open('mistakes10.list', 'r')
    c2db = getdirty.Extractor('comments')
    cbar = tqdm(total=389)
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
            # comments_extr_lvl_2_f(c2db)
            comments_extr_lvl_3_f(c2db)
        except Exception:
            pass
        c2db.i += 1

# def comments_extr_lvl_1_f(c2db):
#    try:
#        c2db.comments_f()
#    except:
#        pass
#    c2db.i = 0
#    while c2db.i < c2db.comments_count:
#        try:
#            comments_extr_lvl_2_f(c2db)
#            comments_extr_lvl_3_f(c2db)
#        except:
#            pass
#        c2db.i += 1

# def comments_extr_lvl_2_f(c2db):
#    try:
#        c2db.page = 1
#        c2db.post = c2db.index
#        c2db.index = c2db.comments[c2db.i][0]
#    except:
#        pass
#    try:
#        c2db.commentvoters_f()
#    except Exception as e:
#        pass
#    c2db.index = c2db.post
#
# def comments_extr_lvl_3_f(c2db):
#    try:
#        db = pushintodb.Comments(
#            c2db.index, c2db.comments[c2db.i][0],
#            c2db.comments[c2db.i][1], c2db.comments[c2db.i][2],
#            c2db.comments[c2db.i][3], c2db.comments[c2db.i][4],
#            c2db.comments[c2db.i][5], c2db.comments[c2db.i][6],
#            list(c2db.commentupvoters), list(c2db.commentdownvoters),
#            boolify_f(c2db.comments[c2db.i][6]),
#            boolify_f(c2db.comments[c2db.i][7]),
#            boolify_f(c2db.comments[c2db.i][8]),
#            boolify_f(c2db.comments[c2db.i][9]))
#    except Exception as e:
#        pass
#    try:
#        session.add(db)
#        session.commit()
#    except Exception as e:
#        session.close()
#        pass


def comments_extr_lvl_3_f(c2db):
    try:
        bodyofcomm = c2db.comments[c2db.i][6]
        idnum = c2db.comments[c2db.i][0]
#        stmt = update(pushintodb.Comments)
#            .where(pushintodb.Comments.id == c2db.comments[c2db.i][0]).\
#            values(create_timestamp = timestamp)
        db = session.query(pushintodb.Comments)\
                    .filter_by(post_id=c2db.index)\
                    .filter_by(body=bodyofcomm)\
                    .update({'id': idnum})
    except Exception as e:
        print(db)
        pass
    try:
        session.commit()
    except Exception as e:
        c2db.i = c2db.maxvalue
        session.close()
        pass


comments_extr_lvl_0_f()
