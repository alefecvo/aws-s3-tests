import os
from behave import given, when, then
from services.s3_services import S3Services
import logging
logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

@given('que eu possuo um arquivo "{arquivo} e as credenciais da AWS válidas')
def step_impl(context, arquivo):
    os.makedirs('data', exist_ok=True)
    context.arquivo = f'data/{arquivo}'

    context.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    context.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    context.region = 'sa-east-1'
    # log.info("## given method ##")
    # log.info(f"AWS_ACCESS_KEY_ID: {context.aws_access_key}")
    # log.info(f"AWS_SECRET_ACCESS_KEY: {'*' * len(context.aws_secret_key) if context.aws_secret_key else ''}")
    # log.info(f"AWS_REGION: {context.region}")

@when('eu envio o arquivo para o bucket "{bucket}" na chave "{chave}"')
def step_impl(context, bucket, chave):
    log.info(f"Preparando para enviar arquivo '{context.arquivo}' para bucket '{bucket}' na chave '{chave}'")
    context.bucket = bucket
    context.chave = chave
    context.s3_client = S3Services.criar_client(
        context.aws_access_key, context.aws_secret_key, context.region
    )
    context.resultado = S3Services.enviar_arquivo_s3(
        context.s3_client, bucket, context.arquivo, chave
    )
    log.info("Arquivo enviado com sucesso.")

@then('o arquivo deve estar disponível no bucket')
def step_impl(context):
    log.info(f"Verificando se o arquivo '{context.chave}' está disponível no bucket '{context.bucket}'")
    response = context.s3_client.list_objects_v2(Bucket=context.bucket, Prefix=context.chave)
    assert 'Contents' in response
    assert any(obj['Key'] == context.chave for obj in response['Contents'])
    log.info("Arquivo encontrado no bucket.")
