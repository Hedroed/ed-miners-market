#!/bin/env python

from sqlalchemy import create_engine, Column, BigInteger, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

import time

Base = declarative_base()

# class CommodityPrice(Base):
#     __tablename__ = "commoditiesPrice"

#     id = Column(Integer, primary_key=True)
#     commodity_id = Column(Integer)
#     sell_price = Column(Integer)
#     sell_demand = Column(Integer)
#     timestamp = Column(BigInteger)

#     market_id = Column(BigInteger, ForeignKey('markets.id'))
#     market = relationship("Market")

#     def __repr__(self):
#         return "<CommodityPrice(commodity_id='%s', system='%s', station='%s', date='%s', market=%s)>" % (self.commodity_id, self.sell_price, self.sell_demand, self.timestamp, self.market)


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


if __name__ == "__main__":
    engine = create_engine('sqlite:///data/trader.test.db', echo=True)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    session = Session()


    commodity_id = 144
    system='Sol'
    station='Galileo'
    market_id=26
    
    timestamp=1
    price = 160000
    demand = 25201


    entry = session.query(CommodityMaxPrice).filter_by(commodity_id=commodity_id, timestamp=timestamp, market_id=market_id).first()
    print(entry)

    if entry is None:

        test_market = Market(id=market_id, system=system, station=station)
        test_commodity = CommodityMaxPrice(commodity_id=commodity_id, sell_price=price, sell_demand=demand, timestamp=timestamp, market=test_market)
        session.merge(test_commodity)

    else:
        if entry.market is None:
            entry.market = Market(id=market_id, system=system, station=station)


        if price > entry.sell_price:
            entry.sell_price = price
        
        if demand > entry.sell_demand:
            entry.sell_demand = demand

        session.merge(entry)

    session.commit()
