from src.config import conf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def _init():
    global _global_session

    engine = create_engine('mssql+pymssql://'+conf.get('mysql', 'username')+':'+conf.get(
        'mysql', 'password')+'@'+conf.get('mysql', 'host')+':'+conf.get('mysql', 'port')+'/'+conf.get('mysql', 'db'), pool_size=8)

    global _global_session
    DbSession = sessionmaker(bind=engine)
    _global_session = DbSession()


def get_session():
    return _global_session
