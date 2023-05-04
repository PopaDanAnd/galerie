
from sqlalchemy import create_engine, Table, Column, Boolean, Integer, String, Text, ForeignKey, func, UniqueConstraint, and_, or_, not_, desc, asc
from sqlalchemy.orm import Session, sessionmaker, relationship, DeclarativeBase
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method


class Base(DeclarativeBase):
    pass
