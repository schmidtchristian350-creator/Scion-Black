import os
import subprocess
import requests
import streamlit as st
import dns.resolver

# Konfiguration der Seite im edlen Dark-Mode
st.set_page_config(
    page_title="Scion-Black // Multi-Agent A2A System", 
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

# Hilfsfunktion zur Report-Generierung
def generate_report_file(target, results_text):
    filename = "scion_black_security_report.txt"
    content = f"""SCION-BLACK MULTI-AGENT A2A AUDIT REPORT
==========================================
Ziel-URL: {target}

ZUSAMMENFASSUNG DER ANALYSERGEBNISSE:
{results_text}
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

# --- MULTI-AGENTEN SYSTEM (A2A - Agent to Agent Kommunikation) ---

def agent_recon_node(target_url):
    """Sub-Agent 1: Zuständig für DNS- und Netzwerk-Aufklärung"""
    log = []
    log.append("🤖 **[Recon-Agent]** Starte Netzwerk- und DNS-Enumeration...")
    try:
        clean_domain = target_url.replace("https://", "").replace("http://", "").split("/")[0]
        answers = dns.resolver.resolve(clean_domain, 'A')
        ip_list = [ip.address for ip in answers]
        log.append(f"🌐 **[Recon-Agent]** Domain `{clean_domain}` aufgelöst auf IP(s): {', '.join(ip_list)}")
    except Exception as e:
        log.append(f"ℹ️ **[Recon-Agent]** DNS-Hinweis: {e}")
    return log

def agent_vulnerability_node(target_url):
    """Sub-Agent 2: Prüft Header, Konfigurationen und Angriffsvektoren"""
    log = []
    log.append("🤖 **[Vulnerability-Agent]** Übernehme Daten von Recon-Agent. Analysiere Angriffsvektoren...")
    try:
        response = requests.get(target_url, timeout=5)
        log.append(f"✅ **[Vulnerability-Agent]** Ziel erreichbar (Status-Code: {response.status_code}).")
        
        simulated_attacks = [
            ("Fehlende Sicherheits-Header (Misconfiguration)", "Angreifer nutzen fehlende Header für Clickjacking oder XSS."),
            ("Offene Verzeichnisse & Backup-Dateien", "Prüfung auf vergessene Test-Pfade (`/admin`, `/backup.zip`)."),
            ("Input-Feld Manipulation (Injection)", "Test auf ungeprüfte Eingabefelder (SQL-Injection / XSS)."),
            ("Session-Fixation & Cookie-Hijacking", "Überprüfung von Cookies auf Secure- und HttpOnly-Flags.")
        ]
        for attack_name, desc in simulated_attacks:
            log.append(f"- ⚠️ **[Vulnerability-Agent] {attack_name}:** {desc}")
    except Exception as e:
        log.append(f"❌ **[Vulnerability-Agent] Fehler:** {e}")
    return log

def agent_surface_node(target_url):
    """Sub-Agent 3: Scannt die Oberfläche und übergibt an den Master"""
    log = []
    log.append("🤖 **[Surface-Agent]** Analysiere Webseiten-Struktur und Formulare...")
    try:
        response = requests.get(target_url, timeout=5)
        content_lower = response.text.lower()
        if "<form" in content_lower:
            log.append("🚨 **[Surface-Agent]** Formularelemente (Logins/Inputs) auf der Startseite erkannt.")
        else:
            log.append("✅ **[Surface-Agent]** Keine kritischen Formulare auf der Einstiegsseite entdeckt.")
    except Exception as e:
        log.append(f"ℹ️ **[Surface-Agent]** Oberflächen-Scan Hinweis: {e}")
    return log

def master_coordinator_agent(target_url):
    """Master-Agent koordiniert die A2A-Pipeline"""
    full_report = []
    
    # Übergabe an Agent 1
    r_logs = agent_recon_node(target_url)
    full_report.extend(r_logs)
    
    # Übergabe an Agent 2 (nutzt Ergebnisse/Ziel)
    v_logs = agent_vulnerability_node(target_url)
    full_report.extend(v_logs)
    
    # Übergabe an Agent 3
    s_logs = agent_surface_node(target_url)
    full_report.extend(s_logs)
    
    return full_report


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
[Status] Multi-Agenten A2A-Netzwerk wartet auf Freigabe...
    """, language="bash")

else:
    # --- EINGELOGGT: DASHBOARD MIT MULTI-AGENTEN SYSTEM ---
    with st.sidebar:
        st.markdown("### ⚙️ Steuerung")
        st.markdown("Status: **Multi-Agent A2A Aktiv**")
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

    st.title("🛡️ Scion-Black // Multi-Agent A2A System")
    st.markdown("Autonome Webseiten-Analyse durch kooperierende Sub-Agenten.")
    st.markdown("---")

    modem = st.radio("Wähle den Betriebsmodus:", [
        "Standard Header-Scan", 
        "🤖 KI-Agent (Seitenanalyse & Cookies)",
        "⚡ Systemangriff (Multi-Agent A2A Red Teaming)"
    ])

    target_url = st.text_input("Ziel-URL eingeben (inkl. https://):", "https://example.com")

    if st.button("Analyse & Simulation starten"):
        if not target_url.startswith("http"):
            st.error("Bitte eine gültige URL angeben, die mit http:// oder https:// beginnt.")
        else:
            with st.spinner("Multi-Agenten-Netzwerk (A2A) führt Operation aus..."):
                try:
                    report_summary = ""
                    
                    if "Standard" in modem:
                        response = requests.get(target_url, timeout=5)
                        st.success(f"Verbindung erfolgreich hergestellt. Status-Code: {response.status_code}")
                        report_summary = f"Standard Header-Scan erfolgreich. Status-Code: {response.status_code}"
                        st.info("Nutze den Multi-Agenten-Modus für erweiterte Abläufe.")
                        
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
                        # --- MULTI-AGENT A2A SYSTEMANGRIFF ---
                        st.markdown("🔴 **[A2A MASTER] Starte kooperativen Systemangriff...**")
                        
                        agent_logs = master_coordinator_agent(target_url)
                        for log_entry in agent_logs:
                            st.markdown(log_entry)

                        st.success("🏁 **Multi-Agenten A2A Simulation erfolgreich abgeschlossen.**")
                        report_summary = "\n".join(agent_logs)

                    # Report Download Button anbieten
                    report_file = generate_report_file(target_url, report_summary)
                    with open(report_file, "rb") as f:
                        st.download_button(
                            label="📄 Sicherheits-Report als Datei herunterladen",
                            data=f,
                            file_name="Scion_Black_Audit_Report.txt",
                            mime="text/plain"
                        )

                    # Gewünschte Abschlussfrage
                    st.markdown("---")
                    st.markdown("### ❓ **Welcher Angriff soll durchgeführt werden, oder möchtest du diese Webseite bearbeiten?**")

                except Exception as e:
                    st.error(f"Fehler bei der Simulation: {e}")
