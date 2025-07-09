import requests
import time

# === CONFIGURATION ===
URL = "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=5.9409699_47.3200746_6.0834844_47.2006872"
BOT_TOKEN = "8015395788:AAFV_ovHTYP0UNaYzPp0wfof7frYmfD4R1I"
CHAT_ID = "5825590629"
CHECK_INTERVAL = 180  # toutes les 3 minutes

# === Fonction Telegram ===
def envoyer_message_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        requests.post(url, data=payload)
    except Exception as e:
        print("Erreur d'envoi Telegram :", e)

# === Fonction principale ===
def verifier_et_alerter():
    deja_signale = False
    print("✅ Bot CROUS lancé.")
    envoyer_message_telegram("🚀 Le bot CROUS est lancé et surveille les logements...")

    while True:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(URL, headers=headers)
            contenu = response.text

            if "Aucun logement trouv" not in contenu:
                if not deja_signale:
                    print("📢 Logement trouvé !")
                    envoyer_message_telegram("🟢 Un logement CROUS est disponible ! 🔗 " + URL)
                    deja_signale = True
            else:
                print("❌ Aucun logement. On continue...")
                deja_signale = False

        except Exception as e:
            print("❗ Erreur :", e)
            envoyer_message_telegram(f"❗ Le bot a eu un problème : {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    verifier_et_alerter()
