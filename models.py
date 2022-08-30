from sqlalchemy import String, Float, Column, Integer, Date, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Price(Base):
    __tablename__ = 'prices'

    ticker = Column(String(128))
    date = Column(Date)
    variable = Column(String(128))
    values = Column(Float)


class Ticker(Base):
    __tablename__ = 'tickers'

    ticker = Column(String(128))
    name = Column(String)
    market = Column(String(128))
    locale = Column(String(128))
    primary_exchange = Column(String(128))
    type = Column(String(128))
    active = Column(Boolean)
    currency_name = Column(String(128))
    cik = Column(String(128))
    composite_figi = Column(String(128))
    share_class_figi = Column(String(128))
    market_cap = Column(Float)
    phone_number = Column(String(128))
    description = Column(String)
    sic_code = Column(Integer)
    sic_description = Column(String(128))
    ticker_root = Column(String(128))
    homepage_url = Column(String)
    total_employees = Column(Integer)
    list_date = Column(Date)
    share_class_shares_outstanding = Column(Integer)
    weighted_shares_outstanding = Column(Integer)


class Exchange(Base):
    __tablename__ = 'exchanges'

    id = Column(Integer)
    type = Column(String(128))
    asset_class = Column(String(128))
    locale = Column(String(128))
    name = Column(String)
    acronym = Column(String(128))
    mic = Column(String(128))
    operating_mic = Column(String(128))
    participant_id = Column(String(128))
    url = Column(String)