from db import LISTA_TAREFAS, LISTA_TAREFAS_CONCLUIDAS, ULTIMO_ID
from os import system
import json

TAREFAS = {"LISTA_TAREFAS": [],
           "LISTA_TAREFAS_CONCLUIDAS": [],
           "ULTIMO_ID": 0}


def criar_arquivo():
    try:
        with open("tarefas.json", mode="x", encoding="utf-8") as f:
            json.dump(TAREFAS, f, indent=4, ensure_ascii=False)
    except FileExistsError:
        return


def salvar_tarefas():
    with open("tarefas.json", mode="w", encoding="utf-8") as file:
        json.dump(TAREFAS, file, ensure_ascii=False, indent=4)
    return


def carregar_tarefas():
    global TAREFAS
    with open("tarefas.json", mode="r", encoding="utf-8") as file:
        tarefas = json.load(file)

    if tarefas:
        TAREFAS = tarefas
    return 


# Menu - Adicionar, Remover, Listar, Marcar como Concluída, Visualizar Concluídas
def menu():
    print("""
    [1] - Listar tarefas;
    [2] - Adicionar tarefa;
    [3] - Remover tarefa;
    [4] - Marcar como concluída;
    [5] - Listas tarefas concluídas;
    [6] - Sair
""")


def pegar_opcao(min=1, max=6):
    while True:
        opcao_escolhida = input("Digite a opção desejada: ")
        try:
            opcao_escolhida = int(opcao_escolhida)
            if opcao_escolhida not in range(min, max+1):
                raise ValueError
            break    
        except:
            print("Digite uma opção válida!")
            opcao_escolhida = pegar_opcao(min, max)
        break
    return opcao_escolhida


def adicionar_tarefa():
    global ULTIMO_ID
    nome_tarefa = input("Digite o nome da tarefa: ")
    dict_tarefa = {
        "id": TAREFAS["ULTIMO_ID"] + 1,
        "nome": nome_tarefa,
        "status": "Pendente",
    }

    TAREFAS["LISTA_TAREFAS"].append(dict_tarefa)
    TAREFAS['ULTIMO_ID'] += 1
    print("Tarefa adicionada!")
    return


def remover_tarefa():
    while True:
        id = input("Digite o ID da tarefa:")
        if id.isnumeric():
            id = int(id)
            break
    for tarefa in TAREFAS["LISTA_TAREFAS"]:
        if tarefa["id"] == id:
            TAREFAS["LISTA_TAREFAS"].remove(tarefa)
    return


def listar_tarefas():
    if len(TAREFAS["LISTA_TAREFAS"]) < 1:
        print("Nenhuma tarefa adicionada!")
        return
    print("Tarefas:")
    for tarefa in TAREFAS["LISTA_TAREFAS"]:
        print(f"{tarefa["id"]} - {tarefa["nome"]} - {tarefa["status"]}")

    return
    

def marcar_como_concluida():
    while True:
        id = input("Digite o ID da tarefa:")
        if id.isnumeric():
            id = int(id)
            break
    for tarefa in TAREFAS["LISTA_TAREFAS"]:
        if tarefa["id"] == id:
            tarefa["status"] = "Concluída"
            TAREFAS["LISTA_TAREFAS"].remove(tarefa)
            TAREFAS["LISTA_TAREFAS_CONCLUIDAS"].append(tarefa)
    print("Tarefa concluída")


def listar_concluidas():
    if len(TAREFAS["LISTA_TAREFAS_CONCLUIDAS"]) < 1:
        print("Nenhuma tarefa concluída!")
        return
    print("Tarefas concluídas:")
    for tarefa in TAREFAS["LISTA_TAREFAS_CONCLUIDAS"]:
        print(f"{tarefa["id"]} - {tarefa["nome"]} - {tarefa["status"]}")
    return


while True:
    criar_arquivo()
    carregar_tarefas()
    menu()
    opcao = pegar_opcao()

    if opcao == 6:
        salvar_tarefas()
        print("Saindo do programa...")
        break

    match opcao:
        case 1:
            system("clear")
            listar_tarefas()
        case 2:
            #adicionar tareafas
            system("clear")    
            adicionar_tarefa()
            salvar_tarefas()
        case 3:
            #remover tarefas
            system("clear")
            listar_tarefas()
            remover_tarefa()
            salvar_tarefas()
        case 4:
            #marcar como concluida
            system("clear")
            listar_tarefas()
            marcar_como_concluida()
            salvar_tarefas()
        case 5:
            #listar tarefas concluidas
            system("clear")
            listar_concluidas()

