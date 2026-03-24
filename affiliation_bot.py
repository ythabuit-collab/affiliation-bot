import requests
import time
import re
import random
from datetime import datetime
from bs4 import BeautifulSoup

TELEGRAM_TOKEN   = "8774069021:AAG3BZQoCbGRzYP4B1ksA3pbjQ_TwJ4rqtk"
TELEGRAM_CHANNEL = "@VitalMenDeals"
TELEGRAM_CHAT_ID = "8559815820"

TWITTER_API_KEY             = "5gO84CpnHMgjolqynRLM9r9e3"
TWITTER_API_SECRET          = "w8Y3ZosgJxlI4qkqW0VYlfkaUazd5rapqss7fRb8abVowIviyx"
TWITTER_ACCESS_TOKEN        = "cnZJQjNVcURWU1AwZHRPVV9fY1k6MTpjaQ"
TWITTER_ACCESS_TOKEN_SECRET = "jJCkBI1svbIKEr8e254Q4d3wrLB0NwB7JNeTabtq7SmDVNISgW"

FACEBOOK_PAGE_ID    = “COLLE_TON_PAGE_ID”
FACEBOOK_PAGE_TOKEN = “COLLE_TON_TOKEN_PAGE”

AMAZON_TAG   = "topdealsjost-21”
FNAC_ID      = “COLLE_TON_ID”
CDISCOUNT_ID = “COLLE_TON_ID”

CHECK_INTERVAL   = 1800
MIN_DISCOUNT_PCT = 35
MAX_POSTS        = 5
BRAND_NAME       = "VitalMen Deals"
TELEGRAM_CHANNEL_NAME = "@VitalMenDeals"

CATEGORIES = {
“Sport & Performance”: [
“halteres reglables”, “barre de traction”,
“kettlebell”, “foam roller”,
“pistolet massage”, “corde sauter”,
“bain de glace”, “banc musculation”,
],
“Sommeil & Recuperation”: [
“masque sommeil”, “couverture lestee”,
“lampe luminotherapie”, “oreiller ergonomique”,
“couverture sauna”, “tapis earthing”,
],
“Soin Homme”: [
“creme hydratante homme”, “serum vitamine c homme”,
“protection solaire homme”, “tondeuse barbe”,
“huile barbe”, “minoxidil barbe”,
“retinol creme homme”, “baume apres rasage”,
],
“Mental & Biohacking”: [
“ashwagandha”, “lion mane champignon”,
“omega 3”, “magnesium bisglycinate”,
“vitamine d3 k2”, “zinc bisglycinate”,
“shilajit”, “collagene marin”,
],
“Tech Sante”: [
“bague connectee sommeil”, “montre connectee sante”,
“lampe lumiere rouge”, “purificateur air”,
“oxymetre pouls”, “balance impedancemetre”,
],
“Style Mode Homme”: [
“sneakers homme”, “chelsea boots homme”,
“montre homme”, “parfum homme”,
“sac dos laptop homme”, “portefeuille slim”,
],
“Nutrition Cuisine”: [
“blender smoothie”, “shaker electrique”,
“air fryer”, “lunch box isotherme”,
“gourde inox sport”, “balance cuisine”,
],
“Cardio Activite”: [
“podometre bracelet”, “tapis marche bureau”,
“velo appartement”, “stepper fitness”,
“jump rope”, “montre sport gps”,
],
}

PHRASES_TG = [
“VitalMen Deals - parce que l homme moderne merite le meilleur prix”,
“Bonne affaire detectee ! -{discount}% sur ce produit incontournable”,
“Deal du moment - fonce avant que ca parte”,
“On a trouve exactement ce qu il te faut a prix reduit”,
“Ton bien-etre ne devrait pas couter une fortune”,
“Investis dans toi-meme sans te ruiner”,
“Qualite maximale, prix minimal - c est VitalMen Deals”,
“Le bon achat au bon moment - economise {savings} euros maintenant”,
“Offre limitee - ce deal ne durera pas longtemps”,
“{savings} euros d economie sur ce produit - profites-en”,
]

PHRASES_TW = [
“-{discount}% sur {title} ! Economise {savings}EUR #VitalMenDeals #BonPlan”,
“DEAL -{discount}% : {title} a {price}EUR au lieu de {old}EUR #HommeModerne”,
“-{discount}% MAINTENANT sur {title} ! {savings}EUR economies #BonPlan”,
“{title} a {price}EUR (-{discount}%) - investis dans toi-meme #VitalMen”,
“Meilleur prix : {title} {price}EUR (-{discount}%) #Deal #HommeOptimal”,
]

def get_phrase_tg(deal):
phrase = random.choice(PHRASES_TG)
try:
return phrase.format(
title=deal[“title”][:50],
price=deal[“price”],
old=deal[“old_price”],
discount=deal[“discount_pct”],
savings=deal[“savings”],
)
except:
return phrase

def get_phrase_tw(deal):
phrase = random.choice(PHRASES_TW)
try:
return phrase.format(
title=deal[“title”][:40],
price=deal[“price”],
old=deal[“old_price”],
discount=deal[“discount_pct”],
savings=deal[“savings”],
)
except:
return phrase

def build_amazon_link(asin):
return “https://www.amazon.fr/dp/” + asin + “?tag=” + AMAZON_TAG

HEADERS_LIST = [
{“User-Agent”: “Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36”, “Accept-Language”: “fr-FR,fr;q=0.9”},
{“User-Agent”: “Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36”, “Accept-Language”: “fr-FR,fr;q=0.9”},
]

def get_h():
return random.choice(HEADERS_LIST)

def scrape_amazon(keyword):
deals = []
try:
params = {“k”: keyword, “s”: “review-rank”, “rh”: “p_n_deal_type:23566064031”}
r = requests.get(“https://www.amazon.fr/s”, params=params, headers=get_h(), timeout=12)
if r.status_code != 200:
return deals
soup = BeautifulSoup(r.text, “html.parser”)
items = soup.select(”[data-component-type=‘s-search-result’]”)
for item in items[:10]:
try:
title_el = item.select_one(“h2 a span”)
asin = item.get(“data-asin”, “”)
price_el = item.select_one(”.a-price .a-offscreen”)
old_el = item.select_one(”.a-price.a-text-price .a-offscreen”)
img_el = item.select_one(”.s-image”)
if not all([title_el, asin, price_el, old_el]):
continue
price = float(price_el.get_text().replace(“EUR”,””).replace(“euro”,””).replace(“e”,””).replace(” “,””).replace(”,”,”.”).split()[0])
old_price = float(old_el.get_text().replace(“EUR”,””).replace(“euro”,””).replace(“e”,””).replace(” “,””).replace(”,”,”.”).split()[0])
if old_price <= price:
continue
disc = int((old_price - price) / old_price * 100)
if disc < MIN_DISCOUNT_PCT:
continue
rating_el = item.select_one(”.a-icon-star-small .a-icon-alt”)
reviews_el = item.select_one(”.a-size-base.s-underline-text”)
deals.append({
“source”: “Amazon”,
“emoji”: “A”,
“title”: title_el.get_text(strip=True)[:80],
“price”: price,
“old_price”: old_price,
“discount_pct”: disc,
“savings”: round(old_price - price, 2),
“link”: build_amazon_link(asin),
“img_url”: img_el.get(“src”, “”) if img_el else “”,
“rating”: rating_el.get_text(strip=True)[:3] if rating_el else “?”,
“reviews”: reviews_el.get_text(strip=True) if reviews_el else “?”,
})
except:
continue
time.sleep(random.uniform(2, 3.5))
except Exception as e:
print(“Amazon error: “ + str(e))
return deals

def score_deal(deal):
score = 0
d = deal[“discount_pct”]
if d >= 70:
score += 50
elif d >= 60:
score += 40
elif d >= 50:
score += 30
elif d >= 40:
score += 20
else:
score += 10
s = deal[“savings”]
if s >= 100:
score += 30
elif s >= 50:
score += 20
elif s >= 25:
score += 10
try:
r = float(deal.get(“rating”, “0”).replace(”,”, “.”))
if r >= 4.5:
score += 15
elif r >= 4.0:
score += 8
except:
pass
return score

def post_telegram(deal, category):
phrase = get_phrase_tg(deal)
rating_line = “”
if deal.get(“rating”, “?”) != “?”:
rating_line = “Note: “ + deal[“rating”]
if deal.get(“reviews”, “?”) != “?”:
rating_line += “ (” + deal[“reviews”] + “ avis)”
rating_line += “\n”

```
msg = (
    phrase + "\n\n"
    + deal["source"] + " - " + category + "\n\n"
    + deal["title"] + "\n\n"
    + "Prix: " + str(deal["price"]) + "EUR"
    + "  (au lieu de " + str(deal["old_price"]) + "EUR)\n"
    + "-" + str(deal["discount_pct"]) + "% -> economise " + str(deal["savings"]) + "EUR\n"
    + rating_line + "\n"
    + "VOIR LE PRODUIT: " + deal["link"] + "\n\n"
    + BRAND_NAME + " | " + TELEGRAM_CHANNEL_NAME + "\n"
    + datetime.now().strftime("%H:%M - %d/%m/%Y")
)

base = "https://api.telegram.org/bot" + TELEGRAM_TOKEN
if deal.get("img_url"):
    payload = {
        "chat_id": TELEGRAM_CHANNEL,
        "photo": deal["img_url"],
        "caption": msg[:1024],
    }
    endpoint = base + "/sendPhoto"
else:
    payload = {
        "chat_id": TELEGRAM_CHANNEL,
        "text": msg,
        "disable_web_page_preview": False,
    }
    endpoint = base + "/sendMessage"
try:
    r = requests.post(endpoint, json=payload, timeout=10)
    return r.status_code == 200
except Exception as e:
    print("Telegram error: " + str(e))
    return False
```

def post_twitter(deal):
if “COLLE” in TWITTER_API_KEY:
return False
try:
import tweepy
client = tweepy.Client(
consumer_key=TWITTER_API_KEY,
consumer_secret=TWITTER_API_SECRET,
access_token=TWITTER_ACCESS_TOKEN,
access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
)
phrase = get_phrase_tw(deal)
tweet = phrase + “\n\n” + deal[“link”]
if len(tweet) > 280:
tweet = phrase[:200] + “\n\n” + deal[“link”]
client.create_tweet(text=tweet)
return True
except Exception as e:
print(“Twitter error: “ + str(e))
return False

def publish_everywhere(deal, category):
ok = []
if post_telegram(deal, category):
ok.append(“Telegram”)
time.sleep(2)
if post_twitter(deal):
ok.append(“Twitter”)
print(“Published: “ + (”, “.join(ok) if ok else “none”))

already_published = set()

def scan_and_publish():
all_deals = []
print(datetime.now().strftime(”%H:%M”) + “ Scan VitalMen Deals…”)
for cat_name, keywords in CATEGORIES.items():
sample = random.sample(keywords, min(2, len(keywords)))
for kw in sample:
print(”  -> “ + cat_name + “ : “ + kw)
for d in scrape_amazon(kw):
d[“category”] = cat_name
d[“score”] = score_deal(d)
all_deals.append(d)
time.sleep(1)
all_deals.sort(key=lambda x: x[“score”], reverse=True)
published = 0
for deal in all_deals:
if published >= MAX_POSTS:
break
key = (deal[“title”][:20] + str(deal[“price”])).replace(” “, “”)
if key in already_published:
continue
already_published.add(key)
print(“DEAL: “ + deal[“source”] + “ | “ + deal[“title”][:40] + “ | -” + str(deal[“discount_pct”]) + “%”)
publish_everywhere(deal, deal[“category”])
published += 1
time.sleep(5)
return published

def main():
print(“VitalMen Deals Bot starting…”)
print(“Amazon tag: “ + AMAZON_TAG)
print(“Canal: “ + TELEGRAM_CHANNEL)

```
requests.post(
    "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage",
    json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": (
            "VitalMen Deals Bot demarre!\n\n"
            "Canal: " + TELEGRAM_CHANNEL + "\n"
            "Twitter: @VitalMenDeals\n"
            "Amazon tag: " + AMAZON_TAG + "\n\n"
            "Categories: " + str(len(CATEGORIES)) + "\n"
            "Reduction min: -" + str(MIN_DISCOUNT_PCT) + "%\n\n"
            "Premier scan en cours..."
        ),
    },
    timeout=10
)

cycle = 0
while True:
    cycle += 1
    print("SCAN #" + str(cycle) + " " + datetime.now().strftime("%H:%M:%S"))
    published = scan_and_publish()
    print("FIN #" + str(cycle) + " " + str(published) + " deals publies")
    time.sleep(CHECK_INTERVAL)
```

if **name** == “**main**”:
main()
