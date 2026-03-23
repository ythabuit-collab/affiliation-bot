“””
VitalMen Deals — Bot Affiliation
Telegram @topdealsjost + Twitter @VitalMenDeals + Facebook VitalMen Deals
Amazon topdealsjost-21 + Fnac + Cdiscount
“””

import requests
import time
import re
import random
from datetime import datetime
from bs4 import BeautifulSoup

# ════════════════════════════════════════════════════════

# ⚙️  CONFIGURATION

# ════════════════════════════════════════════════════════

TELEGRAM_TOKEN   = “8774069021:AAG3BZQoCbGRzYP4B1ksA3pbjQ_TwJ4rqtk”
TELEGRAM_CHANNEL = “@topdealsjost”
TELEGRAM_CHAT_ID = “8559815820”

TWITTER_API_KEY             = “COLLE_ICI”
TWITTER_API_SECRET          = “COLLE_ICI”
TWITTER_ACCESS_TOKEN        = “COLLE_ICI”
TWITTER_ACCESS_TOKEN_SECRET = “COLLE_ICI”

FACEBOOK_PAGE_ID    = “COLLE_TON_PAGE_ID”
FACEBOOK_PAGE_TOKEN = “COLLE_TON_TOKEN_PAGE”

AMAZON_TAG   = “topdealsjost-21”
FNAC_ID      = “COLLE_TON_ID”
CDISCOUNT_ID = “COLLE_TON_ID”

CHECK_INTERVAL   = 1800
MIN_DISCOUNT_PCT = 35
MAX_POSTS        = 5

BRAND_NAME = “VitalMen Deals”
SLOGAN     = “Les meilleures promos pour l’homme moderne 💪”

# ════════════════════════════════════════════════════════

# 🎯  CATÉGORIES BIEN-ÊTRE MASCULIN

# ════════════════════════════════════════════════════════

CATEGORIES = {
“💪 Sport & Performance”: [
“haltères réglables”, “barre de traction murale”,
“kettlebell fonte”, “foam roller massage”,
“pistolet massage percussion”, “corde à sauter lestée”,
“bain de glace portable”, “sac lesté marche”,
“banc musculation pliable”, “élastiques musculation”,
],
“😴 Sommeil & Récupération”: [
“masque sommeil 3d”, “couverture lestée adulte”,
“lampe luminothérapie réveil”, “bouchons oreilles sommeil”,
“oreiller ergonomique cervicales”, “couverture sauna infrarouge”,
“ruban bouche sommeil”, “tapis earthing grounding”,
],
“🧴 Soin & Apparence Homme”: [
“crème hydratante homme”, “sérum vitamine c homme”,
“protection solaire visage homme spf50”,
“tondeuse barbe professionnelle”, “huile barbe homme”,
“minoxidil barbe pousse”, “rétinol crème homme”,
“gua sha visage homme”, “baume après rasage homme”,
],
“🧠 Mental & Biohacking”: [
“ashwagandha stress”, “lion mane champignon”,
“oméga 3 haute concentration”, “magnésium bisglycinate”,
“vitamine d3 k2”, “zinc bisglycinate”,
“shilajit résine”, “collagène marin hydrolysé”,
],
“⌚ Tech & Gadgets Santé”: [
“bague connectée sommeil”, “montre connectée santé homme”,
“lampe lumière rouge thérapie”, “purificateur air chambre”,
“oxymètre pouls”, “balance impédancemètre”,
“tensiomètre connecté poignet”,
],
“👟 Style & Mode Homme”: [
“sneakers homme tendance”, “chelsea boots homme”,
“montre homme minimaliste”, “parfum homme boisé”,
“sac à dos laptop homme”, “portefeuille slim homme”,
“veste bomber homme”, “hoodie oversize homme”,
],
“🥗 Nutrition & Cuisine Saine”: [
“blender smoothie protéiné”, “shaker protéine électrique”,
“air fryer compact”, “lunch box isotherme homme”,
“gourde inox sport 1l”, “balance cuisine digitale”,
],
“🚶 Cardio & Activité”: [
“podomètre bracelet connecté”, “tapis de marche bureau”,
“vélo appartement silencieux”, “stepper fitness compact”,
“jump rope crossfit”, “montre sport gps homme”,
],
}

# ════════════════════════════════════════════════════════

# ✍️  PHRASES VITALMENT DEALS

# ════════════════════════════════════════════════════════

PHRASES = {
“telegram”: [
“💪 VitalMen Deals — parce que l’homme moderne mérite le meilleur prix —”,
“🔥 Bonne affaire détectée ! -{discount}% sur ce produit incontournable —”,
“⚡ Deal du moment — fonce avant que ça parte —”,
“🎯 On a trouvé exactement ce qu’il te faut à prix réduit —”,
“💡 Ton bien-être ne devrait pas coûter une fortune —”,
“🚀 Investis dans toi-même sans te ruiner —”,
“🏆 Qualité maximale, prix minimal — c’est VitalMen Deals —”,
“🧠 Le bon achat au bon moment — économise {savings}€ maintenant —”,
“⏰ Offre limitée — ce deal ne durera pas longtemps —”,
“💎 {savings}€ d’économie sur ce produit — profites-en —”,
],
“twitter”: [
“💪 -{discount}% sur {title} ! Économise {savings}€ 👇 #VitalMenDeals #BonPlan”,
“🔥 DEAL -{discount}% : {title} à {price}€ au lieu de {old}€ 💪 #HommeModerne”,
“⚡ -{discount}% MAINTENANT sur {title} ! {savings}€ économisés 🎯 #BonPlan”,
“🚀 {title} à {price}€ (-{discount}%) — investis dans toi-même 💡 #VitalMen”,
“🏆 Meilleur prix : {title} {price}€ (-{discount}%) 👇 #Deal #HommeOptimal”,
“💎 -{discount}% sur {title} = {savings}€ pour investir ailleurs 💪 #VitalMenDeals”,
],
“facebook”: [
“💪 VITALMENT DEALS — BON PLAN DU JOUR 💪\n\n{title} à seulement {price}€ au lieu de {old}€ !\n\n✅ Réduction : -{discount}%\n💰 Tu économises : {savings}€\n\nParce que l’homme moderne mérite le meilleur sans se ruiner 🔥\n\nLien direct ci-dessous 👇\n❤️ Partage à un ami qui en a besoin !”,
“🔥 ALERTE BON PLAN — VITALMEN DEALS 🔥\n\n{title}\n\nDe {old}€ → seulement {price}€ !\nSoit -{discount}% et {savings}€ dans ta poche.\n\nOn scanne les meilleures offres pour toi 24h/24 💡\n\nFonce avant que ça remonte 👇”,
“🧠 INVESTIS DANS TOI-MÊME INTELLIGEMMENT\n\n{title} à {price}€ (-{discount}%)\n\n{savings}€ économisés = {savings}€ réinvestis dans ta progression.\n\nC’est ça VitalMen Deals 💪\n\nLien direct 👇 Tague un ami qui cherchait ça !”,
“⚡ DEAL EXCLUSIF VITALMEN DEALS ⚡\n\n{title}\n✅ {price}€ au lieu de {old}€\n🏷️ -{discount}% de réduction\n💰 {savings}€ d’économie\n\nL’homme qui s’optimise sait quand saisir une opportunité 🎯\n\n👇 Lien direct ci-dessous !”,
],
}

def get_phrase(platform, deal):
phrases = PHRASES.get(platform, PHRASES[“telegram”])
phrase  = random.choice(phrases)
try:
return phrase.format(
title    = deal[“title”][:50],
price    = deal[“price”],
old      = deal[“old_price”],
discount = deal[“discount_pct”],
savings  = deal[“savings”],
)
except:
return phrase

# ════════════════════════════════════════════════════════

# 🔗  LIENS AFFILIÉS

# ════════════════════════════════════════════════════════

def build_amazon_link(asin):
return f”https://www.amazon.fr/dp/{asin}?tag={AMAZON_TAG}”

def build_fnac_link(url):
if FNAC_ID == “COLLE_TON_ID”: return url
return f”{url.split(’?’)[0]}?affid={FNAC_ID}”

def build_cdiscount_link(url):
if CDISCOUNT_ID == “COLLE_TON_ID”: return url
return f”{url.split(’?’)[0]}?aff={CDISCOUNT_ID}”

# ════════════════════════════════════════════════════════

# 🛒  SCRAPING

# ════════════════════════════════════════════════════════

HEADERS_LIST = [
{“User-Agent”: “Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36”, “Accept-Language”: “fr-FR,fr;q=0.9”},
{“User-Agent”: “Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36”, “Accept-Language”: “fr-FR,fr;q=0.9”},
]

def get_h(): return random.choice(HEADERS_LIST)

def scrape_amazon(keyword):
deals = []
try:
params = {“k”: keyword, “s”: “review-rank”, “rh”: “p_n_deal_type:23566064031”}
r = requests.get(“https://www.amazon.fr/s”, params=params, headers=get_h(), timeout=12)
if r.status_code != 200: return deals

```
    soup  = BeautifulSoup(r.text, "html.parser")
    items = soup.select("[data-component-type='s-search-result']")

    for item in items[:10]:
        try:
            title_el = item.select_one("h2 a span")
            asin     = item.get("data-asin", "")
            price_el = item.select_one(".a-price .a-offscreen")
            old_el   = item.select_one(".a-price.a-text-price .a-offscreen")
            img_el   = item.select_one(".s-image")
            if not all([title_el, asin, price_el, old_el]): continue

            price     = float(price_el.get_text().replace("€","").replace(" ","").replace(",",".").split()[0])
            old_price = float(old_el.get_text().replace("€","").replace(" ","").replace(",",".").split()[0])
            if old_price <= price: continue
            disc = int((old_price - price) / old_price * 100)
            if disc < MIN_DISCOUNT_PCT: continue

            rating_el  = item.select_one(".a-icon-star-small .a-icon-alt")
            reviews_el = item.select_one(".a-size-base.s-underline-text")

            deals.append({
                "source":       "Amazon",
                "emoji":        "🟠",
                "title":        title_el.get_text(strip=True)[:80],
                "price":        price,
                "old_price":    old_price,
                "discount_pct": disc,
                "savings":      round(old_price - price, 2),
                "link":         build_amazon_link(asin),
                "img_url":      img_el.get("src","") if img_el else "",
                "rating":       rating_el.get_text(strip=True)[:3] if rating_el else "?",
                "reviews":      reviews_el.get_text(strip=True) if reviews_el else "?",
            })
        except: continue

    time.sleep(random.uniform(2, 3.5))
except Exception as e:
    print(f"  [Amazon] '{keyword}': {e}")
return deals
```

def scrape_fnac(keyword):
deals = []
try:
r = requests.get(
“https://www.fnac.com/SearchResult/ResultSet.aspx”,
params={“SearchText”: keyword}, headers=get_h(), timeout=12
)
if r.status_code != 200: return deals
soup  = BeautifulSoup(r.text, “html.parser”)
items = soup.select(”.Article-itemWrapper”)[:5]
for item in items:
try:
title_el = item.select_one(”.Article-desc”)
price_el = item.select_one(”.userPrice”)
old_el   = item.select_one(”.oldPrice”)
link_el  = item.select_one(“a.Article-content”)
if not all([title_el, price_el, old_el, link_el]): continue
price     = float(re.search(r’[\d.]+’, price_el.get_text().replace(”,”,”.”).replace(”\xa0”,””)).group())
old_price = float(re.search(r’[\d.]+’, old_el.get_text().replace(”,”,”.”).replace(”\xa0”,””)).group())
if old_price <= price: continue
disc = int((old_price - price) / old_price * 100)
if disc < MIN_DISCOUNT_PCT: continue
href = link_el.get(“href”,””)
if not href.startswith(“http”): href = “https://www.fnac.com” + href
deals.append({
“source”: “Fnac”, “emoji”: “🟡”,
“title”: title_el.get_text(strip=True)[:80],
“price”: price, “old_price”: old_price,
“discount_pct”: disc, “savings”: round(old_price - price, 2),
“link”: build_fnac_link(href), “img_url”: “”,
“rating”: “?”, “reviews”: “?”,
})
except: continue
time.sleep(random.uniform(1.5, 2.5))
except Exception as e:
print(f”  [Fnac] ‘{keyword}’: {e}”)
return deals

def scrape_cdiscount(keyword):
deals = []
try:
r = requests.get(
“https://www.cdiscount.com/search/10/”,
params={“q”: keyword}, headers=get_h(), timeout=12
)
if r.status_code != 200: return deals
soup  = BeautifulSoup(r.text, “html.parser”)
items = soup.select(”.prdtBId”)[:5]
for item in items:
try:
title_el = item.select_one(”.prdtHead h3”)
price_el = item.select_one(”.price span”)
old_el   = item.select_one(”.oldprice”)
link_el  = item.select_one(“a.prdtBlkLnk”)
if not all([title_el, price_el, old_el, link_el]): continue
price     = float(re.search(r’[\d.]+’, price_el.get_text().replace(”,”,”.”).replace(”\xa0”,””)).group())
old_price = float(re.search(r’[\d.]+’, old_el.get_text().replace(”,”,”.”).replace(”\xa0”,””)).group())
if old_price <= price: continue
disc = int((old_price - price) / old_price * 100)
if disc < MIN_DISCOUNT_PCT: continue
href = link_el.get(“href”,””)
if not href.startswith(“http”): href = “https://www.cdiscount.com” + href
deals.append({
“source”: “Cdiscount”, “emoji”: “🔴”,
“title”: title_el.get_text(strip=True)[:80],
“price”: price, “old_price”: old_price,
“discount_pct”: disc, “savings”: round(old_price - price, 2),
“link”: build_cdiscount_link(href), “img_url”: “”,
“rating”: “?”, “reviews”: “?”,
})
except: continue
time.sleep(random.uniform(1.5, 2.5))
except Exception as e:
print(f”  [Cdiscount] ‘{keyword}’: {e}”)
return deals

# ════════════════════════════════════════════════════════

# 📊  SCORE

# ════════════════════════════════════════════════════════

def score_deal(deal):
score = 0
d = deal[“discount_pct”]
if d >= 70: score += 50
elif d >= 60: score += 40
elif d >= 50: score += 30
elif d >= 40: score += 20
else: score += 10
s = deal[“savings”]
if s >= 100: score += 30
elif s >= 50: score += 20
elif s >= 25: score += 10
try:
r = float(deal.get(“rating”,“0”).replace(”,”,”.”))
if r >= 4.5: score += 15
elif r >= 4.0: score += 8
except: pass
return score

# ════════════════════════════════════════════════════════

# 📲  PUBLICATIONS

# ════════════════════════════════════════════════════════

def post_telegram(deal, category):
phrase = get_phrase(“telegram”, deal)
rating_line = “”
if deal.get(“rating”,”?”) != “?”:
rating_line = f”⭐ {deal[‘rating’]}”
if deal.get(“reviews”,”?”) != “?”: rating_line += f” ({deal[‘reviews’]} avis)”
rating_line += “\n”

```
msg = (
    f"{phrase}\n\n"
    f"{deal['emoji']} <b>{deal['source']}</b> — {category}\n\n"
    f"🛍️ <b>{deal['title']}</b>\n\n"
    f"💰 <b>{deal['price']}€</b>  <s>{deal['old_price']}€</s>\n"
    f"🏷️ <b>-{deal['discount_pct']}%</b> → économise <b>{deal['savings']}€</b>\n"
    f"{rating_line}\n"
    f"👉 <a href=\"{deal['link']}\">VOIR LE PRODUIT →</a>\n\n"
    f"📢 {BRAND_NAME} | {TELEGRAM_CHANNEL}\n"
    f"⏰ {datetime.now().strftime('%H:%M — %d/%m/%Y')}"
)

base = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
if deal.get("img_url"):
    payload  = {"chat_id": TELEGRAM_CHANNEL, "photo": deal["img_url"], "caption": msg[:1024], "parse_mode": "HTML"}
    endpoint = f"{base}/sendPhoto"
else:
    payload  = {"chat_id": TELEGRAM_CHANNEL, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": False}
    endpoint = f"{base}/sendMessage"
try:
    r = requests.post(endpoint, json=payload, timeout=10)
    return r.status_code == 200
except Exception as e:
    print(f"  [Telegram] {e}"); return False
```

def post_twitter(deal):
if “COLLE” in TWITTER_API_KEY: return False
try:
import tweepy
client = tweepy.Client(
consumer_key=TWITTER_API_KEY, consumer_secret=TWITTER_API_SECRET,
access_token=TWITTER_ACCESS_TOKEN, access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
)
phrase = get_phrase(“twitter”, deal)
tweet  = f”{phrase}\n\n{deal[‘link’]}”
if len(tweet) > 280: tweet = f”{phrase[:200]}…\n\n{deal[‘link’]}”
client.create_tweet(text=tweet)
return True
except Exception as e:
print(f”  [Twitter] {e}”); return False

def post_facebook(deal):
if “COLLE” in FACEBOOK_PAGE_TOKEN: return False
try:
phrase = get_phrase(“facebook”, deal)
msg    = f”{phrase}\n\n🔗 {deal[‘link’]}”
r = requests.post(
f”https://graph.facebook.com/v19.0/{FACEBOOK_PAGE_ID}/feed”,
data={“message”: msg, “access_token”: FACEBOOK_PAGE_TOKEN},
timeout=10
)
return r.status_code == 200
except Exception as e:
print(f”  [Facebook] {e}”); return False

def publish_everywhere(deal, category):
ok = []
if post_telegram(deal, category): ok.append(“Telegram ✅”)
time.sleep(2)
if post_twitter(deal): ok.append(“Twitter ✅”)
time.sleep(2)
if post_facebook(deal): ok.append(“Facebook ✅”)
print(f”    📢 {’, ’.join(ok) if ok else ‘Telegram uniquement (Twitter/FB à configurer)’}”)

# ════════════════════════════════════════════════════════

# 🔄  BOUCLE PRINCIPALE

# ════════════════════════════════════════════════════════

already_published = set()

def scan_and_publish():
all_deals = []
print(f”[{datetime.now().strftime(’%H:%M’)}] Scan VitalMen Deals…”)

```
for cat_name, keywords in CATEGORIES.items():
    sample = random.sample(keywords, min(2, len(keywords)))
    for kw in sample:
        print(f"  → {cat_name} : '{kw}'")
        for d in scrape_amazon(kw) + scrape_fnac(kw) + scrape_cdiscount(kw):
            d["category"] = cat_name
            d["score"]    = score_deal(d)
            all_deals.append(d)
        time.sleep(1)

all_deals.sort(key=lambda x: x["score"], reverse=True)

published = 0
for deal in all_deals:
    if published >= MAX_POSTS: break
    key = f"{deal['title'][:20]}{deal['price']}".replace(" ","")
    if key in already_published: continue
    already_published.add(key)
    print(f"\n  🔥 {deal['source']} | {deal['title'][:45]} | -{deal['discount_pct']}% | +{deal['savings']}€ éco")
    publish_everywhere(deal, deal["category"])
    published += 1
    time.sleep(5)

return published
```

# ════════════════════════════════════════════════════════

# 🚀  MAIN

# ════════════════════════════════════════════════════════

def main():
print(”=” * 65)
print(f”   {BRAND_NAME} — Bot Affiliation”)
print(f”   {SLOGAN}”)
print(f”   Tag Amazon  : {AMAZON_TAG}”)
print(f”   Canal       : {TELEGRAM_CHANNEL}”)
print(f”   Twitter     : @VitalMenDeals”)
print(f”   Catégories  : {len(CATEGORIES)}”)
print(f”   Réduction   : -{MIN_DISCOUNT_PCT}% minimum”)
print(f”   Intervalle  : {CHECK_INTERVAL // 60} minutes”)
print(”=” * 65)

```
requests.post(
    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
    json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": (
            f"💪 <b>{BRAND_NAME} — Bot démarré !</b>\n\n"
            f"📢 Canal Telegram : {TELEGRAM_CHANNEL}\n"
            f"🐦 Twitter : @VitalMenDeals\n"
            f"📘 Facebook : VitalMen Deals\n"
            f"🔗 Tag Amazon : <code>{AMAZON_TAG}</code>\n\n"
            f"📦 {len(CATEGORIES)} catégories bien-être masculin\n"
            f"📉 Réduction min : -{MIN_DISCOUNT_PCT}%\n\n"
            f"🟢 Premier scan en cours..."
        ),
        "parse_mode": "HTML",
    },
    timeout=10
)

cycle = 0
while True:
    cycle += 1
    print(f"\n══ SCAN #{cycle} ══ {datetime.now().strftime('%H:%M:%S')} ══")
    published = scan_and_publish()
    print(f"══ FIN #{cycle} ══ {published} deal(s) | Prochain dans {CHECK_INTERVAL // 60}min")
    time.sleep(CHECK_INTERVAL)
```

if **name** == “**main**”:
main()
