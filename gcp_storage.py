###############################################
# Script para trabalhar com Buckets na GCP
# gustavo@2021-02-11
###############################################

from google.cloud import storage

import sys


# Inicio
def main():
    if len(sys.argv) < 2:
        print_comando_errado()
    else:
        key = sys.argv[1]

        if(key == "help"):
            print_help()
        else:
            action = ''
            bucket = ''
            try:
                action = sys.argv[2]
                bucket = sys.argv[3]
            except IndexError:
                print()
            print("=> " + action)
            assert action in ['list', 'add', 'del'], \
                print_comando_errado()
            process(key, action, bucket)


# Titulo do comando


def print_titulo():
    print("+----------------------------------------------+")
    print("| Comando para ações no Bucket do Google Cloud |")
    print("+----------------------------------------------+")


def print_comando_errado():
    print_titulo()
    print(" Comando: " + sys.argv[0] + " chave_google comando")
    print(" Para conhecer os comando digite: " + sys.argv[0] + " help")
    sys.exit()

# Ajuda


def print_help():
    print_titulo()
    print(" Comando: " + sys.argv[0] + " chave_google ")
    print("     add nome : Adiciona um novo Storage Bucket")
    print("     del nome : Apaga o Storage Bucket")
    print("     list     : Lista os Storages Bucket")
    sys.exit()


# Criando novos Buckets


def add_bucket(key, bucket_name):
    print("Criando o Bucket " + bucket_name)
    # Autentica service account com base em arquivos de credenciais
    storage_client = storage.Client.from_service_account_json(key)
    # Cria o Bucket
    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "COLDLINE"
    new_bucket = storage_client.create_bucket(bucket, location="us")
    print(
        "Adicionado o bucket {} em {} ".format(
            new_bucket.name, new_bucket.location
        )
    )

# Lista Cloud Storage Buckets


def list_buckets(key):
    print("Listando os Buckets:")
    # Autentica service account com base em arquivos de credenciais
    storage_client = storage.Client.from_service_account_json(key)
    buckets = list(storage_client.list_buckets())
    for bucket in buckets:
        print(" - " + bucket.name)

# Apagando os Buckets


def del_bucket(key, bucket_name):
    print("Deletando o Buckets " + bucket_name)
    # Autentica service account com base em arquivos de credenciais
    storage_client = storage.Client.from_service_account_json(key)
    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete()
    print("Bucket {} deletado".format(bucket.name))


# Verifica parametros
def process(key, action, bucket):
    if(action == "list"):
        list_buckets(key)
    elif(action == "add" or action == "del"):
        if (len(sys.argv) > 3):
            if (action == "add"):
                add_bucket(key, bucket)
            else:
                del_bucket(key, bucket)
        else:
            print_comando_errado()
    else:
        print_comando_errado()


# Rodando Script
if __name__ == '__main__':
    main()
