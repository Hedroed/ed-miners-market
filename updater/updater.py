import zlib
import zmq
import json
import sys
import time
import dateutil.parser
import csv
import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from model import Base, Market, CommodityMaxPrice


ONE_DAY_SECOND = 24 * 60 * 60
PRE_LOOP_SECOND = 14 * 60 * 60

EDDN_RELAY = 'tcp://eddn.edcd.io:9500'
EDDN_TIMEOUT = 600000 # 5 min


#### KNOWN SOFTWARES: ####
#
# "E:D Market Connector"
# "EDDiscovery"
# "EDDI"
# "EDCE"
# "ED-TD.SPACE"
# "EliteOCR"
# "Maddavo's Market Share"
# "RegulatedNoise"
# "RegulatedNoise__DJ"


# Used this to excludes yourself for example has you don't want to handle your own messages ^^
EXCLUDED_SOFTWARES = []


def get_loop_timestamp(timestamp):
    shifted_ts = timestamp - PRE_LOOP_SECOND
    time_in_day = shifted_ts % ONE_DAY_SECOND

    return time_in_day >= 3600, shifted_ts - time_in_day


commodities_mapping = {}
with open('data/inara_commodities_map.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        commodities_mapping[row['commodity_name']] = int(row['commodity_id'])


def save_commodities(data, session):

    excluded = data['header']['softwareName'] in EXCLUDED_SOFTWARES
    if excluded:
        return

    ts = int(dateutil.parser.isoparse(data['message']['timestamp']).timestamp())
    valid, loop_ts = get_loop_timestamp(ts)

    if not valid:
        return

    system = data['message']['systemName']
    station = data['message']['stationName']
    market = data['message']['marketId']

    for commodity in data['message']['commodities']:
        name = commodity['name'].lower()

        if name not in commodities_mapping:
            continue

        commodity_id = commodities_mapping[name]

        price = commodity['sellPrice']
        mean = commodity['meanPrice']

        if price <= mean:
            continue

        demand = commodity['demand']

        entry = session.query(CommodityMaxPrice).filter_by(commodity_id=commodity_id, timestamp=loop_ts, market_id=market).first()

        if entry is None:
            
            market_entry = session.query(Market).filter_by(id=market).first()

            if market_entry is None:
                new_market = Market(id=market, system=system, station=station)
                session.add(new_market)

            new_commodity = CommodityMaxPrice(commodity_id=commodity_id, sell_price=price, sell_demand=demand, timestamp=loop_ts, updated=ts, market_id=market)
            session.add(new_commodity)

        else:
            if entry.market is None:
                session.add(Market(id=market, system=system, station=station))

            if price > entry.sell_price:
                entry.sell_price = price
            
            if price == entry.sell_price and demand > entry.sell_demand:
                entry.sell_demand = demand
            
            if price >= entry.sell_price or demand == entry.sell_demand:
                entry.updated=ts

            session.merge(entry)


def parse_msg(session_factory, data):
    schemaRef = data['$schemaRef']
    if schemaRef.startswith('https://eddn.edcd.io/schemas/commodity/'):
        if schemaRef[-1] == '3':
            session = session_factory()
            save_commodities(data, session)
            session.commit()

        else:
            print('Unknown version: %s' % schemaRef);


def main():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    
    subscriber.setsockopt(zmq.SUBSCRIBE, b"")
    subscriber.setsockopt(zmq.RCVTIMEO, EDDN_TIMEOUT)

    engine = create_engine(os.environ.get('DB_PATH'), echo=True)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    while True:
        try:
            subscriber.connect(EDDN_RELAY)
            
            while True:
                raw_message = subscriber.recv()
                
                if raw_message == False:
                    subscriber.disconnect(EDDN_RELAY)
                    break
                
                message = zlib.decompress(raw_message)
                data = json.loads(message)
                
                parse_msg(session_factory, data)


        except zmq.ZMQError as e:
            print('ZMQSocketException: %s' % e)
            subscriber.disconnect(EDDN_RELAY)
            time.sleep(5)

if __name__ == '__main__':
    main()
