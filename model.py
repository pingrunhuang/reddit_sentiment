from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Index

Base = declarative_base()

class Sentiment(Base):
    __tablename__ = "sentiment"

    id = Column(Integer, autoincrement=True, primary_key=True)
    unix = Column(String(16))
    title = Column(String(4096))
    sentiment = Column(String(16))
    category = Column(String(128))

    def __repr__(self):
        return "<Sentiment(id='%s', unix='%s', sentiment='%s')>" % (self.id, self.unix ,self.sentiment)

class Caching(Base):
    __tablename__ = "caching"

    id = Column(Integer, autoincrement=True, primary_key=True)
    key = Column(String)
    value = Column(String)

    def __repr__(self):
        return "<Caching(id='%s', key='%s', value='%s')>" % (self.id, self.key ,self.value)


