#!/bin/env python

from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

import time

Base = declarative_base()

class Market(Base):
    __tablename__ = "markets"

    id = Column(BigInteger, primary_key=True)
    system = Column(String)
    station = Column(String)

    commodities = relationship("CommodityPrice")

    def __repr__(self):
        return "<Market(id='%s', system='%s', station='%s')>" % (self.id, self.system, self.station)


class CommodityPrice(Base):
    __tablename__ = "commoditiesPrice"

    id = Column(Integer, primary_key=True)
    commodity_id = Column(Integer)
    sell_price = Column(Integer)
    sell_demand = Column(Integer)
    timestamp = Column(BigInteger)

    market_id = Column(BigInteger, ForeignKey('markets.id'))
    market = relationship("Market")

    def __repr__(self):
        return "<CommodityPrice(commodity_id='%s', sell_price='%s', sell_demand='%s', date='%s', market=%s)>" % (self.commodity_id, self.sell_price, self.sell_demand, self.timestamp, self.market)


class CommodityMaxPrice(Base):
    __tablename__ = "commoditiesMaxPrice"

    commodity_id = Column(Integer, primary_key=True)
    sell_price = Column(Integer)
    sell_demand = Column(Integer)
    timestamp = Column(BigInteger, primary_key=True)
    updated = Column(BigInteger)

    market_id = Column(BigInteger, ForeignKey('markets.id'), primary_key=True)
    market = relationship("Market")

    def __repr__(self):
        return "<CommodityMAXPrice(commodity_id='%s', sell_price='%s', sell_demand='%s', date='%s', market=%s)>" % (self.commodity_id, self.sell_price, self.sell_demand, self.timestamp, self.market)

