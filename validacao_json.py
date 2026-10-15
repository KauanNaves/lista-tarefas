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
            dicionario = deepcopy(DICIONARIO_PADRAO)
            json.dump(dicionario, file, ensure_ascii=False, indent=4)

        print(f"O arquivo {arquivo} estava vazio, foi reescrito da forma correta.")
        return {"dados": deepcopy(DICIONARIO_PADRAO), "reescrito": True}


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
        Se "alterou" == True, não precisa prosseguir com outras validações, pois foi totalmente reescrito´
        dict = {"dados": dados_arquivo,
        "alterou": bool}
    """
    dados_arquivo = deepcopy(dados)

    if isinstance(dados_arquivo, dict):

        if dados_arquivo == {}:
            # Dicionário vazio
            dados_arquivo = deepcopy(DICIONARIO_PADRAO)
            return {"dados": dados_arquivo,
                    "alterou": True}

        return {"dados": dados_arquivo,
                "alterou": False}

    dados_arquivo = deepcopy(DICIONARIO_PADRAO)

    return {"dados": dados_arquivo,
            "alterou": True}


# Validação das chaves
def validar_chaves(dados: dict) -> dict:
    """
        Recebe o dicionário e verifica se todas as chaves estão corretas, adiciona e remove as que forem necessárias, retorna um dicionário dados validados e as chaves alteradas, todas as chaves alteradas foram reescritas, então não precisa validar os seus itens
        dict =  {"dados": dados_dicionario,
            "chaves_alterados": set(chaves_alteradas)}

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
            "chaves_alteradas": set(chaves_alteradas)}


# Validação dos itens de cada chave
def validar_itens(dicionario: dict, chave: str) -> dict:
    """
        Recebe somente a chave necessária para validar os dados, por exemplo, recebe somente "LISTA_TAREFAS" e valida
        -- Não valida "ULTIMO_ID" --
        Retorna o dicionário com os dados corretos, e alterado=bool indicando se foi alterado ou não, uma lista com os itens removidos e um indicador se foi reescrito ou não
        dict = {"dados": dados,
                "alterado": alterado,
                "reescrito": True,
                "itens_removidos": itens_removidos}
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

    dados_copia = deepcopy(dados)
    
    for item in dados_copia:
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
        else:
            if not isinstance(item["id"], int):
                itens_removidos.append(item)
                dados.remove(item)
                alterado = True
                
            if not isinstance(item["nome"], str):
                itens_removidos.append(item)
                dados.remove(item)
                alterado = True

            if not isinstance(item["status"], str):
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
        dict = {"dados": dados,
                "alterado": True}
    """

    dados = deepcopy(dicionario_completo)

    def buscar_maior_id(tarefas: list, tarefas_concluidas: list)-> int:
        maior_id = 0
        for item in tarefas:
            if item["id"] > maior_id:
                maior_id = item["id"] 

        for item in tarefas_concluidas:
            if item["id"] > maior_id:
                maior_id = item["id"]

        return maior_id

    maior_id = buscar_maior_id(dados["LISTA_TAREFAS"], dados["LISTA_TAREFAS_CONCLUIDAS"])


    if not isinstance(dados["ULTIMO_ID"], int) or isinstance(dados["ULTIMO_ID"], bool): 
        dados["ULTIMO_ID"] = maior_id
        return {"dados": dados,
                "alterado": True}

    if dados["ULTIMO_ID"] < maior_id:
        dados["ULTIMO_ID"] = maior_id
        return {"dados": dados,
                "alterado": True}
    
    return {"dados": dados,
            "alterado": False}


def testar_json(arquivo_json: str) -> None:
    """
        Testa e valida os dados do arquivo json e salva no final, avisa ao usuário por meio de prints
    """
    print(f"Começando validação do arquivo {arquivo_json}")
    print("Buscando dados...")
    dados = buscar_dados(arquivo_json)
    
    if dados["reescrito"]:
        print(f"{arquivo_json} estava corrompido e foi necessário reescrevê-lo.")
        print("Salvando dados...")
        salvar_dados(dados=dados["dados"], arquivo=arquivo_json)
        return
    
    print("Validando dicionário do arquivo...")
    dados_arquivo = validar_arquivo(dados["dados"])

    if dados_arquivo["alterou"]:
        print("Os dados do arquivo lido estavam corrompidos, foi necessário reescrevê-lo")
        print("Salvando dados...")
        salvar_dados(dados=dados_arquivo["dados"], arquivo=arquivo_json)
        print("Dados salvos...")
        return

    
    print("Validando chaves do dicionário...")
    dados_chave = validar_chaves(dados_arquivo["dados"])

    if dados_chave["chaves_alteradas"]:
        print("Chaves alteradas/excluídas")
        for chave in dados_chave["chaves_alteradas"]:
            print(chave)

    chaves_validar = ["LISTA_TAREFAS", "LISTA_TAREFAS_CONCLUIDAS", "ULTIMO_ID"]

    for chave in chaves_validar:
        if chave in dados_chave["chaves_alteradas"]:
            chaves_validar.remove(chave)
    
    print("Validando itens...")

    if "LISTA_TAREFAS" in chaves_validar:
        dados_tarefas = validar_itens(dados_chave["dados"], "LISTA_TAREFAS")
        if dados_tarefas["alterado"]:
            if dados_tarefas["reescrito"]:
                print("As tarefas pendentes estavam corrompidas, tiverem de ser apagadas e a lista foi reescrita!")
            else:
                print("Itens que foram removidos das tarefas pendentes...")
                for item in dados_tarefas["itens_removidos"]:
                    print(item)
        else:
            print("Tarefas pendentes válidas")
        dados_chave["dados"]["LISTA_TAREFAS"] = dados_tarefas["dados"]

    if "LISTA_TAREFAS_CONCLUIDAS" in chaves_validar:
        dados_tarefas = validar_itens(dados_chave["dados"], "LISTA_TAREFAS_CONCLUIDAS")
        if dados_tarefas["alterado"]:
            if dados_tarefas["reescrito"]:
                print("As tarefas concluidas estavam corrompidas, tiverem de ser apagadas e a lista foi reescrita!")
            else:
                print("Itens que foram removidos das tarefas concluidas...")
                for item in dados_tarefas["itens_removidos"]:
                    print(item)
        else:
            print("Tarefas concluidas válidas")
        dados_chave["dados"]["LISTA_TAREFAS_CONCLUIDAS"] = dados_tarefas["dados"]
    

    dados_id = validar_id(dados_chave["dados"])

    if dados_id["alterado"]:
        print("ULTIMO_ID cadastrado estava inválido, teve de ser corrigido.")
    print("Validação finalizada!")
    print("Salvando dados...")
    salvar_dados(dados=dados_id["dados"], arquivo=arquivo_json)
    print("Dados salvos...")
    return

 



if __name__ == "__main__":
    print(type(True), type(1))