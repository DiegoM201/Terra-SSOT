import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Unit, Tribe

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/units")
def save_unit(unit: Unit):
    try:
        os.makedirs("data/units", exist_ok=True)
        with open(f"data/units/{unit.id}.json", "w") as f:
            f.write(unit.model_dump_json(indent=4))
        return {"status": "success", "file": f"{unit.id}.json"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tribes")
def save_tribe(tribe: Tribe):
    try:
        os.makedirs("data/tribes", exist_ok=True)
        with open(f"data/tribes/{tribe.id}.json", "w") as f:
            f.write(tribe.model_dump_json(indent=4))
        return {"status": "success", "file": f"{tribe.id}.json"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
