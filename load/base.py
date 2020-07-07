from sqlalchemy import create_engine
#nos permite tener acceso a las funcionalidades de orm de sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
#nos permite trabajar con objetos de python en lugar de querys de sql directamente
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///newspaper.db')

Session = sessionmaker(bind=engine)

Base = declarative_base()
