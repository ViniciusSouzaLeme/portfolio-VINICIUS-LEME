from datetime import datetime, timedelta
from collections import Counter, defaultdict
        
def contar_usuarios(arquivo, historico_arquivo):
    usuarios = set()

    with open(arquivo, 'r') as file:
        for linha in file:
            dados = linha.strip().split(',')
            identificacao_usuario = dados[0]
            usuarios.add(identificacao_usuario)
            
    numero_usuarios = len(usuarios)
    registrar_historico(historico_arquivo, "Contar usuários", numero_usuarios)
    return numero_usuarios

def contar_senhas(arquivo, historico_arquivo):
    senha_apenas_letras = 0
    senha_apenas_digitos = 0
    senha_alfanumerica = 0

    with open(arquivo, 'r') as file:
        for linha in file:
            dados = linha.strip().split(',')
            senha = dados[1]

            if senha.isalpha():
                senha_apenas_letras += 1
            elif senha.isdigit():
                senha_apenas_digitos += 1
            else:
                senha_alfanumerica += 1
                
    registrar_historico(historico_arquivo, "Contar senhas", (senha_apenas_letras, senha_apenas_digitos, senha_alfanumerica))
    return senha_apenas_letras, senha_apenas_digitos, senha_alfanumerica


def calcular_tempo_medio_login(arquivo, historico_arquivo):
    tempo_total_login = defaultdict(timedelta)
    contador_login = defaultdict(int)

    with open(arquivo, 'r') as file:
        for linha in file:
            dados = linha.strip().split(',')
            identificacao_usuario = dados[0]
            hora_login = datetime.strptime(dados[3], '%H:%M:%S')
            hora_logout = datetime.strptime(dados[4], '%H:%M:%S')
            tempo_login = hora_logout - hora_login
            tempo_total_login[identificacao_usuario] += tempo_login
            contador_login[identificacao_usuario] += 1

    tempo_medio_login = {}

    for usuario, tempo_total in tempo_total_login.items():
        qtd_login = contador_login[usuario]
        tempo_medio = tempo_total / qtd_login
        tempo_medio_login[usuario] = tempo_medio

    registrar_historico(historico_arquivo, "Calcular tempo médio de login", tempo_medio_login)
    return tempo_medio_login


def encontrar_data_extremos(arquivo, historico_arquivo):
    datas = []
    with open(arquivo, 'r') as file:
        for linha in file:
            dados = linha.strip().split(',')
            data_login = dados[2]
            datas.append(data_login)

    contador_datas = Counter(datas)
    data_mais_logins = contador_datas.most_common(1)[0]
    data_menos_logins = contador_datas.most_common()[-1]

    registrar_historico(historico_arquivo, "Encontrar data com mais e menos logins", (data_mais_logins, data_menos_logins))
    return data_mais_logins, data_menos_logins


def encontrar_usuarios_extremos(arquivo, historico_arquivo):
    usuarios = []
    with open(arquivo, 'r') as file:
        for linha in file:
            dados = linha.strip().split(',')
            identificacao_usuario = dados[0]
            usuarios.append(identificacao_usuario)

    contador_usuarios = Counter(usuarios)
    usuarios_mais_logam = []
    usuarios_menos_logam = []

    maior_qtd_logins = contador_usuarios.most_common(1)[0][1]
    menor_qtd_logins = contador_usuarios.most_common()[-1][1]

    for usuario, qtd_logins in contador_usuarios.items():
        if qtd_logins == maior_qtd_logins:
            usuarios_mais_logam.append(usuario)
        elif qtd_logins == menor_qtd_logins:
            usuarios_menos_logam.append(usuario)

    registrar_historico(historico_arquivo, "Encontrar usuário(s) que mais e menos se logam no sistema", (usuarios_mais_logam, usuarios_menos_logam))
    return usuarios_mais_logam, usuarios_menos_logam


def calcular_tempo_medio_login_geral(arquivo, historico_arquivo):
    tempo_total_login = timedelta()
    contador_login = 0

    with open(arquivo, 'r') as file:
        for linha in file:
            dados = linha.strip().split(',')
            hora_login = datetime.strptime(dados[3], '%H:%M:%S')
            hora_logout = datetime.strptime(dados[4], '%H:%M:%S')
            tempo_login = hora_logout - hora_login
            tempo_total_login += tempo_login
            contador_login += 1

    tempo_medio_login_geral = tempo_total_login / contador_login

    
    registrar_historico(historico_arquivo, "Calcular tempo médio de login geral", tempo_medio_login_geral)
    return tempo_medio_login_geral

def registrar_historico(arquivo, consulta, resultado):
    data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    resultado_str = str(resultado)

    with open(arquivo, 'a') as file:
        file.write(f"{data_hora} - Consulta: {consulta} - Resultado: {resultado_str}\n")

def exibir_menu():
    print("==== MENU ====")
    print("1. Calcular número de usuários")
    print("2. Descobrir quantas senhas seguem um formato")
    print("3. Calcular tempo médio de login de cada usuário")
    print("4. Encontrar data com mais e menos logins")
    print("5. Encontrar usuário(s) que mais e menos se logam no sistema")
    print("6. Calcular tempo médio de login geral")
    print("0. Sair")


def main():
    nome_arquivo = 'log.txt.txt.txt'
    historico_arquivo = 'historico.txt.txt'

    while True:
        exibir_menu()
        opcao = input("Selecione uma opção: ")

        if opcao == '1':
            numero_usuarios = contar_usuarios(nome_arquivo, historico_arquivo)
            print(f"Número de usuários: {numero_usuarios}\n")
        elif opcao == '2':
            letras, digitos, alfanumerico = contar_senhas(nome_arquivo, historico_arquivo)
            print(f"Senhas apenas com letras: {letras}")
            print(f"Senhas apenas com dígitos: {digitos}")
            print(f"Senhas alfanuméricas: {alfanumerico}")
        elif opcao == '3':
            tempo_medio_login = calcular_tempo_medio_login(nome_arquivo, historico_arquivo)
            print("Tempo médio de login para cada usuário:")
            for usuario, tempo_medio in tempo_medio_login.items():
                print(f"{usuario}: {tempo_medio}")
            print()
        elif opcao == '4':
            data_mais_logins, data_menos_logins = encontrar_data_extremos(nome_arquivo, historico_arquivo)
            print("Data com mais logins:")
            print(f"{data_mais_logins[0]} - {data_mais_logins[1]} logins")
            print()
            print("Data com menos logins:")
            print(f"{data_menos_logins[0]} - {data_menos_logins[1]} logins")
            print()
        elif opcao == '5':
            usuarios_mais_logam, usuarios_menos_logam = encontrar_usuarios_extremos(nome_arquivo, historico_arquivo)
            print("Usuário(s) que mais se logam:")
            for usuario in usuarios_mais_logam:
                print(usuario)
            print()
            print("Usuário(s) que menos se logam:")
            for usuario in usuarios_menos_logam:
                print(usuario)
            print()
        elif opcao == '6':
            tempo_medio_geral = calcular_tempo_medio_login_geral(nome_arquivo, historico_arquivo)
            print(f"Tempo médio de login geral: {tempo_medio_geral}\n")
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Por favor, selecione uma opção válida.\n")


if __name__ == '__main__':
    main()