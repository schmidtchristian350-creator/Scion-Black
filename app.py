import requests
import streamlit as st

# Konfiguration der Seite im edlen Dark-Mode (Anthrazit & Blau)
st.set_page_config(
    page_title="Scion-Black // Security Audit", 
    page_icon="🛡️", 
    layout="wide"
)

# --- CSS FÜR SAUBERES, DUNKLES ANTHRAZIT-DESIGN ---
st.markdown("""
    <style>
    /* Globaler Dark Mode mit edlem Anthrazit-Hintergrund */
    .stApp {
        background-color: #121619;
        color: #d1d5db;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Klare, saubere Überschriften in hellem Grau/Weiß */
    h1, h2, h3 {
        color: #f3f4f6 !important;
        font-weight: 600;
        letter-spacing: -0.5px;
    }

    /* Input-Felder dezent und modern */
    .stTextInput input {
        background-color: #1b2227 !important;
        color: #f3f4f6 !important;
        border: 1px solid #2f3e46 !important;
        border-radius: 6px;
    }

    /* Buttons im sauberen Tech-Blau / Dark Style */
    .stButton button {
        background-color: #1f2937 !important;
        color: #f3f4f6 !important;
        border: 1px solid #374151 !important;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border: 1px solid #2563eb !important;
    }

    /* Sidebar / Login Bereich */
    [data-testid="stSidebar"] {
        background-color: #181f24;
        border-right: 1px solid #273038;
    }

    /* Infoboxen und Warnungen harmonisch eingefügt */
    .stAlert {
        background-color: #1b2227 !important;
        color: #d1d5db !important;
        border: 1px solid #2f3e46 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Session State für Login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- SEITENBAR FÜR LOGIN (Links, verschwindet nach erfolgreichem Login) ---
if not st.session_state["logged_in"]:
    with st.sidebar:
        st.markdown("### 🔐 System-Login")
        st.markdown("<p style='color: #9ca3af; font-size: 13px;'>Geschützter Administrationsbereich</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username_input = st.text_input("Benutzername")
            password_input = st.text_input("Passwort", type="password")
            submit_button = st.form_submit_button("Anmelden")
            
            if submit_button:
                if username_input == "Christian" and password_input == "scionblack2026!!!":
                    st.session_state["logged_in"] = True
                    st.rerun()
                else:
                    st.error("Zugriff verweigert: Ungültige Anmeldedaten.")

    # Hauptbereich für nicht eingeloggte Nutzer
    st.title("🛡️ Scion-Black Security Dashboard")
    st.markdown("### Professionelle Webseiten- und Header-Analyse")
    st.markdown("---")
    st.info("ℹ️ **Hinweis:** Bitte melden Sie sich über die linke Seitenleiste an, um fortzufahren.")
    
    st.code("""
[Status] System bereit.
[Status] Warte auf Administrator-Authentifizierung...
    """, language="bash")

else:
    # --- EINGELOGGT: SAUBERES ANTHRAZIT DASHBOARD ---
    with st.sidebar:
        st.markdown("### ⚙️ Steuerung")
        st.markdown("Status: **Aktiv**")
        st.markdown("Rolle: **Administrator**")
        st.markdown("---")
        if st.button("Abmelden"):
            st.session_state["logged_in"] = False
            st.rerun()

    st.title("🛡️ Scion-Black")
    st.markdown("Überprüfung und Optimierung der Web-Infrastruktur.")
    st.markdown("---")

    # Ziel-URL eingeben
    target_url = st.text_input("Ziel-URL eingeben (inkl. https://):", "https://example.com")

    if st.button("Analyse starten"):
        if not target_url.startswith("http"):
            st.error("Bitte eine gültige URL angeben, die mit http:// oder https:// beginnt.")
        else:
            with st.spinner("Analysiere Ziel-Infrastruktur..."):
                try:
                    response = requests.get(target_url, timeout=5)
                    headers = response.headers
                    
                    st.success(f"Verbindung erfolgreich hergestellt. Status-Code: {response.status_code}")
                    
                    checks = {
                        "Strict-Transport-Security": ("HSTS-Header", "Erzwingt verschlüsselte HTTPS-Verbindungen."),
                        "X-Content-Type-Options": ("X-Content-Type-Options", "Verhindert MIME-Sniffing von Dateitypen."),
                        "X-Frame-Options": ("X-Frame-Options", "Schützt vor Clickjacking (Einbetten in fremde Iframes)."),
                        "Content-Security-Policy": ("Content-Security-Policy (CSP)", "Schützt vor Cross-Site Scripting (XSS)-Angriffen."),
                        "Referrer-Policy": ("Referrer-Policy", "Kontrolliert die Weitergabe von URL-Informationen.")
                    }

                    issues = []
                    successes = []

                    for header, (name, desc) in checks.items():
                        if header not in headers:
                            issues.append(f"⚠️ **{name} fehlt:** {desc}")
                        else:
                            successes.append(f"✅ **{name} vorhanden:** Schutz aktiv ({desc})")

                    st.markdown("### 📊 Analyseergebnisse:")
                    
                    for success in successes:
                        st.markdown(success)
                    for issue in issues:
                        st.markdown(issue)
                            
                except Exception as e:
                    st.error(f"Fehler bei der Verbindung zum Ziel: {e}")
