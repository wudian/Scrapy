from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.entity import Project

engine = create_engine('mysql+pymysql://root:root@localhost:3306/investment_platform_db?charset=utf8',echo="debug")
DBSession = sessionmaker(bind=engine)


session = DBSession()
p = Project(name = 'aa')
session.add(p)
session.commit()
session.close()


session.close()

