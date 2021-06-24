from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
from api import user, hostserver, hostproxy
from setting import config
import multiprocessing
import uvicorn

app = FastAPI(debug=config.uvicorn_debug, docs_url='/api/docs',openapi_url='/api/openapi.json', redoc_url='/api/redoc')

register_tortoise(app, db_url=config.db_url, modules={"models": ["libs.models"]}, add_exception_handlers=config.uvicorn_debug)

app.include_router(router=user.router)
app.include_router(router=hostserver.router)
app.include_router(router=hostproxy.router)

if __name__ == '__main__':
    uvicorn.run(app='main:app', host=config.uvicorn_host, port=config.uvicorn_port,reload=config.uvicorn_reload, debug=config.uvicorn_debug, workers=int(multiprocessing.cpu_count()))
