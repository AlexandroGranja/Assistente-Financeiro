import requests
import json

# Teste do endpoint de ajuda
response = requests.post("http://localhost:5000/api/financeiro/processar_mensagem", 
                        json={"message": "ajuda"})
print("Status:", response.status_code)
print("Response:", response.text)

# Teste de registro de gasto
response2 = requests.post("http://localhost:5000/api/financeiro/processar_mensagem", 
                         json={"message": "Almoço 25.50 alimentação"})
print("\nStatus:", response2.status_code)
print("Response:", response2.text)

# Teste do comando total
response3 = requests.post("http://localhost:5000/api/financeiro/processar_mensagem", 
                         json={"message": "total"})
print("\nStatus:", response3.status_code)
print("Response:", response3.text)

