
All in WSL

1/ etcd server setup
======================
 - with current scrip docker-etcd-setup.sh, run:  bash docker-etcd-setup.sh 
 - will create the etcd server to keep key/value storage (payments in AGIX) 
 - check that it works
   * go in dir /var/lib/etcd/cfssl
   * run:  curl --cacert ./ca.pem --cert ./client.pem --key ./client-key.pem "https://172.18.207.5:2379/health"  
   * should return {"health":"true","reason":""} 

 - to run it again: bash create_etcd_node.sh
 - to check logs: docker logs docker-etcd-node-1
 - to check health (no dir change) : curl --cacert /var/lib/etcd/cfssl/ca.pem --cert /var/lib/etcd/cfssl/client.pem --key /var/lib/etcd/cfssl/client-key.pem "https://172.18.207.5:2379/health"  

2/ install SNET CLI
======================
 - installing Anaconda3 for managing Python envs (came with a default Python 3.11.5)
 - add to do this change : pip3 install   clyent==1.2.1
 - then this: pip3 install  requests_mock
 - then run this was OK :  pip3 install -e .
 - quit terminal, run again, and run command:  snet

 - check all orgs in SNET : snet organization list
 - get my orgs info : snet organization info INCUBIQ_ID
 - list my identities (not sure what this is for) : snet identity list 

2b/ install SNET CLI
======================
  (installed a mini conda env)
 - in Python 3.11.5
 - sudo apt install libudev-dev libusb-1.0-0-dev
 - pip install snet-cli


 - check all orgs in SNET : snet organization list
 - get my orgs info : snet organization info INCUBIQ_ID
 - list my identities (not sure what this is for) : snet identity list 


3/ setup Orgs
======================
 - was OK following doc
 - except MAKE SURE all http:// are in fact https:// ...

 => identity : OSAIS
 => org : INCUBIQ_ID
  
   - snet identity create INCUBIQ_SEPOLIA key --private-key <PVT-KEY> --network sepolia

 - update metadata : snet organization update-metadata INCUBIQ_ID --metadata-file organization_metadata.json
 - check current metadata : snet organization print-metadata INCUBIQ_ID

4/ create gRPC stubs and run is as service
======================
  - follow doc to create proto file (remove # in files)


  - missing "utility" and "concurrent" py files for the hello world sample ; requested them 
 
  - cd services/osais
  - python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. ./osais.proto  

  - run server: python ./services/sample/server.py
                python ./services/osais/server_to_osais.py
  - run client: python ./services/sample/client.py

5/ Publish a service to SNET
======================
  - snet service metadata-init     services     "my_test_service_1"     --group-name default_group     --fixed-price 0.00000001     --endpoints http://127.0.0.1:7000
  // tunnel the service: cloudflared tunnel --url http://127.0.0.1:8010
  // replace the "http://127.0.0.1:8010" by the tunnel IP (like "https://recover-rat-title-dem.trycloudflare.com") 
  - snet service metadata-add-description --json '{"description": "Description of my Service.", "url": "https://service.users.guide"}'
  - snet service publish OSAIS_ID SAMPLE_CALL

  // delete service onchain
  - snet service delete OSAIS_ID AI_CALL

  - update a service to SNET :        snet service update-metadata OSAIS_ID AI_CALL --metadata-file service_metadata.json
  - get back the metadata after an update: snet service print-metadata OSAIS_ID AI_CALL
  - get back the published service :  snet sdk generate-client-library python OSAIS_ID SAMPLE_CALL .


6/ Run SNET Daemon
======================
  - cd snet-cli
  - edit and fill up the snetd.config.json  file in the relevant /services/xyz directory
  - run :  ./snetd-linux-amd64-v5.1.2 -c  ../services/sample/snetd.config.json
           ./snetd-linux-amd64-v5.1.2 -c  ../services/osais/snetd.config.json

7/ Call service via SNET
======================

7a/ opening a pre-payment channel
 - snet account deposit 0.000001    # Deposit AGIX Token to MPE. 
 - snet channel open-init INCUBIQ_ID default_group 0.000001 +40days

7b/ making a call
 - conda activate snet
 - snet client call OSAIS_ID SAMPLE_CALL default_group call '{"query":"10", "_type":true}'
 - snet client call OSAIS_ID AI_CALL default_group call '{"ai":"ping", "query":"{width:512, height:512}"}'


 short version after having installed all
============================================

  - run Daemon (1/)
  - run server (4/)
  - call  client via sNet (7b/)


 8/ BUILD THE CLIENT UI
============================================
 
 // taken from here https://github.com/singnet/snet-dapp
 // make sure to have at least 
   yarn version 1.22.21
   node version 18.19.0

// then do a :
 // delete node_modules files and lock files
 - yarn cache clean 
 - yarn install

// to run the dapp:
npm run start

// to finalize config...
// get an Infura dapp key (https://app.infura.io/)

// generate the JS stub of proto files
// in snet-dapp directory, copy the "osais.proto" file from ../services/osais/
//  protoc  --plugin=protoc-gen-ts=./node_modules/.bin/protoc-gen-ts --js_out=import_style=commonjs,binary,namespace_prefix=osais_osais_id_ai_call:. --ts_out=service=grpc-web:. osais.proto
// move those 4 generated JS/TS files into /snet-dapp/src/assets/thirdPartyServices/OSAIS_ID/AI_CALL

// update the .env.sanbox  file
REACT_APP_SANDBOX_SERVICE_ENDPOINT=http://localhost:7001
REACT_APP_SANDBOX_ORG_ID=OSAIS_ID
REACT_APP_SANDBOX_SERVICE_ID=AI_CALL
REACT_APP_WEB3_PROVIDER=wss://sepolia.infura.io/ws/v3/SNET_OSAIS

!! copy .env.sandbox  to  .env  (this is the one read by the dapp)
