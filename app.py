import requests
import streamlit as st
from playwright.sync_api import sync_playwright

# Konfiguration der Seite im edlen Dark-Mode
st.set_page_config(
    page_title="Scion-Black // AI Agent & Security Audit", 
    page_icon="🛡️", 
    layout="wide"
)

# --- CSS FÜR PERFEKTE LESBARKEIT (Heller Text, klare Kontraste) ---
st.markdown("""
    <style>
    /* Globaler Text: Deutlich helleres Grau für exzellente Lesbarkeit */
    .stApp {
        background-color: #0e1117;
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Alle normalen Texte, Labels und Radio-Buttons absolut klar lesbar machen */
    p, label, .stRadio div, .stMarkdown, span {
        color: #f3f4f6 !important;
    }

    /* Überschriften in reinem Weiß */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 600;
        letter-spacing: -0.5px;
    }

    /* Input-Felder kontraststark und klar lesbar */
    .stTextInput input {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid #4b5563 !important;
        border-radius: 6px;
    }

    /* Buttons im sauberen Tech-Look */
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

    /* Sidebar / Login Bereich & dessen Textinhalte */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #f3f4f6 !important;
    }

    /* Infoboxen und Warnungen */
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

# --- SEITENBAR FÜR LOGIN ---
if not st.session_state["logged_in"]:
    with st.sidebar:
        st.markdown("### 🔐 System-Login")
        st.markdown("<p style='color: #d1d5db; font-size: 13px;'>Geschützter Administrationsbereich</p>", unsafe_allow_html=True)
        
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

    st.title("🛡️ Scion-Black Security Dashboard")
    st.markdown("### KI-gestützte Webseiten-Analyse & Agenten-Steuerung")
    st.markdown("---")
    st.info("ℹ️ **Hinweis:** Bitte melden Sie sich über die linke Seitenleiste an, um fortzufahren.")
    
    st.code("""
[Status] System bereit.
[Status] KI-Agent wartet auf Administrator-Freigabe...
    """, language="bash")

else:
    # --- EINGELOGGT: DASHBOARD MIT KI-AGENT ---
    with st.sidebar:
        st.markdown("### ⚙️ Steuerung")
        st.markdown("Status: **KI-Agent Bereit**")
        st.markdown("Rolle: **Administrator**")
        st.markdown("---")
        if st.button("Abmelden"):
            st.session_state["logged_in"] = False
            st.rerun()

    st.title("🛡️ Scion-Black")
    st.markdown("Sicherheits-Audit mit automatisierter Browser-Navigation.")
    st.markdown("---")

    # Auswahl des Modus
    modem = st.radio("Wähle den Betriebsmodus:", ["Standard Header-Scan", "🤖 KI-Agent mit Login & Authentifizierung"])

    target_url = st.text_input("Ziel-URL eingeben (inkl. https://):", "https://example.com")

    # Wenn der KI-Agent Modus gewählt ist, zeigen wir zusätzliche Felder für den Login
    agent_user = ""
    agent_pass = ""
    if "KI-Agent" in modem:
        st.markdown("#### 🤖 Agenten-Zugangsdaten für die Zielwebseite")
        col1, col2 = st.columns(2)
        with col1:
            agent_user = st.text_input("Benutzername / E-Mail für das Ziel:")
        with col2:
            agent_pass = st.text_input("Passwort für das Ziel:", type="password")

    if st.button("Analyse & Agenten-Run starten"):
        if not target_url.startswith("http"):
            st.error("Bitte eine gültige URL angeben, die mit http:// oder https:// beginnt.")
        else:
            with st.spinner("KI-Agent initialisiert Browser und analysiert Ziel..."):
                try:
                    if "Standard" in modem:
                        # Klassischer schneller Header-Check via requests
                        response = requests.get(target_url, timeout=5)
                        headers = response.headers
                        st.success(f"Verbindung erfolgreich hergestellt. Status-Code: {response.status_code}")
                        st.info("Nutze den KI-Agenten-Modus, um automatisierte Login-Prozesse und Tiefenprüfungen durchzuführen.")
                        
                    else:
                        # --- DER KI-AGENT (Playwright Browser Automation) ---
                        st.markdown("🤖 **KI-Agent übernimmt die Kontrolle...**")
                        
                        with sync_playwright() as p:
                            browser = p.chromium.launch(headless=True)
                            page = browser.new_page()
                            
                            st.write(f"🌐 Navigiere zu: `{target_url}`")
                            page.goto(target_url, timeout=10000)
                            
                            if agent_user and agent_pass:
                                st.write("🔑 Suche nach Login-Formularen und versuche automatische Anmeldung...")
                                try:
                                    page.fill("input[type='email'], input[name*='user'], input[id*='user']", agent_user, timeout=3000)
                                    page.fill("input[type='password'], input[name*='pass'], input[id*='pass']", agent_pass, timeout=3000)
                                    page.click("button[type='submit'], input[type='submit'], button:has-text('Login'), button:has-text('Anmelden')", timeout=3000)
                                    page.wait_for_load_timeout(3000)
                                    st.success("✅ Agent hat versucht, die Anmeldedaten zu übermitteln.")
                                except Exception as login_err:
                                    st.warning(f"⚠️ Konnte kein standardisiertes Login-Formular automatisch bedienen: {login_err}")

                            screenshot_path = "agent_view.png"
                            page.screenshot(path=screenshot_path)
                            st.image(screenshot_path, caption="Live-Ansicht des KI-Agenten nach Interaktion")
                            
                            cookies = page.context.cookies()
                            st.markdown(f"🍪 **Gefundene Session-Cookies nach Login:** {len(cookies)} Stück")
                            
                            for cookie in cookies:
                                secure_flag = "🔒 Sicher" if cookie.get("secure") else "⚠️ Unsicher (Kein Secure-Flag)"
                                http_only = "🛡️ HttpOnly" if cookie.get("httpOnly") else "⚠️ JavaScript-lesbar (XSS-Gefahr)"
                                st.write(f"- Cookie: `{cookie['name']}` | {secure_flag} | {http_only}")

                            browser.close()
                            st.success("🏁 KI-Agent hat den Audit erfolgreich abgeschlossen.")

                except Exception as e:
                    st.error(f"Fehler beim Ausführen des Agenten: {e}")
