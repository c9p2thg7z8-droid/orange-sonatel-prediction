import gradio as gr
import pickle
import pandas as pd
import base64

def image_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

LOGO_B64 = image_to_base64("logo.png")
MODEL_PATH = "model_groupe.pkl"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

* { box-sizing: border-box; }

body, .gradio-container {
    font-family: 'Inter', sans-serif !important;
    background: #f5f5f5 !important;
}

.gradio-container {
    max-width: 1000px !important;
    margin: auto !important;
    padding: 0 !important;
    background: transparent !important;
}

/* ── HEADER ── */
.header-wrap {
    background: linear-gradient(135deg, #FF6600 0%, #ff8c00 60%, #008080 100%);
    border-radius: 0 0 32px 32px;
    padding: 28px 40px 36px;
    margin-bottom: 28px;
    box-shadow: 0 8px 32px rgba(255,102,0,0.35);
    position: relative;
    overflow: hidden;
}

.header-wrap::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}

.header-wrap::after {
    content: '';
    position: absolute;
    bottom: -40px; left: -40px;
    width: 160px; height: 160px;
    background: rgba(0,128,128,0.15);
    border-radius: 50%;
}

.logo-box {
    background: white;
    border-radius: 16px;
    padding: 12px 28px;
    display: inline-block;
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    margin-bottom: 18px;
}

.logo-box img { height: 60px; display: block; }

.header-title {
    color: white !important;
    font-size: 28px !important;
    font-weight: 800 !important;
    margin: 0 0 6px !important;
    letter-spacing: -0.5px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.header-sub {
    color: rgba(255,255,255,0.88) !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    margin: 0 !important;
}

/* ── TABS ── */
.tab-nav {
    background: white !important;
    border-radius: 16px !important;
    padding: 6px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08) !important;
    margin-bottom: 20px !important;
    border: none !important;
}

.tab-nav button {
    border-radius: 12px !important;
    border: none !important;
    color: #666 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 10px 20px !important;
    transition: all 0.2s !important;
    background: transparent !important;
}

.tab-nav button.selected {
    background: linear-gradient(135deg, #FF6600, #ff8c00) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(255,102,0,0.35) !important;
}

/* ── CARDS ── */
.card {
    background: white;
    border-radius: 20px;
    padding: 28px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.07);
    border: 1px solid rgba(255,102,0,0.1);
    margin-bottom: 16px;
}

.section-title {
    color: #FF6600 !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 16px !important;
    padding-bottom: 10px;
    border-bottom: 2px solid #fff0e6;
}

/* ── LABELS & INPUTS ── */
label span {
    color: #444 !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.gr-box, .gr-form, .wrap {
    background: white !important;
    border: 1.5px solid #ffe0cc !important;
    border-radius: 12px !important;
    box-shadow: none !important;
}

select, input[type=text], textarea {
    background: #fafafa !important;
    border: 1.5px solid #ffe0cc !important;
    border-radius: 10px !important;
    color: #222 !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
    transition: border 0.2s, box-shadow 0.2s !important;
}

select:focus, input:focus {
    border-color: #FF6600 !important;
    box-shadow: 0 0 0 3px rgba(255,102,0,0.12) !important;
    outline: none !important;
}

/* ── BOUTON PRINCIPAL ── */
button.primary {
    background: linear-gradient(135deg, #FF6600 0%, #ff8c00 100%) !important;
    border: none !important;
    border-radius: 14px !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 14px 36px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 6px 20px rgba(255,102,0,0.38) !important;
    letter-spacing: 0.3px;
}

button.primary:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 32px rgba(255,102,0,0.5) !important;
}

button.primary:active {
    transform: translateY(0px) !important;
}

/* ── RÉSULTATS ── */
.result-card {
    background: linear-gradient(135deg, #fff8f3, #f0fafa);
    border-radius: 16px;
    border: 2px solid transparent;
    background-clip: padding-box;
    position: relative;
}

.result-box textarea {
    background: transparent !important;
    border: 2px solid #008080 !important;
    border-radius: 14px !important;
    color: #005f5f !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    text-align: center !important;
    padding: 16px !important;
    box-shadow: 0 4px 16px rgba(0,128,128,0.12) !important;
}

.result-box label span {
    color: #008080 !important;
}

/* ── BADGE STATS ── */
.stat-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #fff0e6, #ffe8d6);
    border: 1px solid #ffccaa;
    border-radius: 50px;
    padding: 8px 18px;
    font-size: 13px;
    font-weight: 600;
    color: #cc4400;
    margin: 4px;
}

/* ── CSV TAB ── */
.upload-zone {
    border: 2px dashed #ffccaa !important;
    border-radius: 16px !important;
    background: #fff8f3 !important;
    padding: 32px !important;
    text-align: center;
    transition: all 0.2s;
}

.upload-zone:hover {
    border-color: #FF6600 !important;
    background: #fff3ea !important;
}

/* ── INFO TAB ── */
.info-box textarea {
    background: #f8fffe !important;
    border: 1.5px solid #b2dfdf !important;
    border-radius: 14px !important;
    color: #004d4d !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
}

/* ── DIVIDER ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #ffccaa, transparent);
    margin: 20px 0;
}

footer { display: none !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f5f5f5; }
::-webkit-scrollbar-thumb { background: #FF6600; border-radius: 3px; }
"""


# -----------------------------------
# 1. Charger le modèle
# -----------------------------------
def charger_modele():
    try:
        bundle = pickle.load(open(MODEL_PATH, "rb"))
        return bundle["model"], bundle["encoders"], bundle["features"]
    except Exception as e:
        print("Erreur chargement modèle :", e)
        return None, None, None


model, encoders, features = charger_modele()


def get_choices(col):
    try:
        return sorted(encoders[col].classes_.tolist())
    except:
        return []


def get_stats():
    try:
        return len(get_choices("DOMAINE")), len(get_choices("TYPE")), len(encoders["GROUPE"].classes_)
    except:
        return 0, 0, 0


nb_domaines, nb_types, nb_groupes = get_stats()


# -----------------------------------
# 2. Prédiction simple
# -----------------------------------
def predire_interface(domaine, sous_domaine, type_, typologie):
    try:
        if not domaine or not sous_domaine or not type_ or not typologie:
            return """<div style="background:#fff3cd;border:2px solid #ffc107;border-radius:16px;
                        padding:24px;text-align:center;">
                <div style="font-size:36px;">⚠️</div>
                <div style="color:#856404;font-weight:700;font-size:15px;margin-top:8px;">Veuillez remplir tous les champs</div>
            </div>"""

        vals = {
            "DOMAINE": domaine.strip().upper(),
            "SOUS-DOMAINE": sous_domaine.strip().upper(),
            "TYPE": type_.strip().upper(),
            "TYPOLOGIE": typologie.strip().upper()
        }
        row = []
        inconnues = []
        for col in features:
            le = encoders[col]
            v = vals[col]
            if v not in le.classes_:
                inconnues.append(col)
                v = le.classes_[0]
            row.append(le.transform([v])[0])

        if inconnues:
            return f"""<div style="background:#fff3cd;border:2px solid #ffc107;border-radius:16px;
                        padding:24px;text-align:center;">
                <div style="font-size:36px;">⚠️</div>
                <div style="color:#856404;font-weight:700;font-size:16px;margin-top:8px;">Valeurs inconnues détectées</div>
                <div style="color:#856404;font-size:13px;margin-top:6px;">{', '.join(inconnues)}</div>
            </div>"""

        pred = model.predict([row])[0]
        proba = model.predict_proba([row])[0].max()
        groupe = encoders["GROUPE"].inverse_transform([pred])[0]
        pct = int(proba * 100)

        if pct >= 75:
            color, bg, icon, bar = "#005f5f", "linear-gradient(135deg,#e6f7f7,#b2dfdf)", "✅", "#008080"
        elif pct >= 50:
            color, bg, icon, bar = "#cc4400", "linear-gradient(135deg,#fff3e0,#ffe0b2)", "🟡", "#FF6600"
        else:
            color, bg, icon, bar = "#7f0000", "linear-gradient(135deg,#fdecea,#ffcdd2)", "⚠️", "#e53935"

        return f"""
        <div style="background:{bg};border-radius:20px;padding:32px;text-align:center;
                    box-shadow:0 8px 32px rgba(0,0,0,0.12);animation:fadeIn 0.4s ease;">
            <style>@keyframes fadeIn{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:translateY(0)}}}}</style>
            <div style="font-size:52px;margin-bottom:10px;">{icon}</div>
            <div style="color:#888;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;">Groupe prédit</div>
            <div style="color:{color};font-size:28px;font-weight:800;margin:8px 0 24px;letter-spacing:-0.5px;">{groupe}</div>
            <div style="color:#888;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">Niveau de confiance</div>
            <div style="background:rgba(0,0,0,0.08);border-radius:50px;height:14px;overflow:hidden;margin:0 auto;max-width:320px;">
                <div style="background:{bar};height:100%;width:{pct}%;border-radius:50px;
                            box-shadow:0 2px 8px rgba(0,0,0,0.2);"></div>
            </div>
            <div style="color:{color};font-size:26px;font-weight:800;margin-top:12px;">{pct}%</div>
        </div>"""
    except Exception as e:
        return f"<div style='color:red;padding:20px;text-align:center;'>❌ Erreur : {str(e)}</div>"


# -----------------------------------
# 3. Prédiction CSV
# -----------------------------------
def predire_csv(file):
    try:
        df = pd.read_csv(file.name, sep=";")
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
        output = "predictions.csv"
        df.to_csv(output, sep=";", index=False)
        return output
    except Exception as e:
        return str(e)


# -----------------------------------
# 4. Informations du modèle
# -----------------------------------
def info_modele():
    try:
        groupes = encoders["GROUPE"].classes_.tolist()
        return f"""✅ Modèle chargé avec succès

📊 Nombre de variables d'entrée : {len(features)}
📋 Variables utilisées : {', '.join(features)}

🎯 Nombre de groupes prédictibles : {len(groupes)}
📁 Groupes disponibles :
   {chr(10).join(f'   • {g}' for g in groupes)}"""
    except:
        return "❌ Impossible de lire les informations du modèle"


# -----------------------------------
# 5. Interface Gradio
# -----------------------------------
with gr.Blocks(css=CSS, title="Orange Sonatel — Prédiction GROUPE") as app:

    # SPLASH / BIENVENUE
    gr.HTML(f"""
    <div id="splash" style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:9999;
        background:linear-gradient(135deg,#FF6600,#ff8c00 50%,#008080);
        display:flex;flex-direction:column;align-items:center;justify-content:center;
        animation:splashOut 0.6s ease 2.8s forwards;">
        <style>
            @keyframes splashOut{{to{{opacity:0;pointer-events:none;visibility:hidden;}}}}
            @keyframes popIn{{from{{opacity:0;transform:scale(0.85)}}to{{opacity:1;transform:scale(1)}}}}
            @keyframes slideUp{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:translateY(0)}}}}
        </style>
        <div style="background:white;border-radius:20px;padding:16px 36px;margin-bottom:28px;
                    box-shadow:0 8px 32px rgba(0,0,0,0.2);animation:popIn 0.5s ease;">
            <img src="data:image/png;base64,{LOGO_B64}" style="height:64px;display:block;"/>
        </div>
        <h1 style="color:white;font-size:30px;font-weight:800;margin:0 0 10px;
                   text-shadow:0 2px 12px rgba(0,0,0,0.2);animation:slideUp 0.5s ease 0.2s both;">
            Bienvenue 👋
        </h1>
        <p style="color:rgba(255,255,255,0.9);font-size:16px;margin:0 0 6px;
                  animation:slideUp 0.5s ease 0.35s both;">
            Système de Prédiction des Groupes
        </p>
        <p style="color:rgba(255,255,255,0.75);font-size:13px;
                  animation:slideUp 0.5s ease 0.5s both;">
            Outil d’affectation automatique des plaintes clients
        </p>
        <div style="margin-top:22px;background:rgba(255,255,255,0.18);border:2px solid rgba(255,255,255,0.4);border-radius:16px;padding:16px 40px;text-align:center;animation:slideUp 0.5s ease 0.55s both;">
            <div style="color:white;font-size:32px;font-weight:900;letter-spacing:6px;text-shadow:0 2px 12px rgba(0,0,0,0.2);">DSI</div>
            <div style="color:rgba(255,255,255,0.95);font-size:13px;font-weight:600;letter-spacing:0.5px;margin-top:4px;">Direction des Systèmes d’Information</div>
        </div>
        <div style="margin-top:24px;display:flex;gap:8px;animation:slideUp 0.5s ease 0.65s both;">
            <div style="width:8px;height:8px;background:rgba(255,255,255,0.9);border-radius:50%;
                        animation:pulse 1s ease 0.8s infinite;"></div>
            <div style="width:8px;height:8px;background:rgba(255,255,255,0.6);border-radius:50%;
                        animation:pulse 1s ease 1s infinite;"></div>
            <div style="width:8px;height:8px;background:rgba(255,255,255,0.3);border-radius:50%;
                        animation:pulse 1s ease 1.2s infinite;"></div>
        </div>
        <style>@keyframes pulse{{0%,100%{{transform:scale(1);opacity:0.6}}50%{{transform:scale(1.4);opacity:1}}}}</style>
    </div>
    """)

    # HEADER
    gr.HTML(f"""
    <div class="header-wrap">
        <div class="logo-box">
            <img src="data:image/png;base64,{LOGO_B64}" alt="Orange Sonatel" />
        </div>
        <h1 class="header-title">Système de Prédiction des Groupes</h1>
        <p class="header-sub">Outil d'aide à l'affectation automatique des plaintes clients</p>
        <div style="margin-top:18px; display:flex; gap:10px; flex-wrap:wrap;">
            <span class="stat-badge">📂 {nb_domaines} Domaines</span>
            <span class="stat-badge">🔖 {nb_types} Types</span>
            <span class="stat-badge">🎯 {nb_groupes} Groupes</span>
        </div>
    </div>
    """)

    with gr.Tab("🎯 Prédiction simple"):

        gr.HTML('<p class="section-title">📋 Paramètres de la plainte</p>')

        with gr.Row():
            with gr.Column():
                domaine = gr.Dropdown(choices=get_choices("DOMAINE"), label="Domaine", interactive=True, allow_custom_value=True)
                sous_domaine = gr.Dropdown(choices=get_choices("SOUS-DOMAINE"), label="Sous-domaine", interactive=True, allow_custom_value=True)
            with gr.Column():
                type_ = gr.Dropdown(choices=get_choices("TYPE"), label="Type", interactive=True, allow_custom_value=True)
                typologie = gr.Dropdown(choices=get_choices("TYPOLOGIE"), label="Typologie", interactive=True, allow_custom_value=True)

        gr.HTML('<div class="divider"></div>')

        bouton = gr.Button("🚀  Lancer la prédiction", variant="primary")

        gr.HTML('<p class="section-title" style="margin-top:20px;">📊 Résultat</p>')

        resultat = gr.HTML("")

        bouton.click(predire_interface, inputs=[domaine, sous_domaine, type_, typologie], outputs=[resultat])

    with gr.Tab("📂 Prédiction en masse (CSV)"):

        gr.HTML("""
        <div style="background:#fff8f3;border:2px dashed #ffccaa;border-radius:16px;padding:20px;text-align:center;margin-bottom:16px;">
            <p style="color:#cc4400;font-weight:600;margin:0;">📎 Format attendu : colonnes DOMAINE, SOUS-DOMAINE, TYPE, TYPOLOGIE séparées par <b>;</b></p>
        </div>
        """)

        fichier = gr.File(label="📁 Uploader votre fichier CSV")
        bouton_csv = gr.Button("⚡  Générer les prédictions", variant="primary")
        sortie = gr.File(label="⬇️ Télécharger le fichier résultat")

        bouton_csv.click(predire_csv, inputs=fichier, outputs=sortie)

    with gr.Tab("ℹ️ Informations modèle"):

        gr.HTML('<p class="section-title">🔬 Détails techniques du modèle</p>')
        info_btn = gr.Button("🔍  Afficher les informations", variant="primary")
        texte_info = gr.Textbox(label="Rapport du modèle", lines=14, elem_classes=["info-box"], interactive=False)

        info_btn.click(info_modele, outputs=texte_info)

    gr.HTML("""
    <div style="text-align:center;padding:20px 0 10px;color:#aaa;font-size:12px;">
        © 2025 Orange Sonatel — Outil interne de classification des plaintes
    </div>
    """)

app.launch(share=True, show_api=False)
