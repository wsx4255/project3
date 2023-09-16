import json

import boto3
# 创建S3存储桶
s3 = boto3.client('s3')
bucket_id = "ronainput"
resp_s3 = s3.create_bucket(Bucket=bucket_id,CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'},)
print("创建S3存储桶: "+str(resp_s3['Location']))
bucket_id2 = "ronaoutput"
resp_s3 = s3.create_bucket(Bucket=bucket_id2,CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'},)
print("创建S3存储桶: "+str(resp_s3['Location']))

# 創建dynamodb
dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
table = dynamodb.create_table(
    TableName='StudentData',
    KeySchema=[
        {
            'AttributeName': 'name',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'name',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)
print("Table status:", table.table_status)

# 輸入student_dat.json
table = dynamodb.Table('StudentData')

with open("student_data.json") as json_file:
    student_data = json.load(json_file)
    for student in student_data:
        id = student['id']
        name = student['name']
        major = student['major']
        year = student['year']

        table.put_item(
           Item={
               'id': id,
               'name': name,
               'major': major,
               'year': year
           }
        )

# 創建ECR
client = boto3.client('ecr')
response = client.create_repository(
    repositoryName='project3'
)
print(response)