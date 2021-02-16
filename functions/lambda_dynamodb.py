import os 
import boto3
import logging
from datetime import datetime
from dateutil import parser
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)


 
table_name = os.getenv("TABLE_NAME", None)
dynamodb_client = boto3.resource('dynamodb', region_name = 'us-east-1')
table = dynamodb_client.Table(table_name)

def write_into_db(instance_id, expiration_date):
    try:
        item = {
            'InstanceId': instance_id,
            'AutoTerminationDate': expiration_date
        }
        table.put_item(Item=item)
        logging.info(f"Write into DynamoDB successfully {str(item)}")
    except Exception as e:
        logging.warning(e)

def get_instance_id(arn):
        instance = arn.split(":")[5]
        instance_id = instance.split("/")[1]
        return instance_id

def check_instance_id_in_db(instance_id):
    response = table.query(
        KeyConditionExpression=Key('InstanceId').eq(instance_id)
    )
    return bool(response)

def convert_date_to_timestamp(date):
    try:
      dt = parser.parse(date)
      timestamp = datetime.timestamp(dt)
    except Exception as e:
      return False 
    else:
      return int(timestamp)

def handler(event, context):
    logging.info(event)
        
    detail = event['detail']
    service = detail['service']
    resource_type = detail['resource-type']
    if service == 'ec2' and resource_type == 'instance':
        resource = event['resources'][0]
        instance_id = get_instance_id(resource)
        if 'changed-tag-keys' and 'tags' in detail:
            changed_tag_keys = event['detail']['changed-tag-keys']
            if 'AutoTerminationDate' in changed_tag_keys:
                tags = event['detail']['tags']
                if 'AutoTerminationDate' in tags.keys():
                    auto_termination_date = tags['AutoTerminationDate']
                    expiration_date = convert_date_to_timestamp(auto_termination_date)
                    if auto_termination_date and expiration_date:
                      write_into_db(instance_id, expiration_date)
                    else:
                      logging.warning("Empty value or invalid datetime input. Make sure using ISO/RFC3399 format datetime")
                else:
                    if check_instance_id_in_db(instance_id):
                        write_into_db(instance_id,0)
                        logging.info("Writing into DynamoDB with 0")
