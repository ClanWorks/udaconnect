import logging
import psycopg2
import os

from json import loads
from kafka import KafkaConsumer
from geoalchemy2.functions import ST_AsText, ST_Point
from locSchema import LocationSchema
from typing import Dict

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("uda-location-service")

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

TOPIC_NAME = "uda-location"
KAFKA_SERVER = "kafka-service:9092"


def location_to_database():
  logger.warning('Entering location to database')
  kcons = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER])

  logger.warning('kcons created')

  for itm in kcons:

    logger.warning('starting for loop')

    loc_data = itm.value.decode('utf-8')

    logger.warning(f'loc data created: {loc_data}')

    loc_dict = loads(loc_data)

    logger.warning(f'loc_dict created: {loc_dict}')

    validation_results: Dict = LocationSchema().validate(loc_dict)
    if validation_results:
      logger.warning(f"Unexpected data format in payload: {validation_results}")
      raise Exception(f"Invalid payload: {validation_results}")
  
    logger.warning('Validation cleared')

    pid = int(loc_dict['person_id'])
    lon = float(loc_dict['longitude'])
    lat = float(loc_dict['latitude'])
    ctm = loc_dict['creation_time']

    logger.warning(f'Location variables created: {pid}, {lon}, {lat}, {ctm}')

    # https://www.psycopg.org/docs/module.html   
    db_con = psycopg2.connect(
      dbname = DB_NAME,
      user = DB_USERNAME,
      password = DB_PASSWORD,
      host = DB_HOST,
      port = DB_PORT
    )

    logger.warning('db_con created')

    # For geodetic coordinates, first is longitude and second is latitude
    sql_statement = f"INSERT INTO public.location (id, person_id, coordinate, creation_time) values (DEFAULT, {pid}, ST_Point({lon}, {lat}), '{ctm}');"

    logger.warning(f'sql: {sql_statement}')

    # https://www.psycopg.org/docs/usage.html
    # Open a cursor to perform database operations
    cur = db_con.cursor()
    try:
      # Execute a query
      cur.execute(sql_statement)
    except Exception as e:
      logger.error(f"Location not saved: {e}")
    db_con.commit() 
    # Make the changes to the database persistent
    db_con.commit()
    # Close communication with the database
    cur.close()
    db_con.close()
    
    logger.warning('db_con closed')

if __name__ == "__main__":
  location_to_database()


