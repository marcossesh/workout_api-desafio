import asyncio
from uuid import uuid4
from sqlalchemy import text
from workout_api.configs.database import engine
from workout_api.contrib.models import BaseModel

async def create_tables_and_seed():
    # Criar tabelas
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
        print("✅ Tabelas criadas com sucesso!")
    
    # Inserir dados
    async with engine.begin() as conn:
        # Inserir categorias
        await conn.execute(text("""
            INSERT INTO categorias (pk_id, nome, id) VALUES 
            (:pk_id_1, :nome_1, :id_1),
            (:pk_id_2, :nome_2, :id_2),
            (:pk_id_3, :nome_3, :id_3)
            ON CONFLICT (pk_id) DO NOTHING
        """), {
            "pk_id_1": 1, "nome_1": "Bronze", "id_1": str(uuid4()),
            "pk_id_2": 2, "nome_2": "Prata", "id_2": str(uuid4()),
            "pk_id_3": 3, "nome_3": "Ouro", "id_3": str(uuid4()),
        })
        
        # Inserir centros de treinamento
        await conn.execute(text("""
            INSERT INTO centros_treinamento (pk_id, nome, endereco, proprietario, id) VALUES 
            (:pk_id_1, :nome_1, :endereco_1, :prop_1, :id_1),
            (:pk_id_2, :nome_2, :endereco_2, :prop_2, :id_2)
            ON CONFLICT (pk_id) DO NOTHING
        """), {
            "pk_id_1": 1, "nome_1": "Centro 1", "endereco_1": "Rua A, 123", "prop_1": "João Silva", "id_1": str(uuid4()),
            "pk_id_2": 2, "nome_2": "Centro 2", "endereco_2": "Rua B, 456", "prop_2": "Maria Santos", "id_2": str(uuid4()),
        })
        
        print("✅ Dados de teste inseridos!")

if __name__ == "__main__":
    asyncio.run(create_tables_and_seed())