"""Busca candidatas en Wikimedia Commons para cada ficha (tipos100) y guarda tools/candidatas.json."""
import json, re, sys, time, urllib.parse, urllib.request, html
sys.path.insert(0, "tools")
from tipos100 import TIPOS
UA = {"User-Agent": "OncolopediaBuild/1.0 (static encyclopedia build script)"}
API = "https://commons.wikimedia.org/w/api.php?"

def get(params):
    for i in range(5):
        try:
            r = urllib.request.urlopen(urllib.request.Request(API + urllib.parse.urlencode(params), headers=UA), timeout=30)
            return json.load(r)
        except Exception as e:
            time.sleep(3 * (i + 1))
    return {}

def clean(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()

OK = re.compile(r"^(cc0|cc[- ]by(-sa)?[- ]?[0-9.]*|public domain|pd.*)", re.I)
import os
out = json.load(open("tools/candidatas.json")) if os.path.exists("tools/candidatas.json") else {}
for slug, tit, q in TIPOS:
    if slug in out and out[slug]:
        continue
    d = get({"action": "query", "generator": "search", "gsrsearch": q + " filetype:bitmap", "gsrnamespace": 6, "gsrlimit": 10,
             "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime", "iiurlwidth": 900, "format": "json"})
    cands = []
    for p in sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99)):
        ii = (p.get("imageinfo") or [{}])[0]
        m = ii.get("extmetadata", {})
        lic = clean(m.get("LicenseShortName", {}).get("value"))
        if ii.get("mime") not in ("image/jpeg", "image/png") or not OK.match(lic):
            continue
        cands.append({"title": p["title"], "lic": lic, "lic_url": clean(m.get("LicenseUrl", {}).get("value")),
                      "artist": clean(m.get("Artist", {}).get("value"))[:120], "thumb": ii.get("thumburl"),
                      "w": ii.get("thumbwidth"), "h": ii.get("thumbheight"), "page": ii.get("descriptionurl")})
    out[slug] = cands[:6]
    print(slug, len(cands), "|", cands[0]["title"][5:80] if cands else "-", flush=True)
    time.sleep(2)
    json.dump(out, open("tools/candidatas.json", "w"), ensure_ascii=False, indent=1)
json.dump(out, open("tools/candidatas.json", "w"), ensure_ascii=False, indent=1)
