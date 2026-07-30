import requests
import streamlit as st

# Konfiguration der Seite
st.set_page_config(page_title="Scion-Black Security Scanner", page_icon="🛡️", layout="centered")

# --- PASSWORT-SCHUTZ ---
def check_password():
    """Überprüft, ob das eingegebene Passwort korrekt ist."""
    def password_entered():
        # Hier kannst du dein eigenes Passwort festlegen
        if st.session_state["password"] == "scion2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Passwort aus der Session löschen
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Erster Aufruf: Eingabefeld anzeigen
        st.title("🔒 Login erforderlich")
        st.text_input("Bitte gib das Passwort ein, um die App zu entsperren:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Falsches Passwort eingegeben
        st.title("🔒 Login erforderlich")
        st.text_input("Bitte gib das Passwort ein, um die App zu entsperren:", type="password", on_change=password_entered, key="password")
        st.error("😕 Das Passwort ist leider falsch.")
        return False
    else:
        # Korrektes Passwort
        return True

# Wenn das Passwort nicht stimmt, stoppen wir hier die Ausführung der App
if not check_password():
    st.stop()


# --- HAUPTAPP (Nach erfolgreichem Login) ---
st.title("🛡️ Scion-Black Security Scanner")
st.write("Professionelles Tool zur Überprüfung von Webseiten-Sicherheits-Headern.")

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
                
                # Erweiterte Sicherheits-Checks (Headers + Erklärung)
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
