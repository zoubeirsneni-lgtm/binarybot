import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="BinaryBot Admin",
    page_icon="🤖",
    layout="wide"
)

# Titre principal
st.title("🤖 BinaryBot - Constructeur de Stratégies")
st.markdown("---")

# Menu de navigation en sidebar
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Aller vers :", ["🏠 Accueil", "⚙️ Créer une Stratégie", "📜 Générer un Script"])

# Contenu des pages
if menu == "🏠 Accueil":
    st.header("Bienvenue dans l'administration de BinaryBot")
    st.write("Ici, tu pourras configurer tes indicateurs, définir tes logiques séquentielles, et générer tes scripts Pine Script.")
    st.success("Le serveur est opérationnel. Nous sommes prêts à coder le cœur du système.")

elif menu == "⚙️ Créer une Stratégie":
    st.header("Configuration de Stratégie")
    st.info("C'est ici que l'on construira le formulaire pour ajouter des indicateurs et gérer la logique de déclencheur/confirmation.")
    # On mettra le code ici à la prochaine étape

elif menu == "📜 Générer un Script":
    st.header("Générateur Pine Script")
    st.info("C'est ici qu'apparaîtra le code Pine Script prêt à être copié-collé dans TradingView.")
    # On mettra le code ici à la prochaine étape
