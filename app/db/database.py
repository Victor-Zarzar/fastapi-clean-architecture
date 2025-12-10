import warnings

from sqlalchemy.exc import SAWarning
from sqlmodel import Session, create_engine
from sqlmodel.sql.expression import Select, SelectOfScalar

from app.core.config import settings

warnings.filterwarnings("ignore", category=SAWarning)
SelectOfScalar.inherit_cache = True
Select.inherit_cache = True

url = settings.DATABASE_URL

engine = create_engine(url, echo=False, pool_pre_ping=True, pool_recycle=1800)


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
