import requests
from bs4 import BeautifulSoup

class APISearchAgent:
    def __init__(self):
        self.base_url = "https://rapidapi.com/"

    def search_api(self, query):
        search_url = f"{self.base_url}search/{query}"
        response = requests.get(search_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            apis = soup.find_all('a', class_='api-title')
            return [api.text.strip() for api in apis]
        else:
            print("❌ Erro ao buscar APIs")
            return []

if __name__ == "__main__":
    agent = APISearchAgent()
    resultado = agent.search_api("previsão do tempo")
    print("APIs encontradas:", resultado)
