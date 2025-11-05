from sqlalchemy.future import select
from sqlalchemy import delete, table, column, update
from sqlalchemy.exc import IntegrityError
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut, CategoriaUpdate
from workout_api.contrib.dependencies import DatabaseDependency
from datetime import datetime
import uuid

class CategoriaService:

    @staticmethod
    async def criar(categoria_in: CategoriaIn, db: DatabaseDependency):
        try:
            nova_categoria = CategoriaModel(
                nome=categoria_in.nome,
                descricao=categoria_in.descricao,
                id=uuid.uuid4(),
            )

            db.add(nova_categoria)
            await db.commit()
            await db.refresh(nova_categoria)

            return nova_categoria

        except Exception as e:
            await db.rollback()
            raise e

    @staticmethod
    async def buscar_por_id(pk_id: int, db: DatabaseDependency):
        try:
            query = select(CategoriaModel).where(CategoriaModel.pk_id == pk_id)
            resultado = await db.execute(query)
            return resultado.scalars().first()
        except Exception as e:
            raise e
    
    @staticmethod
    async def deletar_categoria(pk_id: int, db: DatabaseDependency):
        try:
            query = delete(CategoriaModel).where(CategoriaModel.pk_id == pk_id)
            await db.execute(query)
            await db.commit()
        except Exception as e:
            raise e
        
    @staticmethod
    async def listar(db: DatabaseDependency):
        try:
            query = select(CategoriaModel)
            resultado = await db.execute(query)
            return resultado.scalars().all()
        except Exception as e:
            raise e

    @staticmethod
    async def atualizar_categoria_por_id(pk_id: int, payload: CategoriaUpdate, db: DatabaseDependency):
        try:
            query = update(CategoriaModel).where(CategoriaModel.pk_id == pk_id).values(
                nome=payload.nome
            ).execution_options(synchronize_session="fetch")
            await db.execute(query)
            await db.commit()
            return await CategoriaService.buscar_por_id(pk_id, db)
        except Exception as e:
            raise e