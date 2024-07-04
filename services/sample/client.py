import os
import sys
import time
import random
import logging
import argparse
 
## All names with 'Example' are replaced with the current name of your service ##
## Importing grpc and auto generated files ##
import grpc
import sample_pb2
import sample_pb2_grpc
 
parser = argparse.ArgumentParser()
 
## Host and port on which the server listens ##
parser.add_argument("--host", default="127.0.0.1", type=str, help="host")
parser.add_argument("--port", default=8010, type=int, help="port")
args = parser.parse_args()
 
def ExampleClient(stub):
  s_time = time.time()
  query = "some query"
  _type = True
 
  ## The rpc method defined in the proto file is called, and the required structure is passed to it as input ##
  result = stub.call(sample_pb2.Query(query=query, _type=_type))
  r_time = time.time() - s_time
 
  print('\n########################################################################################\n')
  print("{:.3}s\n{}".format(r_time, result.answer))
  print('\n########################################################################################\n')
 
def run():
  with grpc.insecure_channel('{}:{}'.format(args.host, args.port)) as channel:
#  with grpc.insecure_channel('ms-french-dock-hollywood.trycloudflare.com') as channel:
#  with grpc.insecure_channel('0.0.0.0:8010') as channel:
    stub = sample_pb2_grpc.ExampleStub(channel)
    ExampleClient(stub)
 
if __name__ == '__main__':
  logging.basicConfig()
  run()
