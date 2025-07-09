import requests
import time

# === CONFIGURATION ===
URL = "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=5.9409699_47.3200746_6.0834844_47.2006872"
BOT_TOKEN = "8015395788:AAFV_ovHTYP0UNaYzPp0wfof7frYmfD4R1I"
CHAT_ID = "5825590629"
CHECK_INTERVAL = 180  # 3 minutes

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "fr-FR,fr;q=0.9",
    "Connection": "keep-alive"
}

def envoyer_message_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def verifier_logements():
    response = requests.get(URL, headers=HEADERS)
    html = response.text
    return "Aucun logement trouvé" not in html

def lancer_bot():
    print("✅ Bot CROUS lancé")
    envoyer_message_telegram("🚀 Le bot CROUS vient de démarrer.")
    deja_signale = False

    while True:
        try:
            if verifier_logements():
                if not deja_signale:
                    envoyer_message_telegram("🟢 Un ou plusieurs logements CROUS sont disponibles ! 🔗 " + URL)
                    deja_signale = True
            else:
                print("❌ Aucun logement trouvé.")
                deja_signale = False
        except Exception as e:
            print("❗ Erreur :", e)
            envoyer_message_telegram("❗ Le bot a rencontré une erreur :\n" + str(e))
            break

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    lancer_bot()
