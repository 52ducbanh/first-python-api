from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

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
        "ans: ": tong,
        "note:" : "completed :)" 
    }
