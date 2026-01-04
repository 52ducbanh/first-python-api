from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class phepcong(BaseModel):
    a : int
    b : int

@app.post("/tinh-tong")
def sum(dat : phepcong):
    a = dat.a 
    b = dat.b
    tong = a + b
    return {
        "First_num: " : a,
        "Second_num: " : b,
        "ans": tong,
        "note:" : "completed :)" 
    }
