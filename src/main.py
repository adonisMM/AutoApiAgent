from transformers import pipeline
import requests
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import pytesseract
import os
import time
from sklearn.cluster import KMeans
import numpy as np
from dotenv import load_dotenv
from task_manager import TaskManager
from error_handler import ErrorHandler
from crewai import Crew, Agent, Task
import git

def check_for_updates():
    try:
        repo = git.Repo('.')
        origin = repo.remote(name='origin')
        origin.pull()
        print("✅ Código atualizado com sucesso do GitHub.")
    except Exception as e:
        print(f"⚠️ Falha ao verificar atualizações: {e}")

# Carregar variáveis do .env
load_dotenv()
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def perguntar_tarefa():
    print("Escolha uma tarefa:")
    print("1️⃣ Buscar uma API")
    print("2️⃣ Criar código para integração com API")
    print("3️⃣ Automatizar uma planilha")
    print("4️⃣ Gerar uma análise de dados")
    print("5️⃣ Criar um software completo")
    print("6️⃣ Modificar um código existente")
    print("7️⃣ Montar uma planilha personalizada")
    print("8️⃣ Outros (Criar briefing)")
    print("9️⃣ Sair")

    escolha = input("Digite o número da sua escolha: ")
    return int(escolha) if escolha.isdigit() else 0

def gerar_briefing(tarefa, objetivo, passos):
    briefing = f"""
🚀 Briefing da Tarefa Personalizada

Descrição da Tarefa: {tarefa}
Objetivo Final: {objetivo}
Entradas Previstas: (Gerado pelo sistema)
Saídas Previstas: (Gerado pelo sistema)
Recursos Sugeridos: (Gerado pelo sistema)
Limitações (Aviso do sistema): Custo 0 se possível, estimativa de custos se houver necessidade.
Tempo Estimado: (Gerado pelo sistema)

Passos manuais que você deseja automatizar: {passos}

➡️ Essa previsão é automática e pode ser ajustada conforme necessidade.
"""
    with open("briefing.txt", "w", encoding="utf-8") as file:
        file.write(briefing)
    print("✅ Briefing gerado com sucesso em 'briefing.txt'")

class APISearchAgent:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def find_api(self, query):
        try:
            self.driver.get(f"https://www.google.com/search?q={query}")
            results = self.driver.find_elements(By.CSS_SELECTOR, ".tF2Cxc")
            api_list = []
            for result in results[:5]:
                api_list.append(result.text)
                print(f"🔎 API encontrada: {result.text}")
            return api_list
        except Exception as e:
            ErrorHandler().log_error(f"Erro ao buscar API: {e}")
            print(f"❌ Erro ao buscar API: {e}")

class DevelopmentTeam:
    def run(self, task):
        print(f"🚀 Equipe de Desenvolvimento iniciou {task}...")

class AnalysisTeam:
    def run(self, task):
        print(f"🔍 Equipe de Análise iniciou {task}...")

class CodeGenAgent:
    def __init__(self):
        self.generator = pipeline("text-generation", model="tiiuae/falcon-7b-instruct")
        self.successful_attempts = 0

    def write_code(self, api_info):
        prompt = f"Escreva um código Python que integre a seguinte API: {api_info}.\n"
        response = self.generator(prompt, max_length=400, do_sample=True)
        generated_code = response[0]['generated_text']
        subprocess.run(["pip", "install", "requests"])
        return generated_code

def main():
    check_for_updates()
    print("🚀 Iniciando o programa...")

    task_choice = perguntar_tarefa()

    search_agent = APISearchAgent()
    code_agent = CodeGenAgent()
    task_manager = TaskManager()
    error_handler = ErrorHandler()

    if task_choice == 1:
        query = input("🔍 Que tipo de API você deseja buscar? ")
        api_list = search_agent.find_api(query)
        print(f"🔍 Resultado da busca: {api_list}")
    elif task_choice == 2:
        print("💻 Criando código para integração de API...")
        api_list = search_agent.find_api("API de previsão do tempo")
        selected_api = api_list[0] if api_list else "Nenhuma API encontrada"
        generated_code = code_agent.write_code(selected_api)
        with open("generated_api_code.py", "w") as file:
            file.write(generated_code)
        print("✅ Código gerado e salvo com sucesso! Testando...")
        code_agent.test_code()
    elif task_choice == 3:
        print("📊 Automatizando uma planilha...")
        DevelopmentTeam().run("Automação de Planilha")
    elif task_choice == 4:
        print("📈 Gerando análise de dados...")
        AnalysisTeam().run("Análise de Dados")
    elif task_choice == 8:
        print("📋 Outra tarefa personalizada selecionada...")
        tarefa = input("📝 Descreva sua tarefa personalizada: ")
        objetivo = input("🎯 Qual é o objetivo final dessa tarefa? ")
        passos = input("🟡 Quais passos manuais você deseja automatizar? ")
        gerar_briefing(tarefa, objetivo, passos)
        DevelopmentTeam().run("Outro")
    elif task_choice == 9:
        print("👋 Encerrando o programa. Até logo!")
        return
    else:
        print("❌ Opção inválida. Encerrando o programa.")

    task_manager.log_task("Tarefa escolhida", "Concluído")

if __name__ == "__main__":
    main()
