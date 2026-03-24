import requests
import time
import re
import random
from datetime import datetime
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = "8774069021:AAG3BZQoCbGRzYP4B1ksA3pbjQ_TwJ4rqtk"
TELEGRAM_CHANNEL = "@VitalMenDeals"
TELEGRAM_CHAT_ID = "8559815820"
AMAZON_TAG = "topdealsjost-21"
CHECK_INTERVAL = 1800
MIN_DISCOUNT = 25
MAX_POSTS = 5

KEYWORDS = [
    "halteres reglables", "kettlebell fonte", "foam roller",
    "pistolet massage", "masque sommeil", "couverture lestee",
    "tondeuse barbe professionnelle", "huile barbe homme",
    "creme hydratante homme", "ashwagandha", "omega 3",
    "magnesium bisglycinate", "vitamine d3 k2", "collagene marin",
    "bague connectee sommeil", "montre connectee sante homme",
    "sneakers homme", "parfum homme", "air fryer compact",
    "blender smoothie", "gourde inox sport", "jump rope crossfit",
    "podometre bracelet", "velo appartement silencieux",
    "banc musculation pliable", "barre de traction murale",
]

PHRASES = [
    "VitalMen Deals - le meilleur prix pour l homme moderne",
    "Bonne affaire - {discount}% de reduction sur ce produit",
    "Deal du moment - economise {savings} euros",
    "Investis dans toi-meme sans te ruiner",
    "Qualite maximale prix minimal - VitalMen Deals",
    "Offre limitee - {discount}% de reduction maintenant",
    "Le bon achat au bon moment - {savings} euros d economie",
]

def get_phrase(deal):
    phrase = random.choice(PHRASES)
    try:
        return phrase.format(
            discount=deal["discount_pct"],
            savings=deal["savings"],
        )
    except:
        return phrase

def build_link(asin):
    return "https://www.amazon.fr/dp/" + asin + "?tag=" + AMAZON_TAG

HEADERS = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36", "Accept-Language": "fr-FR,fr;q=0.9"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36", "Accept-Language": "fr-FR,fr;q=0.9"},
]

def scrape_amazon(keyword):
    deals = []
    try:
        params = {"k": keyword, "s": "review-rank", "rh": "p_n_deal_type:23566064031"}
        r = requests.get("https://www.amazon.fr/s", params=params, headers=random.choice(HEADERS), timeout=12)
        if r.status_code != 200:
            return deals
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("[data-component-type='s-search-result']")
        for item in items[:10]:
            try:
                title_el = item.select_one("h2 a span")
                asin = item.get("data-asin", "")
                price_el = item.select_one(".a-price .a-offscreen")
                old_el = item.select_one(".a-price.a-text-price .a-offscreen")
                img_el = item.select_one(".s-image")
                if not all([title_el, asin, price_el, old_el]):
                    continue
                p_text = price_el.get_text().replace(" ", "").replace(",", ".")
                o_text = old_el.get_text().replace(" ", "").replace(",", ".")
                p_match = re.search(r"[\d.]+", p_text)
                o_match = re.search(r"[\d.]+", o_text)
                if not p_match or not o_match:
                    continue
                price = float(p_match.group())
                old_price = float(o_match.group())
                if old_price <= price:
                    continue
                disc = int((old_price - price) / old_price * 100)
                if disc < MIN_DISCOUNT:
                    continue
                deals.append({
                    "title": title_el.get_text(strip=True)[:80],
                    "price": price,
                    "old_price": old_price,
                    "discount_pct": disc,
                    "savings": round(old_price - price, 2),
                    "link": build_link(asin),
                    "img_url": img_el.get("src", "") if img_el else "",
                })
            except:
                continue
        time.sleep(random.uniform(2, 3.5))
    except Exception as e:
        print("Amazon error: " + str(e))
    return deals

def post_telegram(deal):
    phrase = get_phrase(deal)
    msg = (
        phrase + "\n\n"
        + "Amazon\n\n"
        + deal["title"] + "\n\n"
        + "Prix: " + str(deal["price"]) + " EUR"
        + " (au lieu de " + str(deal["old_price"]) + " EUR)\n"
        + "-" + str(deal["discount_pct"]) + "% -> economise " + str(deal["savings"]) + " EUR\n\n"
        + "VOIR LE PRODUIT: " + deal["link"] + "\n\n"
        + "VitalMen Deals | " + TELEGRAM_CHANNEL + "\n"
        + datetime.now().strftime("%H:%M - %d/%m/%Y")
    )
    base = "https://api.telegram.org/bot" + TELEGRAM_TOKEN
    if deal.get("img_url"):
        payload = {"chat_id": TELEGRAM_CHANNEL, "photo": deal["img_url"], "caption": msg[:1024]}
        endpoint = base + "/sendPhoto"
    else:
        payload = {"chat_id": TELEGRAM_CHANNEL, "text": msg, "disable_web_page_preview": False}
        endpoint = base + "/sendMessage"
    try:
        r = requests.post(endpoint, json=payload, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print("Telegram error: " + str(e))
        return False

already_published = set()

def scan_and_publish():
    all_deals = []
    print(datetime.now().strftime("%H:%M") + " Scan en cours...")
    sample = random.sample(KEYWORDS, min(8, len(KEYWORDS)))
    for kw in sample:
        print("  -> " + kw)
        for d in scrape_amazon(kw):
            d["score"] = d["discount_pct"] + min(d["savings"], 100)
            all_deals.append(d)
        time.sleep(1)
    all_deals.sort(key=lambda x: x["score"], reverse=True)
    published = 0
    for deal in all_deals:
        if published >= MAX_POSTS:
            break
        key = (deal["title"][:20] + str(deal["price"])).replace(" ", "")
        if key in already_published:
            continue
        already_published.add(key)
        print("DEAL: " + deal["title"][:40] + " | -" + str(deal["discount_pct"]) + "%")
        if post_telegram(deal):
            print("  Telegram OK")
        published += 1
        time.sleep(5)
    return published

def main():
    print("VitalMen Deals Bot starting...")
    requests.post(
        "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage",
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": "VitalMen Deals Bot demarre! Canal: " + TELEGRAM_CHANNEL + " | Amazon: " + AMAZON_TAG + " | Premier scan en cours...",
        },
        timeout=10
    )
    cycle = 0
    while True:
        cycle += 1
        print("SCAN #" + str(cycle))
        published = scan_and_publish()
        print("FIN #" + str(cycle) + " - " + str(published) + " deals")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
