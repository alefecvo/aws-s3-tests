# language: pt
Funcionalidade: Enviar arquivo JSON para o S3

Cenário: Enviar um arquivo .json para o bucket S3 usando DataTable
  Dado que eu possuo as seguintes informações
    | arquivo         | bucket                   | chave                |
    | stackspot.json  | s3-github-action-tests   | data/stackspot.json  |
  Quando eu envio o arquivo para o bucket informado na chave informada
  Então o arquivo deve estar disponível no bucket