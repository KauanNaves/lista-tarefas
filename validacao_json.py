import json

from typing import Any

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
        Retorna True ou False caso consiga, ou não, salvar os dados
    """
    return True



# Validação de casos onde o json não é um dicionário









if __name__ == "__main__":
    dados_arquivo = buscar_dados("teste.json")

    dados = dados_arquivo["dados"]
    reescrito = dados_arquivo["reescrito"]


    print(f"Arquivo reescrito\nDados: {dados}"  if reescrito else f"Arquivo lido: {dados}" )