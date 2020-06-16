import zlib
import zmq
import json
import sys
import time
import dateutil.parser
import csv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from sqlmodel import Base, Market, CommodityPrice

EDDN_RELAY = 'tcp://eddn.edcd.io:9500'
EDDN_TIMEOUT = 600000 # 5 min


AUTHORISED_SOFTWARES = [
    "E:D Market Connector",
    "EDDiscovery",
    "EDDI",
    "EDCE",
    "ED-TD.SPACE",
    "EliteOCR",
    "Maddavo's Market Share",
    "RegulatedNoise",
    "RegulatedNoise__DJ"
]
EXCLUDED_SOFTWARES = []

WHITELISTED_COMMODITIES = [
    'lowtemperaturediamond',
    'opal',
    'painite',
]


commodities_mapping = {}
with open('./inara_commodities_map.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        commodities_mapping[row['commodity_name']] = int(row['commodity_id'])

def convert_commodity_v1_to_v3(d):
    return {
        '$schemaRef': 'https://eddn.edcd.io/schemas/commodity/3',
        'header': d['header'],
        'message': {
            'systemName': d['message']['systemName'],
            'stationName': d['message']['stationName'],
            'timestamp': d['message']['timestamp'],
            'commodities' : [{
                'name': d['message'].get('itemName', None),
                'buyPrice': d['message'].get('buyPrice', None),
                'stock': d['message'].get('stationStock', None),
                'stockBracket': d['message'].get('supplyLevel', None),
                'sellPrice': d['message'].get('sellPrice', None),
                'demand': d['message'].get('demand', None),
                'demandBracket': d['message'].get('demandLevel', None),
            }]
        }
    }


def print_commodities(data):
    excluded = data['header']['softwareName'] in EXCLUDED_SOFTWARES

    print('    - Software: %s / %s' % (data['header']['softwareName'], data['header']['softwareVersion']))
    print('        - %s' % ('EXCLUDED' if excluded else 'UNEXCLUDED' ))

    if not excluded:

        print('    - Timestamp: %s ' % data['message']['timestamp'])
        print('    - Uploader ID: %s ' % data['header']['uploaderID'])
        print('        - System Name: %s ' % data['message']['systemName'])
        print('        - Station Name: %s ' % data['message']['stationName'])
        print('        - Market ID: %s ' % data['message']['marketId'])

        for commodity in data['message']['commodities']:
            if commodity['name'].lower() == "lowtemperaturediamond":
            # if commodity['name'] in WHITELISTED_COMMODITIES:
                print('            - Name: %s' % commodity['name'])
                print('                - Mean Price: %s' % commodity['meanPrice'])
                print('                - Buy Price: %s' % commodity['buyPrice'])
                print('                - Stock: %s (level: %s)' % (commodity['stock'], commodity['stockBracket']))
                print('                - Sell Price: %s' % commodity['sellPrice'])
                print('                - Demand: %s (level: %s)' % (commodity['demand'], commodity['demandBracket']))


def commodity_name_to_id(commodity_name):
    return commodities_mapping[commodity_name]


def save_commodities(data, session):

    excluded = data['header']['softwareName'] in EXCLUDED_SOFTWARES
    if not excluded:

        ts = dateutil.parser.isoparse(data['message']['timestamp'])

        system = data['message']['systemName']
        station = data['message']['stationName']
        market = data['message']['marketId']

        market_obj = Market(id=market, system=system, station=station)

        for commodity in data['message']['commodities']:
            name = commodity['name'].lower()
            if name in WHITELISTED_COMMODITIES:
                commodity_id = commodity_name_to_id(name)
                sell = commodity['sellPrice']
                mean = commodity['meanPrice']

                if sell > mean:
                    demand = commodity['demand']

                    commodity_obj = CommodityPrice(commodity_id=commodity_id, sell_price=sell, sell_demand=demand, timestamp=int(ts.timestamp()), market=market_obj)
                    session.merge(commodity_obj)


def main():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    
    subscriber.setsockopt(zmq.SUBSCRIBE, b"")
    subscriber.setsockopt(zmq.RCVTIMEO, EDDN_TIMEOUT)

    engine = create_engine('sqlite:///data/trader.db', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

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
                
                # Handle commodity
                if data['$schemaRef'].startswith('https://eddn.edcd.io/schemas/commodity/'):
                    # print(data)

                    # Handle version
                    # if data['$schemaRef'][-1] == '1':
                    #     print('Receiving commodity-v1 message...')
                    #     print('    - Converting to v3...')
                    
                    #     data = convert_commodity_v1_to_v3(data)
                    #     print_commodities(data)

                    if data['$schemaRef'][-1] == '3':
                        # print_commodities(data)

                        session = Session()
                        save_commodities(data, session)
                        session.commit()


                    else:
                        print('Unknown version: ' + data['$schemaRef']);


        except zmq.ZMQError as e:
            print('ZMQSocketException: %s' % e)
            subscriber.disconnect(EDDN_RELAY)
            time.sleep(5)

if __name__ == '__main__':
    main()
