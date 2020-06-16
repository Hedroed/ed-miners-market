import zlib
import zmq
import json
import sys
import time
import dateutil.parser
import csv
from sqlalchemy import create_engine, Column, BigInteger, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()

class Software(Base):
    __tablename__ = "software"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String, unique=True)
    count = Column(Integer)

    schemas = relationship("Schema")

    def __repr__(self):
        return "<Software(id='%s', name='%s', count='%s')>" % (self.id, self.name, self.count)


class Schema(Base):
    __tablename__ = "schemas"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String)
    count = Column(Integer)

    software_id = Column(BigInteger, ForeignKey('software.id'))
    software = relationship("Software")

    def __repr__(self):
        return "<Schema(id='%s', name='%s', count='%s')>" % (self.id, self.name, self.count)


EDDN_RELAY = 'tcp://eddn.edcd.io:9500'
EDDN_TIMEOUT = 600000 # 5 min


def save_stats(data, session):

    soft = data['header']['softwareName']

    schema = data['$schemaRef']

    soft_entry = session.query(Software).filter_by(name=soft).first()

    if soft_entry is None:
        
        new_software = Software(name=soft, count=1)
        session.add(new_software)
        new_schema = Schema(name=schema, count=1, software=soft_entry)
        session.add(new_schema)

    else:
        schema_entry = session.query(Schema).filter_by(software_id=soft_entry.id, name=schema).first()
        
        if schema_entry is None:
            new_schema = Schema(name=schema, count=1, software=soft_entry)
            session.add(new_schema)

        else:
            schema_entry.count += 1
            session.merge(schema_entry)
            soft_entry.count += 1
            session.merge(soft_entry)


def main():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    
    subscriber.setsockopt(zmq.SUBSCRIBE, b"")
    subscriber.setsockopt(zmq.RCVTIMEO, EDDN_TIMEOUT)

    engine = create_engine('sqlite:///data/softwarestats.db', echo=False)
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
                
                session = Session()
                save_stats(data, session)
                session.commit()



        except zmq.ZMQError as e:
            print('ZMQSocketException: %s' % e)
            subscriber.disconnect(EDDN_RELAY)
            time.sleep(5)

if __name__ == '__main__':
    main()
