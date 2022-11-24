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
    contact = Column(String(255), nullable=False)
    new_image_urls = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)

    def __init__(self, tid, title, content, image_urls, contact, new_image_urls, url):
        self.tid = tid
        self.title = title
        self.content = content
        self.image_urls = image_urls
        self.contact = contact
        self.new_image_urls = new_image_urls
        self.url = url
