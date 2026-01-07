import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration centrale de l'application"""
    
    # API Configuration
    GOOGLE_BOOKS_API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY', 'AIzaSyDQasuxSU4ZIvawpmPryrV_t6uQrXyb6gc')
    GOOGLE_BOOKS_BASE_URL = 'https://www.googleapis.com/books/v1/volumes'
    
    # Model Configuration
    MODEL_PATH = 'dae_model.pkl'
    MODEL_DIR = 'models'
    
    # App Configuration
    PAGE_TITLE = "📚 Système de Recommandation de Livres"
    PAGE_ICON = "📚"
    LAYOUT = "wide"
    
    # Recommendation Settings
    MAX_RECOMMENDATIONS = 20
    DEFAULT_RECOMMENDATIONS = 10
    MIN_RATING = 1
    MAX_RATING = 10
    
    # API Settings
    API_TIMEOUT = 5
    API_RATE_LIMIT_DELAY = 0.1
    
    # Data Paths
    DATA_DIR = 'data'
    RATINGS_FILE = os.path.join(DATA_DIR, 'ratings.csv')
    
    # Logging
    LOG_DIR = 'logs'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Valide la configuration"""
        if not cls.GOOGLE_BOOKS_API_KEY:
            print("⚠️ ATTENTION: Clé API Google Books non configurée!")
            print("   L'application fonctionnera avec limite de 100 requêtes/jour")
        else:
            print("✅ Clé API Google Books configurée")
        return True