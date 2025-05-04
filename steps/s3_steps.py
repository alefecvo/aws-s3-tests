import os
from behave import given, when, then

from services.s3_services import S3Services


@given('que eu possuo um arquivo "{arquivo}"')
def step_impl(context, arquivo):
    os.makedirs('data', exist_ok=True)
    context.arquivo = f'data/{arquivo}'
    # Cria o arquivo para garantir que ele existe
    with open(context.arquivo, 'w') as f:
        f.write('{"nome": "StackSpot"}')


@given('as credenciais da AWS válidas')
def step_impl(context):
    context.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    context.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    context.region = os.getenv('AWS_REGION')


@when('eu envio o arquivo para o bucket "{bucket}" na chave "{chave}"')
def step_impl(context, bucket, chave):
    context.bucket = bucket
    context.chave = chave
    context.s3_client = S3Services.criar_client(
        context.aws_access_key, context.aws_secret_key, context.region
    )
    context.resultado = S3Services.enviar_arquivo_s3(
        context.s3_client, bucket, context.arquivo, chave
    )


@then('o arquivo deve estar disponível no bucket')
def step_impl(context):
    response = context.s3_client.list_objects_v2(Bucket=context.bucket, Prefix=context.chave)
    assert 'Contents' in response
    assert any(obj['Key'] == context.chave for obj in response['Contents'])
