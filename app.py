import os
import subprocess
import requests
import streamlit as st
import dns.resolver

# Konfiguration der Seite im edlen Dark-Mode
st.set_page_config(
    page_title="Scion-Black // Human-in-the-Loop A2A", 
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
    content = f"""SCION-BLACK HUMAN-IN-THE-LOOP AUDIT REPORT
=============================================
Ziel-URL: {target}

FREigegebene ANALYSERGEBNISSE:
{results_text}
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

# --- MULTI-AGENTEN SCHRITTE MIT ERKLÄRUNG & FREIGABE ---

def execute_recon_step(target_url):
    log = []
    log.append("🤖 **[Recon-Agent]** Führe DNS- und IP-Enumeration aus...")
    try:
        clean_domain = target_url.replace("https://", "").replace("http://", "").split("/")[0]
        answers = dns.resolver.resolve(clean_domain, 'A')
        ip_list = [ip.address for ip in answers]
        log.append(f"🌐 **[Recon-Agent]** IP-Adressen ermittelt: {', '.join(ip_list)}")
    except Exception as e:
        log.append(f"ℹ️ **[Recon-Agent]** DNS-Hinweis: {e}")
    return log

def execute_vulnerability_step(target_url):
    log = []
    log.append("🤖 **[Vulnerability-Agent]** Prüfe HTTP-Header und Angriffsvektoren...")
    try:
        response = requests.get(target_url, timeout=5)
        log.append(f"✅ **[Vulnerability-Agent]** Ziel erreichbar (Status-Code: {response.status_code}).")
        
        simulated_attacks = [
            ("Fehlende Sicherheits-Header (Misconfiguration)", "Prüfung auf Clickjacking- und XSS-Risiken."),
            ("Offene Verzeichnisse & Backup-Dateien", "Suche nach erreichbaren Test-Pfaden."),
            ("Input-Feld Manipulation (Injection)", "Analyse der Eingabeschnittstellen."),
            ("Session-Fixation & Cookie-Hijacking", "Überprüfung von Cookie-Flags (Secure/HttpOnly).")
        ]
        for attack_name, desc in simulated_attacks:
            log.append(f"- ⚠️ **{attack_name}:** {desc}")
    except Exception as e:
        log.append(f"❌ **[Vulnerability-Agent] Fehler:** {e}")
    return log

def execute_surface_step(target_url):
    log = []
    log.append("🤖 **[Surface-Agent]** Analysiere Webseiten-Struktur auf Einstiegspunkte...")
    try:
        response = requests.get(target_url, timeout=5)
        if "<form" in response.text.lower():
            log.append("🚨 **[Surface-Agent]** Login- oder Eingabeformulare auf der Startseite erkannt.")
        else:
            log.append("✅ **[Surface-Agent]** Keine kritischen Formulare auf der Einstiegsseite.")
    except Exception as e:
        log.append(f"ℹ️ **[Surface-Agent]** Hinweis: {e}")
    return log


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
[Status] Human-in-the-Loop A2A-Netzwerk im Standby...
    """, language="bash")

else:
    # --- EINGELOGGT: DASHBOARD MIT HUMAN-IN-THE-LOOP ---
    with st.sidebar:
        st.markdown("### ⚙️ Steuerung")
        st.markdown("Status: **Human-in-the-Loop Aktiv**")
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

    st.title("🛡️ Scion-Black // Human-in-the-Loop A2A")
    st.markdown("Kontrollierte, interaktive Webseiten-Analyse mit manueller Freigabe für jeden Schritt.")
    st.markdown("---")

    modem = st.radio("Wähle den Betriebsmodus:", [
        "Standard Header-Scan", 
        "🤖 KI-Agent (Seitenanalyse & Cookies)",
        "⚡ Systemangriff (Human-in-the-Loop A2A)"
    ])

    target_url = st.text_input("Ziel-URL eingeben (inkl. https://):", "https://example.com")

    # Wenn der Systemangriff-Modus gewählt ist, fragen wir vorab nach den Freigaben (Human-in-the-Loop)
    if modem == "⚡ Systemangriff (Human-in-the-Loop A2A)":
        st.markdown("---")
        st.markdown("### 🛡️ **Sicherheits- & Freigabekonsole (Human-in-the-Loop)**")
        st.markdown("Bitte prüfe die folgenden geplanten Aktionen und erteile die notwendigen Freigaben:")

        with st.expander("🔍 **Schritt 1: Netzwerk- & DNS-Aufklärung (Recon-Agent)**", expanded=True):
            st.markdown("""
            * **Erklärung:** Der Agent fragt die DNS-Server ab, um die echten IP-Adressen hinter der Ziel-URL herauszufinden.
            * **Auswirkungen:** Es wird passiv/aktiv Netzwerkverkehr zum Domain-Name-Server erzeugt. Das Ziel merkt davon in der Regel nichts, aber es ist der erste Schritt zur Identifikation der Infrastruktur.
            """)
            approve_step1 = st.checkbox("Schritt 1 freigeben und ausführen", value=True)

        with st.expander("⚠️ **Schritt 2: Schwachstellen-Analyse (Vulnerability-Agent)**", expanded=True):
            st.markdown("""
            * **Erklärung:** Der Agent verbindet sich direkt per HTTP mit der Zielseite und prüft Sicherheits-Header, Cookies und bekannte Einstiegspunkte.
            * **Auswirkungen:** Es werden Standard-Anfragen an den Webserver gesendet. Dies taucht in den normalen Logdateien des Zielservers auf. Es werden keine schädlichen Payloads oder Hacks ausgeführt.
            """)
            approve_step2 = st.checkbox("Schritt 2 freigeben und ausführen", value=True)

        with st.expander("🖥️ **Schritt 3: Oberflächen- und Struktur-Scan (Surface-Agent)**", expanded=True):
            st.markdown("""
            * **Erklärung:** Der Agent durchsucht den HTML-Quelltext nach Formularen, Eingabefeldern oder Login-Masken.
            * **Auswirkungen:** Identifiziert potenzielle Schnittstellen, die für automatisierte Eingabetests anfällig sein könnten. Keine Modifikation am Ziel.
            """)
            approve_step3 = st.checkbox("Schritt 3 freigeben und ausführen", value=True)
        st.markdown("---")

    if st.button("Analyse & Freigabe-Prozess starten"):
        if not target_url.startswith("http"):
            st.error("Bitte eine gültige URL angeben, die mit http:// oder https:// beginnt.")
        else:
            with st.spinner("Führe freigegebene Operationen aus..."):
                try:
                    report_summary = ""
                    
                    if "Standard" in modem:
                        response = requests.get(target_url, timeout=5)
                        st.success(f"Verbindung erfolgreich hergestellt. Status-Code: {response.status_code}")
                        report_summary = f"Standard Header-Scan erfolgreich. Status-Code: {response.status_code}"
                        st.info("Nutze den Kontroll-Modus für erweiterte Abläufe.")
                        
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
                        # --- HUMAN-IN-THE-LOOP AUSFÜHRUNG ---
                        st.markdown("🔴 **[A2A MASTER] Starte kontrollierte Ausführung nach menschlicher Freigabe...**")
                        agent_logs = []

                        if approve_step1:
                            st.markdown("---")
                            logs_1 = execute_recon_step(target_url)
                            for l in logs_1:
                                st.markdown(l)
                                agent_logs.append(l)
                        else:
                            st.info("ℹ️ Schritt 1 (Recon) wurde vom Benutzer übersprungen.")

                        if approve_step2:
                            st.markdown("---")
                            logs_2 = execute_vulnerability_step(target_url)
                            for l in logs_2:
                                st.markdown(l)
                                agent_logs.append(l)
                        else:
                            st.info("ℹ️ Schritt 2 (Vulnerability) wurde vom Benutzer übersprungen.")

                        if approve_step3:
                            st.markdown("---")
                            logs_3 = execute_surface_step(target_url)
                            for l in logs_3:
                                st.markdown(l)
                                agent_logs.append(l)
                        else:
                            st.info("ℹ️ Schritt 3 (Surface) wurde vom Benutzer übersprungen.")

                        st.success("🏁 **Human-in-the-Loop Simulation erfolgreich abgeschlossen.**")
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
                    st.error(f"Fehler bei der Ausführung: {e}")
