from tkinter import Image
import boto3
import pandas as pd

region="us-east-1"
bucket="iris-rekognition"
min_confidence = 80
max_labels = 10

def list_objects(bucket,region):
    client=boto3.client('s3', region_name=region)
    response = client.list_objects_v2(
        Bucket=bucket
    )
    object_list = []
    for object in response['Contents']:
        object_list.append(object['Key'])
    return(object_list)

def detect_labels(photo, bucket):
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
    print()
    df = pd.DataFrame(response['Labels'])
    df.to_csv('results.csv', mode='a', index=True, header=True)
    for label in response['Labels']:
        print ("Label: " + label['Name'])
        print ("Confidence: " + str(label['Confidence']) + "%")
        print ("Instances:")
        for instance in label['Instances']:
            print ("    Bounding box")
            print ("       Top: " + str(instance['BoundingBox']['Top']))
            print ("       Left: " + str(instance['BoundingBox']['Left']))
            print ("       Width: " +  str(instance['BoundingBox']['Width']))
            print ("       Height: " +  str(instance['BoundingBox']['Height']))
            print ("  Confidence: " + str(instance['Confidence']) +"%")
            print()
        print ("Parents:")
        for parent in label['Parents']:
            print ("     " + parent['Name'])
    print ()
    return response['Labels']

def main():
    photos = list_objects(bucket, region)
    for photo in photos:
        print ()
        print ("###################"  + " Starting Labels for "  + photo + "###################")
        detect_labels(photo, bucket)
        print ("###################"  + " Ending Labels for "  + photo + "###################")
        print ()

if __name__ == "__main__":
    main()
