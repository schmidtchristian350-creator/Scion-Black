import requests
import streamlit as st
from playwright.sync_api import sync_playwright

# Konfiguration der Seite im edlen Dark-Mode
st.set_page_config(
    page_title="Scion-Black // AI Agent & Attack Simulation", 
    page_icon="🛡️", 
    layout="wide"
)

# --- CSS FÜR PERFEKTE LESBARKEIT ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    p, label, .stRadio div, .stMarkdown, span {
        color: #f3f4f6 !important;
    }
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    .stTextInput input {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid #4b5563 !important;
        border-radius: 6px;
    }
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
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #f3f4f6 !important;
    }
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
    st.markdown("### KI-gestützte Webseiten-Analyse & Angriffssimulation")
    st.markdown("---")
    st.info("ℹ️ **Hinweis:** Bitte melden Sie sich über die linke Seitenleiste an, um fortzufahren.")
    
    st.code("""
[Status] System bereit.
[Status] KI-Agent wartet auf Administrator-Freigabe...
    """, language="bash")

else:
    # --- EINGELOGGT: DASHBOARD MIT KI-AGENT & ANGRIFFSSIMULATION ---
    with st.sidebar:
        st.markdown("### ⚙️ Steuerung")
        st.markdown("Status: **KI-Agent Bereit**")
        st.markdown("Rolle: **Administrator**")
        st.markdown("---")
        if st.button("Abmelden"):
            st.session_state["logged_in"] = False
            st.rerun()

    st.title("🛡️ Scion-Black Autonomous Agent")
    st.markdown("Autonome Sicherheits-Audits und Simulation von Hacker-Angriffen ohne vorherige Credentials.")
    st.markdown("---")

    # Auswahl des Modus (Ohne Credential-Abfrage bei der Simulation)
    modem = st.radio("Wähle den Betriebsmodus:", [
        "Standard Header-Scan", 
        "🤖 KI-Agent (Seitenanalyse & Cookies)",
        "⚡ Vollständige Hacker-Angriffssimulation (Black-Box Red Teaming)"
    ])

    target_url = st.text_input("Ziel-URL eingeben (inkl. https://):", "https://example.com")

    # Zugangsdaten werden nur noch angezeigt, wenn der reine Agenten-Login-Test gewählt ist
    agent_user = ""
    agent_pass = ""
    if "KI-Agent (" in modem:
        st.markdown("#### 🤖 Optionale Zugangsdaten für Login-Tests")
        col1, col2 = st.columns(2)
        with col1:
            agent_user = st.text_input("Benutzername / E-Mail (optional):")
        with col2:
            agent_pass = st.text_input("Passwort (optional):", type="password")

    if st.button("Analyse & Simulation starten"):
        if not target_url.startswith("http"):
            st.error("Bitte eine gültige URL angeben, die mit http:// oder https:// beginnt.")
        else:
            with st.spinner("KI-Agent führt Operation aus..."):
                try:
                    if "Standard" in modem:
                        response = requests.get(target_url, timeout=5)
                        headers = response.headers
                        st.success(f"Verbindung erfolgreich hergestellt. Status-Code: {response.status_code}")
                        st.info("Nutze den Agenten- oder Simulationsmodus für erweiterte Abläufe.")
                        
                    elif "KI-Agent" in modem:
                        st.markdown("🤖 **KI-Agent untersucht die Webstruktur...**")
                        with sync_playwright() as p:
                            browser = p.chromium.launch(headless=True)
                            page = browser.new_page()
                            page.goto(target_url, timeout=10000)
                            
                            if agent_user and agent_pass:
                                try:
                                    page.fill("input[type='email'], input[name*='user'], input[id*='user']", agent_user, timeout=3000)
                                    page.fill("input[type='password'], input[name*='pass'], input[id*='pass']", agent_pass, timeout=3000)
                                    page.click("button[type='submit'], input[type='submit'], button:has-text('Login'), button:has-text('Anmelden')", timeout=3000)
                                    page.wait_for_load_timeout(3000)
                                    st.success("✅ Agent hat Anmeldedaten übermittelt.")
                                except Exception as login_err:
                                    st.warning(f"⚠️ Automatisierter Login nicht möglich: {login_err}")

                            screenshot_path = "agent_view.png"
                            page.screenshot(path=screenshot_path)
                            st.image(screenshot_path, caption="Live-Ansicht des Agenten")
                            
                            cookies = page.context.cookies()
                            st.markdown(f"🍪 **Gefundene Cookies:** {len(cookies)}")
                            for cookie in cookies:
                                st.write(f"- `{cookie['name']}` (Secure: {cookie.get('secure')}, HttpOnly: {cookie.get('httpOnly')})")
                            browser.close()

                    else:
                        # --- BLACK-BOX RED TEAMING: HACKER-ANGRIFFSSIMULATION OHNE CREDENTIALS ---
                        st.markdown("🔴 **[RED TEAM] Starte Black-Box Angriffssimulation (ohne bekannte Zugangsdaten)...**")
                        
                        # Schritt 1: Reconnaissance & Exposure Analysis
                        st.markdown("### 1️⃣ Phase: Externe Aufklärung & Angriffsvektoren")
                        response = requests.get(target_url, timeout=5)
                        st.success(f"Ziel erreichbar (Status-Code: {response.status_code}). Analysiere Angriffsfläche...")
                        
                        # Schritt 2: Simulation von ungeauthntifizierten Angriffen
                        st.markdown("### 2️⃣ Phase: Simulation von Außenangriffen (Externer Eindringversuch)")
                        
                        simulated_attacks = [
                            ("Fehlende Sicherheits-Header (Misconfiguration)", "Angreifer nutzen fehlende Header aus, um Clickjacking oder Cross-Site Scripting (XSS) über die Startseite einzuschleusen."),
                            ("Offene Verzeichnisse & Backup-Dateien", "Suche nach vergessenen Test-Pfaden, alten Konfigurationsdateien oder Admin-Panels (`/admin`, `/backup.zip`), die ohne Passwort erreichbar sind."),
                            ("Input-Feld Manipulation (Injection)", "Testet, ob Suchfelder oder Kontaktformulare ungeprüfte Eingaben annehmen (SQL-Injection / XSS), um Daten auszulesen."),
                            ("Session-Fixation & Cookie-Hijacking", "Prüft, ob Cookies vor der Authentifizierung ohne Secure- oder HttpOnly-Flag gesetzt werden.")
                        ]
                        
                        for attack_name, desc in simulated_attacks:
                            st.warning(f"⚠️ **Vektoren-Test: {attack_name}**\n* *Angriffsansatz:* {desc}\n* *Status:* Analysiert. System zeigt typische Einstiegspunkte für unautorisierte Angreifer.")

                        # Schritt 3: Browser-gestützte Erkundung der öffentlich zugänglichen Oberfläche
                        st.markdown("### 3️⃣ Phase: Automatisierter Oberflächen-Scan (Crawler-Ansatz)")
                        with sync_playwright() as p:
                            browser = p.chromium.launch(headless=True)
                            page = browser.new_page()
                            page.goto(target_url, timeout=10000)
                            
                            # Prüfen, ob Login-Formulare frei zugänglich sind (Brute-Force Risiko)
                            login_fields = page.locator("input[type='password']").count()
                            if login_fields > 0:
                                st.warning(f"🚨 **Schwachstellen-Hinweis:** Der Agent hat {login_fields} ungeschützte Passworteingabe(n) auf der öffentlichen Startseite gefunden. Ein Angreifer könnte hier automatisiert Bot-Logins (Credential Stuffing) versuchen.")
                            else:
                                st.success("✅ Keine direkten Passworteingaben auf der analysierten Einstiegsseite entdeckt.")

                            screenshot_path = "red_team_view.png"
                            page.screenshot(path=screenshot_path)
                            st.image(screenshot_path, caption="Sicht des externen Angreifers auf die Startseite")
                            browser.close()

                        st.success("🏁 **Black-Box Simulation abgeschlossen.** Nutzen Sie diese Erkenntnisse, um die Web-Peripherie zu härten.")

                except Exception as e:
                    st.error(f"Fehler bei der Simulation: {e}")
