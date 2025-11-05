from uuid import uuid4
from fastapi import APIRouter, HTTPException, status
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut, CategoriaUpdate
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.categorias.service import CategoriaService

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CategoriaOut)
async def criar_categoria(categoria: CategoriaIn, db: DatabaseDependency):
    try:
        return await CategoriaService.criar(categoria, db)
    except Exception as e:
        raise e
    
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CategoriaOut])
async def listar_categorias(db: DatabaseDependency):
    try:
        return await CategoriaService.listar(db)
    except Exception as e:
        raise e
    
@router.get("/{pk_id}", status_code=status.HTTP_200_OK, response_model=CategoriaOut)
async def buscar_categoria(pk_id: int, db: DatabaseDependency):
    try:
        categoria = await CategoriaService.buscar_por_id(pk_id, db)
        if not categoria:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")
        return categoria
    except Exception as e:
        raise e

@router.delete("/{pk_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_categoria(pk_id: int, db: DatabaseDependency):
    try:
        categoria = await CategoriaService.buscar_por_id(pk_id, db)
        if not categoria:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")
        await CategoriaService.deletar_categoria(pk_id, db)
    except Exception as e:
        raise e
    
@router.put("/{pk_id}", status_code=status.HTTP_200_OK, response_model=CategoriaOut)
async def atualizar_categoria(pk_id: int, payload: CategoriaUpdate, db: DatabaseDependency):
    try:
        categoria = await CategoriaService.atualizar_categoria_por_id(pk_id, payload, db)
        if not categoria:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")
        return categoria
    except Exception as e:
        raise e