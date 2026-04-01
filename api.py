from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import pickle, pandas as pd, io, os, requests, hashlib, secrets

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="."), name="static")

bundle = pickle.load(open("model_groupe.pkl", "rb"))
model, encoders, features = bundle["model"], bundle["encoders"], bundle["features"]

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
OLLAMA_URL = "http://localhost:11434/api/chat"

# Utilisateurs (mot de passe hashé SHA256)
USERS = {
    "admin": hashlib.sha256("orange2025".encode()).hexdigest(),
    "agent": hashlib.sha256("sonatel2025".encode()).hexdigest(),
}

# Tokens actifs en mémoire
active_tokens = {}

security = HTTPBearer(auto_error=False)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials or credentials.credentials not in active_tokens.values():
        raise HTTPException(status_code=401, detail="Non autorisé")
    return credentials.credentials

def get_choices(col):
    try: return sorted(encoders[col].classes_.tolist())
    except: return []

class LoginData(BaseModel):
    username: str
    password: str

class Plainte(BaseModel):
    domaine: str
    sous_domaine: str
    type_: str
    typologie: str

class ChatMessage(BaseModel):
    message: str

@app.get("/")
def index():
    return FileResponse("index.html")

@app.post("/login")
def login(data: LoginData):
    hashed = hashlib.sha256(data.password.encode()).hexdigest()
    if data.username in USERS and USERS[data.username] == hashed:
        token = secrets.token_hex(32)
        active_tokens[data.username] = token
        return {"token": token, "username": data.username}
    raise HTTPException(status_code=401, detail="Identifiants incorrects")

@app.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials:
        for user, tok in list(active_tokens.items()):
            if tok == credentials.credentials:
                del active_tokens[user]
    return {"message": "Déconnecté"}

@app.get("/choices")
def choices(token=Depends(verify_token)):
    return {
        "domaines": get_choices("DOMAINE"),
        "sous_domaines": get_choices("SOUS-DOMAINE"),
        "types": get_choices("TYPE"),
        "typologies": get_choices("TYPOLOGIE"),
        "nb_groupes": len(encoders["GROUPE"].classes_),
        "groupes": encoders["GROUPE"].classes_.tolist()
    }

@app.post("/predict")
def predict(p: Plainte, token=Depends(verify_token)):
    vals = {
        "DOMAINE": p.domaine.strip().upper(),
        "SOUS-DOMAINE": p.sous_domaine.strip().upper(),
        "TYPE": p.type_.strip().upper(),
        "TYPOLOGIE": p.typologie.strip().upper()
    }
    row, inconnues = [], []
    for col in features:
        le = encoders[col]
        v = vals[col]
        if v not in le.classes_:
            inconnues.append(col)
            v = le.classes_[0]
        row.append(le.transform([v])[0])
    if inconnues:
        return {"error": f"Valeurs inconnues : {', '.join(inconnues)}"}
    pred = model.predict([row])[0]
    proba = model.predict_proba([row])[0].max()
    groupe = encoders["GROUPE"].inverse_transform([pred])[0]
    return {"groupe": groupe, "confiance": round(float(proba) * 100, 1)}

@app.post("/predict-csv")
async def predict_csv(file: UploadFile = File(...), token=Depends(verify_token)):
    content = await file.read()
    df = pd.read_csv(io.StringIO(content.decode("utf-8")), sep=";")
    for col in features:
        df[col] = df[col].astype(str).str.strip().str.upper()
    X = df[features].copy()
    for col in features:
        le = encoders[col]
        X[col] = X[col].apply(lambda v: v if v in le.classes_ else le.classes_[0])
        X[col] = le.transform(X[col])
    preds = model.predict(X)
    probas = model.predict_proba(X).max(axis=1)
    df["GROUPE_PREDIT"] = encoders["GROUPE"].inverse_transform(preds)
    df["CONFIANCE"] = (probas * 100).round(1).astype(str) + "%"
    return df.to_dict(orient="records")

@app.post("/chat")
def chat(msg: ChatMessage, token=Depends(verify_token)):
    payload = {
        "model": "mistral",
        "messages": [
            {"role": "system", "content": "Tu es un assistant intelligent de la DSI Orange Sonatel. Tu aides les agents a traiter les plaintes clients. Reponds toujours en francais de maniere concise et professionnelle."},
            {"role": "user", "content": msg.message}
        ],
        "stream": False
    }
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        if r.status_code != 200:
            return {"response": f"Erreur Ollama {r.status_code}: {r.text[:200]}"}
        return {"response": r.json()["message"]["content"].strip()}
    except Exception as e:
        return {"response": f"Erreur : {str(e)}"}
