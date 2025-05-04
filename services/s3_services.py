import boto3


class S3Services:
    def criar_client(aws_access_key, aws_secret_key, region):
        return boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )

    def enviar_arquivo_s3(s3_client, bucket, arquivo_local, chave_s3):
        s3_client.upload_file(arquivo_local, bucket, chave_s3)
        return True
