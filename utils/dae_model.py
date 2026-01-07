import torch
import torch.nn as nn

class DenoisingAutoEncoder(nn.Module):
    """Denoising AutoEncoder pour recommandation de livres"""
    
    def __init__(self, num_items, latent_dim=64, dropout_prob=0.2):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(num_items, 256),
            nn.ReLU(),
            nn.Dropout(dropout_prob),
            nn.Linear(256, latent_dim),
            nn.ReLU(),
            nn.Dropout(dropout_prob)
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 256),
            nn.ReLU(),
            nn.Dropout(dropout_prob),
            nn.Linear(256, num_items),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))