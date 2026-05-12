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
    # PARTIE 1 : LES INDICATEURS (GÉNÉRATION DE LIGNES)
    # ==========================================
    st.header("Étape 1 : Ajouter les Indicateurs (Boîte à outils)")
    type_indic = st.selectbox("Choisir l'indicateur", ["EMA", "SMA (Mid Bollinger)", "Stochastique"])

    with st.form("formulaire_indicateur"):
        params = {}
        
        if type_indic == "EMA":
            col1, col2 = st.columns(2)
            params["periode"] = col1.number_input("Période", min_value=1, value=50)
            params["source"] = col2.selectbox("Source", ["close", "open", "high", "low"])
            
        elif type_indic == "SMA (Mid Bollinger)":
            st.info("On ne garde que la ligne du milieu, mais on saisit les paramètres de la bande.")
            col1, col2, col3 = st.columns(3)
            params["periode"] = col1.number_input("Période (Length)", min_value=1, value=5)
            params["mult"] = col2.number_input("Multiplicateur (StdDev)", min_value=0.1, value=1.0, step=0.1)
            params["source"] = col3.selectbox("Source", ["close", "open", "high", "low"])
            
        elif type_indic == "Stochastique":
            col1, col2, col3 = st.columns(3)
            params["k"] = col1.number_input("K", min_value=1, value=14)
            params["d"] = col2.number_input("D", min_value=1, value=17)
            params["smooth"] = col3.number_input("Smooth", min_value=1, value=11)
            
        if st.form_submit_button("➕ Ajouter à la stratégie"):
            # On crée les "lignes" qui seront utilisables pour les croisements
            lignes_generees = []
            idx = len(st.session_state.mes_indicateurs)
            
            if type_indic == "EMA":
                nom_affiche = f"EMA {params['periode']}"
                lignes_generees.append({"id": f"ema_{idx}", "nom": nom_affiche, "type": "price_line"})
            elif type_indic == "SMA (Mid Bollinger)":
                nom_affiche = f"SMA (Bollinger Mid) {params['periode']}"
                lignes_generees.append({"id": f"sma_{idx}", "nom": nom_affiche, "type": "price_line"})
            elif type_indic == "Stochastique":
                nom_k = f"Stoch K ({params['k']},{params['d']},{params['smooth']})"
                nom_d = f"Stoch D ({params['k']},{params['d']},{params['smooth']})"
                lignes_generees.append({"id": f"stoch_k_{idx}", "nom": nom_k, "type": "oscillateur"})
                lignes_generees.append({"id": f"stoch_d_{idx}", "nom": nom_d, "type": "oscillateur"})
                
            st.session_state.mes_indicateurs.append({
                "type": type_indic, 
                "params": params,
                "lignes": lignes_generees
            })
            st.success(f"✅ {type_indic} ajouté avec ses lignes !")

    # Affichage des indicateurs ajoutés
    if len(st.session_state.mes_indicateurs) == 0:
        st.info("Aucun indicateur ajouté.")
    else:
        for index, indic in enumerate(st.session_state.mes_indicateurs):
            st.write(f"**{index + 1}. {indic['type']}**")
            for ligne in indic["lignes"]:
                st.markdown(f"  ↳ `{ligne['nom']}`")
        if st.button("🗑️ Réinitialiser la liste"):
            st.session_state.mes_indicateurs = []
            st.rerun()

    st.markdown("---")
    
    # ==========================================
    # PARTIE 2 : LA LOGIQUE (LIGNE A CROISE LIGNE B)
    # ==========================================
    st.header("Étape 2 : Logique de Croisement")
    
    # On rassemble toutes les lignes créées à l'étape 1 pour les mettre dans les menus déroulants
    toutes_les_lignes = []
    for indic in st.session_state.mes_indicateurs:
        toutes_les_lignes.extend(indic["lignes"])
        
    options_lignes = [ligne["nom"] for ligne in toutes_les_lignes]

    if len(options_lignes) >= 2: # Il faut au moins 2 lignes pour faire un croisement
        with st.form("formulaire_logique"):
            
            # --- RÈGLE CALL ---
            st.subheader("📈 Règle CALL (Hausse)")
            col_c1, col_c2, col_c3 = st.columns([1,1,1])
            ligne_dec_call = col_c1.selectbox("Ligne 1", options_lignes, key="dec_call_1")
            col_c2.markdown("<br><h3 style='text-align:center; color:green'>CROISE À LA HAUSSE</h3><br>", unsafe_allow_html=True)
            ligne_dec_call_2 = col_c3.selectbox("Ligne 2", options_lignes, key="dec_call_2")
            
            # --- RÈGLE PUT ---
            st.subheader("📉 Règle PUT (Baisse)")
            col_p1, col_p2, col_p3 = st.columns([1,1,1])
            ligne_dec_put = col_p1.selectbox("Ligne 1", options_lignes, key="dec_put_1")
            col_p2.markdown("<br><h3 style='text-align:center; color:red'>CROISE À LA BAISSE</h3><br>", unsafe_allow_html=True)
            ligne_dec_put_2 = col_p3.selectbox("Ligne 2", options_lignes, key="dec_put_2")
            
            st.markdown("""<hr style="border: 2px solid gray;">""", unsafe_allow_html=True)
            
            # --- FENÊTRE & CONFIRMATION ---
            st.subheader("⏱️ Confirmation Séquentielle")
            fenetre = st.number_input("Combien de bougies max pour confirmer ?", min_value=1, max_value=10, value=3)
            
            conf_col1, conf_col2, conf_col3 = st.columns([1,1,1])
            ligne_conf_1 = conf_col1.selectbox("Confirmation Ligne 1", options_lignes, key="conf_1")
            conf_col2.markdown("<br><h3 style='text-align:center; color:blue'>CROISE À LA HAUSSE</h3><br>", unsafe_allow_html=True)
            ligne_conf_2 = conf_col3.selectbox("Confirmation Ligne 2", options_lignes, key="conf_2")
            
            if st.form_submit_button("💾 Sauvegarder la logique"):
                st.session_state.logique_strategie = {
                    "call_1": ligne_dec_call, "call_2": ligne_dec_call_2,
                    "put_1": ligne_dec_put, "put_2": ligne_dec_put_2,
                    "conf_1": ligne_conf_1, "conf_2": ligne_conf_2,
                    "fenetre": fenetre
                }
                st.success("✅ Logique sauvegardée !")
    else:
        st.warning("⚠️ Ajoute au moins 2 indicateurs (ou 1 Stochastique qui compte pour 2) pour créer des croisements.")

    if st.session_state.logique_strategie:
        st.markdown("---")
        st.subheader("📋 Résumé de votre logique :")
        log = st.session_state.logique_strategie
        st.markdown(f"📈 **CALL :** `{log['call_1']}` croise `{log['call_2']}`")
        st.markdown(f"📉 **PUT :** `{log['put_1']}` croise `{log['put_2']}`")
        st.markdown(f"⏱️ **Si déclenché :** Attendre `{log['fenetre']}` bougies max pour voir `{log['conf_1']}` croiser `{log['conf_2']}`")


# --- PAGE GÉNÉRATEUR ---
elif menu == "📜 Générer un Script":
    st.header("📜 Générateur de Code Pine Script v5")
    
    if not st.session_state.mes_indicateurs or not st.session_state.logique_strategie:
        st.warning("⚠️ Tu dois d'abord créer et configurer ta stratégie dans le menu de gauche !")
    else:
        st.success("Stratégie détectée ! Voici ton code.")
        
        # --- MOTEUR DE TRADUCTION ---
        indicateurs = st.session_state.mes_indicateurs
        logique = st.session_state.logique_strategie
        fenetre = logique["fenetre"]
        
        # Fonction pour trouver l'ID technique d'une ligne à partir de son nom d'affichage
        def get_id_from_nom(nom_affiche):
            for indic in indicateurs:
                for ligne in indic["lignes"]:
                    if ligne["nom"] == nom_affiche:
                        return ligne["id"]
            return "close"

        id_call_1 = get_id_from_nom(logique["call_1"])
        id_call_2 = get_id_from_nom(logique["call_2"])
        id_put_1 = get_id_from_nom(logique["put_1"])
        id_put_2 = get_id_from_nom(logique["put_2"])
        id_conf_1 = get_id_from_nom(logique["conf_1"])
        id_conf_2 = get_id_from_nom(logique["conf_2"])

        # 1. Génération des Inputs et Calculs
        inputs_code = ""
        vars_calcul = ""
        vars_plot = ""
        
        for i, indic in enumerate(indicateurs):
            if indic["type"] == "EMA":
                inputs_code += f"periode_ema_{i} = input.int({indic['params']['periode']}, title=\"EMA {i+1} Période\")\nsource_ema_{i} = input.source(close, title=\"EMA {i+1} Source\")\n"
                vars_calcul += f"ema_{i} = ta.ema(source_ema_{i}, periode_ema_{i})\n"
                vars_plot += f"plot(ema_{i}, color=color.blue, title=\"EMA {i+1}\")\n"
                
            elif indic["type"] == "SMA (Mid Bollinger)":
                inputs_code += f"periode_sma_{i} = input.int({indic['params']['periode']}, title=\"SMA Mid {i+1} Période\")\nsource_sma_{i} = input.source(close, title=\"SMA Mid {i+1} Source\")\n"
                vars_calcul += f"sma_{i} = ta.sma(source_sma_{i}, periode_sma_{i})\n"
                vars_plot += f"plot(sma_{i}, color=color.orange, title=\"SMA Mid {i+1}\")\n"
                
            elif indic["type"] == "Stochastique":
                inputs_code += f"stoch_k_{i} = input.int({indic['params']['k']}, title=\"Stoch K {i+1}\")\nstoch_d_{i} = input.int({indic['params']['d']}, title=\"Stoch D {i+1}\")\nstoch_smooth_{i} = input.int({indic['params']['smooth']}, title=\"Stoch Smooth {i+1}\")\n"
                vars_calcul += f"[stoch_k_val_{i}, stoch_d_val_{i}] = ta.stoch(close, high, low, stoch_k_{i}, stoch_d_{i}, stoch_smooth_{i})\n"

        # Assemblage du code final
        code_pine = f"""//@version=5
indicator("BinaryBot - Logique Avancée", overlay=true)

// --- PARAMÈTRES ---
{inputs_code}
// --- CALCULS ---
{vars_calcul}
// --- DESSIN ---
{vars_plot}

// --- LOGIQUE SÉQUENTIELLE (DOUBLE MÉMOIRE) ---
var int fenetre_call = 0
var int fenetre_put = 0

// 1. Déclencheurs
if ta.crossover({id_call_1}, {id_call_2})
    fenetre_call := {fenetre}

if ta.crossunder({id_put_1}, {id_put_2})
    fenetre_put := {fenetre}

// 2. Mémoires (Rebours)
if fenetre_call > 0
    fenetre_call -= 1
if fenetre_put > 0
    fenetre_put -= 1

// 3. Confirmations & Signaux
signal_call = false
signal_put = false

if fenetre_call > 0 and ta.crossover({id_conf_1}, {id_conf_2})
    signal_call := true
    fenetre_call := 0

if fenetre_put > 0 and ta.crossunder({id_conf_1}, {id_conf_2})
    signal_put := true
    fenetre_put := 0

// 4. AFFICHAGE
plotshape(signal_call, title="Signal CALL", style=shape.triangleup, location=location.belowbar, color=color.green, size=size.normal)
plotshape(signal_put, title="Signal PUT", style=shape.triangledown, location=location.abovebar, color=color.red, size=size.normal)
"""
        
        st.code(code_pine, language="pine")
        st.info("Cliquez sur l'icône 'Copier' en haut à droite de la boîte noire ci-dessus.")
