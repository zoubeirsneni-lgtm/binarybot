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
    # PARTIE 1 : LES INDICATEURS (CORRIGÉ)
    # ==========================================
    st.header("Étape 1 : Ajouter les Indicateurs")
    
    # ATTENTION : LE SELECTBOX EST MAINTENANT EN DEHORS DU FORMULAIRE !
    type_indic = st.selectbox("Choisir l'indicateur", ["EMA", "SMA (Mid Bollinger)", "Stochastique"])

    # Le formulaire ne contient plus que les paramètres dynamiques
    with st.form("formulaire_indicateur"):
        params = {}
        
        # --- CAS 1 : L'EMA ---
        if type_indic == "EMA":
            col1, col2 = st.columns(2)
            params["periode"] = col1.number_input("Période", min_value=1, value=50)
            params["source"] = col2.selectbox("Source", ["close", "open", "high", "low"])
            
        # --- CAS 2 : LA SMA (MID BOLLINGER) ---
        elif type_indic == "SMA (Mid Bollinger)":
            st.info("On ne garde que la ligne du milieu, mais on saisit les paramètres de la bande.")
            col1, col2, col3 = st.columns(3)
            params["periode"] = col1.number_input("Période (Length)", min_value=1, value=5)
            params["mult"] = col2.number_input("Multiplicateur (StdDev)", min_value=0.1, value=1.0, step=0.1)
            params["source"] = col3.selectbox("Source", ["close", "open", "high", "low"])
            
        # --- CAS 3 : LE STOCHASTIQUE ---
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
    # PARTIE 2 : LA LOGIQUE SÉQUENTIELLE
    # ==========================================
    st.header("Étape 2 : Définir la Logique (Déclencheur & Confirmation)")
    
    if len(st.session_state.mes_indicateurs) >= 1:
        with st.form("formulaire_logique"):
            st.subheader("1. Le Déclencheur (Trigger)")
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
