# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative

import settings

def db_connect():     
    """ Performs database connection using database settings from settings.py.
        :return: sqlalchemy engine instance     
    """
    # return create_engine('sqlite:///images.db', echo=True)
    return create_engine('{drivername}://{username}:{password}@{host}:{port}/{database}'\
        .format(**settings.DATABASES['sqlalchemy'])
    ) 

engine = db_connect() 
session_maker = sessionmaker()

@as_declarative()
class Base(object):
    def __init__(self):
        self.conn = engine.connect()
        self.session = session_maker(bind=self.conn)
        self.close()

    def open(self):
        self.conn = engine.connect()
        self.session = session_maker(bind=self.conn)

    def close(self):
        self.session.close()
        self.conn.close()
        engine.dispose()
