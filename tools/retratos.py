import json,sys,time
sys.argv=[sys.argv[0]]
exec(open('tools/commons.py').read().split('import os')[0])
Q=json.load(open(sys.argv[0].replace('retratos.py','retratos_q.json')))
out={}
try: out=json.load(open('tools/retratos.json'))
except: pass
for k,q in Q.items():
    if out.get(k): continue
    d = get({"action": "query", "generator": "search", "gsrsearch": q + " filetype:bitmap", "gsrnamespace": 6, "gsrlimit": 12,
             "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime", "iiurlwidth": 500, "format": "json"})
    c=[]
    for p in sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99)):
        ii = (p.get("imageinfo") or [{}])[0]; m = ii.get("extmetadata", {})
        lic = clean(m.get("LicenseShortName", {}).get("value"))
        if ii.get("mime") not in ("image/jpeg", "image/png") or not OK.match(lic): continue
        c.append({"title": p["title"], "lic": lic, "lic_url": clean(m.get("LicenseUrl", {}).get("value")),"artist": clean(m.get("Artist", {}).get("value"))[:120], "thumb": ii.get("thumburl"),"w": ii.get("thumbwidth"), "h": ii.get("thumbheight"), "page": ii.get("descriptionurl"),"ow":ii.get("width")})
    out[k]=c[:6]
    print(k,'|',' || '.join(x['title'][5:55]+' ['+x['lic']+']' for x in c[:6]),flush=True); time.sleep(1.5)
    json.dump(out,open('tools/retratos.json','w'),ensure_ascii=False,indent=1)
