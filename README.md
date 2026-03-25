# 🔮 Système de Prédiction des Groupes — Orange Sonatel

> Outil d'aide à l'affectation automatique des plaintes clients  
> **DSI — Direction des Systèmes d'Information**

---

## 📸 Aperçu

### 🖐️ Écran de bienvenue
![Bienvenue](screenshots/bienvenue.png)

### 🖥️ Interface principale
![Interface](screenshots/interface.png)

### ✅ Résultat de prédiction
![Résultat](screenshots/resultat.png)

---

## 📌 Description

Ce projet est un système de machine learning développé dans le cadre d'un stage à **Orange Sonatel**.  
Il permet de prédire automatiquement le **groupe de traitement** d'une plainte client en fonction de ses caractéristiques.

---

## 🚀 Fonctionnalités

- 🎯 **Prédiction simple** — Sélectionner les paramètres et obtenir le groupe prédit avec un niveau de confiance
- 📂 **Prédiction en masse** — Uploader un fichier CSV et télécharger les résultats
- ℹ️ **Informations modèle** — Visualiser les détails du modèle (variables, groupes disponibles)
- 🎨 **Interface moderne** — Design aux couleurs Orange Sonatel avec animations et écran de bienvenue

---

## 🛠️ Technologies utilisées

| Technologie | Usage |
|---|---|
| Python | Langage principal |
| scikit-learn | Modèle Random Forest |
| Gradio | Interface web |
| pandas | Traitement des données |
| FastAPI | API REST |

---

## ⚙️ Installation

```bash
# Cloner le repo
git clone https://github.com/c9p2thg7z8-droid/orange-sonatel-prediction.git
cd orange-sonatel-prediction

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

---

## ▶️ Lancement

```bash
# Interface Gradio
python interface_gradio.py

# Ou site web complet
uvicorn api:app --reload
```

Ouvre ensuite **http://localhost:7860** (Gradio) ou **http://localhost:8000** (site web).

---

## 📁 Structure du projet

```
├── interface_gradio.py           # Interface Gradio principale
├── api.py                        # API FastAPI
├── index.html                    # Site web
├── pythonscriptpremeiretache.py  # Script d'entraînement du modèle
├── model_groupe.pkl              # Modèle entraîné
├── logo.png                      # Logo Orange Sonatel
├── requirements.txt              # Dépendances
└── screenshots/
    ├── bienvenue.png             # Écran de bienvenue
    ├── interface.png             # Interface principale
    └── resultat.png              # Résultat de prédiction
```

---

## 👤 Auteur

Développé par **Cheikh FAYE** — Stagiaire à la **DSI — Orange Sonatel**  
© 2025 Orange Sonatel
