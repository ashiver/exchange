import datetime
from flask.ext.login import UserMixin
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, LargeBinary, Float
from sqlalchemy.orm import relationship
from .database import Base, engine



class Brew(Base):
    __tablename__ = "brews"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    picture = Column(LargeBinary)
    description = Column(Text)
    brew_type = Column(String(128))
    brew_value = Column(Float, default=1)
    brew_date = Column(DateTime)
    brew_count = Column(Integer)
    brewer_id = Column(Integer, ForeignKey('users.id'))
    comments = relationship("Comment", backref="brew")
    owners = relationship("User", backref="owner")
    

class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True)
    active = Column(Boolean, default='True')
    datetime = Column(DateTime, default=datetime.datetime.now)
    brew_id = Column(Integer, ForeignKey('brews.id'))
    bottles = Column(Integer)
    agent_id = Column(Integer, ForeignKey('users.id'))
    

class Proposal(Base):
    __tablename__ = "proposals"
    
    id = Column(Integer, primary_key=True)
    active = Column(Boolean, default='True')
    datetime = Column(DateTime, default=datetime.datetime.now)
    trade_id = Column(Integer, ForeignKey('trades.id'))
    brew_id = Column(Integer, ForeignKey('brews.id'))
    bottles = Column(Integer)
    agent_id = Column(Integer, ForeignKey('users.id'))

    
    
class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)
    brew_id = Column(Integer, ForeignKey('brews.id'))
    proposal_id = Column(Integer, ForeignKey('proposals.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
    
    
    
class User(Base, UserMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    username = Column(String(128), unique=True)
    password = Column(String(128))
    superuser = Column(Boolean, default='False')
    active = Column(Boolean, default='True')
    city_state = Column(String(128))
    zipcode = Column(Integer)
    bio = Column(Text)
    picture = Column(String, default="http://icons.iconarchive.com/icons/icons8/windows-8/128/Food-Beer-icon.png")
    joindate = Column(DateTime, default=datetime.datetime.now)
    products = relationship("Brew", backref="brewer")
    trades = relationship("Trade", backref="agent")
    proposals = relationship("Proposal", backref="agent")
    comments = relationship("Comment", backref="author")
    
class Holding(Base):
    __tablename__ = "market"
    
    id = Column(Integer, primary_key=True)
    brew_id = Column(Integer, ForeignKey('brews.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))
    shares = Column(Integer)
     
    
Base.metadata.create_all(engine)
