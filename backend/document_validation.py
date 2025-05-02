import boto3
from botocore.exceptions import ClientError
import re
import cv2
import numpy as np
import pytesseract
from PIL import Image
import io
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

#DEFINIR VARIÁVEIS DE AMBIENTE DEPOIS
def validate_documents(document_image, selfie_image):
    rekognition = boto3.client('rekognition',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
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

def validate_rg(document_image_bytes):
    """
    Valida um RG brasileiro usando OCR e regras específicas
    """
    try:
        # Converter bytes para imagem
        image = Image.open(io.BytesIO(document_image_bytes))
        img_np = np.array(image)

        # Pré-processamento da imagem
        gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # Extrair texto com OCR
        text = pytesseract.image_to_string(thresh, lang='por')

        # Padrões para validação de RG
        rg_pattern = r'\b\d{1,2}\.?\d{3}\.?\d{3}-?[0-9X]\b'
        rg_matches = re.findall(rg_pattern, text)

        # Verificar palavras-chave que indicam um RG
        keywords = ['identidade', 'registro geral', 'rg', 'secretaria', 'segurança']
        has_keywords = any(keyword in text.lower() for keyword in keywords)

        # Verificar se encontrou um número de RG e palavras-chave
        is_valid = len(rg_matches) > 0 and has_keywords

        # Verificar se há uma foto no documento
        # Isso requer análise de imagem mais avançada, mas podemos usar o Rekognition
        rekognition = boto3.client('rekognition',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )

        face_detection = rekognition.detect_faces(
            Image={'Bytes': document_image_bytes},
            Attributes=['ALL']
        )

        has_face = len(face_detection['FaceDetails']) > 0

        return {
            "valid": is_valid and has_face,
            "rg_number": rg_matches[0] if rg_matches else None,
            "confidence": 0.9 if (is_valid and has_face) else 0.5,
            "has_face": has_face,
            "extracted_text": text[:200]  # Primeiros 200 caracteres para debug
        }

    except Exception as e:
        return {"error": str(e), "valid": False}