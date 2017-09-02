# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, func, ForeignKey, Integer, Float, String 
from sqlalchemy import Boolean, DateTime, types, distinct
from sqlalchemy import Table, text, MetaData, Column, Integer, or_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import PrimaryKeyConstraint, ForeignKeyConstraint, UniqueConstraint
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

    def get_thematic_training_set(self):
        super().open()
        records = self.session.query(\
                Images.album_id,\
                Images.image_hash,\
                Albums.album_id,\
                Albums.album_type,\
                Albums.super_id\
            )\
            .join(Albums, Albums.album_id == Images.album_id)\
            .filter(Albums.album_type == 1)\
            .all()   
        super().close()
        return records

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
        records = self.session.query(Images).filter(Images.album_id == '-2481783').all()   
        super().close()
        return records
    
    def get_albums(self):
        super().open()
        query = self.session.query(distinct(Images.album_id), Images.album_id)
        records = query.all()
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

class Albums(Base):
    __tablename__ = 'albums'
    super_id = Column(Integer, default=0)
    album_id = Column(Integer, primary_key=True)
    album_type = Column(Integer, nullable=False, default=0)
    __table_args__ = (
        UniqueConstraint('super_id'),
    )

    def get_by_super_id(self, super_id):        
        super().open()
        records = self.session.query(Albums).filter(Albums.super_id == super_id).first()   
        super().close()
        return records

    # def insert(self, albums):
    #     super().open()
    #     for album in albums:
    #         a = Albums()
    #         a.album_id = album.album_id
    #         self.session.add(a)
    #         self.session.commit()
    #     super().close()

    def update(self, album_id, album_type):
        super().open()
        try:  
            self.session.query(Albums).filter(Albums.album_id == album_id).update({
                'album_type': album_type
            })
            self.session.commit()
        except Exception as e:
            print(e)
        super().close()

class AlbumsTags(Base):
    __tablename__ = 'albums_tags'
    albums_tags_id = Column(Integer, primary_key=True)
    album_id = Column(Integer, ForeignKey('albums.album_id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.tags_id'), nullable=False)

# engine = db_connect() 
# session_maker = sessionmaker()
Base.metadata.create_all(engine)