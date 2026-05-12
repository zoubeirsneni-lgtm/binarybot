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
            params["k"] = col1.number_input("K (Length)", min_value=1, value=14)
            params["d"] = col2.number_input("D (Smooth D)", min_value=1, value=17)
            params["smooth"] = col3.number_input("Smooth K", min_value=1, value=11)
            
        if st.form_submit_button("➕ Ajouter à la stratégie"):
            lignes_generees = []
            idx = len(st.session_state.mes_indicateurs)
            
            if type_indic == "EMA":
                lignes_generees.append({"id": f"ema_{idx}", "nom": f"EMA {params['periode']}", "type": "price_line"})
            elif type_indic == "SMA (Mid Bollinger)":
                lignes_generees.append({"id": f"sma_{idx}", "nom": f"SMA (Bollinger Mid) {params['periode']}", "type": "price_line"})
            elif type_indic == "Stochastique":
                lignes_generees.append({"id": f"stoch_k_{idx}", "nom": f"Stoch K ({params['k']},{params['d']},{params['smooth']})", "type": "oscillateur"})
                lignes_generees.append({"id": f"stoch_d_{idx}", "nom": f"Stoch D ({params['k']},{params['d']},{params['smooth']})", "type": "oscillateur"})
                
            st.session_state.mes_indicateurs.append({"type": type_indic, "params": params, "lignes": lignes_generees})
            st.success(f"✅ {type_indic} ajouté !")

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
    # PARTIE 2 : LA LOGIQUE
    # ==========================================
    st.header("Étape 2 : Logique de Croisement")
    
    toutes_les_lignes = []
    for indic in st.session_state.mes_indicateurs:
        toutes_les_lignes.extend(indic["lignes"])
    options_lignes = [ligne["nom"] for ligne in toutes_les_lignes]

    if len(options_lignes) >= 2:
        with st.form("formulaire_logique"):
            
            st.subheader("📈 Déclencheur CALL (Hausse)")
            c1, c2, c3 = st.columns([1,1,1])
            ligne_dec_call = c1.selectbox("Ligne 1", options_lignes, key="dec_call_1")
            c2.markdown("<br><h3 style='text-align:center; color:green'>CROISE À LA HAUSSE</h3><br>", unsafe_allow_html=True)
            ligne_dec_call_2 = c3.selectbox("Ligne 2", options_lignes, key="dec_call_2")
            
            st.subheader("📉 Déclencheur PUT (Baisse)")
            p1, p2, p3 = st.columns([1,1,1])
            ligne_dec_put = p1.selectbox("Ligne 1", options_lignes, key="dec_put_1")
            p2.markdown("<br><h3 style='text-align:center; color:red'>CROISE À LA BAISSE</h3><br>", unsafe_allow_html=True)
            ligne_dec_put_2 = p3.selectbox("Ligne 2", options_lignes, key="dec_put_2")
            
            st.markdown("""<hr style="border: 2px solid gray; margin-top: 20px; margin-bottom: 20px;">""", unsafe_allow_html=True)
            
            st.subheader("⏱️ Fenêtre de validité")
            fenetre = st.number_input("Combien de bougies max pour confirmer ?", min_value=1, max_value=10, value=3)
            
            st.markdown("""<hr style="border: 2px solid gray; margin-top: 20px; margin-bottom: 20px;">""", unsafe_allow_html=True)

            st.subheader("✅ Confirmation pour le CALL")
            cc1, cc2, cc3 = st.columns([1,1,1])
            ligne_conf_call = cc1.selectbox("Conf. CALL Ligne 1", options_lignes, key="conf_call_1")
            cc2.markdown("<br><h3 style='text-align:center; color:green'>CROISE À LA HAUSSE</h3><br>", unsafe_allow_html=True)
            ligne_conf_call_2 = cc3.selectbox("Conf. CALL Ligne 2", options_lignes, key="conf_call_2")

            st.subheader("✅ Confirmation pour le PUT")
            cp1, cp2, cp3 = st.columns([1,1,1])
            ligne_conf_put = cp1.selectbox("Conf. PUT Ligne 1", options_lignes, key="conf_put_1")
            cp2.markdown("<br><h3 style='text-align:center; color:red'>CROISE À LA BAISSE</h3><br>", unsafe_allow_html=True)
            ligne_conf_put_2 = cp3.selectbox("Conf. PUT Ligne 2", options_lignes, key="conf_put_2")
            
            if st.form_submit_button("💾 Sauvegarder la logique"):
                st.session_state.logique_strategie = {
                    "call_1": ligne_dec_call, "call_2": ligne_dec_call_2,
                    "put_1": ligne_dec_put, "put_2": ligne_dec_put_2,
                    "conf_call_1": ligne_conf_call, "conf_call_2": ligne_conf_call_2,
                    "conf_put_1": ligne_conf_put, "conf_put_2": ligne_conf_put_2,
                    "fenetre": fenetre
                }
                st.success("✅ Logique parfaite sauvegardée !")
    else:
        st.warning("⚠️ Ajoute au moins 2 indicateurs.")

    if st.session_state.logique_strategie:
        st.markdown("---")
        st.subheader("📋 Résumé :")
        log = st.session_state.logique_strategie
        st.markdown(f"📈 **CALL :** `{log['call_1']}` croise `{log['call_2']}`. Confirmé par `{log['conf_call_1']}` croise `{log['conf_call_2']}`.")
        st.markdown(f"📉 **PUT :** `{log['put_1']}` croise `{log['put_2']}`. Confirmé par `{log['conf_put_1']}` croise `{log['conf_put_2']}`.")
        st.markdown(f"⏱️ **Fenêtre :** `{log['fenetre']}` bougies.")


# --- PAGE GÉNÉRATEUR (MIS À JOUR PINE SCRIPT V6) ---
elif menu == "📜 Générer un Script":
    st.header("📜 Générateur de Code Pine Script v6")
    
    if not st.session_state.mes_indicateurs or not st.session_state.logique_strategie:
        st.warning("⚠️ Tu dois d'abord configurer ta stratégie !")
    else:
        st.success("Stratégie détectée !")
        
        indicateurs = st.session_state.mes_indicateurs
        logique = st.session_state.logique_strategie
        fenetre = logique["fenetre"]
        
        def get_id(nom):
            for ind in indicateurs:
                for l in ind["lignes"]:
                    if l["nom"] == nom: return l["id"]
            return "close"

        id_call_1 = get_id(logique["call_1"])
        id_call_2 = get_id(logique["call_2"])
        id_put_1 = get_id(logique["put_1"])
        id_put_2 = get_id(logique["put_2"])
        id_conf_call_1 = get_id(logique["conf_call_1"])
        id_conf_call_2 = get_id(logique["conf_call_2"])
        id_conf_put_1 = get_id(logique["conf_put_1"])
        id_conf_put_2 = get_id(logique["conf_put_2"])

        inputs_code, vars_calcul, vars_plot = "", "", ""
        
        for i, ind in enumerate(indicateurs):
            if ind["type"] == "EMA":
                inputs_code += f"periode_ema_{i} = input.int({ind['params']['periode']}, title=\"EMA {i+1}\")\nsource_ema_{i} = input.source(close, title=\"Source EMA {i+1}\")\n"
                vars_calcul += f"ema_{i} = ta.ema(source_ema_{i}, periode_ema_{i})\n"
                vars_plot += f"plot(ema_{i}, color=color.blue, title=\"EMA {i+1}\")\n"
            elif ind["type"] == "SMA (Mid Bollinger)":
                inputs_code += f"periode_sma_{i} = input.int({ind['params']['periode']}, title=\"SMA Mid {i+1}\")\nsource_sma_{i} = input.source(close, title=\"Source SMA Mid {i+1}\")\n"
                vars_calcul += f"sma_{i} = ta.sma(source_sma_{i}, periode_sma_{i})\n"
                vars_plot += f"plot(sma_{i}, color=color.orange, title=\"SMA Mid {i+1}\")\n"
            elif ind["type"] == "Stochastique":
                # MISE À JOUR POUR PINE SCRIPT V6 : ta.stoch n'accepte plus que 4 arguments
                inputs_code += f"stoch_length_{i} = input.int({ind['params']['k']}, title=\"Stoch Length {i+1}\")\nstoch_smooth_k_{i} = input.int({ind['params']['smooth']}, title=\"Stoch Smooth K {i+1}\")\nstoch_smooth_d_{i} = input.int({ind['params']['d']}, title=\"Stoch Smooth D {i+1}\")\n"
                vars_calcul += f"raw_stoch_{i} = ta.stoch(close, high, low, stoch_length_{i})\nstoch_k_val_{i} = ta.sma(raw_stoch_{i}, stoch_smooth_k_{i})\nstoch_d_val_{i} = ta.sma(stoch_k_val_{i}, stoch_smooth_d_{i})\n"

        # Assemblage du code final en Version 6
        code_pine = f"""//@version=6
indicator("BinaryBot - Logique Complète", overlay=true)

// --- PARAMÈTRES ---
{inputs_code}
// --- CALCULS ---
{vars_calcul}
// --- DESSIN ---
{vars_plot}

// --- LOGIQUE SÉQUENTIELLE ---
var int fenetre_call = 0
var int fenetre_put = 0

// 1. Déclencheurs
if ta.crossover({id_call_1}, {id_call_2})
    fenetre_call := {fenetre}

if ta.crossunder({id_put_1}, {id_put_2})
    fenetre_put := {fenetre}

// 2. Mémoires
if fenetre_call > 0
    fenetre_call -= 1
if fenetre_put > 0
    fenetre_put -= 1

// 3. Confirmations EXPLICITES
signal_call = false
signal_put = false

if fenetre_call > 0 and ta.crossover({id_conf_call_1}, {id_conf_call_2})
    signal_call := true
    fenetre_call := 0

if fenetre_put > 0 and ta.crossunder({id_conf_put_1}, {id_conf_put_2})
    signal_put := true
    fenetre_put := 0

// 4. AFFICHAGE
plotshape(signal_call, title="Signal CALL", style=shape.triangleup, location=location.belowbar, color=color.green, size=size.normal)
plotshape(signal_put, title="Signal PUT", style=shape.triangledown, location=location.abovebar, color=color.red, size=size.normal)
"""
        
        st.code(code_pine, language="pine")
        st.info("Cliquez sur l'icône 'Copier' en haut à droite de la boîte noire ci-dessus.")
