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

# INITIALISATION DE LA MÉMOIRE (Très important pour Streamlit)
# On crée une liste vide dans la session si elle n'existe pas encore
if "mes_indicateurs" not in st.session_state:
    st.session_state.mes_indicateurs = []

# Contenu des pages
if menu == "🏠 Accueil":
    st.header("Bienvenue dans l'administration de BinaryBot")
    st.write("Ici, tu pourras configurer tes indicateurs, définir tes logiques séquentielles, et générer tes scripts Pine Script.")
    st.success("Le serveur est opérationnel.")

# --- NOUVELLE PAGE FORMULAIRE ---
elif menu == "⚙️ Créer une Stratégie":
    st.header("Étape 1 : Ajouter les Indicateurs")
    st.write("Configure les indicateurs qui composeront ta stratégie.")
    
    # On utilise un "formulaire" Streamlit pour regrouper les boutons et les champs
    with st.form("formulaire_indicateur"):
        # Menu déroulant pour le type d'indicateur
        type_indic = st.selectbox("Choisir l'indicateur", ["EMA", "SMA (Mid Bollinger)", "Stochastique"])
        
        # Affichage dynamique des paramètres selon l'indicateur choisi
        params = {} # Dictionnaire qui stockera les réglages
        
        if type_indic in ["EMA", "SMA (Mid Bollinger)"]:
            col1, col2 = st.columns(2)
            params["periode"] = col1.number_input("Période", min_value=1, value=50 if type_indic == "EMA" else 5)
            params["source"] = col2.selectbox("Source", ["close", "open", "high", "low"])
            
        elif type_indic == "Stochastique":
            st.write("Paramètres du Stochastique")
            col1, col2, col3 = st.columns(3)
            params["k"] = col1.number_input("K", min_value=1, value=14)
            params["d"] = col2.number_input("D", min_value=1, value=17)
            params["smooth"] = col3.number_input("Smooth", min_value=1, value=11)
        
        # Bouton de soumission du formulaire
        bouton_ajouter = st.form_submit_button("➕ Ajouter à la stratégie")
        
        # Action quand on clique sur le bouton
        if bouton_ajouter:
            # On crée un dictionnaire représentant l'indicateur
            nouvel_indic = {
                "type": type_indic,
                "params": params
            }
            # On l'ajoute à notre mémoire de session
            st.session_state.mes_indicateurs.append(nouvel_indic)
            st.success(f"✅ {type_indic} ajouté avec succès !")

    # --- AFFICHAGE DE CE QUI A ÉTÉ AJOUTÉ ---
    st.markdown("---")
    st.subheader("Indicateurs actuellement dans la stratégie :")
    
    if len(st.session_state.mes_indicateurs) == 0:
        st.info("Aucun indicateur ajouté pour le moment.")
    else:
        # On affiche chaque indicateur sauvegardé en mémoire
        for index, indic in enumerate(st.session_state.mes_indicateurs):
            st.write(f"**{index + 1}. {indic['type']}** -> Paramètres : `{indic['params']}`")
            
        # Bouton pour tout effacer (utile pour tester)
        if st.button("🗑️ Réinitialiser la liste"):
            st.session_state.mes_indicateurs = []
            st.rerun() # Force le rechargement de la page pour mettre à jour l'affichage

elif menu == "📜 Générer un Script":
    st.header("Générateur Pine Script")
    st.info("C'est ici qu'apparaîtra le code Pine Script prêt à être copié-collé dans TradingView.")
