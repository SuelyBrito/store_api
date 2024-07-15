from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi import FastAPI
from pymongo import MongoClient

import os

import motor.motor_asyncio
from bson.objectid import ObjectId
# Crie uma instância do cliente MongoDB
#client = MongoClient()

# Conecte-se ao servidor MongoDB

client = MongoClient('mongodb://localhost:27017/')
db_client = client['db_produtos']
collection = db_client['itens']
  