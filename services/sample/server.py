## Importing the necessary libraries of the service ##
import time
import logging
import argparse
from concurrent import futures
 
## Importing grpc and auto generated files ##
import grpc
import sample_pb2
import sample_pb2_grpc
 
_ONE_DAY_IN_SECONDS = 60 * 60 * 24
 
## Host and port on which the server listens ##
parser = argparse.ArgumentParser(description='')
parser.add_argument("--host", type=str, default="0.0.0.0",  help= "host" )
parser.add_argument("--port", type=int, default=8010,  help= "port" )
args = parser.parse_args()


class Model():
    def __init__(self):
        pass

    def predict(self, q, t):
        return "result1", "result2", "result3"


## Creating a class inherited from <name>Servicer (ExampleServicer) from Example_pb2_grpc ##
class ExampleServicer(sample_pb2_grpc.ExampleServicer):
    def __init__(self):
        self.model = Model()

    ## Redefining the main method from proto, which will be called ##
    ## Accepts and returns the corresponding structures defined in the proto file ##
    def call(self, request, context):
        try:
            query = request.query
            _type = request._type
            result, result2, result3 = self.model.predict(query, _type)
            print(result, result2, result3)
        except Exception as e:
            print("Error: {}".format(e))
            raise Exception("Error: {}".format(e))
        return sample_pb2.Answer(answer=result, answer2=result2, answer3=result3)
 
## Replacing Example with the desired <name> ##
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sample_pb2_grpc.add_ExampleServicer_to_server(ExampleServicer(), server)
    server.add_insecure_port('{}:{}'.format(args.host, args.port))
    server.start()
    print('Server start')
 
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
 
if __name__ == '__main__':
    logging.basicConfig()
    serve()