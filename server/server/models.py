#!/bin/env python

from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

import time

Base = declarative_base()

class Market(Base):
    __tablename__ = "markets"

    id = Column(BigInteger, primary_key=True)
    system = Column(String(256))
    station = Column(String(256))

    commodities = relationship("CommodityMaxPrice", back_populates="market")

    def __repr__(self):
        return "<Market(id='%s', system='%s', station='%s')>" % (self.id, self.system, self.station)


class CommodityMaxPrice(Base):
    __tablename__ = "commodities"

    commodity_id = Column(Integer, primary_key=True)
    sell_price = Column(Integer)
    sell_demand = Column(Integer)
    timestamp = Column(BigInteger, primary_key=True)
    updated = Column(BigInteger)
    reports = Column(BigInteger, nullable=False, default=0)

    market_id = Column(BigInteger, ForeignKey('markets.id'), primary_key=True)
    market = relationship("Market", back_populates="commodities")

    def __repr__(self):
        return "<CommodityMaxPrice(commodity_id='%s', sell_price='%s', sell_demand='%s', date='%s', market=%s)>" % (self.commodity_id, self.sell_price, self.sell_demand, self.timestamp, self.market)
