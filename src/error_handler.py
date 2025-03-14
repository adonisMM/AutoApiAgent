import json
import os
import time

class ErrorHandler:
    def __init__(self):
        self.error_log = "log_history.log"
        self.error_history = "error_history.json"

        # Criar arquivo de histórico de erros se não existir
        if not os.path.exists(self.error_history):
            with open(self.error_history, "w") as file:
                json.dump({}, file)

    def log_error(self, error_message):
        """Registra o erro no log e no arquivo de histórico"""
        with open(self.error_log, "a") as log_file:
            log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ERRO: {error_message}\n")
        self.save_error_history(error_message)

    def save_error_history(self, error_message):
        """Salva o erro no histórico para futura consulta"""
        with open(self.error_history, "r") as file:
            error_data = json.load(file)

        if error_message not in error_data:
            error_data[error_message] = {"count": 1}
        else:
            error_data[error_message]["count"] += 1

        with open(self.error_history, "w") as file:
            json.dump(error_data, file, indent=4)

    def check_error_history(self, error_message):
        """Verifica se o erro já foi registrado anteriormente"""
        with open(self.error_history, "r") as file:
            error_data = json.load(file)

        if error_message in error_data:
            print(f"⚠️ Erro já registrado anteriormente ({error_data[error_message]['count']} ocorrência(s)).")
            return True
        return False

    def auto_resolve(self, error_message):
        """Tenta corrigir o erro automaticamente"""
        if "ModuleNotFoundError" in error_message:
            module_name = error_message.split("'")[1]
            print(f"📦 Tentando instalar o módulo ausente: {module_name}")
            os.system(f"pip install {module_name}")
            return True
        return False

# Teste da lógica (pode ser removido na versão final)
if __name__ == "__main__":
    error_handler = ErrorHandler()

    # Simulação de erro para teste
    test_error = "ModuleNotFoundError: No module named 'example_module'"
    
    if error_handler.check_error_history(test_error):
        print("✅ Erro já reconhecido. Verificando soluções anteriores...")
    else:
        print("🆕 Novo erro detectado. Registrando...")
        error_handler.log_error(test_error)
        error_handler.auto_resolve(test_error)
