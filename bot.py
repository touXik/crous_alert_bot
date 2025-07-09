from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests

# === CONFIGURATION ===
URL = "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=5.9409699_47.3200746_6.0834844_47.2006872"
BOT_TOKEN = "8015395788:AAFV_ovHTYP0UNaYzPp0wfof7frYmfD4R1I"
CHAT_ID = "5825590629"
CHECK_INTERVAL = 180  # 5 minutes

# === Fonction Telegram ===
def envoyer_message_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

# === Configuration Chrome headless ===
def verifier_logements():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    time.sleep(5)
    contenu = driver.page_source
    driver.quit()

    return "Aucun logement trouvé" not in contenu

# === Bot principal ===
def lancer_bot():
    print("✅ Bot CROUS lancé")
    deja_signale = False

    while True:
        try:
            if verifier_logements():
                if not deja_signale:
                    print("📢 Logement trouvé !")
                    envoyer_message_telegram("🟢 Un logement CROUS est disponible ! 🔗 " + URL)
                    deja_signale = True
            else:
                print("❌ Aucun logement. On continue...")
                deja_signale = False
        except Exception as e:
            print("❗ Erreur :", e)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    lancer_bot()

