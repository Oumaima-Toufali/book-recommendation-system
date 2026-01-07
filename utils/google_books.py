import requests
from typing import Dict, List, Optional
import time

class GoogleBooksAPI:
    """Interface pour l'API Google Books"""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self._cache = {}
    
    def search_by_isbn(self, isbn: str) -> Optional[Dict]:
        """Recherche un livre par ISBN"""
        if isbn in self._cache:
            return self._cache[isbn]
        
        try:
            params = {'q': f'isbn:{isbn}'}
            
            if self.api_key:
                params['key'] = self.api_key
            
            response = self.session.get(self.base_url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('totalItems', 0) > 0:
                    book_info = self._parse_book_info(data['items'][0])
                    self._cache[isbn] = book_info
                    return book_info
            elif response.status_code == 403:
                print("Limite API atteinte ou clé invalide")
            
            return None
            
        except requests.exceptions.Timeout:
            print(f"Timeout pour ISBN {isbn}")
            return None
        except Exception as e:
            print(f"Erreur API pour ISBN {isbn}: {e}")
            return None
    
    def _parse_book_info(self, item: Dict) -> Dict:
        """Parse les informations du livre"""
        volume_info = item.get('volumeInfo', {})
        
        return {
            'isbn': self._extract_isbn(volume_info),
            'title': volume_info.get('title', 'Titre non disponible'),
            'authors': volume_info.get('authors', ['Auteur inconnu']),
            'publisher': volume_info.get('publisher', 'Éditeur inconnu'),
            'published_date': volume_info.get('publishedDate', 'N/A'),
            'description': volume_info.get('description', 'Pas de description disponible'),
            'page_count': volume_info.get('pageCount', 'N/A'),
            'categories': volume_info.get('categories', []),
            'language': volume_info.get('language', 'N/A'),
            'thumbnail': volume_info.get('imageLinks', {}).get(
                'thumbnail', 
                'https://via.placeholder.com/128x200?text=No+Cover'
            ).replace('http://', 'https://'),
            'preview_link': volume_info.get('previewLink', '#'),
            'average_rating': volume_info.get('averageRating', 'N/A'),
            'ratings_count': volume_info.get('ratingsCount', 0)
        }
    
    def _extract_isbn(self, volume_info: Dict) -> str:
        """Extrait l'ISBN du livre"""
        identifiers = volume_info.get('industryIdentifiers', [])
        for identifier in identifiers:
            if identifier.get('type') in ['ISBN_13', 'ISBN_10']:
                return identifier.get('identifier', '')
        return ''
    
    def batch_search(self, isbn_list: List[str], delay: float = 0.1) -> Dict[str, Dict]:
        """Recherche plusieurs livres avec rate limiting"""
        results = {}
        total = len(isbn_list)
        
        for idx, isbn in enumerate(isbn_list, 1):
            print(f"Recherche {idx}/{total}: {isbn}")
            book_info = self.search_by_isbn(isbn)
            
            if book_info:
                results[isbn] = book_info
            
            time.sleep(delay)
        
        return results