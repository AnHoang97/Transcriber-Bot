import boto3
import os
import uuid
import time
import json
from urllib.parse import urlparse


def move_file_to_bucket(file_dir, bucket_name):
    print(f"[BACKEND] move {file_dir} to the bucket {bucket_name}.")
    client = boto3.resource('s3')
    bucket = client.Bucket(bucket_name)
    bucket.upload_file(file_dir, os.path.basename(file_dir))
    return "s3://" + bucket_name + "/" + os.path.basename(file_dir)


def remove_file_from_bucket(key, bucket_name):
    client = boto3.resource('s3')
    bucket = client.Bucket(bucket_name)
    bucket.delete_objects(
        Delete={
            'Objects': [
                {
                    'Key': key,
                },
            ]
        }
    )


def read_and_delete_transcript_from_s3(key, bucket_name):
    print(f"[BACKEND] Read json file {key} from the bucket {bucket_name}.")
    client = boto3.client('s3')
    result = client.get_object(Bucket=bucket_name, Key=key)
    response = json.loads(result["Body"].read().decode())
    client.delete_object(Bucket=bucket_name, Key=key)
    return response['results']['transcripts'][0]['transcript']


def transcribe_file(file_dir, bucket_name, language="en-US"):
    job_name = str(uuid.uuid4())
    print(
        f"[BACKEND] Start the transcript job {job_name} with the file from {file_dir}.")

    voice_file_uri = move_file_to_bucket(file_dir, bucket_name)

    client = boto3.client('transcribe', region_name="eu-central-1")
    response = client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=language,
        MediaFormat='ogg',
        Media={
            'MediaFileUri': voice_file_uri,
        },
        OutputBucketName=bucket_name
    )

    while True:
        status = client.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        time.sleep(1)

    transcript = read_and_delete_transcript_from_s3(
        job_name + ".json", bucket_name)

    p = urlparse(voice_file_uri, allow_fragments=False)
    remove_file_from_bucket(p.path[1:], p.netloc)
    return transcript
