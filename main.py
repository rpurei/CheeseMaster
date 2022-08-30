from config import APP_HOST, APP_PORT
from endpoints.api import router as api_router
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app = FastAPI(docs_url='/api/docs',
              openapi_url='/api/openapi.json')
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
