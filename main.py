from db import LISTA_TAREFAS


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


# Pegar opção do usuário
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


# Adicionar tarefas
def adicionar_tarefa():
    nome_tarefa = input("Digite o nome da tarefa: ")
    dict_tarefa = {
        "id": len(LISTA_TAREFAS) + 1,
        "nome": nome_tarefa,
        "status": "Pendente",
    }
    LISTA_TAREFAS.append(dict_tarefa)
    print("Tarefa adicionada!")
    return


# Remover tarefas
def remover_tarefa():
    while True:
        id = input("Digite o ID da tarefa:")
        if id.isnumeric():
            id = int(id)
            break
    LISTA_TAREFAS.pop(id-1)
    return


# Listar tarefas
def listar_tarefas():
    if len(LISTA_TAREFAS) < 1:
        print("Nenhuma tarefa adicionada!")
        return
    for tarefa in LISTA_TAREFAS:
        print(f"{tarefa["id"]} - {tarefa["nome"]} - {tarefa["status"]}")

    return


while True:
    menu()
    opcao = pegar_opcao()

    if opcao == 6:
        print("Saindo do programa...")
        break

    match opcao:
        case 1:
            listar_tarefas()
        case 2:
            #adicionar tareafas
            adicionar_tarefa()
        case 3:
            #remover tarefas
            remover_tarefa()
        case 4:
            #marcar como concluida
            pass
        case 5:
            #listar tarefas concluidas
            pass