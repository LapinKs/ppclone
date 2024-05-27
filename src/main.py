from fastapi import FastAPI

from src.adaptive_logic.router import router as api_rout
from src.config import driver

app = FastAPI()

app.include_router(api_rout)

@app.on_event("startup")
async def startup():
    driver.verify_connectivity()


@app.on_event("shutdown")
async def shutdown():
    driver.close()
