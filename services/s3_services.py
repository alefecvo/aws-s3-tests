import boto3
import logging

log = logging.getLogger(__name__)

class S3Services:
    @staticmethod
    def criar_client(aws_access_key, aws_secret_key, region):
        log.info("##Criando conexao com a AWS e obtendo credenciais##")
        return boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )

    @staticmethod
    def enviar_arquivo_s3(s3_client, bucket, arquivo_local, chave_s3):
        log.info(f"Enviando arquivo '{arquivo_local}' para bucket '{bucket}' na chave '{chave_s3}'")
        s3_client.upload_file(arquivo_local, bucket, chave_s3)
        log.info("Upload realizado com sucesso.")
        return True