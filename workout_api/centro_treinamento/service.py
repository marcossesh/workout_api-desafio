from sqlalchemy.future import select
from sqlalchemy import delete, table, column, update
from sqlalchemy.exc import IntegrityError
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut, CentroTreinamentoUpdate
from workout_api.contrib.dependencies import DatabaseDependency
from datetime import datetime
import uuid

class CentroTreinamentoService:

    @staticmethod
    async def listar(db: DatabaseDependency):
        try:
            query = select(CentroTreinamentoModel)
            resultado = await db.execute(query)
            return resultado.scalars().all()
        except Exception as e:
            raise e
        
    @staticmethod
    async def buscar_por_id(pk_id: int, db: DatabaseDependency):
        try:
            query = select(CentroTreinamentoModel).where(CentroTreinamentoModel.pk_id == pk_id)
            resultado = await db.execute(query)
            return resultado.scalars().first()
        except Exception as e:
            raise e
    
    @staticmethod
    async def buscar_por_nome(nome: str, db: DatabaseDependency):
        try:
            query = select(CentroTreinamentoModel).where(CentroTreinamentoModel.nome == nome)
            resultado = await db.execute(query)
            return resultado.scalars().first()
        except Exception as e:
            raise e
        
    @staticmethod
    async def buscar_por_proprietario(proprietario: str, db: DatabaseDependency):
        try:
            query = select(CentroTreinamentoModel).where(CentroTreinamentoModel.proprietario == proprietario)
            resultado = await db.execute(query)
            return resultado.scalars().first()
        except Exception as e:
            raise e
    
    @staticmethod
    async def criar(centro_treinamento: CentroTreinamentoIn, db: DatabaseDependency):
        try:
            novo_centro_treinamento = CentroTreinamentoModel(
                nome=centro_treinamento.nome,
                endereco=centro_treinamento.endereco,
                proprietario=centro_treinamento.proprietario,
                id=uuid.uuid4(),
            )

            db.add(novo_centro_treinamento)
            await db.commit()
            await db.refresh(novo_centro_treinamento)
            return novo_centro_treinamento
        except Exception as e:
            await db.rollback()
            raise e
        
    @staticmethod
    async def deletar_centro_treinamento(pk_id: int, db: DatabaseDependency):
        try:
            centro_treinamento_existente = await CentroTreinamentoService.buscar_por_id(pk_id, db)
            if not centro_treinamento_existente:
                return None
            
            delete_query = delete(CentroTreinamentoModel).where(CentroTreinamentoModel.pk_id == pk_id)
            await db.execute(delete_query)
            await db.commit()
            return True
        except Exception as e:
            await db.rollback()
            raise e
        
    @staticmethod
    async def atualizar_centro_treinamento_por_id(pk_id: int, payload: CentroTreinamentoUpdate, db: DatabaseDependency):
        try:
            centro_treinamento = await CentroTreinamentoService.buscar_por_id(pk_id, db)
            if not centro_treinamento:
                return None
            
            update_data = payload.model_dump(exclude_unset=True)
            if not update_data:
                return centro_treinamento
            
            update_query = update(CentroTreinamentoModel).where(
                CentroTreinamentoModel.pk_id == pk_id
            ).values(**update_data)

            await db.execute(update_query)
            await db.commit()
            await db.refresh(centro_treinamento)

            return centro_treinamento
        except Exception as e:
            raise e



