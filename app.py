import streamlit as st

# Configuration de la page
st.set_page_config(page_title="BinaryBot Admin", page_icon="🤖", layout="wide")

st.title("🤖 BinaryBot - Constructeur de Stratégies")
st.markdown("---")

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Aller vers :", ["🏠 Accueil", "⚙️ Créer une Stratégie", "📜 Générer un Script"])

# --- INITIALISATION DE LA MÉMOIRE ---
if "mes_indicateurs" not in st.session_state:
    st.session_state.mes_indicateurs = []
if "logique_strategie" not in st.session_state:
    st.session_state.logique_strategie = {}

# --- PAGES ---
if menu == "🏠 Accueil":
    st.header("Bienvenue dans l'administration de BinaryBot")
    st.write("Ici, tu pourras configurer tes indicateurs, définir tes logiques séquentielles, et générer tes scripts Pine Script.")

# --- PAGE FORMULAIRE ---
elif menu == "⚙️ Créer une Stratégie":
    
    # ==========================================
    # PARTIE 1 : LES INDICATEURS
    # ==========================================
    st.header("Étape 1 : Ajouter les Indicateurs")
    with st.form("formulaire_indicateur"):
        type_indic = st.selectbox("Choisir l'indicateur", ["EMA", "SMA (Mid Bollinger)", "Stochastique"])
        params = {}
        
        if type_indic in ["EMA", "SMA (Mid Bollinger)"]:
            col1, col2 = st.columns(2)
            params["periode"] = col1.number_input("Période", min_value=1, value=50 if type_indic == "EMA" else 5)
            params["source"] = col2.selectbox("Source", ["close", "open", "high", "low"])
        elif type_indic == "Stochastique":
            col1, col2, col3 = st.columns(3)
            params["k"] = col1.number_input("K", min_value=1, value=14)
            params["d"] = col2.number_input("D", min_value=1, value=17)
            params["smooth"] = col3.number_input("Smooth", min_value=1, value=11)
            
        if st.form_submit_button("➕ Ajouter à la stratégie"):
            st.session_state.mes_indicateurs.append({"type": type_indic, "params": params})
            st.success(f"✅ {type_indic} ajouté !")

    # Affichage des indicateurs ajoutés
    if len(st.session_state.mes_indicateurs) == 0:
        st.info("Aucun indicateur ajouté.")
    else:
        for index, indic in enumerate(st.session_state.mes_indicateurs):
            st.write(f"**{index + 1}. {indic['type']}** -> `{indic['params']}`")
        if st.button("🗑️ Réinitialiser la liste"):
            st.session_state.mes_indicateurs = []
            st.rerun()

    st.markdown("---")
    
    # ==========================================
    # PARTIE 2 : LA LOGIQUE SÉQUENTIELLE (NOUVEAU)
    # ==========================================
    st.header("Étape 2 : Définir la Logique (Déclencheur & Confirmation)")
    
    # On ne montre cette partie QUE s'il y a au moins 2 indicateurs (besoin d'un déclencheur et d'une confirmation)
    if len(st.session_state.mes_indicateurs) >= 1:
        with st.form("formulaire_logique"):
            st.subheader("1. Le Déclencheur (Trigger)")
            # On crée une liste lisible pour l'utilisateur basée sur ce qu'il a ajouté
            choix_indicateurs = [f"{i['type']} ({i['params']})" for i in st.session_state.mes_indicateurs]
            
            col_dec1, col_dec2 = st.columns(2)
            declencheur_indic = col_dec1.selectbox("Indicateur de déclenchement", choix_indicateurs)
            declencheur_action = col_dec2.selectbox("Action", ["Croisement à la hausse (Call)", "Croisement à la baisse (Put)"])
            
            st.subheader("2. La Fenêtre de validité (Mémoire)")
            fenetre = st.number_input("Combien de bougies max pour confirmer ?", min_value=1, max_value=10, value=3)
            
            st.subheader("3. La Confirmation")
            col_conf1, col_conf2 = st.columns(2)
            confirmation_indic = col_conf1.selectbox("Indicateur de confirmation", choix_indicateurs)
            confirmation_action = col_conf2.selectbox("Action", ["Croisement à la hausse", "Croisement à la baisse"])
            
            if st.form_submit_button("💾 Sauvegarder la logique"):
                # On sauvegarde les choix dans la mémoire
                st.session_state.logique_strategie = {
                    "declencheur": declencheur_indic,
                    "action_declencheur": declencheur_action,
                    "fenetre": fenetre,
                    "confirmation": confirmation_indic,
                    "action_confirmation": confirmation_action
                }
                st.success("✅ Logique de la stratégie sauvegardée en mémoire !")
    else:
        st.warning("⚠️ Ajoute au moins un indicateur dans l'Étape 1 pour pouvoir configurer la logique.")

    # Affichage de la logique sauvegardée
    if st.session_state.logique_strategie:
        st.markdown("---")
        st.subheader("📋 Résumé de votre logique active :")
        log = st.session_state.logique_strategie
        st.write(f"🔥 **Déclencheur :** {log['declencheur']} -> {log['action_declencheur']}")
        st.write(f"⏱️ **Fenêtre :** {log['fenetre']} bougies")
        st.write(f"✅ **Confirmation :** {log['confirmation']} -> {log['action_confirmation']}")

elif menu == "📜 Générer un Script":
    st.header("Générateur Pine Script")
    st.info("C'est ici qu'apparaîtra le code Pine Script (Prochaine étape).")
