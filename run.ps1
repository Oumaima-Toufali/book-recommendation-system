
# Script de lancement de l'application Book Recommender

Write-Host \"\" -ForegroundColor Cyan
Write-Host \"====================================\" -ForegroundColor Cyan
Write-Host \"  Book Recommender DAE - Launcher  \" -ForegroundColor Cyan
Write-Host \"====================================\" -ForegroundColor Cyan
Write-Host \"\"

# Vérifier si l'environnement virtuel existe
if (-not (Test-Path \"venv\")) {
    Write-Host \"❌ Environnement virtuel non trouvé!\" -ForegroundColor Red
    Write-Host \"\"
    Write-Host \"Création de l'environnement virtuel...\" -ForegroundColor Yellow
    python -m venv venv
    Write-Host \"✅ Environnement virtuel créé!\" -ForegroundColor Green
    Write-Host \"\"
    Write-Host \"Installation des dépendances...\" -ForegroundColor Yellow
    & \"venv\Scripts\python.exe\" -m pip install --upgrade pip
    & \"venv\Scripts\pip.exe\" install -r requirements.txt
    Write-Host \"✅ Dépendances installées!\" -ForegroundColor Green
}

# Activer l'environnement virtuel
Write-Host \"📦 Activation de l'environnement virtuel...\" -ForegroundColor Yellow
& \"venv\Scripts\Activate.ps1\"

# Vérifier que le modèle existe
if (-not (Test-Path \"dae_model.pkl\")) {
    Write-Host \"\"
    Write-Host \"⚠️ ATTENTION: Fichier 'dae_model.pkl' non trouvé!\" -ForegroundColor Yellow
    Write-Host \"Placez votre modèle à la racine du projet avant de continuer.\" -ForegroundColor Yellow
    Write-Host \"\"
    Read-Host \"Appuyez sur Entrée pour continuer quand même ou Ctrl+C pour annuler\"
}

# Vérifier la configuration .env
if (-not (Test-Path \".env\")) {
    Write-Host \"\"
    Write-Host \"⚠️ Fichier .env non trouvé!\" -ForegroundColor Yellow
    Write-Host \"Création d'un fichier .env par défaut...\" -ForegroundColor Yellow
    @\"
GOOGLE_BOOKS_API_KEY=votre_clé_api_ici
DEBUG=False
LOG_LEVEL=INFO
\"@ | Out-File -FilePath \".env\" -Encoding UTF8
    Write-Host \"✅ Fichier .env créé. N'oubliez pas d'ajouter votre clé API!\" -ForegroundColor Green
}

Write-Host \"\"
Write-Host \"🌐 Lancement de Streamlit...\" -ForegroundColor Green
Write-Host \"\"
Write-Host \"📌 L'application s'ouvrira dans votre navigateur\" -ForegroundColor Cyan
Write-Host \"📌 URL: http://localhost:8501\" -ForegroundColor Cyan
Write-Host \"📌 Pour arrêter: Ctrl+C\" -ForegroundColor Cyan
Write-Host \"\"

# Lancer Streamlit
streamlit run app.py
