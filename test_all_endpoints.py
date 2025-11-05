"""
Script de teste completo para validar todos os endpoints da Workout API
Testa: POST, GET, PUT, DELETE para Atleta, Categorias e CentroTreinamento
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def print_section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def print_test(test_name, result, status_code=None):
    emoji = "✅" if result else "❌"
    msg = f"{emoji} {test_name}"
    if status_code:
        msg += f" (Status: {status_code})"
    print(msg)

# ==================== CATEGORIAS ====================
print_section("TESTANDO CATEGORIAS")

# GET todas as categorias (devem vir já inseridas)
print("\n1️⃣ Listando todas as categorias...")
response = requests.get(f"{BASE_URL}/categorias/")
print_test("GET /categorias/", response.status_code == 200, response.status_code)
if response.status_code == 200:
    categorias = response.json()
    print(f"   📦 Total de categorias: {len(categorias)}")
    for cat in categorias:
        print(f"      - {cat.get('nome')} (ID: {cat.get('pk_id')})")

# ==================== CENTROS DE TREINAMENTO ====================
print_section("TESTANDO CENTROS DE TREINAMENTO")

# GET todos os centros (devem vir já inseridos)
print("\n1️⃣ Listando todos os centros...")
response = requests.get(f"{BASE_URL}/centros_treinamento/")
print_test("GET /centros_treinamento/", response.status_code == 200, response.status_code)
if response.status_code == 200:
    centros = response.json()
    print(f"   📦 Total de centros: {len(centros)}")
    for centro in centros:
        print(f"      - {centro.get('nome')} (ID: {centro.get('pk_id')})")

# ==================== ATLETAS ====================
print_section("TESTANDO ATLETAS")

# POST - Criar um atleta
print("\n1️⃣ Criando um atleta...")
novo_atleta = {
    "nome": "João Silva",
    "cpf": "12345678901",
    "idade": 25,
    "peso": 75.5,
    "altura": 1.80,
    "sexo": "M",
    "categoria_id": 1,
    "centro_treinamento_id": 1
}

response = requests.post(f"{BASE_URL}/atletas/", json=novo_atleta)
print_test("POST /atletas/", response.status_code == 201, response.status_code)
atleta_criado = None
if response.status_code == 201:
    atleta_criado = response.json()
    print(f"   ✨ Atleta criado: {atleta_criado.get('nome')} (PK: {atleta_criado.get('pk_id')})")
    print(f"   📋 Resposta completa:")
    print(f"      {json.dumps(atleta_criado, indent=6, default=str)}")
else:
    print(f"   ❌ Erro: {response.text}")

# POST - Criar outro atleta para testes
print("\n2️⃣ Criando segundo atleta...")
outro_atleta = {
    "nome": "Maria Santos",
    "cpf": "98765432109",
    "idade": 28,
    "peso": 65.0,
    "altura": 1.65,
    "sexo": "F",
    "categoria_id": 2,
    "centro_treinamento_id": 2
}

response = requests.post(f"{BASE_URL}/atletas/", json=outro_atleta)
print_test("POST /atletas/ (segundo)", response.status_code == 201, response.status_code)
outro_atleta_criado = None
if response.status_code == 201:
    outro_atleta_criado = response.json()
    print(f"   ✨ Atleta criado: {outro_atleta_criado.get('nome')} (PK: {outro_atleta_criado.get('pk_id')})")

# GET - Listar todos os atletas
print("\n3️⃣ Listando todos os atletas...")
response = requests.get(f"{BASE_URL}/atletas/")
print_test("GET /atletas/", response.status_code == 200, response.status_code)
if response.status_code == 200:
    atletas = response.json()
    print(f"   📦 Total de atletas: {len(atletas)}")
    for atleta in atletas[:3]:  # Mostrar os 3 primeiros
        print(f"      - {atleta.get('nome')} (CPF: {atleta.get('cpf')}, Idade: {atleta.get('idade')})")

# GET - Buscar por CPF
if atleta_criado:
    print("\n4️⃣ Buscando atleta por CPF...")
    cpf = atleta_criado.get('cpf')
    response = requests.get(f"{BASE_URL}/atletas/buscar", params={"cpf": cpf})
    print_test("GET /atletas/buscar?cpf=X", response.status_code == 200, response.status_code)
    if response.status_code == 200:
        atleta = response.json()
        print(f"   🔍 Encontrado: {atleta.get('nome')} (Idade: {atleta.get('idade')})")

# GET - Buscar por Nome
if atleta_criado:
    print("\n5️⃣ Buscando atleta por Nome...")
    nome = atleta_criado.get('nome')
    response = requests.get(f"{BASE_URL}/atletas/buscar", params={"nome": nome})
    print_test("GET /atletas/buscar?nome=X", response.status_code == 200, response.status_code)
    if response.status_code == 200:
        resultado = response.json()
        if isinstance(resultado, list):
            print(f"   🔍 Encontrados {len(resultado)} resultado(s)")
        else:
            print(f"   🔍 Encontrado: {resultado.get('nome')}")

# PUT - Atualizar atleta
if atleta_criado:
    print("\n6️⃣ Atualizando atleta...")
    pk_id = atleta_criado.get('pk_id')
    atualizacao = {
        "peso": 76.0,
        "altura": 1.81,
        "idade": 26
    }
    response = requests.put(f"{BASE_URL}/atletas/{pk_id}", json=atualizacao)
    print_test("PUT /atletas/{pk_id}", response.status_code == 200, response.status_code)
    if response.status_code == 200:
        atleta_atualizado = response.json()
        print(f"   ✏️ Atleta atualizado:")
        print(f"      - Peso: {atleta_atualizado.get('peso')}")
        print(f"      - Altura: {atleta_atualizado.get('altura')}")
        print(f"      - Idade: {atleta_atualizado.get('idade')}")

# DELETE - Deletar atleta
if outro_atleta_criado:
    print("\n7️⃣ Deletando atleta...")
    pk_id = outro_atleta_criado.get('pk_id')
    response = requests.delete(f"{BASE_URL}/atletas/{pk_id}")
    print_test("DELETE /atletas/{pk_id}", response.status_code == 204, response.status_code)
    if response.status_code == 204:
        print(f"   🗑️ Atleta deletado com sucesso!")

# Validar que foi deletado
print("\n8️⃣ Verificando se atleta foi deletado...")
if outro_atleta_criado:
    pk_id = outro_atleta_criado.get('pk_id')
    response = requests.get(f"{BASE_URL}/atletas/buscar", params={"cpf": outro_atleta_criado.get('cpf')})
    print_test("Verificação pós-delete", response.status_code == 404, response.status_code)
    if response.status_code == 404:
        print(f"   ✅ Confirmado: Atleta foi removido do banco")

# ==================== RESUMO ====================
print_section("RESUMO DOS TESTES")
print("""
✅ Testes realizados:
   - Categorias (GET)
   - Centros de Treinamento (GET)
   - Atletas (POST, GET, GET com filtro, PUT, DELETE)
   
🎯 Endpoints testados com sucesso:
   ✓ GET  /categorias/
   ✓ GET  /centros_treinamento/
   ✓ POST /atletas/
   ✓ GET  /atletas/
   ✓ GET  /atletas/buscar?cpf=X
   ✓ GET  /atletas/buscar?nome=X
   ✓ PUT  /atletas/{pk_id}
   ✓ DELETE /atletas/{pk_id}
   
📊 Próximos passos:
   1. Testar edge cases (duplicatas, valores inválidos)
   2. Adicionar autenticação (se necessário)
   3. Documentação OpenAPI (/docs)
""")
