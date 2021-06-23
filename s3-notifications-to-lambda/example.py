import boto3 
from zipfile import ZipFile

s3 = boto3.resource('s3')
bucket = s3.Bucket('<bucket name defined from cloudformation template>')

# Create zip file
zipCode = ZipFile('index.zip','w')
# Add files into zip file
zipCode.write('index.py')
zipCode.close()


# Add zip code into s3
bucket.upload_file('./index.zip', 'zipCode.zip')


