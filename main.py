from config import APP_HOST, APP_PORT
from endpoints.api import router as api_router
from fastapi import FastAPI
import uvicorn

app = FastAPI(docs_url='/api/docs',
              openapi_url='/api/openapi.json')
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "CheeseMaster online!"}


if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
