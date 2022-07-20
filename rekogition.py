from tkinter import Image
import boto3

region="us-east-1"
bucket="dummy-rekognition"
profile_name = "jaweed"
min_confidence = 80
max_labels = 10

def list_objects(bucket,region):
    boto3.setup_default_session(profile_name = profile_name)
    client=boto3.client('s3', region_name=region)
    response = client.list_objects_v2(
        Bucket=bucket
    )
    object_list = []
    for object in response['Contents']:
        object_list.append(object['Key'])
    return(object_list)


def detect_labels(photo, bucket):
    boto3.setup_default_session(profile_name=profile_name)
    client=boto3.client('rekognition', region_name = region)
    response=client.detect_labels(
        Image = {
            'S3Object':
        {
            'Bucket': bucket,
            'Name': photo,
            }
        },
		MaxLabels = max_labels,
		MinConfidence = min_confidence,
        )
    print('Detected labels for ' + photo)
    print()
    for label in response['Labels']:
        print ("Label: " + label['Name'])
        print ("Confidence: " + str(label['Confidence']))
        print ("Instances:")
        for instance in label['Instances']:
            print ("  Bounding box")
            print ("      Top: " + str(instance['BoundingBox']['Top']))
            print ("      Left: " + str(instance['BoundingBox']['Left']))
            print ("      Width: " +  str(instance['BoundingBox']['Width']))
            print ("      Height: " +  str(instance['BoundingBox']['Height']))
            print ("  Confidence: " + str(instance['Confidence']))
            print()
        print ("Parents:")
        for parent in label['Parents']:
            print ("   " + parent['Name'])
        print ("###################" + 'END labels for ' + photo("###################")
        print ()
    return len(response['Labels'])


photos = list_objects(bucket, region)

for photo in photos:
    detect_labels(photo, bucket)

