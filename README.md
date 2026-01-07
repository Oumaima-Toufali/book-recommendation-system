# 📚 AI Book Recommendation System  
### Denoising Autoencoder (DAE) • Deep Learning • Streamlit

> 🚀 Système intelligent de recommandation de livres basé sur le **Deep Learning**, combinant **Denoising Autoencoder** et **filtrage collaboratif**, avec une **interface web interactive** prête pour un usage réel.

---

## 🎯 Pourquoi ce projet ?

Les systèmes de recommandation sont au cœur des plateformes modernes (Netflix, Amazon, Spotify).  
Ce projet démontre ma capacité à **concevoir, entraîner et déployer un modèle IA** complet, depuis les données jusqu’à l’interface utilisateur.

👉 **Objectif** : fournir des recommandations personnalisées et robustes à partir d’interactions utilisateurs-livres bruitées.

---

## 🧠 Approche technique

- 🔹 **Modèle** : Denoising Autoencoder (DAE)
- 🔹 **Paradigme** : Apprentissage non supervisé
- 🔹 **Données** : Matrice utilisateur–livre (ratings)
- 🔹 **Stratégie** :
  - Ajout de bruit pour améliorer la robustesse
  - Apprentissage d’une représentation latente
  - Reconstruction pour prédire les préférences

---

## 🖥️ Interface Utilisateur (Streamlit)

Interface web permettant une interaction simple et intuitive avec le modèle.

![User Interface](frontend/frontend.jpeg)

### Fonctionnalités UI :
- Sélection de l’utilisateur
- Choix du nombre de recommandations
- Visualisation des livres recommandés
- Récupération automatique des métadonnées (Google Books API)
- Export des résultats en CSV

---

## ✨ Fonctionnalités clés

- ✅ Recommandations personnalisées
- ✅ Modèle Deep Learning (PyTorch)
- ✅ Interface web prête pour démonstration
- ✅ Intégration API externe (Google Books)
- ✅ Optimisation des appels API (cache)
- ✅ Architecture modulaire et maintenable

---

## 🧩 Architecture du projet

```text
book-recommender-dae/
│
├── app.py                  # Application Streamlit
├── dae_model.pkl           # Modèle entraîné
├── config.py               # Configuration
├── utils/                  # Logique métier
│   ├── model_loader.py
│   ├── recommender.py
│   └── google_books.py
├── frontend/
│   └── frontend.jpeg       # UI Screenshot
├── data/                   # Données
├── tests/                  # Tests unitaires
└── README.md

---

##🛠️ Stack technologique
Domaine	Technologies
Langage	Python
Deep Learning	PyTorch
ML	Scikit-learn
Data	Pandas, NumPy
Web UI	Streamlit
API	Google Books API
Versioning	Git / GitHub

📊 Dataset
Book-Crossing Dataset

+1.1M évaluations

Plusieurs milliers d’utilisateurs

Données réelles et bruitées (cas réel)

--- 
##🚀 Installation rapide
bash
Copier le code
git clone <repo-url>
cd book-recommender-dae
pip install -r requirements.txt
streamlit run app.py
🔍 Cas d’usage métier
Plateformes e-commerce

Librairies en ligne

Applications éducatives

Systèmes de recommandation personnalisés

Proof of Concept IA
---
##📈 Évolutions possibles
🔄 Hybridation avec du content-based filtering

📊 Visualisation des embeddings

🧪 Feedback utilisateur (online learning)

🌐 API REST (FastAPI)

☁️ Déploiement Cloud / Docker
---
##👩‍💻 Profil & Compétences démontrées
✔ Deep Learning
✔ Systèmes de recommandation
✔ Data preprocessing
✔ Architecture logicielle
✔ Déploiement d’IA avec UI
✔ Intégration d’API externes

---
👤 Auteur
Oumaima Toufali
🎓 Data Science & Cloud Computing Engineer
💡 Intérêts : IA, ML, MLOps, systèmes intelligents