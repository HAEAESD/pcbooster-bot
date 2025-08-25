# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI(title="PCBooster Key API")

# 🔹 Mot de passe pour générer les clés
ADMIN_PASSWORD = "FcMMM2684"

# 🔹 Clés générées (pour éviter doublons)
used_keys = set()

class KeyRequest(BaseModel):
    admin_password: str

@app.post("/generate_key")
def generate_key(req: KeyRequest):
    if req.admin_password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Mot de passe incorrect")
    
    # Génération d’une clé unique
    key = str(uuid.uuid4())
    used_keys.add(key)
    return {"key": key}

@app.get("/")
def root():
    return {"message": "API PCBooster est en ligne !"}
