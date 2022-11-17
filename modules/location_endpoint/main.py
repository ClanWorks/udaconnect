import time
from concurrent import futures

import grpc
import order_pb2
import order_pb2_grpc


class LocationEPServicer(location_pb2_grpc.LocationEPServiceServicer):
    def Create(self, request, context):

        loc_data = {
            "person_id": int(request.person_id),
            "longitude": request.longitude,
            "latitude": request.latitude,
            "creation_time": request.creation_time,
        }
        print(loc_data)

        return order_pb2.OrderMessage(**request_value)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
order_pb2_grpc.add_OrderServiceServicer_to_server(OrderServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)





  int32 person_id = 1;
  string logitude = 2;
  string latitude = 3;
  google.protobuf.Timestamp creation_time = 4;
