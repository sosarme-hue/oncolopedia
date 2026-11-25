import json,sys,time
sys.argv=[sys.argv[0]]
exec(open('tools/commons.py').read().split('import os')[0])
Q={"cancer-de-mama-triple-negativo":"triple negative breast carcinoma histopathology","cancer-de-vulva":"vulvar squamous cell carcinoma","cancer-de-vagina":"vaginal carcinoma histology","cancer-de-recto":"rectal adenocarcinoma","timoma-y-carcinoma-timico":"thymoma histopathology","tumores-neuroendocrinos-de-pancreas":"pancreatic neuroendocrine tumor histology","cancer-de-higado":"hepatocellular carcinoma histopathology","cancer-de-vejiga-y-rinon":"urothelial carcinoma bladder histopathology","leucemias":"leukemia blood smear","leucemia-linfocitica-cronica":"chronic lymphocytic leukemia smear","leucemia-mieloide-cronica":"chronic myeloid leukemia blood smear","linfoma-difuso-de-celulas-b-grandes":"diffuse large B-cell lymphoma histopathology","macroglobulinemia-de-waldenstrom":"lymphoplasmacytic lymphoma","condrosarcoma":"chondrosarcoma histopathology","gliomas-de-bajo-grado":"pilocytic astrocytoma","cancer-de-orofaringe":"oropharyngeal carcinoma p16"}
out=json.load(open('tools/candidatas.json'))
for slug,q in Q.items():
    d = get({"action": "query", "generator": "search", "gsrsearch": q + " filetype:bitmap", "gsrnamespace": 6, "gsrlimit": 12,
             "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime", "iiurlwidth": 900, "format": "json"})
    c=[]
    for p in sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99)):
        ii = (p.get("imageinfo") or [{}])[0]; m = ii.get("extmetadata", {})
        lic = clean(m.get("LicenseShortName", {}).get("value"))
        if ii.get("mime") not in ("image/jpeg", "image/png") or not OK.match(lic): continue
        c.append({"title": p["title"], "lic": lic, "lic_url": clean(m.get("LicenseUrl", {}).get("value")),"artist": clean(m.get("Artist", {}).get("value"))[:120], "thumb": ii.get("thumburl"),"w": ii.get("thumbwidth"), "h": ii.get("thumbheight"), "page": ii.get("descriptionurl")})
    out[slug+"#r"]=c[:6]
    print(slug,'|',' || '.join(x['title'][5:60] for x in c[:6]),flush=True); time.sleep(2)
json.dump(out, open("tools/candidatas.json", "w"), ensure_ascii=False, indent=1)
