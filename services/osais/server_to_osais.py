## Importing the necessary libraries of the service ##
import time
import logging
import argparse
import requests
import re
import json
from concurrent import futures
 
## Importing grpc and auto generated files ##
import grpc
import osais_pb2
import osais_pb2_grpc
 
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

HOST = "0.0.0.0"
PORT = 8011
OSAIS_PRIVATE='https://opensourceais.com/api/v1/private/'  
OSAIS_PUBLIC='https://opensourceais.com/api/v1/public/'  
OSAIS_TOKEN = "908bba88d90a98efbad0d641c5905a83daeae82cc5750eead2dd83a743c7e134"
OSAIS_SECRET = "b8b04fc31a4cee6058c8679b9a823f04aeed56dc6f41d3ebc2a27e2bb7789beb"

## authentication token (as global)
authToken=None
 
## Host and port on which the server listens ##
parser = argparse.ArgumentParser(description='')
parser.add_argument("--host", type=str, default=HOST,  help= "host" )
parser.add_argument("--port", type=int, default=PORT,  help= "port" )
args = parser.parse_args()

def fix_json_string(query):
    # Regex to find property names not wrapped in double quotes
    pattern = r'(?<!")(\b\w+\b)(?=\s*:)'
    # Add double quotes around the property names
    fixed_query = re.sub(pattern, r'"\1"', query)
    return fixed_query

class Model():
    def __init__(self):
        pass

    ## Call into OSAIS with AI and Query params 
    ## Will return a UID if call was processed
    def callAI(self, query, ai):

        # Decode the JSON string query into a Python dictionary
        try:
            fixed_query = fix_json_string(query)
            decoded_json = json.loads(fixed_query)
            keys = decoded_json.keys()
        except json.JSONDecodeError as e:
            print("Failed to decode QUERY:", e)
            return "Bad params for ai "+ai 

        # call OSAIS here
        url = OSAIS_PRIVATE+'client/ai/'+ai  

        # process params
        data = {}
        for key in decoded_json.keys():
            data[key]=decoded_json[key]

        data = {
            "witdh": 400,
            "height": 400
        }
        json_string = json.dumps(data)
        print("will pass QUERY:", json_string)

        # auth header
        headers = {
            'Authorization': 'Bearer '+authToken,
            'Content-Type': 'application/x-www-form-urlencoded',
            'charset': "UTF-8"
        }

        response = requests.post(url, data=data, headers=headers)

        # Check the status code and content of the response
        if response.status_code == 201:
            response_json = json.loads(response.content)
            msg='Acknowledged, processing with UID: '+ str(response_json["data"]["uid"])
            return msg
        else:
            print(response.request.body)
            print('Failed:', response.status_code, response.content)
            return "Could not process request for ai "+ai 

## from grpc to rest ; process in / out of an OSAIS AI call
class postOSAISServicer(osais_pb2_grpc.postOSAISServicer):
    def __init__(self):
        self.model = Model()

    ## Redefining the main method from proto, which will be called ##
    ## Accepts and returns the corresponding structures defined in the proto file ##
    def call(self, request, context):
        try:
            query = request.query
            ai = request.worker
            print("calling "+ai + " with params :"+query )
            result = self.model.callAI(query, ai)
            print(result)
        except Exception as e:
            print("Error: {}".format(e))
            raise Exception("Error: {}".format(e))
        return osais_pb2.Answer(answer=result)

## to authenticate into OSAIS
def authenticate():
    global authToken
    url = OSAIS_PUBLIC+'client/login'  
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'charset': "UTF-8"
    }

    response = requests.post(url, data={
        'token': OSAIS_TOKEN,
        'secret': OSAIS_SECRET
    }, headers=headers)

    if response.status_code == 201:
        decoded_json = json.loads(response.content)
        authToken = decoded_json["data"]["authToken"]
        print("Authenticated into OSAIS with authToken "+authToken)
        return True

    print('Failed:', response.status_code, response.content)
    return False

## run server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    osais_pb2_grpc.add_postOSAISServicer_to_server(postOSAISServicer(), server)
    server.add_insecure_port('{}:{}'.format(args.host, args.port))
    server.start()
    print('OSAIS Server started')
    authenticate()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
 
if __name__ == '__main__':
    logging.basicConfig()
    serve()