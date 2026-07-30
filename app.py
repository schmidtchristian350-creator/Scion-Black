import requests
import streamlit as st

# Titel der App im Browser
st.set_page_config(page_title="Web Security Scanner", page_icon="🛡️", layout="centered")

st.title("🛡️ Scion-Black")
st.write("Dieses Tool überprüft Webseiten auf grundlegende Sicherheits-Header, um Unternehmen bei der Absicherung zu helfen.")

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
                
                # Sicherheits-Checks durchführen
                issues = []
                
                # Check 1: HSTS (Zwingt Browser zu verschlüsselter Verbindung)
                if 'Strict-Transport-Security' not in headers:
                    issues.append("❌ **HSTS-Header fehlt:** Die Seite erzwingt keine strikte Transportverschlüsselung.")
                else:
                    issues.append("✅ **HSTS-Header vorhanden:** Gut gemacht!")
                    
                # Check 2: X-Content-Type-Options (Schützt vor MIME-Sniffing)
                if 'X-Content-Type-Options' not in headers:
                    issues.append("❌ **X-Content-Type-Options fehlt:** Anfällig für MIME-Sniffing-Angriffe.")
                else:
                    issues.append("✅ **X-Content-Type-Options vorhanden:** Gut gemacht!")

                # Ergebnisse in der App anzeigen
                st.subheader("Ergebnis der Überprüfung:")
                for issue in issues:
                    st.write(issue)
                    
            except Exception as e:
                st.error(f"Fehler bei der Verbindung zur Webseite: {e}")
