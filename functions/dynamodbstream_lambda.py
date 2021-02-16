import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns_topic = os.getenv("SNS_TOPIC_ARN", None)
ec2 = boto3.client('ec2')
sns = boto3.client('sns')

def send_message(sns_subject, message):
    sns.publish(Subject = sns_subject, Message = message, TopicArn = sns_topic)

def handler(event, context):
    if not sns_topic:
        logging.warn("SNS Arn is not specified")
    sns_subject = ""
    sns_message = ""
    try:
        for record in event['Records']:
            if record['eventName'] == 'REMOVE':
                instance_id =  record['dynamodb']['Keys']['InstanceId']['S']
                termination_date = record['dynamodb']['OldImage']['AutoTerminationDate']['N']
                if instance_id and termination_date:
                    response = ec2.terminate_instances(InstanceIds=[instance_id])
                    logging.info(f'instance {instance_id} is terminating...')
                    sns_subject = "Terminating instance "+ str(instance_id)
                    sns_message = str(response)
                elif not termination_date:
                    sns_subject = "Remove item from DynamoDB but not terminating the instance"
                    sns_message = str(record)
                else:
                    sns_subject = "Instance or termination date not valid"
                    sns_message = str(record)
                send_message(sns_subject, sns_message)        
                logging.info(f'Sending out email through topic {sns_topic}')
    except Exception as e:
        print(e)
        raise e

