#!/usr/bin/python
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, Text, Boolean, ForeignKey, SmallInteger
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import mapper, sessionmaker

engine = create_engine('postgresql+psycopg2://wgtx@localhost:5432/dirtydb', echo = False)
Session = sessionmaker(bind = engine)
metadata = MetaData()

domains_table = Table('domains', metadata,
        Column('id', SmallInteger, primary_key = True),
        Column('readers_count', Integer),
        Column('prefix', Text),
        Column('name', Text),
        Column('title', Text),
        Column('description', Text),
        Column('democracy', Boolean),
        Column('public', Boolean),
        Column('owner', Text),
        Column('president', Text)
        )

posts_table = Table('posts', metadata,
        Column('domain_id', SmallInteger),
        Column('user_id', Integer),
        Column('user_login', Text),
        Column('id', Integer, primary_key = True),
        Column('rating', SmallInteger),
        Column('title', Text),
        Column('text', Text),
        Column('link_title', Text),
        Column('link_descriprion', Text),
        Column('link_url', Text),
        Column('comments_count', SmallInteger),
        Column('tags', postgresql.ARRAY(Text)),
        Column('upvoters', postgresql.ARRAY(Text, dimensions = 2)),
        Column('downvoters', postgresql.ARRAY(Text, dimensions = 2)),
        Column('golden', Boolean),
        Column('can_delete', Boolean),
        Column('can_unpublish', Boolean),
        Column('can_moderate', Boolean),
        Column('can_edit', Boolean),
        Column('create_timestamp', postgresql.TIMESTAMP(timezone = True))
        )

comments_table = Table('comments', metadata,
        Column('post_id', Integer),
        Column('id', Integer, primary_key = True),
        Column('parent_id', Text),
        Column('tree_level',SmallInteger),
        Column('rating',SmallInteger),
        Column('user_id',Integer),
        Column('login', Text),
        Column('body', Text),
        Column('upvoters', postgresql.ARRAY(Text, dimensions = 2)),
        Column('downvoters', postgresql.ARRAY(Text, dimensions = 2)),
        Column('can_delete', Boolean),
        Column('can_remove_thread', Boolean),
        Column('can_edit', Boolean),
        Column('can_moderate', Boolean),
        Column('create_timestamp', postgresql.TIMESTAMP(timezone = True))
        )

users_table = Table('users', metadata,
        Column('idu', Integer, primary_key = True),
        Column('login', Text),
        Column('gender', Text),
        Column('rank', Text),
        Column('karma', SmallInteger),
        Column('golden', Boolean),
        Column('active', Boolean),
        Column('deleted', Boolean)
        )

#user_karma = Table('users', metadata,
#        Column('login', Text),
#        Column('upvoters', postgresql.ARRAY(Text, dimensions = 2)),
#        Column('downvoters', postgresql.ARRAY(Text, dimensions = 2))
#        )

class UsersVotes(object):
    def __init__(self, login, upvoters, downvoters):
        self.login = login
        self.upvoters = upvoters
        self.downvoters = downvoters

    def __repr__(self):
        return "<UsersVotes('%s','%s','%s')>" % (self.login, self.upvoters, self.downvoters)

class Users(object):
    def __init__(self, idu, login, gender, rank, karma, golden, active, deleted):
        self.idu = idu
        self.login = login
        self.gender = gender
        self.rank = rank
        self.karma = karma
        self.golden = golden
        self.active = active
        self.deleted = deleted
    
    def __repr__(self):
        return "<Users('%s','%s','%s','%s','%s','%s','%s','%s',)>" %\
                (self.idu, self.login, self.gender, self.rank, self.karma, self.golden, self.active, self.deleted)

class Comments(object):
    def __init__(self, post_id, comment_id, parent_id, tree_level, rating, user_id, user_login, body, upvoters, downvoters, can_delete, can_remove_thread, can_edit, can_moderate, create_timestamp):
        self.post_id = post_id
        self.comment_id = comment_id
        self.parent_id = parent_id
        self.tree_level = tree_level
        self.rating = rating
        self.user_id = user_id
        self.user_login = user_login
        self.body = body
        self.upvoters = upvoters
        self.downvoters = downvoters
        self.can_delete = can_delete
        self.can_remove_thread = can_remove_thread
        self.can_edit = can_edit
        self.can_moderate = can_moderate
        self.create_timestamp = create_timestamp

    def __repr__(self):
        return "<Comments('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %\
                (self.post_id, self.comment_id, self.parent_id, self.tree_level, self.rating,\
                 self.user_id, self.user_login, self.body, self.upvoters, self.downvoters, self.can_delete,\
                 self.can_remove_thread, self.can_edit, self.can_moderate, self.create_timestamp)
    
class Domains(object):
    def __init__(self, domain_id, readers_count, prefix, name, title,\
                descriprion, democracy, public, owner, president):
        self.domain_id = domain_id
        self.readers_count = readers_count 
        self.prefix = prefix
        self.name = name
        self.title = title
        self.descriprion = descriprion 
        self.democracy = democracy
        self.public = public
        self.owner = owner
        self.president = president

    def __repr__(self):
        return "<Domains('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" %\
                (self.domain_id, self.readers_count, self.prefix, self.name, self.title,\
                self.descriprion, self.democracy, self.public, self.owner, self.president)

class Posts(object):
    def __init__(self, domain_id, user_id, user_login, post_id, rating, title, text,\
                link_title, link_descriprtion, link_url, comments_count, tags, upvoters,\
                downvoters, golden, can_delete, can_unpublish, can_moderate, can_edit,\
                create_timestamp):
        self.domain_id = domain_id
        self.user_id = user_id
        self.user_login = user_login
        self.post_id = post_id 
        self.rating = rating
        self.title = title
        self.text = text 
        self.link_title = link_title 
        self.link_descriprtion = link_descriprtion
        self.link_url = link_url 
        self.comments_count = comments_count
        self.tags = tags
        self.upvoters = upvoters
        self.downvoters = downvoters
        self.golden = golden
        self.can_delete = can_delete
        self.can_unpublish = can_unpublish
        self.can_moderate = can_moderate
        self.can_edit = can_edit
        self.create_timestamp = create_timestamp
        
    def __repr__ (self):
        return "<Posts('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',\
                 '%s', %s, %s, '%s','%s')>"%(self.domain_id,self.user_id,self.user_login,\
                 self.post_id, self.rating, self.title, self.text, self.link_title,\
                 self.link_descriprtion, self.link_url, self.comments_count, self.tags,\
                 self.upvoters, self.downvoters, self.golden, self.can_delete,\
                 self.can_unpublish, self.can_moderate, self.can_edit, self.create_timestamp)

mapper(Domains, domains_table)
mapper(Posts, posts_table)
mapper(Users, users_table)
#mapper(UsersVotes, user_karma)
mapper(Comments, comments_table)
metadata.create_all(engine)
