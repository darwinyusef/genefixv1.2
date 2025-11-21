import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import sys
import os

# Agregar el directorio raíz al path para poder importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from app.models import Base
from app.config.database import get_db
from app.config.config import create_access_token

# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Crea una nueva sesión de base de datos para cada test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Cliente de prueba de FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Crea un usuario de prueba"""
    from app.models import User
    user = User(
        id=1,
        username="testuser",
        name="Test User",
        email="test@example.com",
        password="hashed_password",
        rol="admin"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_token(test_user):
    """Genera un token JWT válido para pruebas"""
    token = create_access_token(data={"sub": str(test_user.id)})
    return token


@pytest.fixture
def test_configuration(db_session):
    """Crea configuración de contador para tests"""
    from app.models import Configuration
    config = Configuration(
        key="counter",
        value="1000",
        description="Test counter",
        type="integer"
    )
    db_session.add(config)
    db_session.commit()
    db_session.refresh(config)
    return config
