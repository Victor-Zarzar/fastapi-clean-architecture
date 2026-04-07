import warnings

from sqlalchemy import create_engine
from sqlalchemy.exc import SAWarning
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel.sql.expression import Select, SelectOfScalar

from app.core.config import settings

warnings.filterwarnings("ignore", category=SAWarning)
SelectOfScalar.inherit_cache = True
Select.inherit_cache = True

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=1800,
)

session_maker = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
)


def get_db():
    with session_maker() as db:
        yield db
