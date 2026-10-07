from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(150), unique=True)
    password = Column(String(255))
    role = Column(String(50), default="applicant")


class Instrument(Base):
    __tablename__ = "instruments"

    id = Column(Integer, primary_key=True, index=True)
    instrument_id = Column(String(100), unique=True)
    owner_name = Column(String(150))
    type = Column(String(100))
    manufacturer = Column(String(150))
    capacity = Column(String(100))
    district = Column(String(100))
    status = Column(String(50), default="Registered")
    created_at = Column(DateTime, default=datetime.utcnow)


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    instrument_id = Column(String(100))
    officer = Column(String(150))
    result = Column(String(50))
    remarks = Column(Text)
    data_hash = Column(String(64))
    created_at = Column(DateTime, default=datetime.utcnow)


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    certificate_id = Column(String(100), unique=True)
    instrument_id = Column(String(100))
    owner_name = Column(String(150))
    district = Column(String(100))
    status = Column(String(50), default="VALID")
    valid_until = Column(String(50))
    integrity_hash = Column(String(64))