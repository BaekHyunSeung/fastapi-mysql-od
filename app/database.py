#DB연결 엔진
import json
import pathlib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = pathlib.Path(__file__).parent.parent
with open(BASE_DIR / "secrets.json") as f:
    secrets = json.loads(f.read())

#DB URL 구성
DB_URL = f"mysql+pymysql://{secrets['DB']['user']}:{secrets['DB']['password']}@{secrets['DB']['host']}:{secrets['DB']['port']}/{secrets['DB']['database']}?charset=utf8"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()