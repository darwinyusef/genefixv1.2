from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from dotenv import load_dotenv
load_dotenv() 
import os

# 🤓This URL typically includes information such as the database dialect (e.g.,
# mysql, postgresql), username, password, host, and database name. In this code
# snippet, the value for `DATABASE_URL` is retrieved from an environment
# variable using `os.getenv("DATABASE_URL")`, which allows for more secure and
# flexible configuration of the database connection settings.

# Configura tu URL de conexión aquí
# DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(# The `DATABASE_URL` variable is storing the connection URL for the database.

DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Crear las tablas
Base.metadata.create_all(bind=engine)

# 🤓 The comment `# Dependencia para usar DB` is indicating that the following function `get_db()` is a
# dependency function used for interacting with the database. This function is a generator function
# that yields a database session (`db`) to the caller, allowing operations to be performed on the
# database within the context of that session.
# Dependencia para usar DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
