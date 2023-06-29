import boto3
import os

BUCKET = 'redial'
s3 = boto3.client('s3')

s3_res = boto3.resource("s3")
bucket = s3_res.Bucket(BUCKET)

def create_dir(dir_name):
    if not os.path.exists(dir_name):
            os.makedirs(dir_name)

def get_object(key):
    s3.download_file(Bucket= BUCKET, Key = key, Filename = key)

def get_dir(dir_name):
    create_dir(dir_name)
    for s3_object in bucket.objects.filter(Prefix=dir_name):
        print(s3_object.key)
        bucket.download_file(s3_object.key, s3_object.key)

def get_dir_objs(dir_name):
    create_dir(dir_name)
    print("called here " + dir_name)
    objs = []
    for s3_object in bucket.objects.filter(Prefix = dir_name):
        print(s3_object.key)
        objs.append([s3.get_object(Bucket = BUCKET, Key = s3_object.key)['Body'].read(), s3_object.key])
    return objs

def get_obj(key):
    print("get obj called")
    return s3.get_object(Bucket = BUCKET, Key= key)['Body'].read()