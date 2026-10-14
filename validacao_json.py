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


# Validação de casos onde o json não é um dicionário ou é um dicionário vazio
def validar_arquivo(dados: dict) -> dict:
    """
        Retorna um dicionário com os dados, e indicando se os dados tiverem que ser alterado ou não
        Se "alterou" == True, não precisa prosseguir com outras validações, pois foi totalmente reescrito
    """
    dados_arquivo = deepcopy(dados)

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


# Validação das chaves
def validar_chaves(dados: dict):
    dados_dicionario = deepcopy(dados)
    chaves_alteradas = []
    chaves = set(dados_dicionario.keys())
    chaves_corretas = {"LISTA_TAREFAS", "LISTA_TAREFAS_CONCLUIDAS", "ULTIMO_ID"}
    chaves_incorretas = []
    chaves_removidas = []

    if chaves != chaves_corretas: # Compara as chaves do dicionário e remove as incorretas do dicionario, adicionando na lista de chaves_incorretas
        for chave in chaves:
            if chave not in chaves_corretas:
                chaves_incorretas.append(chave)
                dados_dicionario.pop(chave)

    for chave in chaves_incorretas: # Percorre as chaves incorretas e as retiram da lista de chaves 
        chaves.remove(chave)

    if chaves != chaves_corretas: # Compara se as chaves são as corretas
        if "LISTA_TAREFAS" not in chaves:
            dados_dicionario["LISTA_TAREFAS"] = []
            chaves_alteradas.append("LISTA_TAREFAS")

        if "LISTA_TAREFAS_CONCLUIDAS" not in chaves:
            dados_dicionario["LISTA_TAREFAS_CONCLUIDAS"] = []
            chaves_alteradas.append("LISTA_TAREFAS_CONCLUIDAS")

        if "ULTIMO_ID" not in chaves:
            dados_dicionario["ULTIMO_ID"] = 0
            chaves_alteradas.append("ULTIMO_ID")



    return {"dados": dados_dicionario,
            "chaves_alterados": set(chaves_alteradas)
                }


# Validação dos itens de cada chave
def validar_item():

        # Validando item por item
    if "LISTA_TAREFAS" not in chaves_alteradas:
        for item in dados_dicionario["LISTA_TAREFAS"]:
            if set(item.keys()) != {"id", "nome", "status"}:
                itens_apagados.append(item)
                dados_dicionario["LISTA_TAREFAS"].remove(item)
                continue
            else:
                if not isinstance(item["id"], int):
                    itens_apagados.append(item)
                    dados_dicionario["LISTA_TAREFAS"].remove(item)
                    continu 
                if not isinstance(item["nome"], str):
                    itens_apagados.append(item)
                    dados_dicionario["LISTA_TAREFAS"].remove(item)
                    continu 
                if not isinstance(item["status"], str):
                    itens_apagados.append(item)
                    dados_dicionario["LISTA_TAREFAS"].remove(item)
                    continue       


    if "LISTA_TAREFAS_CONCLUIDAS" not in chaves_alteradas:
            for item in dados_dicionario["LISTA_TAREFAS_CONCLUIDAS"]:
                if set(item.keys()) != {"id", "nome", "status"}:
                    itens_apagados.append(item)
                    dados_dicionario["LISTA_TAREFAS_CONCLUIDAS"].remove(item)
                    continue
                else:
                    if not isinstance(item["id"], int):
                        itens_apagados.append(item)
                        dados_dicionario["LISTA_TAREFAS_CONCLUIDAS"].remove(item)
                        continue

                    if not isinstance(item["nome"], str):
                        itens_apagados.append(item)
                        dados_dicionario["LISTA_TAREFAS_CONCLUIDAS"].remove(item)
                        continue

                    if not isinstance(item["status"], str):
                        itens_apagados.append(item)
                        dados_dicionario["LISTA_TAREFAS_CONCLUIDAS"].remove(item)
                        continue           
            


if __name__ == "__main__":




