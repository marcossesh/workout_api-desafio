from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.atleta.service import AtletaService
from typing import Optional

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def criar_atleta(atleta: AtletaIn, db: DatabaseDependency):
    try:
        novo_atleta = await AtletaService.criar(atleta, db)
        return novo_atleta 
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}"
        )
    except Exception as e:
        raise e

@router.get("/", status_code=status.HTTP_200_OK)
async def listar_atletas(db: DatabaseDependency):
    try:
        return await AtletaService.listar(db)
    except Exception as e:
        raise e
    
@router.get("/buscar")
async def buscar_atleta(
    nome: Optional[str] = Query(None),
    cpf: Optional[str] = Query(None),
    db: DatabaseDependency = None
):
    try:
        if cpf:
            atleta = await AtletaService.buscar_por_cpf(cpf, db)
            if not atleta:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            return atleta
        
        if nome:
            atleta = await AtletaService.buscar_por_nome(nome, db)
            if not atleta:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            return atleta
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INFORME NOME OU CPF")
    
    except Exception as e:
        raise e
    
@router.delete("/{pk_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_atleta(pk_id: int, db: DatabaseDependency):
    try:
        atleta = await AtletaService.buscar_por_id(pk_id, db)
        if not atleta:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")
        
        await AtletaService.deletar_por_id(pk_id, db)
    except Exception as e:
        raise e

@router.put("/{pk_id}", status_code=status.HTTP_200_OK)
async def atualizar_atleta(pk_id: int, payload: AtletaUpdate, db: DatabaseDependency):
    try:
        atleta = await AtletaService.atualizar_atleta_por_id(pk_id, payload, db)
        if not atleta:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não Encontrado")
        return atleta
    except Exception as e:
        raise e