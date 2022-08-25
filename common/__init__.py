from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData

load_dotenv(".env")

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db_url: str = getenv("DB_LINK", "sqlite:///app.db")
engine = create_engine(db_url, pool_recycle=280)  # echo=True
db_meta = MetaData(bind=engine, naming_convention=convention)
