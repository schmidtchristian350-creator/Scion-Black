import requests
import streamlit as st

# Konfiguration der Seite im Dark / Hacker Look
st.set_page_config(
    page_title="SCION-BLACK // SECURITY EXPLOIT & HEADER AUDIT", 
    page_icon="⚡", 
    layout="wide"
)

# --- CSS FÜR SCHWARZES, GEFÄHRLICHES DESIGN ---
st.markdown("""
    <style>
    /* Globaler Dark Mode Hintergrund und Text */
    .stApp {
        background-color: #08090a;
        color: #e0e0e0;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Überschriften mit leichtem Neon/Gefahr-Touch */
    h1, h2, h3 {
        color: #ff3333 !important;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 1px;
    }

    /* Input-Felder im Terminal-Stil */
    .stTextInput input {
        background-color: #121417 !important;
        color: #00ffcc !important;
        border: 1px solid #ff3333 !important;
        border-radius: 4px;
    }

    /* Buttons mit aggressivem Rot/Schwarz-Look */
    .stButton button {
        background-color: #1a0000 !important;
        color: #ff3333 !important;
        border: 1px solid #ff3333 !important;
        border-radius: 4px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #ff3333 !important;
        color: #000000 !important;
        border: 1px solid #ff0000 !important;
    }

    /* Sidebar / Login Bereich anpassen */
    [data-testid="stSidebar"] {
        background-color: #0d0f12;
        border-right: 1px solid #ff3333;
    }

    /* Infoboxen und Warnungen */
    .stAlert {
        background-color: #121417 !important;
        color: #e0e0e0 !important;
        border: 1px solid #333 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Session State für Login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- SEITENBAR FÜR LOGIN (Links, verschwindet nach erfolgreichem Login) ---
if not st.session_state["logged_in"]:
    with st.sidebar:
        st.markdown("### ⚡ SYSTEM ACCESS")
        st.markdown("<p style='color: #ff3333; font-size: 12px;'>RESTRICTED AREA // ADMINS ONLY</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username_input = st.text_input("IDENT / USER")
            password_input = st.text_input("PASSCODE", type="password")
            submit_button = st.form_submit_button("INITIALISIEREN")
            
            if submit_button:
                if username_input == "admin" and password_input == "scion2026":
                    st.session_state["logged_in"] = True
                    st.rerun()
                else:
                    st.error("ACCESS DENIED // Falsche Credentials")

    # Hauptbereich für nicht eingeloggte Nutzer
    st.title("⚡ SCION-BLACK // SECURITY CORE")
    st.markdown("### Offensive Vulnerability & Threat Intelligence")
    st.markdown("---")
    st.warning("⚠️ **WARNUNG:** Dieses System führt automatisierte Sicherheitsanalysen durch. Unautorisiertes Scannen fremder Infrastrukturen ist strafbar. Bitte authentifiziere dich über das Terminal links.")
    
    st.code("""
[INFO] Initialisiere Kern-Protokolle...
[INFO] Status: Warten auf Authentifizierung...
[TARGET] Keine Ziele geladen.
    """, language="bash")

else:
    # --- EINGELOGGT: VOLLSCREEN DARK OPS MODUS ---
    with st.sidebar:
        st.markdown("### ⚡ OPERATIONAL")
        st.markdown("Status: **ONLINE**")
        st.markdown("Agent: **ADMIN**")
        st.markdown("---")
        if st.button("ABMELDEN // LOCK"):
            st.session_state["logged_in"] = False
            st.rerun()

    st.title("⚡ SCION-BLACK // TARGET AUDIT ENGINE")
    st.markdown("<p style='color: #ff3333;'>SYSTEM ACTIVE // GEFAHRENANALYSE BEREIT</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Ziel-URL eingeben
    target_url = st.text_input("ZIEL-ADRESSE (URL eingeben inkl. https://):", "https://example.com")

    if st.button("SCAN STARTEN // ANALYSIERE ZIEL"):
        if not target_url.startswith("http"):
            st.error("FEHLER: Ungültiges Protokoll. URL muss mit http:// oder https:// beginnen.")
        else:
            with st.spinner("⚡ Scanne Ziel-Infrastruktur nach Schwachstellen..."):
                try:
                    response = requests.get(target_url, timeout=5)
                    headers = response.headers
                    
                    st.success(f"VERBINDUNG ERFOLGREICH // Status-Code: {response.status_code}")
                    
                    checks = {
                        "Strict-Transport-Security": ("HSTS-Header", "Erzwingt unverschlüsselte Downgrades. Angreifer können Daten abfangen."),
                        "X-Content-Type-Options": ("X-Content-Type-Options", "MIME-Sniffing aktiv. Browser könnten manipulierte Dateien ausführen."),
                        "X-Frame-Options": ("X-Frame-Options", "Clickjacking-Risiko. Die Seite kann in fremde Webseiten eingebettet werden."),
                        "Content-Security-Policy": ("Content-Security-Policy (CSP)", "Fehlender Schutz gegen Cross-Site Scripting (XSS) Injektionen."),
                        "Referrer-Policy": ("Referrer-Policy", "Sensible Datenlecks über HTTP-Referrer-Header möglich.")
                    }

                    issues = []
                    successes = []

                    for header, (name, desc) in checks.items():
                        if header not in headers:
                            issues.append(f"🔴 **SCHWACHSTELLE DETEKTIERT [{name}]:** {desc}")
                        else:
                            successes.append(f"🟢 **GESICHERT [{name}]:** Abwehr aktiv. ({desc})")

                    st.markdown("### 📊 ANALYSE-ERGEBNISSE:")
                    
                    for success in successes:
                        st.markdown(success)
                    for issue in issues:
                        st.markdown(issue)
                            
                except Exception as e:
                    st.error(f"FATALER FEHLER: Verbindung zum Ziel fehlgeschlagen -> {e}")
