import boto3
from botocore.exceptions import ClientError

def validate_documents(document_image, selfie_image):
    rekognition = boto3.client('rekognition',
        aws_access_key_id='YOUR_ACCESS_KEY',
        aws_secret_access_key='YOUR_SECRET_KEY',
        region_name='YOUR_REGION'
    )

    try:
        # Comparar faces
        response = rekognition.compare_faces(
            SourceImage={'Bytes': selfie_image},
            TargetImage={'Bytes': document_image},
            SimilarityThreshold=90
        )

        # Detectar texto no documento
        text_detection = rekognition.detect_text(
            Image={'Bytes': document_image}
        )

        return {
            "face_match": len(response['FaceMatches']) > 0,
            "similarity": response['FaceMatches'][0]['Similarity'] if response['FaceMatches'] else 0,
            "document_text": text_detection['TextDetections']
        }

    except ClientError as e:
        return {"error": str(e)}