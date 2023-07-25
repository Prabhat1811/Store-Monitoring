from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.db import create_db_and_tables, engine
from app.routers import reports

app = FastAPI()


app.include_router(reports.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables(engine)


@app.exception_handler(Exception)
async def catchall_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content="Internal Server Error",
    )
