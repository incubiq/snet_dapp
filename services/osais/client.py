import os
import sys
import time
import random
import logging
import argparse
 
## All names with 'Example' are replaced with the current name of your service ##
## Importing grpc and auto generated files ##
import grpc
import osais_pb2
import osais_pb2_grpc
 
parser = argparse.ArgumentParser()
 
## Host and port on which the server listens ##
parser.add_argument("--host", default="127.0.0.1", type=str, help="host")
parser.add_argument("--port", default=8011, type=int, help="port")
args = parser.parse_args()
 
def OSAISClient(stub):
  s_time = time.time()
  _query = '{"width": 512, "height": 512}'
  _ai = "sdxl"
 
  ## The rpc method defined in the proto file is called, and the required structure is passed to it as input ##
  result = stub.call(osais_pb2.Query(query=_query, ai=_ai))
  r_time = time.time() - s_time
 
  print('\n########################################################################################\n')
  print("{:.3}s\n{}".format(r_time, result.answer))
  print('\n########################################################################################\n')
 
def run():
  with grpc.insecure_channel('{}:{}'.format(args.host, args.port)) as channel:
#  with grpc.insecure_channel('ms-french-dock-hollywood.trycloudflare.com') as channel:
#  with grpc.insecure_channel('0.0.0.0:8010') as channel:
    stub = osais_pb2_grpc.postOSAISStub(channel)
    OSAISClient(stub)
 
if __name__ == '__main__':
  logging.basicConfig()
  run()
