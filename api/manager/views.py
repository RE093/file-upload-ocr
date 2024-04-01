from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import UploadFileSerializer
import os
from .utils import ocr
from rest_framework.permissions import AllowAny
import boto3
from pathlib import Path



class UploadFileView(GenericViewSet):
    # authentication_classes = [AllowAny,]
    serializer_class = UploadFileSerializer

    def create(self, request):
        files = request.data.getlist('file')
        connection_id = request.data['connectionId']
        file_count = len(files)

        BUCKET = settings.AWS_UNTRUSTED_STORAGE_BUCKET_NAME
        REGION = settings.AWS_S3_REGION
        ACCESS_KEY = settings.AWS_S3_ACCESS_KEY_ID
        SECRET_ACCESS_KEY = settings.AWS_S3_SECRET_ACCESS_KEY

        uploadList = []
        s3 = boto3.client('s3', region_name=REGION, aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_ACCESS_KEY)
        
        for file in files:
            file_name = file.name
            file_path = Path(str(file))
            extension = file_path.suffix
            formatted_filename = file_name + extension

            try:
                s3.upload_fileobj(
                    file, 
                    BUCKET, 
                    formatted_filename, 
                    ExtraArgs={
                        "Metadata": {
                            "upload_id": str(file_name),
                            "connection_id": str(connection_id),
                            "original_name": str(file_name),
                            "file_count": str(file_count)
                        }
                    },
                )
                presigned_untrusted_url = s3.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': BUCKET,
                        'Key': formatted_filename
                    },
                    ExpiresIn=settings.S3_UNTRUSTED_PRESIGNED_URL_LIFETIME)

                uploadList.extend([{
                    'uploadId': file_name,
                    'originalName': file_name,
                    'name': formatted_filename,
                    'file': presigned_untrusted_url,
                    'extension': extension
                }])

            except Exception as e:
                print(e)
                return Response(status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK, data={"uploads": uploadList})