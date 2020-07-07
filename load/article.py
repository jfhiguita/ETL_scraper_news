from sqlalchemy import Column, String, Integer

from base import Base

class Article(Base):
    __tablename__ = 'articles'

    id = Column(String, primary_key=True)
    body = Column(String)
    host = Column(String)
    title = Column(String)
    newspaper_uid = Column(String)
    url = Column(String, unique=True)

    def __init__(self, 
                 uid,
                 body,
                 host,
                 newspaper_uid,
                 title,
                 url):
        self.id = uid
        self.body = body
        self.host = host
        self.newspaper_uid = newspaper_uid
        self.title = title
        self.url = url
