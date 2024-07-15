from http import client
from fastapi import FastAPI
from store.routers import api_router

app = FastAPI()
app.include_router(api_router)

