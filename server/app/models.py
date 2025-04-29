from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, DECIMAL, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    approval_token = Column(String(255), unique=True, nullable=True)
    rol = Column(String(255), nullable=True)
    email_verified_at = Column(DateTime, nullable=True)
    password = Column(String(255), nullable=True)
    remember_token = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relaciones
    causaciones = relationship("CausacionContable", back_populates="user", cascade="all, delete")


class PasswordResetToken(Base):
    __tablename__ = 'password_reset_tokens'

    email = Column(String(255), primary_key=True, index=True)
    token = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=True)


class CausacionContable(Base):
    __tablename__ = 'causacioncontable'

    id = Column(Integer, primary_key=True, index=True)
    id_documento = Column(String, nullable=True)
    id_comprobante = Column(Integer, nullable=False)
    id_nit = Column(Integer, nullable=False)
    fecha = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_manual = Column(DateTime, nullable=True)
    id_cuenta = Column(Integer, nullable=False)
    valor = Column(DECIMAL(15, 2), nullable=False)
    tipo = Column(SmallInteger, nullable=False)
    concepto = Column(Text, nullable=False)
    documento_referencia = Column(String(255), nullable=True)
    token = Column(String(255), nullable=True)
    extra = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    estado = Column(String(255), default='entregado')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User', back_populates='causaciones')


class Configuration(Base):
    __tablename__ = 'configurations'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, nullable=False)
    value = Column(Text, nullable=True)
    description = Column(String(255), nullable=True)
    type = Column(String(255), default='string', nullable=True)
    state = Column(String(255), default='string', nullable=True)
    id_user = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))