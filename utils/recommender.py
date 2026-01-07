import numpy as np
import pandas as pd
import torch
from typing import List, Dict, Tuple, Optional

class BookRecommender:
    """Génère des recommandations de livres"""
    
    def __init__(self, model_loader, google_books_api):
        self.model_loader = model_loader
        self.api = google_books_api
    
    def get_recommendations(
        self,
        user_id: int,
        n_recommendations: int = 10,
        exclude_rated: bool = True
    ) -> List[Tuple[str, float, Dict]]:
        """Génère des recommandations pour un utilisateur"""
        try:
            if not self.model_loader.is_loaded():
                print("Modèle non chargé")
                return []
            
            if user_id not in self.model_loader.user_mapping:
                print(f"Utilisateur {user_id} non trouvé")
                return []
            
            user_idx = self.model_loader.user_mapping[user_id]
            num_books = len(self.model_loader.isbn_mapping)
            user_vector = np.zeros(num_books)
            
            with torch.no_grad():
                user_tensor = torch.FloatTensor(user_vector).unsqueeze(0)
                predictions = self.model_loader.model(user_tensor).squeeze(0).numpy()
            
            recommendations_df = pd.DataFrame({
                'isbn': list(self.model_loader.isbn_mapping.keys()),
                'score': predictions
            })
            
            recommendations_df = recommendations_df.sort_values('score', ascending=False)
            buffer = min(n_recommendations * 2, len(recommendations_df))
            top_recommendations = recommendations_df.head(buffer)
            
            results = []
            for _, row in top_recommendations.iterrows():
                if len(results) >= n_recommendations:
                    break
                
                isbn = row['isbn']
                score = float(row['score'])
                book_info = self.api.search_by_isbn(isbn)
                
                if book_info:
                    results.append((isbn, score, book_info))
            
            return results
            
        except Exception as e:
            print(f"Erreur lors de la génération des recommandations: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_user_stats(self, user_id: int) -> Optional[Dict]:
        """Récupère les statistiques d'un utilisateur"""
        if user_id not in self.model_loader.user_mapping:
            return None
        
        return {
            'user_id': user_id,
            'exists': True,
            'user_index': self.model_loader.user_mapping[user_id]
        }