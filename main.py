from senha import API_KEY
from rules.emprego import REGRAS_EMPREGO, LINKS_FABIO_EMPREGO, LINKS_DAVID_EMPREGO
from rules.emprestimo import REGRAS_EMPRESTIMO, TEXTO_BASE, LINKS_FABIO_ES, LINKS_FINANZACREDIT_ES, LINKS_NIVALDO_ES, LINKS_ROOTS_ES
from rules.cartao import REGRAS_CARTAO, LINKS_NIVALDO_CARTAO
import google.generativeai as genai
import os
import time

# Configurar o modelo
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Função para gerar texto
def gerar_texto(prompt):
    response = model.generate_content(prompt)
    if response and hasattr(response, "text"):
        return response.text.strip()
    else:
        print("Erro: resposta vazia ou inválida")
        return None

# Função para limpar o terminal
def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")

# Função para obter entrada de valores válidos
def obter_escolha(mensagem, opcoes_validas):
    while True:
        escolha = input(mensagem).strip()
        if escolha in opcoes_validas:
            if escolha == "0":
                return escolha 
            limpar_terminal()
            return escolha
        print("\nOpção inválida. Tente novamente.")

while True: 
    limpar_terminal()
    
    print("Selecione o tipo de copy:\n")
    print("1 - Emprego")
    print("2 - Empréstimo")
    print("3 - Cartão")

    opcao_tipo = obter_escolha("\nDigite o número correspondente: ", ["0", "1", "2", "3"])
    if opcao_tipo == "0":
        continue 
    
    if opcao_tipo == "1":
        tipo = "Emprego"
        regras = REGRAS_EMPREGO
        print("\nOpção escolhida: EMPREGO")
        clientes_disponiveis = {
            "1": ("Fábio", LINKS_FABIO_EMPREGO),
            "2": ("David", LINKS_DAVID_EMPREGO),
        }
    elif opcao_tipo == "3":
        tipo = "Cartão"
        regras = REGRAS_CARTAO
        print("\nOpção escolhida: CARTÃO")
        clientes_disponiveis = {
            "1": ("Nivaldo", LINKS_NIVALDO_CARTAO),
        }
    else:
        tipo = "Empréstimo"
        regras = REGRAS_EMPRESTIMO
        print("\nOpção escolhida: EMPRÉSTIMO\n")
        clientes_disponiveis = {
            "1": ("Fábio", LINKS_FABIO_ES),
            "2": ("FinanzaCredit", LINKS_FINANZACREDIT_ES),
            "3": ("Nivaldo", LINKS_NIVALDO_ES),
            "4": ("Roots", LINKS_ROOTS_ES),
        }

    time.sleep(2)
    limpar_terminal()

    while True:
        print(f"[{tipo}] Selecione o cliente:\n")
        for key, (nome, _) in clientes_disponiveis.items():
            print(f"{key} - {nome}")
        print("0 - Voltar")

        opcao_cliente = obter_escolha("\nDigite o número correspondente: ", ["0"] + list(clientes_disponiveis.keys()))
        if opcao_cliente == "0":
            break

        nome_cliente, links_cliente = clientes_disponiveis[opcao_cliente]
        print(f"\nCliente escolhido: {nome_cliente}")

        time.sleep(2)
        limpar_terminal()

        pasta_destino = "Output"
        os.makedirs(pasta_destino, exist_ok=True)

        nomes_arquivos = [
            f"{dia}-{str(i).zfill(2)}.txt"
            for dia in ["segunda", "terca", "quarta", "quinta", "sexta", "sabado", "domingo"]
            for i in range(1, 6)
        ]

        for nome_arquivo in nomes_arquivos:
            texto_gerado = gerar_texto(regras + TEXTO_BASE + links_cliente)

            if texto_gerado:
                caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

                with open(caminho_arquivo, "w", encoding="utf-8") as file:
                    file.write(texto_gerado)

                print(f"Resposta salva em: {caminho_arquivo}")

            time.sleep(5)

        print("\nTodos os arquivos foram gerados com sucesso!")
        exit()
