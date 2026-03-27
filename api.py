from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pickle, pandas as pd, io, os, requests

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="."), name="static")

bundle = pickle.load(open("model_groupe.pkl", "rb"))
model, encoders, features = bundle["model"], bundle["encoders"], bundle["features"]

HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.3"

def get_choices(col):
    try: return sorted(encoders[col].classes_.tolist())
    except: return []

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

@app.get("/choices")
def choices():
    return {
        "domaines": get_choices("DOMAINE"),
        "sous_domaines": get_choices("SOUS-DOMAINE"),
        "types": get_choices("TYPE"),
        "typologies": get_choices("TYPOLOGIE"),
        "nb_groupes": len(encoders["GROUPE"].classes_),
        "groupes": encoders["GROUPE"].classes_.tolist()
    }

@app.post("/predict")
def predict(p: Plainte):
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
async def predict_csv(file: UploadFile = File(...)):
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
def chat(msg: ChatMessage):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    prompt = f"[INST] Tu es un assistant DSI Orange Sonatel. Reponds en francais.\n\n{msg.message} [/INST]"
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 300, "temperature": 0.7, "return_full_text": False}
    }
    try:
        r = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        result = r.json()
        if isinstance(result, list) and len(result) > 0:
            return {"response": result[0]["generated_text"].strip()}
        if isinstance(result, dict) and "error" in result:
            return {"response": result["error"]}
        return {"response": str(result)}
    except Exception as e:
        return {"response": f"Erreur : {str(e)}"}
