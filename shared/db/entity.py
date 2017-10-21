from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker  , relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    logo_url = Column(String(512))
    name = Column(String(64))
    introduction = Column(String(512))
    industry = Column(String(32))
    financing_phase = Column(String(32))
    city = Column(String(32))
    start_date = Column(String(12))
    investment_platform = Column(String(128))
    site = Column(String(64))
    company_name  = Column(String(64))
    product_description = Column(String(1024))
    picture_set = Column(String(1024))
    advantage = Column(String(1024))
    achievement = Column(String(1024))
    raised_fund = Column(String(20))
    founder = Column(String(64))
    founder_description = Column(String(1024))

class Company_member(Base):
    __tablename__ = 'company_member'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    position = Column(String(64))
    experience = Column(String(128))
    project_id = Column(Integer)
    investment_platform = Column(String(128))

class Financing_phase(Base):
    __tablename__ = 'financing_phase'
    id = Column(Integer, primary_key=True)
    phase = Column(String(32))
    amount = Column(String(32))
    investor = Column(String(96))
    date = Column(String(16))
    project_id = Column(Integer)
    investment_platform = Column(String(128))

class Shareholder(Base):
    __tablename__ = 'shareholder'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    rate = Column(String(64))
    amount = Column(String(256))
    project_id = Column(Integer)
    time = Column(String(32))

class Chandashi_rank(Base):
    __tablename__ = 'chandashi_rank'

    project_id = Column(Integer, primary_key=True)
    name = Column(String(64))
    appname = Column(String(128))
    hotindex = Column(Integer)
    ranktype1 = Column(String(64))
    rank1 = Column(String(64))
    ranktype2 = Column(String(64))
    rank2 = Column(String(64))

class Seochinaz_rank(Base):
    __tablename__ = 'seochinaz_rank'

    id = Column(Integer, primary_key=True) #TODO id --> project_id
    site = Column(String(64), unique=True) #TODO not unique, because of 2 platform 1 same project
    alexaRank = Column(String(64))
    baiduWeight = Column(String(64))
    baiduTraffic = Column(String(64))
    baiduRecordsNumber = Column(String(64))
    oneMonthRecordsNumber = Column(String(64))
    baiduIndexNumber = Column(String(64))
    baiduTheChainNumber = Column(String(64))
    keyWordNumber = Column(String(64))
    alexaTrafficRank = Column(String(64))
    prValue = Column(String(64))
    googleRecordsNumber = Column(String(64))
    googleTheChainNumber = Column(String(64))
    tllSiteRecordsNumber = Column(String(64))
    tllSiteTheChainNumber = Column(String(64))
    sougouRecordsNumber = Column(String(64))
    theChainNumber = Column(String(64))