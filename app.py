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
            st.session_state.mes_indicateurs.append({"type": type_indic, "params": params})
            st.success(f"✅ {type_indic} ajouté !")

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
    # PARTIE 2 : LA LOGIQUE SÉQUENTIELLE (MISE À JOUR CALL / PUT)
    # ==========================================
    st.header("Étape 2 : Définir la Logique (Déclencheur & Confirmation)")
    
    if len(st.session_state.mes_indicateurs) >= 1:
        choix_indicateurs = [f"{i['type']} ({i['params']})" for i in st.session_state.mes_indicateurs]
        
        with st.form("formulaire_logique"):
            # --- RÈGLE CALL (HAUSSE) ---
            st.subheader("📈 Règle CALL (Achat / Hausse)")
            col_c1, col_c2 = st.columns(2)
            log_dec_call = col_c1.selectbox("Déclencheur CALL", choix_indicateurs, key="dec_call")
            log_conf_call = col_c2.selectbox("Confirmation CALL", choix_indicateurs, key="conf_call")
            
            st.markdown("""<hr style="border: 1px dashed gray;">""", unsafe_allow_html=True)
            
            # --- RÈGLE PUT (BAISSE) ---
            st.subheader("📉 Règle PUT (Vente / Baisse)")
            col_p1, col_p2 = st.columns(2)
            log_dec_put = col_p1.selectbox("Déclencheur PUT", choix_indicateurs, key="dec_put")
            log_conf_put = col_p2.selectbox("Confirmation PUT", choix_indicateurs, key="conf_put")
            
            st.markdown("""<hr style="border: 1px dashed gray;">""", unsafe_allow_html=True)
            
            # --- FENÊTRE COMMUNE ---
            st.subheader("⏱️ Fenêtre de validité (Mémoire)")
            fenetre = st.number_input("Combien de bougies max pour confirmer ?", min_value=1, max_value=10, value=3)
            
            if st.form_submit_button("💾 Sauvegarder la logique"):
                st.session_state.logique_strategie = {
                    "dec_call": log_dec_call,
                    "conf_call": log_conf_call,
                    "dec_put": log_dec_put,
                    "conf_put": log_conf_put,
                    "fenetre": fenetre
                }
                st.success("✅ Logique CALL et PUT sauvegardée en mémoire !")
    else:
        st.warning("⚠️ Ajoute au moins un indicateur dans l'Étape 1.")

    if st.session_state.logique_strategie:
        st.markdown("---")
        st.subheader("📋 Résumé de votre logique active :")
        log = st.session_state.logique_strategie
        st.write(f"📈 **CALL :** {log['dec_call']} -> puis confirmation {log['conf_call']}")
        st.write(f"📉 **PUT :** {log['dec_put']} -> puis confirmation {log['conf_put']}")
        st.write(f"⏱️ **Fenêtre :** {log['fenetre']} bougies")

# --- PAGE GÉNÉRATEUR ---
elif menu == "📜 Générer un Script":
    st.header("📜 Générateur de Code Pine Script v5")
    
    if not st.session_state.mes_indicateurs or not st.session_state.logique_strategie:
        st.warning("⚠️ Tu dois d'abord créer et configurer ta stratégie dans le menu de gauche !")
    else:
        st.success("Stratégie détectée dans la mémoire ! Voici ton code prêt à copier.")
        
        # --- DÉBUT DU MOTEUR DE TRADUCTION ---
        indicateurs = st.session_state.mes_indicateurs
        logique = st.session_state.logique_strategie
        fenetre = logique["fenetre"]
        
        # Trouver les index des indicateurs choisis
        idx_dec_call = next((i for i, ind in indicateurs if f"{ind['type']} ({ind['params']})" == logique["dec_call"]), None)
        idx_conf_call = next((i for i, ind in indicateurs if f"{ind['type']} ({ind['params']})" == logique["conf_call"]), None)
        idx_dec_put = next((i for i, ind in indicateurs if f"{ind['type']} ({ind['params']})" == logique["dec_put"]), None)
        idx_conf_put = next((i for i, ind in indicateurs if f"{ind['type']} ({ind['params']})" == logique["conf_put"]), None)

        # 1. Génération des Inputs et Calculs
        inputs_code = ""
        vars_calcul = ""
        vars_plot = ""
        
        for i, ind in enumerate(indicateurs):
            if ind["type"] == "EMA":
                inputs_code += f"periode_ema_{i} = input.int({ind['params']['periode']}, title=\"EMA {i+1} Période\")\nsource_ema_{i} = input.source(close, title=\"EMA {i+1} Source\")\n"
                vars_calcul += f"ema_{i} = ta.ema(source_ema_{i}, periode_ema_{i})\n"
                vars_plot += f"plot(ema_{i}, color=color.blue, title=\"EMA {i+1}\")\n"
                
            elif ind["type"] == "SMA (Mid Bollinger)":
                inputs_code += f"periode_sma_{i} = input.int({ind['params']['periode']}, title=\"SMA (Bollinger Mid) {i+1} Période\")\nsource_sma_{i} = input.source(close, title=\"SMA (Bollinger Mid) {i+1} Source\")\n"
                vars_calcul += f"sma_{i} = ta.sma(source_sma_{i}, periode_sma_{i})\n"
                vars_plot += f"plot(sma_{i}, color=color.orange, title=\"SMA Mid {i+1}\")\n"
                
            elif ind["type"] == "Stochastique":
                inputs_code += f"stoch_k_{i} = input.int({ind['params']['k']}, title=\"Stoch K {i+1}\")\nstoch_d_{i} = input.int({ind['params']['d']}, title=\"Stoch D {i+1}\")\nstoch_smooth_{i} = input.int({ind['params']['smooth']}, title=\"Stoch Smooth {i+1}\")\n"
                vars_calcul += f"[stoch_k_val_{i}, stoch_d_val_{i}] = ta.stoch(close, high, low, stoch_k_{i}, stoch_d_{i}, stoch_smooth_{i})\n"

        # Fonction interne pour trouver la variable de croisement
        def get_cross_vars(idx_ind, is_stoch_k_cross_d=True):
            type_ind = indicateurs[idx_ind]["type"]
            if type_ind == "EMA": return f"ema_{idx_ind}", f"sma_{idx_ind}" # Par défaut on croise EMA avec la SMA si présente
            if type_ind == "SMA (Mid Bollinger)": return f"sma_{idx_ind}", f"ema_{idx_ind}"
            if type_ind == "Stochastique": 
                return f"stoch_k_val_{idx_ind}", f"stoch_d_val_{idx_ind}"

        var_dec_call_1, var_dec_call_2 = get_cross_vars(idx_dec_call)
        var_conf_call_1, var_conf_call_2 = get_cross_vars(idx_conf_call)
        var_dec_put_1, var_dec_put_2 = get_cross_vars(idx_dec_put)
        var_conf_put_1, var_conf_put_2 = get_cross_vars(idx_conf_put)

        # Assemblage du code final
        code_pine = f"""//@version=5
indicator("BinaryBot Stratégie CALL/PUT", overlay=true)

// --- PARAMÈTRES DYNAMIQUES ---
{inputs_code}
// --- CALCULS DES INDICATEURS ---
{vars_calcul}
// --- DESSIN DES LIGNES ---
{vars_plot}

// --- LOGIQUE SÉQUENTIELLE DOUBLE MÉMOIRE (CALL & PUT) ---
var int fenetre_call = 0
var int fenetre_put = 0

// 1. Événements Déclencheurs
if ta.crossover({var_dec_call_1}, {var_dec_call_2})
    fenetre_call := {fenetre}

if ta.crossunder({var_dec_put_1}, {var_dec_put_2})
    fenetre_put := {fenetre}

// 2. Compteurs à rebours
if fenetre_call > 0
    fenetre_call := fenetre_call - 1

if fenetre_put > 0
    fenetre_put := fenetre_put - 1

// 3. Événements de Confirmations & Signaux
signal_call = false
signal_put = false

if fenetre_call > 0 and ta.crossover({var_conf_call_1}, {var_conf_call_2})
    signal_call := true
    fenetre_call := 0 // Reset après confirmation

if fenetre_put > 0 and ta.crossunder({var_conf_put_1}, {var_conf_put_2})
    signal_put := true
    fenetre_put := 0 // Reset après confirmation

// 4. AFFICHAGE VISUEL
plotshape(signal_call, title="Signal CALL", style=shape.triangleup, location=location.belowbar, color=color.green, size=size.normal)
plotshape(signal_put, title="Signal PUT", style=shape.triangledown, location=location.abovebar, color=color.red, size=size.normal)
"""
        
        # Affichage du code avec bouton copier natif de Streamlit
        st.code(code_pine, language="pine")
        st.info("Cliquez sur l'icône 'Copier' en haut à droite de la boîte noire ci-dessus.")
