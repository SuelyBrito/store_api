from decimal import Decimal
from typing import List, Optional
from fastapi import Query
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import MongoClient
import pymongo
from store.core.config  import db_client,client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundException
from bson import Decimal128
class ProductUsecase:
    def __init__(self) -> None:
        try:
            self.cliente = MongoClient('localhost',27017) 
            self.database = self.cliente['db_produto']
            self.collection = self.database['colle_prod']
            print("Conexao com o banco de dados estabelecida com sucesso!")
        except Exception as e:
            print(f"Erro ao conectar com o banco de dados: {e}")
        
    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        await self.collection.insert_one(product_model.model_dump())

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Produto nao encontrado com id: {id}")

        return ProductOut(**result)

    async def query(self) -> List[ProductOut]:
        return [ProductOut(**item) async for item in self.collection.find()]


    async def get_produto_by_valor(self ,min_price: Optional[float] = Query(None, description="Minimum product price"), max_price: Optional[float] = Query(None, description="Maximum product price")):
        query = {}
        if   min_price is not None and max_price is not None:
             query['price'] = {"$gte": min_price, "$lte": max_price}
        elif min_price is not None:
             query['price'] = {"$gte": min_price}
        elif max_price is not None:
             query['price'] = {"$lte": max_price}

        products = []
        async for item in self.collection.find(filter_query):
            products.append(ProductOut(**item))
        return products


    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": body.model_dump(exclude_none=True)},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Produto nao encontrado com filtro: {id}")

        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()
