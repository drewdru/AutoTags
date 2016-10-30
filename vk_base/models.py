# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, func, ForeignKey, Integer, Float, String 
from sqlalchemy import Boolean, DateTime, types, distinct
from sqlalchemy import Table, text, MetaData, Column, Integer, or_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.ext.declarative import as_declarative
# from sqlalchemy import *
try:
    from . import settings
except Exception:
    import settings

def db_connect():     
    """     
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance     
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

class Images(Base):
    __tablename__ = 'images'
    super_id = Column(Integer, primary_key=True)
    image_id = Column(Integer, nullable=False)
    owner_id = Column(Integer, nullable=False)
    album_id = Column(Integer, nullable=False)
    image_caption = Column(String, nullable=True)
    image_hash = Column(String, nullable=True)

    def insert(self, image_info, image_hash):
        super().open()
        image = Images()        
        image.image_id = image_info['id']
        image.owner_id = image_info['owner_id']
        image.album_id = image_info['album_id']
        image.image_caption = image_info['text']
        image.image_hash = image_hash
        self.session.add(image)
        self.session.commit()
        super().close()
    
    def update_album_id(self, image_id, album_id):
        super().open()
        try:  
            self.session.query(Images).filter(Images.image_id == image_id).update({
                'album_id': album_id
            })
            self.session.commit()
        except Exception as e:
            print(e)
        super().close()
    
    def get_failed_album_images(self):
        super().open()
        records = query = self.session.query(Images).filter(Images.album_id == '-2481783').all()   
        super().close()
        return records


class ImagesTags(Base):
    __tablename__ = 'images_tags'
    images_tags_id = Column(Integer, primary_key=True)
    image_super_id_id = Column(Integer, ForeignKey('images.super_id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.tags_id'), nullable=False)


class Tags(Base):
    __tablename__ = 'tags'
    tags_id = Column(Integer, primary_key=True)
    tag_name = Column(String, nullable=False)

# engine = db_connect() 
# session_maker = sessionmaker()

Base.metadata.create_all(engine)

# engine = db_connect() 
# session_maker = sessionmaker()
# metadata = MetaData(engine)

# images = Table('images', metadata,
#     super_id = Column(Integer, primary_key=True),
#     image_id = Column(Integer, nullable=False),
#     owner_id = Column(Integer, default=settings.VK['owner_id'], nullable=False),
#     album_id = Column(Integer, nullable=False),
#     image_caption = Column(String, nullable=True),
#     image_hash = Column(String, nullable=True),
# )
# images.create()

# tags = Table('tags', metadata,
#     tags_id = Column(Integer, primary_key=True),
#     tag_name = Column(String, nullable=False),
# )
# tags.create()

# images_tags = Table('images_tags', metadata,
#     images_tags_id = Column(Integer, primary_key=True),
#     image_id = Column(Integer, ForeignKey('images.id'), nullable=False),
#     tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False),
# )
# images_tags.create()