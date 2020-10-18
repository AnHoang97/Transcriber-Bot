import boto3
import os
import uuid
import time
import json
import logging


def move_file_to_bucket(file_dir: str, bucket_name: str) -> str:
    logging.info(f"Move {file_dir} to the bucket {bucket_name}.")
    client = boto3.resource('s3')
    bucket = client.Bucket(bucket_name)
    bucket.upload_file(file_dir, os.path.basename(file_dir))
    # return "s3://" + bucket_name + "/" + os.path.basename(file_dir)
    return os.path.basename(file_dir)


def remove_file_from_bucket(key: str, bucket_name: str) -> None:
    client = boto3.resource('s3')
    bucket = client.Bucket(bucket_name)
    bucket.delete_objects(
        Delete={ 'Objects': [
                {
                    'Key': key,
                },
            ]
        }
    )


def read_and_delete_transcript_from_s3(key: str, bucket_name: str) -> str:
    logging.info(f"Read json file {key} from the bucket {bucket_name}.")
    client = boto3.client('s3')
    result = client.get_object(Bucket=bucket_name, Key=key)
    response = json.loads(result["Body"].read().decode())
    client.delete_object(Bucket=bucket_name, Key=key)
    return response['results']['transcripts'][0]['transcript']


def transcribe_file(file_dir: str, bucket_name: str, language: str ="en-US") -> str:
    job_name = str(uuid.uuid4())
    logging.info(
        f"Start the transcript job {job_name} with the file from {file_dir}.")

    file_key = move_file_to_bucket(file_dir, bucket_name)

    client = boto3.client('transcribe', region_name="eu-central-1")
    response = client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=language,
        MediaFormat='ogg',
        Media={
            'MediaFileUri': "/".join(["s3:/", bucket_name, file_key]),
        },
        OutputBucketName=bucket_name
    )

    while True:
        status = client.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        time.sleep(1)

    logging.info(
        f"The transcript job {job_name} is done.")

    transcript = read_and_delete_transcript_from_s3(
        job_name + ".json", bucket_name)

    remove_file_from_bucket(file_key, bucket_name)
    return transcript
