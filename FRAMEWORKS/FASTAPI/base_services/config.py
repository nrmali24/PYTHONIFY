from fastapi import FastAPI
from fastapi_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists,create_database
import json


app = FastAPI()

try:
    with open("//config.json") as f:
        config = json.load(f)


    server=config["credentials"]["server"]
    username=config["credentials"]["username"]
    password=config["credentials"]["password"]
    database=config["credentials"]["database"]
    server_host=config["credentials"]["server_host"]
    SQLALCHEMY_DATABASE_URL=f"{server}://{username}:{password}@{server_host}/{database}"
    engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread": False})


    if not database_exists(engine.url):
        create_database(engine.url)
        
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base=declarative_base()

    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(str(e))
    





user_port=5559


