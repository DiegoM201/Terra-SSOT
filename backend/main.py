from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
import os
import json
from models import Unit, Tribe

app = FastAPI(title="Terra Forge Compiler API")

# Enable CORS for the local React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production if needed, but this is a local dev tool
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup data directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
UNITS_DIR = os.path.join(DATA_DIR, "units")
TRIBES_DIR = os.path.join(DATA_DIR, "tribes")

os.makedirs(UNITS_DIR, exist_ok=True)
os.makedirs(TRIBES_DIR, exist_ok=True)

@app.post("/api/units")
def create_unit(unit: Unit):
    try:
        filename = f"{unit.name.lower().replace(' ', '_')}.json"
        file_path = os.path.join(UNITS_DIR, filename)
        with open(file_path, "w") as f:
            # Output perfectly formatted JSON for the headless engine
            json.dump(unit.model_dump(), f, indent=4)
        return {"message": f"Unit '{unit.name}' saved successfully.", "file": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tribes")
def create_tribe(tribe: Tribe):
    try:
        filename = f"{tribe.name.lower().replace(' ', '_')}.json"
        file_path = os.path.join(TRIBES_DIR, filename)
        with open(file_path, "w") as f:
            # Output perfectly formatted JSON for the headless engine
            json.dump(tribe.model_dump(), f, indent=4)
        return {"message": f"Tribe '{tribe.name}' saved successfully.", "file": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
