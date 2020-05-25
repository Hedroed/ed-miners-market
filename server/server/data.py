from .models import Base, Market, CommodityMaxPrice

import csv
import time
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy.sql import func


ONE_DAY_SECOND = 24 * 60 * 60
PRE_LOOP_SECOND = 15 * 60 * 60

INARA_URL = "https://inara.cz/galaxy-commodity/%d"

def get_loop_timestamp(timestamp):
    shifted_ts = timestamp - PRE_LOOP_SECOND
    time_in_day = shifted_ts % ONE_DAY_SECOND
    return shifted_ts - time_in_day


class CommodityMapping():

    def __init__(self, path='./inara_commodities_map.csv'):

        self.mapping_to_name = {}
        self.mapping_to_id = {}

        with open(path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.mapping_to_id[row['commodity_name']] = int(row['commodity_id'])
                self.mapping_to_name[int(row['commodity_id'])] = row['commodity_name']

    def to_name_safe(self, id_):
        return self.mapping_to_name.get(id_, "Not Found")
    
    def to_id_safe(self, name):
        return self.mapping_to_id.get(name, 0)

class DataManager():

    def __init__(self, db_path, mapping_path):
        self.engine = create_engine(db_path, echo=False)
        Base.metadata.create_all(self.engine)

        self.session_factory = sessionmaker(bind=self.engine)

        self.mapping = CommodityMapping(path=mapping_path)

    def get_session(self):
        return self.session_factory()


    def get_commodity_prices(self, commodity_id, timestamp=None, limit=10):
        if timestamp is None:
            to_ts = get_loop_timestamp(int(time.time()))
        else:
            to_ts = get_loop_timestamp(timestamp)

        from_ts = to_ts - ONE_DAY_SECOND

        session = self.get_session()

        """
        select b.commodity_id, b.market_id, c.system, c.station, a.sell_price, datetime(b.last_ts, 'unixepoch'), datetime(a.updated, 'unixepoch')
        from commoditiesMaxPrice a, (
            select commodity_id, market_id, max(timestamp) as last_ts
            from commoditiesMaxPrice
            where timestamp > 1589414400 and timestamp <= 1589500800 and commodity_id = 144
            group by commodity_id, market_id
        ) b,
        markets c
        where a.commodity_id = b.commodity_id and a.market_id = b.market_id and a.timestamp = b.last_ts and a.market_id = c.id
        order by sell_price;
        """

        last_updated = session.query(CommodityMaxPrice.commodity_id, CommodityMaxPrice.market_id, func.max(CommodityMaxPrice.timestamp).label("max_timestamp")).filter(CommodityMaxPrice.commodity_id==commodity_id, CommodityMaxPrice.timestamp>from_ts, CommodityMaxPrice.timestamp<=to_ts).group_by(CommodityMaxPrice.commodity_id, CommodityMaxPrice.market_id).subquery()
        
        res = session.query(CommodityMaxPrice).join(last_updated,and_(CommodityMaxPrice.commodity_id==last_updated.c.commodity_id, CommodityMaxPrice.market_id==last_updated.c.market_id, CommodityMaxPrice.timestamp==last_updated.c.max_timestamp)).order_by(CommodityMaxPrice.sell_price.desc()).limit(limit).all()

        return [
            {
                "price": p.sell_price,
                "demand": p.sell_demand,
                "date": p.updated or p.timestamp,
                "commodity": {
                    "id": p.commodity_id,
                    "name": self.mapping.to_name_safe(p.commodity_id),
                    "inaraLink": INARA_URL % p.commodity_id
                },
                "market": {
                    "id": p.market.id,
                    "system": p.market.system,
                    "station": p.market.station,
                },
            } for p in res
        ]

    def get_commodity_max_prices(self, commodity_id, days=30):
        session = self.get_session()

        """
        select *
        from commoditiesMaxPrice a, (
            select timestamp, max_price, max(sell_demand) as max_demand from (
                select b.timestamp, max_price, sell_demand from commoditiesMaxPrice a, (
                    select timestamp, max(sell_price) as max_price from commoditiesMaxPrice group by timestamp
                ) b
                where a.timestamp = b.timestamp and max_price = sell_price
            ) group by timestamp, max_price
        ) b, markets m
        where sell_price = max_price and sell_demand = max_demand and a.timestamp = b.timestamp and a.market_id = m.id
        order by timestamp desc
        limit 30
        ;

        select *
        from (
            select *, row_number() over (partition by timestamp order by sell_price desc, sell_demand desc) as num
            from commoditiesMaxPrice
            where commodity_id = 144
            ), markets
        where num=1 and id=market_id
        order by timestamp desc
        limit 30
        ;
        """

        ordered_by_loop = session.query(CommodityMaxPrice, func.row_number().over(partition_by=CommodityMaxPrice.timestamp, order_by=(CommodityMaxPrice.sell_price.desc(), CommodityMaxPrice.sell_demand.desc())).label("num")).filter_by(commodity_id=commodity_id).subquery()

        res = session.query(CommodityMaxPrice).select_entity_from(ordered_by_loop).filter(ordered_by_loop.c.num <= 1).all()

        return [
            {
                "price": p.sell_price,
                "demand": p.sell_demand,
                "date": p.timestamp,
                "commodity": {
                    "id": p.commodity_id,
                    "name": self.mapping.to_name_safe(p.commodity_id),
                    "inaraLink": INARA_URL % p.commodity_id
                },
                "market": {
                    "id": p.market.id,
                    "system": p.market.system,
                    "station": p.market.station,
                },
            } for p in res
        ]

    def get_makets(self, limit=10):
        session = self.get_session()

        return session.query(Market).limit(limit).all()
    
    def get_maket(self, id_):
        session = self.get_session()

        return session.query(Market).filter_by(id=id_).first()

    def get_commodities(self, limit=10):
        return [
            {
                "id": id_,
                "name": name,
                "inaraLink": INARA_URL % id_
            } for id_, name in self.mapping.mapping_to_name.items()
        ]
    
    def get_commodity(self, id_):
        name = self.mapping.to_name_safe(id_)
        return {
            "id": id_,
            "name": name,
            "inaraLink": INARA_URL % id_
        }
