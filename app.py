from fastapi import FastAPI
from routers.ilumination_protocol import ilumination_protocol_router
from starlette.middleware.cors import CORSMiddleware
from db.db import create_tables
from settings.settings import settings

create_tables()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ilumination_protocol_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)


