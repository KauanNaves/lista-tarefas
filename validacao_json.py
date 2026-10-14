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
def validar_chaves(dados: dict) -> dict:
    """
        Recebe o dicionário e verifica se todas as chaves estão corretas, adiciona e remove as que forem necessárias, retorna um dicionário dados validados e as chaves alteradas, todas as chaves alteradas foram reescritas, então não precisa validar os seus itens
    """

    dados_dicionario = deepcopy(dados)
    chaves_alteradas = []
    chaves = set(dados_dicionario.keys())
    chaves_corretas = {"LISTA_TAREFAS", "LISTA_TAREFAS_CONCLUIDAS", "ULTIMO_ID"}
    chaves_incorretas = []

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
            "chaves_alterados": set(chaves_alteradas)}


# Validação dos itens de cada chave
def validar_itens(dicionario: dict, chave: str) -> dict:
    """
        Recebe somente a chave necessária para validar os dados, por exemplo, recebe somente "LISTA_TAREFAS" e valida
        -- Não valida "ULTIMO_ID" --
        Retorna o dicionário com os dados corretos, e alterado=bool indicando se foi alterado ou não, uma lista com os itens removidos e um indicador se foi reescrito ou não
    """
    dados = deepcopy(dicionario[chave])
    itens_removidos = list()
    alterado = False

    if not isinstance(dados, list):
        dados = []
        alterado = True
        return {"dados": dados,
                "alterado": alterado,
                "reescrito": True,
                "itens_removidos": itens_removidos}

    chaves_corretas = {"id", "nome", "status"}

    

    for item in dados:
        if not isinstance(item, dict):
            itens_removidos.append(item)
            dados.remove(item)
            alterado = True
            continue
        chaves = set(item.keys())
        if chaves != chaves_corretas:
            itens_removidos.append(item)
            dados.remove(item)
            alterado = True
            continue

    return {"dados": dados,
            "alterado": alterado,
            "reescrito": False,
            "itens_removidos": itens_removidos}


# Validação do "ULTIMO_ID"
def validar_id(dicionario_completo: dict) -> dict:
    """
        Recebe o dicionário completo e valida o ultimo_id, verifica se é um inteiro e se é maior que o maior id cadastrado
        Retorna um dicionário com os dados e indicando se foi alterado
    """

    dados = deepcopy(dicionario_completo)

    def buscar_maior_id(tarefas: list, tarefas_concluidas: list)-> id:
        maior_id = 0
        for item in tarefas:
            if item["id"] > maior_id:
                maior_id = item["id"] 

        for item in tarefas_concluidas:
            if item["id"] > maior_id:
                maior_id = item["id"]

        return maior_id

    maior_id = buscar_maior_id(dados["LISTA_TAREFAS"], dados["LISTA_TAREFAS_CONCLUIDAS"])


    if not isinstance(dados["ULTIMO_ID"], int): 
        dados["ULTIMO_ID"] = maior_id
        return {"dados": dados,
                "alterado": True}

    if dados["ULTIMO_ID"] < maior_id:
        dados["ULTIMO_ID"] = maior_id
        return {"dados": dados,
                "alterado": True}
    return {"dados": dados,
            "alterado": False}





