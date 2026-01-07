
import pickle
import pandas as pd
import numpy as np
import torch
from typing import Optional, Dict, Any
import os

from utils.dae_model import DenoisingAutoEncoder

class ModelLoader:
    """Charge et gère le modèle DAE"""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.user_mapping = None
        self.isbn_mapping = None
        self.reverse_isbn_mapping = None
        self.is_loaded_flag = False
    
    def load_model(self) -> bool:
        """Charge le modèle depuis le fichier pickle"""
        try:
            if not os.path.exists(self.model_path):
                print(f"Fichier modèle introuvable: {self.model_path}")
                return False
            
            print(f"Chargement du modèle depuis {self.model_path}...")
            
            # Charger avec torch.load
            try:
                data = torch.load(self.model_path, map_location='cpu', weights_only=False)
                print("✅ Chargé avec torch.load")
            except Exception as e:
                print(f"❌ Erreur torch.load: {e}")
                return False
            
            # Vérifier le type de data
            if isinstance(data, dict):
                # Format: {'model': ..., 'user_mapping': ..., 'isbn_mapping': ...}
                print("Format: Dictionnaire")
                self.model = data.get('model')
                self.user_mapping = data.get('user_mapping', {})
                self.isbn_mapping = data.get('isbn_mapping', {})
            elif isinstance(data, DenoisingAutoEncoder):
                # Format: Le modèle directement (ERREUR - mappings manquants)
                print("⚠️ Format: Modèle seul (sans mappings)")
                print("❌ ERREUR: Le fichier .pkl doit contenir user_mapping et isbn_mapping")
                print("\nVotre modèle doit être sauvegardé comme:")
                print("torch.save({")
                print("    'model': model,")
                print("    'user_mapping': user_mapping,")
                print("    'isbn_mapping': isbn_mapping")
                print("}, 'dae_model.pkl')")
                return False
            else:
                print(f"⚠️ Format inconnu: {type(data)}")
                return False
            
            # Vérifications
            if not self.user_mapping:
                print("❌ ERREUR: user_mapping vide ou manquant")
                return False
            
            if not self.isbn_mapping:
                print("❌ ERREUR: isbn_mapping vide ou manquant")
                return False
            
            if self.model is None:
                print("❌ ERREUR: Modèle est None")
                return False
            
            # Créer le mapping inverse
            self.reverse_isbn_mapping = {
                v: k for k, v in self.isbn_mapping.items()
            }
            
            # Mode évaluation
            self.model.eval()
            
            self.is_loaded_flag = True
            print(f"✅ Modèle chargé avec succès!")
            print(f"   - Utilisateurs: {len(self.user_mapping)}")
            print(f"   - Livres: {len(self.isbn_mapping)}")
            
            sample_users = list(self.user_mapping.keys())[:5]
            print(f"   - Exemples IDs: {sample_users}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_user_vector(self, user_id: int) -> Optional[int]:
        if not self.is_loaded_flag:
            return None
        return self.user_mapping.get(user_id)
    
    def is_loaded(self) -> bool:
        return self.is_loaded_flag
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            'users': len(self.user_mapping) if self.user_mapping else 0,
            'books': len(self.isbn_mapping) if self.isbn_mapping else 0,
            'loaded': self.is_loaded_flag
        }