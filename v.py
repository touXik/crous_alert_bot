import asyncio
from playwright.async_api import async_playwright
import requests
import time
import traceback
import sys

# === CONFIGURATION ===
URL = "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=5.9409699_47.3200746_6.0834844_47.2006872"
BOT_TOKEN = "8015395788:AAFV_ovHTYP0UNaYzPp0wfof7frYmfD4R1I"
CHAT_ID = "5825590629"
CHECK_INTERVAL = 180  # 3 minutes

def envoyer_message_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Erreur Telegram :", e)

async def verifier_logements():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL)
        await page.wait_for_timeout(5000)  # attend 5 secondes
        content = await page.content()
        await browser.close()
        return "Aucun logement trouvé" not in content

async def lancer_bot():
    print("✅ Bot CROUS lancé")
    envoyer_message_telegram("🚀 Le bot CROUS vient de démarrer.")

    deja_signale = False

    while True:
        try:
            logements = await verifier_logements()
            if logements:
                if not deja_signale:
                    print("📢 Logement trouvé !")
                    envoyer_message_telegram("🟢 Un logement CROUS est disponible ! 🔗 " + URL)
                    deja_signale = True
            else:
                print("❌ Aucun logement. On continue...")
                deja_signale = False
        except Exception as e:
            erreur_texte = f"❗ Le bot a rencontré une erreur et s'est arrêté.\n\nDétail :\n{traceback.format_exc()}"
            print(erreur_texte)
            envoyer_message_telegram(erreur_texte)
            sys.exit(1)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(lancer_bot())
