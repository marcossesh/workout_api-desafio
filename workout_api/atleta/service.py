from sqlalchemy.future import select
from sqlalchemy import delete, table, column, update
from sqlalchemy.exc import IntegrityError
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.contrib.dependencies import DatabaseDependency
from datetime import datetime

class AtletaService:
    
    @staticmethod
    async def buscar_por_cpf(cpf: str, db: DatabaseDependency):
        try:
            query = select(AtletaModel).where(AtletaModel.cpf == cpf)
            resultado = await db.execute(query)
            return resultado.scalars().first()
        except Exception as e:
            raise e
    
    @staticmethod
    async def buscar_por_nome(nome: str, db: DatabaseDependency):
        try:
            query = select(AtletaModel).filter(AtletaModel.nome.ilike(f"%{nome}%"))
            resultado = await db.execute(query)
            return resultado.scalars().all()
        except Exception as e:
            raise e
    
    @staticmethod
    async def criar(atleta_in: AtletaIn, db: DatabaseDependency):
        try:
            atleta_existente = await AtletaService.buscar_por_cpf(atleta_in.cpf, db)
            if atleta_existente:
                raise IntegrityError("CPF já cadastrado", None, None)
            
            novo_atleta = AtletaModel(
                nome=atleta_in.nome,
                cpf=atleta_in.cpf,
                idade=atleta_in.idade,
                peso=atleta_in.peso,
                altura=atleta_in.altura,
                sexo=atleta_in.sexo,
                created_at=datetime.now(),
                categoria_id=atleta_in.categoria_id,
                centro_treinamento_id=atleta_in.centro_treinamento_id
            )
            
            db.add(novo_atleta)
            await db.commit()
            await db.refresh(novo_atleta)
            
            return novo_atleta
            
        except Exception as e:
            await db.rollback()
            raise e

    @staticmethod
    async def listar(db: DatabaseDependency):
        try:
            query = select(AtletaModel)
            resultado = await db.execute(query)
            return resultado.scalars().all()
        except Exception as e:
            raise e
        
    @staticmethod
    async def buscar_por_id(pk_id: int, db: DatabaseDependency):
        try:
            query = select(AtletaModel).where(AtletaModel.pk_id == pk_id)
            resultado = await db.execute(query)
            return resultado.scalars().first()
        except Exception as e:
            raise e
        
    @staticmethod
    async def deletar_por_id(pk_id: int, db: DatabaseDependency):
        try:
            atleta = await AtletaService.buscar_por_id(pk_id, db)
            if not atleta:
                return None
            
            delete_query = delete(AtletaModel).where(AtletaModel.pk_id == pk_id)
            await db.execute(delete_query)
            await db.commit()
            return True
        except Exception as e:
            await db.rollback()
            raise e
    
    @staticmethod
    async def atualizar_atleta_por_id(pk_id: int, payload: AtletaUpdate, db: DatabaseDependency):
        try:
            atleta = await AtletaService.buscar_por_id(pk_id, db)
            if not atleta:
                return None
            
            update_data = payload.model_dump(exclude_unset=True)
            
            if not update_data:
                return atleta
            
            update_query = update(AtletaModel).where(
                AtletaModel.pk_id == pk_id
            ).values(**update_data)
            
            await db.execute(update_query)
            await db.commit()
            await db.refresh(atleta)
            
            return atleta
        except Exception as e:
            await db.rollback()
            raise e