from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

password="root"
DATABASE_URL = "mysql://root:"+password+"@localhost:3306/movie_booking2"

db_engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=db_engine)

Base = declarative_base()