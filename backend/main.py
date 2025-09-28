from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.draft import router

app = FastAPI(title="Draft")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(router, prefix="/api") 



@app.get("/")
def read_root():
    return {"message": "Draft!"}