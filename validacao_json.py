import json
from typing import Any
from copy import deepcopy

# Validação do arquivo .json
NOME_ARQUIVO = "tarefas.json"
DICIONARIO_PADRAO = {
    "LISTA_TAREFAS": [],
    "LISTA_TAREFAS_CONCLUIDAS": [],
    "ULTIMO_ID": 0
}

""" Funções auxiliares: buscar e salvar dados
 -> Buscar dados trata o caso onde o json é vazio
"""
def buscar_dados(arquivo: str = NOME_ARQUIVO) -> dict:
    """
        Retorna um dict: {"dados": dados, "reescrito", bool}
    """
    try:
        with open(arquivo, mode="r", encoding="utf-8") as file:
            dados = json.load(file)
            return {"dados": dados,
                    "reescrito": False}

    except json.decoder.JSONDecodeError:
        with open(arquivo, mode="w", encoding="utf-8") as file:
            json.dump(DICIONARIO_PADRAO, file, ensure_ascii=False, indent=4)

        print(f"O arquivo {arquivo} estava vazio, foi reescrito da forma correta.")
        return {"dados": DICIONARIO_PADRAO, "reescrito": True}


def salvar_dados(dados: Any, arquivo: str = NOME_ARQUIVO) -> bool:
    """
        Retorna True caso consiga salvar os dados
    """
    with open(arquivo, mode="w", encoding="utf-8") as file:
        json.dump(dados, file, ensure_ascii=False, indent=4)

    return True


# Validação de casos onde o json não é um dicionário
def validar_arquivo(dados: dict) -> dict:
    """
        Retorna um dicionário com os dados, e indicando se os dados tiverem que ser alterado ou não
        Se "alterou" == True, não precisa prosseguir com outras validações, pois foi totalmente reescrito
    """
    dados_arquivo = deepcopy(dados["dados"])

    if isinstance(dados_arquivo, dict):

        if dados_arquivo == {}:
            # Dicionário vazio
            dados_arquivo = DICIONARIO_PADRAO
            return {"dados": dados_arquivo,
                    "alterou": True}

        return {"dados": dados_arquivo,
                "alterou": False}

    dados_arquivo = DICIONARIO_PADRAO

    return {"dados": dados_arquivo,
            "alterou": True}

    








if __name__ == "__main__":

    dados_ = {"dados": {"a": 1},
              "alterou": False}

    retorno = validar_arquivo(dados_)

    if retorno["alterou"]:
        print("Arquivo reescrito")

    print(retorno["dados"])



