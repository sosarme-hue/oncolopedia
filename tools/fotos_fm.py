"""Añade img/img_alt/img_pie al front-matter de las páginas ES y EN que tienen foto descargada."""
import json, os, glob, re
P = json.load(open('tools/fotos_pick.json')); PIES = json.load(open('tools/fotos_pies.json'))
DIRS = {"diagnostico": "diagnosis", "investigacion": "research", "personajes": "people", "preguntas-frecuentes": "faq", "prevencion-y-cribado": "prevention-and-screening",
        "psicooncologia": "psycho-oncology", "tipos-de-cancer": "cancer-types", "tratamientos": "treatments", "vivir-con-cancer": "living-with-cancer"}
n = 0
for k in P:
    fn = next((f"{p}-{k}.jpg" for p in "atp" if os.path.exists(f"assets/img/{p}-{k}.jpg")), None)
    if not fn: continue
    es = glob.glob(f"src/es/*/*-{k}.md")
    es = [f for f in es if re.match(r"src/es/[^/]+/[0-9]+-" + re.escape(k) + r"\.md$", f)]
    if len(es) != 1: print("??", k, es); continue
    d, base = es[0].split("/")[2], os.path.basename(es[0]); num = base.split("-")[0]
    en = glob.glob(f"src/en/{DIRS[d]}/{num}-*.md")
    alt_es, alt_en = PIES[k]
    for f, alt in [(es[0], alt_es)] + ([(en[0], alt_en)] if en else []):
        t = open(f, encoding="utf8").read()
        if re.search(r"^img:", t, re.M): continue
        add = f"img: {fn}\nimg_alt: {alt}\nimg_pie: {alt}.\n"
        t = re.sub(r"^(desc:.*\n)", lambda m: m.group(1) + add, t, count=1, flags=re.M)
        open(f, "w", encoding="utf8").write(t); n += 1
print(n, "ficheros")
