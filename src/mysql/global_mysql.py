from src.config import conf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


def _init():
    global _global_session

    mysql_config = 'mysql+pymysql://'+conf.get('mysql', 'username')+':'+conf.get(
        'mysql', 'password')+'@'+conf.get('mysql', 'host')+':'+conf.get('mysql', 'port')+'/'+conf.get('mysql', 'db')+'?charset=utf8mb4'
    # print(mysql_config)
    engine = create_engine(mysql_config, max_overflow=int(conf.get('mysql', 'max_overflow')), pool_size=int(conf.get('mysql', 'pool_size')), pool_timeout=int(
        conf.get('mysql', 'pool_timeout')), pool_recycle=int(conf.get('mysql', 'pool_recycle')), echo=bool(conf.get('mysql', 'echo')))

    DbSession = sessionmaker(bind=engine)
    _global_session = scoped_session(DbSession)


def get_session():
    return _global_session


def add_data(instance):
    _global_session.add(instance)
    _global_session.commit()
    _global_session.close()


def add_all(instances):
    _global_session.add_all(instances)
    _global_session.commit()
    _global_session.close()
