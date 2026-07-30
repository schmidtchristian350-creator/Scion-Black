import requests
import streamlit as st

# Konfiguration der Seite im edlen Dark-Mode (Anthrazit & optimierter Kontrast)
st.set_page_config(
    page_title="Scion-Black // Security Audit", 
    page_icon="🛡️", 
    layout="wide"
)

# --- CSS FÜR SAUBERES, DUNKLES DESIGN MIT OPTIMALER LESBARKEIT ---
st.markdown("""
    <style>
    /* Globaler Dark Mode mit tiefem Anthrazit und exzellent lesbarem Text */
    .stApp {
        background-color: #0e1117;
        color: #e5e7eb;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Klare, saubere Überschriften in hellem Weiß */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 600;
        letter-spacing: -0.5px;
    }

    /* Input-Felder kontraststark und klar lesbar */
    .stTextInput input {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid #374151 !important;
        border-radius: 6px;
    }

    /* Buttons im sauberen Tech-Look mit perfektem Kontrast */
    .stButton button {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid #4b5563 !important;
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
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }

    /* Infoboxen und Warnungen mit hohem Kontrast für beste Lesbarkeit */
    .stAlert {
        background-color: #1f2937 !important;
        color: #f3f4f6 !important;
        border: 1px solid #374151 !important;
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
    st.markdown("Überprüfung, Schwachstellen-Analyse und Angriffsvektoren der Web-Infrastruktur.")
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
                    
                    # Erweiterte Checks mit konkreten Erklärungen zu Angriffsvektoren
                    checks = {
                        "Strict-Transport-Security": (
                            "HSTS-Header", 
                            "Erzwingt verschlüsselte HTTPS-Verbindungen.",
                            "🔴 **Angriffsszenario (Man-in-the-Middle):** Fehlt dieser Header, können Angreifer im selben WLAN (z. B. Café oder Flughafen) unverschlüsselte Anfragen abfangen (SSL-Stripping), den Nutzer auf eine gefälschte HTTP-Seite umleiten und so Zugangsdaten oder Sitzungs-Cookies im Klartext abgreifen."
                        ),
                        "X-Content-Type-Options": (
                            "X-Content-Type-Options", 
                            "Verhindert MIME-Sniffing von Dateitypen.",
                            "🔴 **Angriffsszenario (MIME-Sniffing / XSS):** Ohne diesen Header ignorieren Browser manchmal den echten Dateityp und interpretieren hochgeladene, harmlose Dateien (wie ein Profilbild) plötzlich als ausführbaren Programmcode (JavaScript), wodurch Angreifer Schadcode im Browser des Opfers ausführen können."
                        ),
                        "X-Frame-Options": (
                            "X-Frame-Options", 
                            "Schützt vor Clickjacking.",
                            "🔴 **Angriffsszenario (Clickjacking):** Wenn dieser Header fehlt, kann ein Angreifer deine Webseite unsichtbar in einen Rahmen (Iframe) auf seiner eigenen bösartigen Website einbinden. Klickt der Nutzer dort auf scheinbare Gewinnspiel-Buttons, klickt er in Wirklichkeit auf deiner echten Seite (z. B. auf 'Konto löschen' oder 'Geld überweisen')."
                        ),
                        "Content-Security-Policy": (
                            "Content-Security-Policy (CSP)", 
                            "Schützt vor Cross-Site Scripting (XSS).",
                            "🔴 **Angriffsszenario (Cross-Site Scripting / Data Theft):** Das Fehlen einer CSP ist eine schwere Lücke. Angreifer können über Kommentarfelder oder Formulare bösartigen JavaScript-Code einschleusen. Der Browser führt diesen aus, liest sensible Session-Tokens aus und schickt sie direkt an den Hacker, der sich daraufhin als der Nutzer einloggen kann."
                        ),
                        "Referrer-Policy": (
                            "Referrer-Policy", 
                            "Kontrolliert die Weitergabe von URL-Informationen.",
                            "🔴 **Angriffsszenario (Information Disclosure):** Ohne strikte Richtlinie sendet der Browser bei jedem externen Link-Klick die komplette vorherige URL (inklusive interner Pfade, IDs oder Token-Fragmente) an fremde Server. Angreifer können so über ihre Server-Logfiles sensible URLs und Zugangslinks von Besuchern einsehen."
                        )
                    }

                    issues = []
                    successes = []

                    for header, (name, desc, attack_vector) in checks.items():
                        if header not in headers:
                            issues.append(f"### ⚠️ {name} fehlt\n* **Schutz:** {desc}\n* {attack_vector}\n---")
                        else:
                            successes.append(f"✅ **{name} vorhanden:** Schutz aktiv ({desc})")

                    st.markdown("### 📊 Analyseergebnisse & Angriffsvektoren:")
                    
                    if successes:
                        st.markdown("#### Gesicherte Bereiche:")
                        for success in successes:
                            st.markdown(success)
                    
                    if issues:
                        st.markdown("#### 🚨 Gefundene Schwachstellen & potenzielle Einfallstore:")
                        for issue in issues:
                            st.markdown(issue)
                            
                except Exception as e:
                    st.error(f"Fehler bei der Verbindung zum Ziel: {e}")
