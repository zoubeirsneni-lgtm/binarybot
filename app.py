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
        st.warning("⚠️ Ajoute au moins un indicateur dans l'Étape 1.")

    if st.session_state.logique_strategie:
        st.markdown("---")
        st.subheader("📋 Résumé de votre logique active :")
        log = st.session_state.logique_strategie
        st.write(f"🔥 **Déclencheur :** {log['declencheur']} -> {log['action_declencheur']}")
        st.write(f"⏱️ **Fenêtre :** {log['fenetre']} bougies")
        st.write(f"✅ **Confirmation :** {log['confirmation']} -> {log['action_confirmation']}")

# --- PAGE GÉNÉRATEUR (LE CERVEAU) ---
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
        
        # Trouver les index des indicateurs choisis pour la logique
        str_dec = logique["declencheur"]
        str_conf = logique["confirmation"]
        idx_dec = next((i for i, ind in indicateurs if f"{ind['type']} ({ind['params']})" == str_dec), None)
        idx_conf = next((i for i, ind in indicateurs if f"{ind['type']} ({ind['params']})" == str_conf), None)

        # 1. Génération des Inputs (Menus dynamiques dans TradingView)
        inputs_code = ""
        vars_calcul = ""
        vars_plot = ""
        
        for i, ind in enumerate(indicateurs):
            if ind["type"] == "EMA":
                inputs_code += f"periode_ema_{i} = input.int({ind['params']['periode']}, title=\"EMA {i+1} Période\")\n"
                inputs_code += f"source_ema_{i} = input.source(close, title=\"EMA {i+1} Source\")\n"
                vars_calcul += f"ema_{i} = ta.ema(source_ema_{i}, periode_ema_{i})\n"
                vars_plot += f"plot(ema_{i}, color=color.blue, title=\"EMA {i+1}\")\n"
                
            elif ind["type"] == "SMA (Mid Bollinger)":
                inputs_code += f"periode_sma_{i} = input.int({ind['params']['periode']}, title=\"SMA (Bollinger Mid) {i+1} Période\")\n"
                inputs_code += f"source_sma_{i} = input.source(close, title=\"SMA (Bollinger Mid) {i+1} Source\")\n"
                vars_calcul += f"sma_{i} = ta.sma(source_sma_{i}, periode_sma_{i})\n"
                vars_plot += f"plot(sma_{i}, color=color.orange, title=\"SMA Mid {i+1}\")\n"
                
            elif ind["type"] == "Stochastique":
                inputs_code += f"stoch_k_{i} = input.int({ind['params']['k']}, title=\"Stoch K {i+1}\")\n"
                inputs_code += f"stoch_d_{i} = input.int({ind['params']['d']}, title=\"Stoch D {i+1}\")\n"
                inputs_code += f"stoch_smooth_{i} = input.int({ind['params']['smooth']}, title=\"Stoch Smooth {i+1}\")\n"
                vars_calcul += f"[stoch_k_val_{i}, stoch_d_val_{i}] = ta.stoch(close, high, low, stoch_k_{i}, stoch_d_{i}, stoch_smooth_{i})\n"
                # Le stochastique se dessine dans un panneau séparé par défaut dans TradingView

        # 2. Génération de la logique séquentielle
        # Déterminer les noms de variables pour le déclencheur
        type_dec = indicateurs[idx_dec]["type"]
        if type_dec in ["EMA", "SMA (Mid Bollinger)"]:
            var_dec = f"ema_{idx_dec}" if type_dec == "EMA" else f"sma_{idx_dec}"
        else:
            var_dec = f"stoch_k_val_{idx_dec}" # On croise la ligne K par défaut pour le déclencheur Stoch
            
        # Déterminer les noms de variables pour la confirmation (Stochastique K croise D)
        type_conf = indicateurs[idx_conf]["type"]
        if type_conf == "Stochastique":
            var_conf_1 = f"stoch_k_val_{idx_conf}"
            var_conf_2 = f"stoch_d_val_{idx_conf}"
        else:
            var_conf_1 = f"ema_{idx_conf}" if type_conf == "EMA" else f"sma_{idx_conf}"
            var_conf_2 = var_conf_1 # Pas de croisement interne sur EMA/SMA

        # Déterminer le sens (hausse/baisse)
        is_call_dec = "hausse" in logique["action_declencheur"]
        is_call_conf = "hausse" in logique["action_confirmation"]
        
        cross_dec = f"ta.crossover({var_dec}, {var_conf_2 if type_dec == 'Stochastique' else ('sma_'+str(idx_dec) if type_dec=='EMA' else 'ema_'+str(idx_dec))})" if is_call_dec else f"ta.crossunder({var_dec}, {'sma_'+str(idx_dec) if type_dec=='EMA' else ('ema_'+str(idx_dec) if type_dec=='SMA (Mid Bollinger)' else 'stoch_d_val_'+str(idx_dec))})"
        
        # Correction dynamique des croisements exacts selon l'exemple de l'utilisateur (EMA croise SMA)
        if type_dec == "EMA": var_dec_2 = f"sma_{idx_dec}"
        elif type_dec == "SMA (Mid Bollinger)": var_dec_2 = f"ema_{idx_dec}"
        else: var_dec_2 = f"stoch_d_val_{idx_dec}"

        cross_dec = f"ta.crossover({var_dec}, {var_dec_2})" if is_call_dec else f"ta.crossunder({var_dec}, {var_dec_2})"
        cross_conf = f"ta.crossover({var_conf_1}, {var_conf_2})" if is_call_conf else f"ta.crossunder({var_conf_1}, {var_conf_2})"

        # Assemblage du code final
        code_pine = f"""//@version=5
indicator("BinaryBot Stratégie", overlay=true)

// --- PARAMÈTRES DYNAMIQUES ---
{inputs_code}
// --- CALCULS DES INDICATEURS ---
{vars_calcul}
// --- DESSIN DES LIGNES ---
{vars_plot}

// --- LOGIQUE SÉQUENTIELLE (MÉMOIRE) ---
var int fenetre_restante = 0
var int direction_declencheur = 0 // 1 = Call, -1 = Put

// 1. Événement Déclencheur
if {cross_dec}
    fenetre_restante := {fenetre}
    direction_declencheur := {1 if is_call_dec else -1}

// 2. Compteur à rebours (sauf si un nouveau déclencheur a lieu)
if fenetre_restante > 0 and not {cross_dec}
    fenetre_restante := fenetre_restante - 1

// 3. Événement de Confirmation
signal_call = false
signal_put = false

if fenetre_restante > 0
    if {cross_conf} and direction_declencheur == 1
        signal_call := true
        fenetre_restante := 0 // On remet à zéro après confirmation
    if {cross_conf} and direction_declencheur == -1
        signal_put := true
        fenetre_restante := 0 // On remet à zéro après confirmation

// 4. AFFICHAGE VISUEL DES SIGNAUX
plotshape(signal_call, title="Signal CALL", style=shape.triangleup, location=location.belowbar, color=color.green, size=size.normal)
plotshape(signal_put, title="Signal PUT", style=shape.triangledown, location=location.abovebar, color=color.red, size=size.normal)
"""
        
        # Affichage du code avec bouton copier
        st.code(code_pine, language="pine")
        
        if st.button("📋 Copier le code"):
            st.toast("Code copié dans le presse-papier !", icon="✅")
            st.code(code_pine, language="pine") # Streamlit gère le copier nativement avec le bouton en haut à droite de la boîte
