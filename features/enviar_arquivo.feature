#language: pt
Funcionalidade: Enviar arquivo JSON para o S3

  Cenário: Enviar um arquivo .json para o bucket S3
    Dado que eu possuo um arquivo "stackspot.json" e as credenciais da AWS válidas
    Quando eu envio o arquivo para o bucket "s3-github-action-tests" na chave "data/stackspot.json"
    Então o arquivo deve estar disponível no bucket