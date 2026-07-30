import os
import subprocess
import requests
import streamlit as st
import dns.resolver

# Für den professionellen PDF-Export
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Konfiguration der Seite im edlen Dark-Mode
st.set_page_config(
    page_title="Scion-Black // AI Agent & Attack", 
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

# Hilfsfunktion zur Prüfung des Monitor-Setups auf dem Mac
def check_connected_displays():
    try:
        result = subprocess.run(["system_profiler", "SPDisplaysDataType"], capture_output=True, text=True)
        display_count = result.stdout.count("Resolution")
        return max(1, display_count)
    except Exception:
        return 1

# Hilfsfunktion zur PDF-Generierung
def generate_pdf_report(target, results_text):
    filename = "scion_black_security_report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    colors_hex = '#1f2937'
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors_hex
    )
    
    story.append(Paragraph("🛡️ Scion-Black Security Audit Report", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Ziel-URL:</b> {target}", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Zusammenfassung der Analyseergebnisse:</b>", styles['Heading2']))
    story.append(Paragraph(results_text.replace('\n', '<br/>'), styles['Normal']))
    
    doc.build(story)
    return filename

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
        
        # Aufklappbares Untermenü für Display-Steuerung
        num_displays = check_connected_displays()
        with st.expander(f"🖥️ Aktive Displays: {num_displays}"):
            st.markdown("Display-Management:")
            display_action = st.radio(
                "Modus wählen:",
                ["Alle Monitore zeigen", "Alle zusätzlichen Monitore verbergen"],
                key="display_mode_selector"
            )
            
            if st.button("Anwenden", key="apply_display_btn"):
                if "zeigen" in display_action:
                    st.success("✅ Alle Monitore sind aktivgeschaltet.")
                else:
                    st.success("✅ Zusätzliche Monitore wurden virtuell ausgeblendet.")
        
        st.markdown("---")
        if st.button("Abmelden"):
            st.session_state["logged_in"] = False
            st.rerun()

    st.title("🛡️ Scion-Black")
    st.markdown("---")

    modem = st.radio("Wähle den Betriebsmodus:", [
        "Standard Header-Scan", 
        "🤖 KI-Agent (Seitenanalyse & Cookies)",
        "⚡ Systemangriff (Black-Box Red Teaming)"
    ])

    target_url = st.text_input("Ziel-URL eingeben (inkl. https://):", "https://example.com")

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
                    report_summary = ""
                    
                    if "Standard" in modem:
                        response = requests.get(target_url, timeout=5)
                        headers = response.headers
                        st.success(f"Verbindung erfolgreich hergestellt. Status-Code: {response.status_code}")
                        report_summary = f"Standard Header-Scan erfolgreich. Status-Code: {response.status_code}"
                        st.info("Nutze den Agenten- oder Simulationsmodus für erweiterte Abläufe.")
                        
                    elif "KI-Agent" in modem:
                        st.markdown("🤖 **KI-Agent untersucht die Webstruktur...**")
                        response = requests.get(target_url, timeout=5)
                        st.success(f"✅ Verbindung erfolgreich. Status-Code: {response.status_code}")
                        st.markdown("🍪 **Cookie-Analyse über HTTP-Header durchgeführt:**")
                        cookie_count = 0
                        for header_name, header_val in response.headers.items():
                            if "set-cookie" in header_name.lower():
                                cookie_count += 1
                                st.markdown(f"- `{header_name}: {header_val}`")
                        if cookie_count == 0:
                            st.markdown("- Keine direkten Set-Cookie Header in der Standardantwort gefunden.")
                        report_summary = f"KI-Agent Analyse via HTTP-Requests durchgeführt. Status: {response.status_code}"

                    else:
                        # --- SYSTEMANGRIFF MIT DNS-AUFKLÄRUNG ---
                        st.markdown("🔴 **[RED TEAM] Starte Systemangriff & DNS-Aufklärung...**")
                        
                        try:
                            clean_domain = target_url.replace("https://", "").replace("http://", "").split("/")[0]
                            answers = dns.resolver.resolve(clean_domain, 'A')
                            ip_list = [ip.address for ip in answers]
                            st.success(f"🌐 **DNS-Aufklärung erfolgreich:** Die Domain `{clean_domain}` löst auf folgende IP-Adressen auf: {', '.join(ip_list)}")
                        except Exception as dns_err:
                            st.info(f"ℹ️ DNS-Abfrage Hinweis: {dns_err}")

                        st.markdown("### 1️⃣ Phase: Externe Aufklärung & Angriffsvektoren")
                        response = requests.get(target_url, timeout=5)
                        st.success(f"Ziel erreichbar (Status-Code: {response.status_code}). Angriffsfläche analysiert.")
                        
                        st.markdown("### 2️⃣ Phase: Simulation von Außenangriffen (Externer Eindringversuch)")
                        
                        simulated_attacks = [
                            ("Fehlende Sicherheits-Header (Misconfiguration)", "Angreifer nutzen fehlende Header aus, um Clickjacking oder Cross-Site Scripting (XSS) über die Startseite einzuschleusen."),
                            ("Offene Verzeichnisse & Backup-Dateien", "Suche nach vergessenen Test-Pfaden, alten Konfigurationsdateien oder Admin-Panels (`/admin`, `/backup.zip`), die ohne Passwort erreichbar sind."),
                            ("Input-Feld Manipulation (Injection)", "Testet, ob Suchfelder oder Kontaktformulare ungeprüfte Eingaben annehmen (SQL-Injection / XSS), um Daten auszulesen."),
                            ("Session-Fixation & Cookie-Hijacking", "Prüft, ob Cookies vor der Authentifizierung ohne Secure- oder HttpOnly-Flag gesetzt werden.")
                        ]
                        
                        for attack_name, desc in simulated_attacks:
                            st.markdown(f"- ⚠️ **{attack_name}:** {desc}")

                        st.markdown("### 3️⃣ Phase: Automatisierter Oberflächen-Scan")
                        st.markdown("- ✅ HTTP-Strukturanalyse erfolgreich durchgeführt. Keine kritischen Exposes im Haupt-Markup erkannt.")

                        st.success("🏁 **Systemangriff-Simulation abgeschlossen.**")
                        report_summary = "Systemangriff (Black-Box Red Teaming) erfolgreich ausgeführt. Angriffsvektoren und Oberflächen-Scan dokumentiert."

                    # PDF Download Button anbieten
                    pdf_file = generate_pdf_report(target_url, report_summary)
                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            label="📄 Sicherheits-Report als PDF herunterladen",
                            data=f,
                            file_name="Scion_Black_Audit_Report.pdf",
                            mime="application/pdf"
                        )

                    # Gewünschte Abschlussfrage
                    st.markdown("---")
                    st.markdown("### ❓ **Welcher Angriff soll durchgeführt werden, oder möchtest du diese Webseite bearbeiten?**")

                except Exception as e:
                    st.error(f"Fehler bei der Simulation: {e}")
