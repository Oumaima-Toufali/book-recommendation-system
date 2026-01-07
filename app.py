import streamlit as st
import pandas as pd
import logging
from datetime import datetime
from config import Config
from utils.model_loader import ModelLoader
from utils.google_books import GoogleBooksAPI
from utils.recommender import BookRecommender
from utils.dae_model import DenoisingAutoEncoder

# Configuration de la page
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout=Config.LAYOUT,
    initial_sidebar_state="expanded"
)

# Validation de la configuration
Config.validate()

# Style CSS personnalisé
st.markdown("""
    <style>
    .book-container {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background: #fafafa;
    }
    .score-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 5px 15px;
        border-radius: 20px;
        color: white;
        font-weight: bold;
        display: inline-block;
        margin: 5px 0;
    }
    .header-title {
        text-align: center;
        color: #2c3e50;
        padding: 20px;
        font-size: 2.5em;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

# Initialisation
@st.cache_resource
def init_components():
    """Initialise les composants de l'application"""
    model_loader = ModelLoader(Config.MODEL_PATH)
    if not model_loader.load_model():
        st.error("Impossible de charger le modèle. Vérifiez que 'dae_model.pkl' existe.")
        st.stop()
    
    api = GoogleBooksAPI(
        Config.GOOGLE_BOOKS_API_KEY,
        Config.GOOGLE_BOOKS_BASE_URL
    )
    
    recommender = BookRecommender(model_loader, api)
    
    return model_loader, api, recommender

# Chargement
try:
    model_loader, api, recommender = init_components()
except Exception as e:
    st.error(f"Erreur d'initialisation: {e}")
    st.stop()

# En-tête
st.markdown(
    f'<div class="header-title">{Config.PAGE_TITLE}</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    stats = model_loader.get_stats()
    
    if stats['users'] > 0:
        # Récupérer tous les User-IDs disponibles
        available_user_ids = sorted(model_loader.user_mapping.keys())
        
        # Selectbox avec les vrais User-IDs
        user_id = st.selectbox(
            "Choisissez un utilisateur",
            options=available_user_ids,
            index=0,
            help=f"{len(available_user_ids)} utilisateurs disponibles"
        )
        
        # Afficher quelques exemples
        st.caption(f"📋 Exemples d'IDs : {', '.join(map(str, available_user_ids[:5]))}...")
        
    else:
        st.error("Aucun utilisateur trouvé dans le modèle")
        st.stop()
    
    n_recommendations = st.slider(
        "Nombre de recommandations",
        min_value=5,
        max_value=Config.MAX_RECOMMENDATIONS,
        value=Config.DEFAULT_RECOMMENDATIONS
    )
    
    st.markdown("---")
    
    st.subheader("📊 Statistiques du modèle")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("👥 Utilisateurs", stats['users'])
    with col2:
        st.metric("📚 Livres", stats['books'])
    
    st.markdown("---")
    
    st.subheader("ℹ️ À propos")
    st.info(
        "Ce système utilise un **Denoising Autoencoder (DAE)** "
        "pour générer des recommandations personnalisées."
    )

# Corps principal
st.header("🎯 Vos recommandations personnalisées")

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    generate_btn = st.button("🚀 Générer les recommandations", type="primary", use_container_width=True)
with col2:
    if st.button("🔄 Rafraîchir", use_container_width=True):
        st.rerun()
with col3:
    show_details = st.checkbox("📖 Détails", value=True)

if generate_btn:
    with st.spinner("🔍 Recherche des meilleurs livres..."):
        recommendations = recommender.get_recommendations(
            user_id,
            n_recommendations
        )
    
    if recommendations:
        st.success(f"✅ {len(recommendations)} livres trouvés!")
        
        # Option d'export
        export_df = pd.DataFrame([
            {
                'Rang': idx,
                'Titre': book['title'],
                'Auteurs': ', '.join(book['authors']),
                'Score': f"{score:.2f}",
                'ISBN': isbn,
                'Éditeur': book['publisher'],
                'Date': book['published_date']
            }
            for idx, (isbn, score, book) in enumerate(recommendations, 1)
        ])
        
        csv = export_df.to_csv(index=False)
        st.download_button(
            label="📥 Télécharger les recommandations (CSV)",
            data=csv,
            file_name=f"recommendations_user_{user_id}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        
        # Affichage des recommandations
        for idx, (isbn, score, book) in enumerate(recommendations, 1):
            with st.container():
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.image(book['thumbnail'], use_column_width=True)
                
                with col2:
                    st.markdown(f"### {idx}. {book['title']}")
                    st.markdown(f"**✍️ Auteur(s):** {', '.join(book['authors'])}")
                    st.markdown(f"**📖 Éditeur:** {book['publisher']}")
                    st.markdown(
                        f'<span class="score-badge">⭐ Score: {score:.2f}</span>',
                        unsafe_allow_html=True
                    )
                    
                    if show_details:
                        with st.expander("📋 Plus de détails"):
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.write(f"**📅 Date:** {book['published_date']}")
                                st.write(f"**📄 Pages:** {book['page_count']}")
                                st.write(f"**🌐 Langue:** {book['language']}")
                            with col_b:
                                if book['average_rating'] != 'N/A':
                                    st.write(f"**⭐ Note moyenne:** {book['average_rating']}/5")
                                st.write(f"**👥 Évaluations:** {book['ratings_count']}")
                                if book['categories']:
                                    st.write(f"**🏷️ Catégories:** {', '.join(book['categories'][:3])}")
                            
                            st.write("**📝 Description:**")
                            desc = book['description']
                            if len(desc) > 400:
                                desc = desc[:400] + "..."
                            st.write(desc)
                            
                            if book['preview_link'] != '#':
                                st.link_button("🔗 Voir sur Google Books", book['preview_link'])
                
                st.markdown("---")
    
    else:
        st.warning("⚠️ Aucune recommandation trouvée pour cet utilisateur.")
        st.info("💡 Essayez avec un autre ID utilisateur.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 20px;'>"
    "Développé avec ❤️ | Filtrage Collaboratif & DAE | Powered by Streamlit"
    "</div>",
    unsafe_allow_html=True
)