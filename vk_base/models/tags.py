from sqlalchemy import Column, Integer, String
from . import modelsHelper

class Tags(modelsHelper.Base):
    __tablename__ = 'tags'
    tags_id = Column(Integer, primary_key=True)
    tag_name = Column(String, nullable=False)
