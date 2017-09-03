from sqlalchemy import Column, Integer, String
from . import modelsHelper

class Albums(modelsHelper.Base):
    __tablename__ = 'albums'
    album_id = Column(Integer, primary_key=True)
    album_type = Column(Integer, nullable=False, default=0)
    album_title = Column(String, nullable=False)
    album_description = Column(String, nullable=False)

    # def insert(self, albums):
    #     super().open()
    #     for album in albums:
    #         a = Albums()
    #         a.album_id = album.album_id
    #         self.session.add(a)
    #         self.session.commit()
    #     super().close()

    def update(self, album_id, album_type, album_title, album_description):
        super().open()
        try:
            self.session.query(Albums).filter(Albums.album_id == album_id)\
            .update({
                'album_type': album_type,
                'album_title': album_title,
                'album_description': album_description,
            })
            self.session.commit()
        except Exception as e:
            print(e)
        super().close()
