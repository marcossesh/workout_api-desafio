from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status, Query
from pydantic import UUID4
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut, CentroTreinamentoUpdate
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from sqlalchemy.exc import IntegrityError
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select
from workout_api.centro_treinamento.service import CentroTreinamentoService
from typing import Optional

router = APIRouter()

@router.post("/" , status_code=status.HTTP_201_CREATED)
async def criar_centro_treinamento(centro_treinamento: CentroTreinamentoIn, db: DatabaseDependency):
    try:
        novo_centro_treinamento = await CentroTreinamentoService.criar(centro_treinamento, db)
        if novo_centro_treinamento:
            return novo_centro_treinamento
    except IntegrityError as e:
        raise e
    except Exception as e:
        raise e
    
@router.get("/buscar", status_code=status.HTTP_200_OK)
async def listar(
    nome: Optional[str] = Query(None),
    proprietario: Optional[str] = Query(None),
    db: DatabaseDependency = None
):
    try:
        if nome:
            centro_treinamento = await CentroTreinamentoService.buscar_por_nome(nome, db)
            if centro_treinamento:
                return centro_treinamento
        if proprietario:
            centro_treinamento = await CentroTreinamentoService.buscar_por_proprietario(proprietario, db)
            if centro_treinamento:
                return centro_treinamento

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INFORME NOME OU PROPRIETARIO")
    
    except Exception as e:
        raise e

@router.get("/", status_code=status.HTTP_200_OK)
async def listar(db: DatabaseDependency):
    try:
        centro_treinamento = await CentroTreinamentoService.listar(db)
        return centro_treinamento
    except Exception as e:
        raise e
    
@router.delete("/{pk_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar(pk_id: int, db:DatabaseDependency):
    try:
        centro_treinamento = await CentroTreinamentoService.buscar_por_id(pk_id)
        if not centro_treinamento:
            raise HTTPException(status_code=status.HTTP_404_BAD_REQUEST, detail="Não Encontrado")
        await CentroTreinamentoService.deletar_centro_treinamento(pk_id, db)

    except Exception as e:
        raise e
    
@router.put("/{pk_id}", status_code=status.HTTP_200_OK)
async def atualizar(pk_id: int, payload: CentroTreinamentoUpdate, db:DatabaseDependency):
    try:
        centro_treinamento = await CentroTreinamentoService.buscar_por_id(pk_id, db)
        if not centro_treinamento:
            raise HTTPException(status_code=status.HTTP_404_BAD_REQUEST, detail="Não Encontrado")
        atualizar_centro = await CentroTreinamentoService.atualizar_centro_treinamento_por_id(pk_id, payload, db)
        return atualizar_centro
    
    except Exception as e:
        raise e