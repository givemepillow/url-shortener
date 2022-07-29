from sqlalchemy import (
    Column, BigInteger,
    MetaData, String, Table, DateTime, func, Index,
)

convention = {
    'all_column_names': lambda constraint, table: ''.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix%(table_name)s%(all_column_names)s',
    'uq': 'uq%(table_name)s%(all_column_names)s',
    'ck': 'ck%(table_name)s%(constraint_name)s',
    'fk': 'fk%(table_name)s%(all_column_names)s%(referred_table_name)s',
    'pk': 'pk%(table_name)s'
}

metadata = MetaData(naming_convention=convention)

urls = Table(
    'urls', metadata,
    Column('id', BigInteger, primary_key=True),
    Column('short_url', String(10), nullable=False, unique=True),
    Column('long_url', String(2048), nullable=False),
    Column('created_at', DateTime, default=func.now(), onupdate=func.now()),
    Index('idx_short_url', 'short_url', unique=True)
)
