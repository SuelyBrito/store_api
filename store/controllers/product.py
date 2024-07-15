from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4
from store.core.exceptions import NotFoundException
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.usecases.product import ProductUsecase
from decimal import Decimal
from bson import Decimal128
router = APIRouter(tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    
    body: ProductIn = Body(...), usecase: ProductUsecase = Depends()
) -> ProductOut:
     
    try:
        return await usecase.create(body=body)
    except Exception as e:
            print(f"Erro ao adicionar Produto: {e}")
   

@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(usecase: ProductUsecase = Depends()) -> List[ProductOut]:
    return await usecase.query()

@router.get(path="/{vlmin},{vlmax}", status_code=status.HTTP_200_OK)
async def get_produto_by_valor(
    vlmin: Optional[Decimal],
    vlmax: Optional[Decimal],
    usecase: ProductUsecase = Depends()) -> List[ProductOut]: 
    return await usecase.get_produto_by_valor(vlmin=vl_min, vlmax=vlmax)


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
   
    usecase: ProductUsecase = Depends(),
) -> ProductUpdateOut:
    try:
        return await usecase.update(id=id, body=body)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Produto  não encontrado no id: {id}' 
        )

@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
