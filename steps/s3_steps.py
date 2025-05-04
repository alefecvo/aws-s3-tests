import os
from behave import given, when, then
from services.s3_services import S3Services
import logging

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)


@given('que eu possuo as seguintes informações')
def step_impl(context):
    # DataTable é acessível via context.table
    row = context.table[0]
    context.arquivo = f"data/{row['arquivo']}"
    context.bucket = row['bucket']
    context.chave = row['chave']

    os.makedirs('data', exist_ok=True)
    context.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    context.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    context.region = 'sa-east-1'


@when('eu envio o arquivo para o bucket informado na chave informada')
def step_impl(context):
    log.info(
        f"Preparando para enviar arquivo '{context.arquivo}' para bucket '{context.bucket}' na chave '{context.chave}'")
    context.s3_client = S3Services.criar_client(
        context.aws_access_key, context.aws_secret_key, context.region
    )
    context.resultado = S3Services.enviar_arquivo_s3(
        context.s3_client, context.bucket, context.arquivo, context.chave
    )
    log.info("Arquivo enviado com sucesso.")


@then('o arquivo deve estar disponível no bucket')
def step_impl(context):
    log.info(f"Verificando se o arquivo '{context.chave}' está disponível no bucket '{context.bucket}'")
    response = context.s3_client.list_objects_v2(Bucket=context.bucket, Prefix=context.chave)
    assert 'Contents' in response
    assert any(obj['Key'] == context.chave for obj in response['Contents'])
    log.info("Arquivo encontrado no bucket.")
