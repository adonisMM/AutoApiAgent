import os
import subprocess
import time
import json

class TaskManager:
    def __init__(self):
        self.history_log = "log_history.log"

    def log_history(self, message):
        with open(self.history_log, "a") as log_file:
            log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

    def check_existing_structure(self):
        print("🔍 Verificando estrutura existente...")
        required_files = [
            "src/apisearch.py",
            "src/captcha_solver.py",
            "src/codegen.py",
            "src/main.py",
            "src/error_handler.py"
        ]
        for file in required_files:
            if not os.path.exists(file):
                self.log_history(f"❌ Arquivo ausente: {file}")
                print(f"❌ Arquivo ausente: {file}")
            else:
                self.log_history(f"✅ Estrutura OK: {file}")
                print(f"✅ Estrutura OK: {file}")

    def handle_task(self, task_type):
        print(f"⚙️ Executando a tarefa: {task_type}")
        self.log_history(f"Iniciando tarefa: {task_type}")

        if task_type == "app":
            subprocess.run(["python", "src/main.py"])
        elif task_type == "web_scraping":
            subprocess.run(["python", "src/apisearch.py"])
        elif task_type == "planilha":
            subprocess.run(["python", "src/codegen.py"])
        else:
            print("❌ Tarefa inválida.")
            self.log_history("❌ Tarefa inválida solicitada.")

if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.check_existing_structure()

    print("\nQual tarefa deseja executar?")
    print("1️⃣ - Criar App")
    print("2️⃣ - Realizar Web Scraping")
    print("3️⃣ - Gerar Planilha Automatizada")
    print("4️⃣ - Outra tarefa personalizada")

    task_choice = input("Escolha uma opção (1-4): ")
    task_options = {
        "1": "app",
        "2": "web_scraping",
        "3": "planilha",
        "4": "custom"
    }

    selected_task = task_options.get(task_choice, "invalid")
    task_manager.handle_task(selected_task)
