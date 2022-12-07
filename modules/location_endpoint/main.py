import time
from concurrent import futures
from kafka import KafkaProducer

import os 
import json
import grpc
import location_pb2
import location_pb2_grpc

# The Kafka producer
# https://kafka.apache.org/23/javadoc/index.html?org/apache/kafka/clients/producer/KafkaProducer.html

def kafka_message(msg):
  # TOPIC_NAME = os.environ["TOPIC_NAME"]
  # KAFKA_SERVER = os.environ["KAFKA_SERVER"]

  TOPIC_NAME = "uda-location"
  KAFKA_SERVER = "kafka-service:9092"

  kprod = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
  kafka_data = json.dumps(msg).encode()
  kprod.send(TOPIC_NAME, kafka_data)
  print("Location data sent")

# Location EP Servicer class
class LocationEPServicer(location_pb2_grpc.LocationEPServiceServicer):
  def Create(self, request, context):

    loc_data = {
      "person_id": int(request.person_id),
      "longitude": request.longitude,
      "latitude": request.latitude,
      "creation_time": request.creation_time,
    }

    kafka_message(loc_data)

    return location_pb2.LocationEPMessage(**loc_data)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationEPServiceServicer_to_server(LocationEPServicer(), server)

print("Server starting on port 5070...")
server.add_insecure_port("[::]:5070")
server.start()
# Keep thread alive
try:
  while True:
    time.sleep(86400)
except KeyboardInterrupt:
  server.stop(0)


