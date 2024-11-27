import json
import boto3
import time
from datetime import datetime

# Initialize the S3 client
s3_client = boto3.client('s3')

# S3 bucket and folder details
BUCKET_NAME = 'projectkafkabucket'
FOLDER_NAME = 'sensor_data/'

# Batch size
BATCH_SIZE = 10

# Buffer to hold the batch
buffer = []

def lambda_handler(event, context):
    global buffer
    try:
        # Process incoming records
        for record in event['Records']:
            # Decode the Kinesis data
            payload = json.loads(record['kinesis']['data'])
            buffer.append(payload)
            
            # Check if the buffer size reached the BATCH_SIZE
            if len(buffer) >= BATCH_SIZE:
                # Create a timestamped filename for the batch
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                file_name = f"{FOLDER_NAME}batch_{timestamp}.json"
                
                # Upload the batch to S3
                s3_client.put_object(
                    Bucket=BUCKET_NAME,
                    Key=file_name,
                    Body=json.dumps(buffer, indent=2)
                )
                
                # Clear the buffer after uploading
                buffer = []
        
        return {
            'statusCode': 200,
            'body': json.dumps('Processed records successfully!')
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing records: {str(e)}")
        }
