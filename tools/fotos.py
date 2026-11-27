import json,sys,time
sys.argv=[sys.argv[0]]
exec(open('tools/commons.py').read().split('import os')[0])
Q=json.load(open('tools/fotos_q.json'))
out={}
try: out=json.load(open('tools/fotos_cand.json'))
except: pass
for k,q in Q.items():
    if out.get(k): continue
    d = get({"action": "query", "generator": "search", "gsrsearch": q + " filetype:bitmap", "gsrnamespace": 6, "gsrlimit": 15,
             "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime", "iiurlwidth": 400, "format": "json"})
    c=[]
    for p in sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99)):
        ii = (p.get("imageinfo") or [{}])[0]; m = ii.get("extmetadata", {})
        lic = clean(m.get("LicenseShortName", {}).get("value"))
        if ii.get("mime") not in ("image/jpeg", "image/png") or not OK.match(lic) or (ii.get("width") or 0)<500: continue
        c.append({"title": p["title"], "lic": lic, "lic_url": clean(m.get("LicenseUrl", {}).get("value")),"artist": clean(m.get("Artist", {}).get("value"))[:120], "thumb": ii.get("thumburl"),"w": ii.get("width"), "h": ii.get("height"), "page": ii.get("descriptionurl")})
    out[k]=c[:12]
    print(k,len(c),flush=True); time.sleep(1)
    json.dump(out,open('tools/fotos_cand.json','w'),ensure_ascii=False,indent=1)
