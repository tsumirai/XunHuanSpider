from operator import truediv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Index, distinct, update
from sqlalchemy.types import *

Base = declarative_base()


class Xunhuan(Base):
    __tablename__ = 'xunhuan_content'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tid = Column(BigInteger, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    image_urls = Column(String(255), nullable=False)
    qq = Column(String(255), nullable=False)
    wx = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)

    def __init__(self, tid, title, content, image_urls, qq, wx, url):
        self.tid = tid
        self.title = title
        self.content = content
        self.image_urls = image_urls
        self.qq = qq
        self.wx = wx
        self.url = url
