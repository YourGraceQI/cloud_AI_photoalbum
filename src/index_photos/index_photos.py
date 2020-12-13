from __future__ import print_function
import json
import boto3
import requests
from elasticsearch import Elasticsearch, RequestsHttpConnection


def connectES(esEndPoint):
 print ('Connecting to the ES Endpoint {0}'.format(esEndPoint))
 try:
  esClient = Elasticsearch(
   hosts=[{'host': esEndPoint, 'port': 443}],
   use_ssl=True,
   verify_certs=True,
   connection_class=RequestsHttpConnection)
  return esClient
 except Exception as E:
  print("Unable to connect to {0}".format(esEndPoint))
  print(E)
  exit(3)

def createIndex(esClient):
 try:
  res = esClient.indices.exists('metadata-store')
  print("Index Exists ... {}".format(res))
  if res is False:
   esClient.indices.create('metadata-store', body="photos")
   return 1
 except Exception as E:
  print("Unable to Create Index {0}".format("metadata-store"))
  print(E)
  exit(4)

def getLabels(bucket,photo):
    client=boto3.client('rekognition')
    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=12)

    print('Detected labels for ' + photo)
    labels = []
    for label in response['Labels']:
        print ("Label: " + label['Name'])
        labels.append(label['Name'])
    return labels

def lambda_handler(event, context):
    # TODO implement
    bucket = event['Records'][0]['s3']['bucket']['name']
    time = event['Records'][0]['eventTime']
    objectKey = event['Records'][0]['s3']['object']['key']
    labels = getLabels(bucket,objectKey)
    imgInfo = {
        "objectKey":objectKey,
        "bucket":bucket,
        "createdTimestamp":time,
        "labels":labels
    }
    imgInfo = json.dumps(imgInfo)
    headers = { "Content-Type": "application/json" }
    endPoint = "search-photo-storage-3gex4uqz77gf2abn5bvis25ilm.us-east-1.es.amazonaws.com"
    #r = requests.post(headers = headers,"https://search-photo-storage-3gex4uqz77gf2abn5bvis25ilm.us-east-1.es.amazonaws.com/post", data=imgInfo)
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

