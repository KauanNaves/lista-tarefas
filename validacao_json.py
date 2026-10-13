import json
from typing import Any

NOME_ARQUIVO = "tarefas.json"

TAREFAS = {"LISTA_TAREFAS": [],
           "LISTA_TAREFAS_CONCLUIDAS": [],
           "ULTIMO_ID": 0
        }


def buscar_dados(arquivo: str = NOME_ARQUIVO) -> dict | None: # Se retornar None é porque o arquivo foi totalmente reescrito
    try:
        with open(arquivo, mode="r", encoding="utf-8") as file:
            dados_arquivo = json.load(file)
        return dados_arquivo
    except json.JSONDecodeError:
        print("Arquivo corrompido, reescrevendo novamente. (Tarefas que estavam salvas forma perdidas)")
        with open(arquivo, mode="w", encoding="utf-8") as file:
            json.dump(TAREFAS, file, ensure_ascii=False, indent=4)
            print("Arquivo corrigido.\n")
        return False
    

def salvar_dados(dados_salvar, arquivo:str = NOME_ARQUIVO) -> bool: # Retorna True se conseguir salvar os dados
    try:
        with open(arquivo, mode="w", encoding="utf-8") as file:
            json.dump(dados, file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Erro {e} ao tentar salvar dados no arquivo.")
        raise Exception
    

def validar_dicionario(dados) -> dict | bool: # Retorna os dados caso é um dicionário, retorna False caso as correções foram necessárias e reescrito o arquivo
    if not isinstance(dados, dict):
        if salvar_dados(dados):
            return False

    return dados


def validar_chaves(dados: dict) -> bool | dict: # Retorna False se não precisa mais verificar, retorna os dados caso ainda precise de verificação
    chaves = dados.keys()

    chaves_corretas = ["LISTA_TAREFAS", "LISTA_TAREFAS_CONCLUIDAS", "ULTIMO_ID"]

    correcoes = 0

    chaves_apagar = []

    for chave in chaves:
        if chave not in chaves_corretas:
            chaves_apagar.append(chave)

    for chave in chaves_apagar:
        del dados[chave]

    if "LISTA_TAREFAS" not in chaves:
        dados["LISTA_TAREFAS"] = dict()
        correcoes += 1

    if "LISTA_TAREFAS_CONCLUIDAS" in chaves:
        dados["LISTA_TAREFAS_CONCLUIDAS"] = dict()
        correcoes += 1

    if "ULTIMO_ID" in chaves:
        dados["ULTIMO_ID"] = 0
        correcoes += 1


    salvar_dados(dados)
    return False if correcoes == 3 else dados


def validar_itens(dados: dict, concluidas: bool = False):
    chave = "LISTA_TAREFAS_CONCLUIDAS" if concluidas else "LISTA_TAREFAS"

    def validar_item(item: dict):
        chaves = item.keys()
        if list(chaves) != ["id", "nome", "status"]:
            return False

    for item in dados[chave]:
        if validar_item(item):
            print(f"Item: {item} inválido, será apagado.")
            dados[chave].remove(item)
    global TAREFAS
    TAREFAS = dados
    salvar_dados(dados)
    return None


def validar_id():
    dados = buscar_dados()
    if dados is None:
        return
    maior_id = 0
    for item in dados["LISTA_TAREFAS"]:
        if item["id"] > maior_id:
            maior_id = item["id"]

    for item in dados["LISTA_TAREFAS_CONCLUIDAS"]:
        if item["id"] > maior_id:
                    maior_id = item["id"]

    print(f"ULTIMO_ID é número {isinstance(dados["ULTIMO_ID"], int)}")

    if not isinstance(dados["ULTIMO_ID"], int):
        dados["ULTIMO_ID"] = maior_id
        TAREFAS = dados
        return 

    if dados["ULTIMO_ID"] < maior_id:
        dados["ULTIMO_ID"] = maior_id
        TAREFAS = dados
        return

    TAREFAS = dados
    return dados


def testar_json(arquivo: str = NOME_ARQUIVO):
    dados = buscar_dados()
    if not dados:
        salvar_dados(dados)
        return

    dados_dict = validar_dicionario(dados)
    if not dados_dict:
        salvar_dados(dados_dict)
        return

    dados_chaves = validar_chaves(dados_dict)
    if not dados_chaves:
        salvar_dados(dados_chaves)
        return

    validar_itens(dados_chaves)

    validar_id()


