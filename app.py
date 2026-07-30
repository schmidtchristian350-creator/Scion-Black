import requests
import streamlit as st

# Konfiguration der Seite im professionellen Look
st.set_page_config(
    page_title="Scion-Black | Security Scanner", 
    page_icon="🛡️", 
    layout="wide"
)

# --- CSS für saubere, neutrale Optik ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .login-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
    </style>
""", unsafe_allow_html=True)

# Session State für den Login initialisieren
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Haupttitel der App
st.title("🛡️ Scion-Black Security Scanner")
st.write("Professionelles Tool zur Überprüfung von Webseiten-Sicherheits-Headern und Absicherung von Unternehmensstrukturen.")
st.markdown("---")

# Wenn der Benutzer NOCH NICHT eingeloggt ist -> Layout aufteilen
if not st.session_state["logged_in"]:
    # Wir erstellen zwei Spalten: Links der Login, Rechts eine Info-Spalte
    col_login, col_info = st.columns([1, 2])
    
    with col_login:
        st.markdown("### 🔒 Admin Login")
        with st.form("login_form"):
            username_input = st.text_input("Benutzername")
            password_input = st.text_input("Passwort", type="password")
            submit_button = st.form_submit_button("Einloggen")
            
            if submit_button:
                # Fester Admin-Account
                if username_input == "admin" and password_input == "scion2026":
                    st.session_state["logged_in"] = True
                    st.rerun()
                else:
                    st.error("Falscher Benutzername oder falsches Passwort.")
                    
    with col_info:
        st.markdown("### Willkommen bei Scion-Black")
        st.info(
            "Dieses System ist für autorisierte Administratoren und Sicherheitsprüfungen vorgesehen. "
            "Bitte loggen Sie sich auf der linken Seite ein, um Zugriff auf das Audit-Dashboard und den Scanner zu erhalten."
        )

# Wenn der Benutzer EINGELOGGT ist -> Login ist weg, Scanner erscheint vollflächig
else:
    # Oben rechts oder als dezenten Hinweis die Option zum Ausloggen anbieten
    col_top1, col_top2 = st.columns([5, 1])
    with col_top2:
        if st.button("Abmelden"):
            st.session_state["logged_in"] = False
            st.rerun()

    st.success("Erfolgreich angemeldet als **Admin**.")
    
    # Eingabefeld für die Ziel-URL
    target_url = st.text_input("Gib die Webadresse ein (inkl. https://):", "https://example.com")

    if st.button("Scanner starten"):
        if not target_url.startswith("http"):
            st.error("Bitte gib eine gültige URL ein, die mit http:// oder https:// beginnt.")
        else:
            with st.spinner("Analysiere Sicherheits-Header..."):
                try:
                    # HTTP-Anfrage an die Zielseite senden
                    response = requests.get(target_url, timeout=5)
                    headers = response.headers
                    
                    st.success(f"Verbindung erfolgreich! Statuscode: {response.status_code}")
                    
                    # Sicherheits-Checks definieren
                    checks = {
                        "Strict-Transport-Security": ("HSTS-Header", "Erzwingt verschlüsselte HTTPS-Verbindungen."),
                        "X-Content-Type-Options": ("X-Content-Type-Options", "Verhindert MIME-Sniffing von Dateitypen."),
                        "X-Frame-Options": ("X-Frame-Options", "Schützt vor Clickjacking (Einbetten in fremde Iframes)."),
                        "Content-Security-Policy": ("Content-Security-Policy (CSP)", "Schützt vor Cross-Site Scripting (XSS)-Angriffen."),
                        "Referrer-Policy": ("Referrer-Policy", "Kontrolliert, welche URL-Informationen bei Links mitgesendet werden.")
                    }

                    issues = []
                    successes = []

                    for header, (name, desc) in checks.items():
                        if header not in headers:
                            issues.append(f"❌ **{name} fehlt:** {desc}")
                        else:
                            successes.append(f"✅ **{name} vorhanden:** Gut abgesichert! ({desc})")

                    # Ergebnisse übersichtlich anzeigen
                    st.subheader("📊 Ergebnisse der Sicherheits-Analyse:")
                    
                    for success in successes:
                        st.write(success)
                    for issue in issues:
                        st.write(issue)
                            
                except Exception as e:
                    st.error(f"Fehler bei der Verbindung zur Webseite: {e}")
