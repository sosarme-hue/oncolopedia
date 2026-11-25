#!/usr/bin/env python3
"""Oncolopedia · generador estático (basado en el de Geneticapedia).

Uso: python3 build.py  ->  escribe la web en dist/
Contenido en src/es/**.md y src/en/**.md (cabecera --- clave: valor ---).
"""
import html, json, math, os, re, shutil
from datetime import date
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "dist")
SITE = "https://oncolopedia.com/"
TODAY = "2026-11-24"
MAIL = "partenopides@gmail.com"
V = "1"

# ----- secciones -----
SECTIONS = {
    "es": [
        ("tipos-de-cancer", "Tipos de cáncer", "Los cánceres, uno a uno", "Fichas de los cánceres más frecuentes y de los que más preguntas generan: qué son, síntomas, diagnóstico, tratamiento, pronóstico y dónde informarse."),
        ("diagnostico", "Diagnóstico", "Del síntoma al informe", "Biopsia y anatomía patológica, pruebas de imagen, estadio y grado, biomarcadores, marcadores tumorales y estudio del riesgo hereditario."),
        ("tratamientos", "Tratamientos", "Las armas contra el cáncer", "Cirugía, radioterapia, quimioterapia, hormonoterapia, terapias dirigidas, inmunoterapia, trasplante y cuidados paliativos: para qué sirve cada uno y qué esperar."),
        ("prevencion-y-cribado", "Prevención y cribado", "Prevenir y detectar a tiempo", "El Código Europeo contra el Cáncer, tabaco, alcohol y sol, vacunas, los programas de cribado en España y los síntomas que no hay que ignorar."),
        ("vivir-con-cancer", "Vivir con cáncer", "Durante y después del tratamiento", "Guías prácticas para pacientes y familias: entender el informe, la primera consulta, cuándo llamar al equipo, dolor y síntomas, sexualidad, cuidadores, decisiones compartidas, trabajo y derechos."),
        ("psicooncologia", "Psicooncología", "La mente también se cuida", "El impacto emocional del cáncer en la persona y en su familia: miedo, ansiedad y depresión, miedo a la recaída, hablar con los hijos, imagen corporal, duelo y dónde pedir ayuda psicológica."),
        ("personajes", "Personajes", "Las personas detrás de la oncología", "Médicos, científicos y pacientes que cambiaron la historia del cáncer, de Percivall Pott a la inmunoterapia."),
        ("investigacion", "Investigación", "La investigación, con contexto", "Ensayos clínicos, medicina de precisión, nuevos fármacos y cómo leer una noticia sobre cáncer sin falsas esperanzas ni alarmas."),
        ("preguntas-frecuentes", "Preguntas frecuentes", "Preguntas frecuentes", "Respuestas cortas y claras a las dudas y los mitos más habituales sobre el cáncer."),
    ],
    "en": [
        ("cancer-types", "Cancer types", "Cancers, one by one", "Fact sheets on the most common cancers and those that raise most questions: what they are, symptoms, diagnosis, treatment, outlook and where to learn more."),
        ("diagnosis", "Diagnosis", "From symptom to report", "Biopsy and pathology, imaging, stage and grade, biomarkers, tumour markers and assessing inherited risk."),
        ("treatments", "Treatments", "The tools against cancer", "Surgery, radiotherapy, chemotherapy, hormone therapy, targeted therapy, immunotherapy, transplantation and palliative care: what each one is for and what to expect."),
        ("prevention-and-screening", "Prevention and screening", "Prevent and detect early", "The European Code Against Cancer, tobacco, alcohol and sun, vaccines, screening programmes and the symptoms you should not ignore."),
        ("living-with-cancer", "Living with cancer", "During and after treatment", "Practical guides for patients and families: reading the report, the first appointment, when to call your team, pain and symptoms, sexuality, carers, shared decisions, work and rights."),
        ("psycho-oncology", "Psycho-oncology", "Caring for the mind too", "The emotional impact of cancer on the person and their family: fear, anxiety and depression, fear of recurrence, talking to children, body image, grief and where to get psychological help."),
        ("people", "People", "The people behind oncology", "Doctors, scientists and patients who changed the history of cancer, from Percivall Pott to immunotherapy."),
        ("research", "Research", "Research, in context", "Clinical trials, precision medicine, new drugs and how to read cancer news without false hope or alarm."),
        ("faq", "FAQ", "Frequently asked questions", "Short, clear answers to the most common questions and myths about cancer."),
    ],
}
EXTRA = {
    "es": [("atlas", "Atlas"), ("historia", "Historia"), ("glosario", "Glosario"), ("quiz", "Quiz"), ("fuentes", "Fuentes"), ("blog", "Blog")],
    "en": [("atlas", "Atlas"), ("history", "History"), ("glossary", "Glossary"), ("quiz", "Quiz"), ("sources", "Sources"), ("blog", "Blog")],
}
PROJECT = {
    "es": [("quien-esta-detras", "Quién está detrás"), ("enfoque-editorial", "Enfoque editorial"), ("aviso-legal", "Aviso legal"), ("privacidad", "Privacidad"), ("cookies", "Cookies")],
    "en": [("about", "About"), ("editorial-approach", "Editorial approach"), ("legal-notice", "Legal notice"), ("privacy", "Privacy"), ("cookies", "Cookies")],
}
# página equivalente en el otro idioma (ruta es -> ruta en)
PAIR = {"": "", "quien-esta-detras/": "about/", "enfoque-editorial/": "editorial-approach/", "aviso-legal/": "legal-notice/",
        "privacidad/": "privacy/", "cookies/": "cookies/", "historia/": "history/", "glosario/": "glossary/", "quiz/": "quiz/", "fuentes/": "sources/", "blog/": "blog/", "temas/": "topics/", "atlas/": "atlas/"}
for (a, *_), (b, *_) in zip(SECTIONS["es"], SECTIONS["en"]):
    PAIR[a + "/"] = b + "/"

T = {
    "es": dict(skip="Saltar al contenido", menu="Menú", other="English", otherlang="en", tagline="Comprender el cáncer. Conocer las opciones.",
               desc="Enciclopedia de oncología en castellano: tipos de cáncer, diagnóstico, tratamientos, prevención, cribado, vivir con cáncer, historia y glosario. Con fuentes oficiales y escrita por un médico.",
               foot="Enciclopedia divulgativa de oncología: ciencia, salud e historia. No ofrece diagnóstico, tratamiento ni segunda opinión individual.",
               help="¿Tienes un síntoma que no se va o te preocupa un diagnóstico? Habla con tu médico de familia o con tu equipo de oncología. Para apoyo y orientación gratuita: <b>Infocáncer de la AECC, 900 100 036</b>, 24 horas.",
               sec="Secciones", proj="Proyecto", net="Red de webs", read="Leer →", upd="Actualizado", refs="Fuentes",
               err="¿Has visto un error? Escríbenos a", by="Texto: Alejandro Rosàs, médico de familia",
               author="Creada por Alejandro Rosàs, médico de familia con más de 38 años de experiencia en atención primaria, especialista en Medicina Preventiva y Salud Pública (col. 28574, Barcelona).",
               lic='© 2026 Alejandro Rosàs · Contenido bajo licencia <a href="https://creativecommons.org/licenses/by-nc/4.0/deed.es" rel="license noopener" style="display:inline">CC BY-NC 4.0</a>, salvo indicación en contrario',
               more="En esta sección", home="Inicio", disclaimer="Información divulgativa. No sustituye la valoración de tu equipo médico ni sirve para decidir un tratamiento.",
               posts="Entradas recientes", allposts="Todas las entradas", locale="es_ES"),
    "en": dict(skip="Skip to content", menu="Menu", other="Español", otherlang="es", tagline="Understand cancer. Know the options.",
               desc="An oncology encyclopedia for everyone: cancer types, diagnosis, treatments, prevention, screening, living with cancer, history and glossary. Sourced from official bodies, written by a doctor.",
               foot="An encyclopedia of oncology for the general public: science, health and history. It does not provide diagnosis, treatment or individual second opinions.",
               help="Have a symptom that will not go away, or worried about a diagnosis? Talk to your doctor or your cancer team. In the UK, Macmillan Support Line: <b>0808 808 00 00</b>; in the US, the NCI Cancer Information Service: <b>1-800-4-CANCER</b>.",
               sec="Sections", proj="Project", net="Sister sites", read="Read →", upd="Updated", refs="Sources",
               err="Spotted a mistake? Write to", by="Text: Alejandro Rosàs, family physician",
               author="Created by Alejandro Rosàs, a family physician with over 38 years in primary care and a specialist in Preventive Medicine and Public Health (licence 28574, Barcelona).",
               lic='© 2026 Alejandro Rosàs · Content licensed under <a href="https://creativecommons.org/licenses/by-nc/4.0/" rel="license noopener" style="display:inline">CC BY-NC 4.0</a> unless otherwise stated',
               more="In this section", home="Home", disclaimer="General information only. It does not replace advice from your care team and should not be used to choose a treatment.",
               posts="Latest posts", allposts="All posts", locale="en_GB"),
}
NETWORK = [("Medicapedia", "https://medicapedia.org"), ("Farmacos.ai", "https://farmacos.ai"), ("Geneticapedia", "https://geneticapedia.com"),
           ("Psycholopedia", "https://psycholopedia.com"), ("Enfermeria.si", "https://enfermeria.si"), ("Enciclopedias.si", "https://enciclopedias.si")]

esc = html.escape


def prefix(path):
    """'' -> './', 'a/' -> '../', 'a/b/' -> '../../' (path relative to site root, lang dir included)."""
    d = path.count("/")
    return "./" if d == 0 else "../" * d


AVAIL = {"es": None, "en": None}


def avail(lang):
    if AVAIL[lang] is None:
        a = set()
        for s in SECTIONS[lang]:
            d = os.path.join(SRC, lang, s[0])
            if os.path.isdir(d) and any(f.endswith(".md") for f in os.listdir(d)):
                a.add(s[0])
        if os.path.exists(os.path.join(SRC, lang, "datos.py")):
            a.update(u for u, _ in EXTRA[lang] if u != "blog")
        bd = os.path.join(SRC, lang, "blog")
        if os.path.isdir(bd) and any(f.endswith(".md") for f in os.listdir(bd)):
            a.add("blog")
        AVAIL[lang] = a
    return AVAIL[lang]


def nav(lang, r):
    base = r + ("en/" if lang == "en" else "")
    more = [("temas", "Más temas")] if lang == "es" else [("topics", "More topics")]
    items = ([(s[0], s[1]) for s in SECTIONS[lang][:5] if s[0] in avail(lang)]
             + [x for x in EXTRA[lang] if x[0] in avail(lang) and x[0] in ("atlas", "blog")] + more)
    return "".join(f'<a href="{base}{u}/">{esc(t)}</a>' for u, t in items)


def page(lang, path, title, desc, body, *, ldtype="WebPage", extra_ld=None, full_title=False, alt=None, og_type="website"):
    """path: relative to site root, ending with '/' or '' for home or '404.html'."""
    t = T[lang]
    r = prefix(path)
    base = r + ("en/" if lang == "en" else "")
    url = SITE + path
    if alt is None:
        rel = path[3:] if lang == "en" else path
        if lang == "es":
            alt = ("en/" + PAIR[rel]) if rel in PAIR else None
            seg = PAIR.get(rel, "").strip("/").split("/")[0]
            proj = [u for u, _ in PROJECT["en"]]
            if alt and seg and seg not in avail("en") and seg not in proj:
                alt = None
        else:
            inv = {v: k for k, v in PAIR.items()}
            alt = inv.get(rel)
    es_url = en_url = None
    if lang == "es":
        es_url, en_url = path, alt
    else:
        es_url, en_url = alt, path
    hreflang = ""
    if es_url is not None and en_url is not None:
        hreflang = (f'<link rel="alternate" hreflang="es" href="{SITE}{es_url}"><link rel="alternate" hreflang="en" href="{SITE}{en_url}">'
                    f'<link rel="alternate" hreflang="x-default" href="{SITE}{es_url}">')
    other_href = r + (en_url if lang == "es" else es_url) if (es_url is not None and en_url is not None) else r + ("en/" if lang == "es" else "")
    ft = title if full_title else f"{title} · Oncolopedia"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": SITE + "#org", "name": "Oncolopedia", "url": SITE, "logo": SITE + "assets/favicon.svg"},
        {"@type": "WebSite", "@id": SITE + "#web", "name": "Oncolopedia", "url": SITE, "inLanguage": ["es", "en"], "publisher": {"@id": SITE + "#org"}},
        dict({"@type": ldtype, "@id": url + "#page", "url": url, "name": title, "description": desc, "inLanguage": lang,
              "isPartOf": {"@id": SITE + "#web"}, "dateModified": TODAY}, **(extra_ld or {}))]}
    sections_links = "".join(f'<a href="{base}{s[0]}/">{esc(s[1])}</a>' for s in SECTIONS[lang] if s[0] in avail(lang)) + "".join(f'<a href="{base}{u}/">{esc(n)}</a>' for u, n in EXTRA[lang] if u in avail(lang))
    proj_links = "".join(f'<a href="{base}{u}/">{esc(n)}</a>' for u, n in PROJECT[lang])
    net_links = "".join(f'<a href="{u}" rel="noopener">{n}</a>' for n, u in NETWORK)
    rss = f'<link rel="alternate" type="application/rss+xml" title="Oncolopedia" href="{base}blog/feed.xml">' if "blog" in avail(lang) else ""
    noindex = '<meta name="robots" content="noindex">' if path.endswith("404.html") else ""
    canon = "" if noindex else f'<link rel="canonical" href="{url}">'
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(ft)}</title>
<meta name="description" content="{esc(desc)}">{noindex}
{canon}
{hreflang}
<meta property="og:title" content="{esc(ft)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="{og_type}"><meta property="og:site_name" content="Oncolopedia"><meta property="og:url" content="{url}"><meta property="og:locale" content="{t['locale']}"><meta name="twitter:card" content="summary_large_image"><meta property="og:image" content="{SITE}assets/og-oncolopedia.png">
<meta name="theme-color" content="#123746">
{rss}
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{r}assets/fonts/SourceSans3-400-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}assets/fonts/fonts.css?v={V}">
<link rel="stylesheet" href="{r}assets/site.css?v={V}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">{t['skip']}</a>
<header class="top"><div class="wrap">
  <a class="brand" href="{base}" aria-label="Oncolopedia"><span class="sym" aria-hidden="true"><img src="{r}assets/favicon.svg" alt="" width="26" height="26" style="display:block"></span>Oncolopedia</a>
  <button class="burger" type="button" aria-expanded="false" aria-controls="menu">{t['menu']}</button>
  <nav class="menu" id="menu" aria-label="{t['sec']}">{nav(lang, r)}</nav>
  <a class="lang" href="{other_href}" hreflang="{t['otherlang']}" lang="{t['otherlang']}">{t['other']}</a>
</div></header>

<main id="main">
{body}
</main>
<footer class="foot"><div class="wrap">
  <div class="cols">
    <div><a class="brand" href="{base}"><span class="sym" aria-hidden="true"><img src="{r}assets/favicon.svg" alt="" width="26" height="26" style="display:block"></span>Oncolopedia</a><p style="margin-top:10px">{t['foot']}</p><div class="help">{t['help']}</div></div>
    <div><h4>{t['sec']}</h4>{sections_links}</div>
    <div><h4>{t['proj']}</h4>{proj_links}</div>
    <div><h4>{t['net']}</h4>{net_links}</div>
  </div>
  <p style="margin:22px 0 0">{t['author']} <a style="display:inline" href="{base}{PROJECT[lang][0][0]}/">{PROJECT[lang][0][1]}</a></p><p style="margin:6px 0 0">{t['tagline']}</p><p style="margin:6px 0 0">{t['lic']}</p>
</div></footer>
<script src="{r}assets/app.js?v={V}" defer></script>
</body>
</html>
"""


def write(path, content):
    fp = os.path.join(OUT, path if path.endswith(".html") or "." in os.path.basename(path) else os.path.join(path, "index.html"))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)


def read_md(fp):
    raw = open(fp, encoding="utf-8").read()
    meta = {}
    if raw.startswith("---"):
        head, raw = raw[3:].split("\n---", 1)
        for line in head.strip().splitlines():
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, raw.strip()


IMG = json.load(open(os.path.join(SRC, "imagenes.json"), encoding="utf-8")) if os.path.exists(os.path.join(SRC, "imagenes.json")) else {}


def credit(fn, lang="es"):
    c = IMG.get(fn)
    if not c:
        return ""
    lic = f'<a href="{esc(c["license_url"])}" rel="license noopener">{esc(c["license"])}</a>' if c.get("license_url") else esc(c["license"])
    art = c["artist"]
    if len(art) % 2 == 0 and art[:len(art) // 2] == art[len(art) // 2:]:
        art = art[:len(art) // 2]
    art = re.sub(r"^Unknown author\s*Unknown author$", "Unknown author", art)
    if lang == "es":
        art = art.replace("Unknown author", "Autor desconocido")
    if lang == "en":
        art = art.replace("Autor desconocido", "Unknown author").replace("obra derivada", "derivative work").replace("artículo de", "article by").replace("Subido por", "Uploaded by")
        lic = lic.replace("Public domain", "Public domain")
    else:
        lic = lic.replace(">Public domain<", ">Dominio público<").replace("Public domain", "Dominio público").replace(">No restrictions<", ">Sin restricciones<").replace(">Copyrighted free use<", ">Uso libre con copyright<")
    return f'<span class="credit">{"Imagen" if lang == "es" else "Image"}: {esc(art)} · {lic} · <a href="{esc(c["page"])}" rel="noopener">{esc(c.get("source", "Wikimedia Commons"))}</a></span>'


def has_img(fn):
    return bool(fn) and (os.path.exists(os.path.join(ROOT, "assets", "img", fn)) or bool(IMG.get(fn, {}).get("url")))


def isrc(fn, r="@@R@@"):
    if os.path.exists(os.path.join(ROOT, "assets", "img", fn)):
        return f"{r}assets/img/{fn}"
    u = IMG.get(fn, {}).get("url")
    return esc(u) if u else f"{r}assets/img/{fn}"


def figure(fn, alt, cap, lang, cls="fig"):
    if not has_img(fn):
        return ""
    c = IMG.get(fn, {})
    wh = f' width="{c["w"]}" height="{c["h"]}"' if c else ""
    return f'<figure class="{cls}"><img src="{isrc(fn)}" alt="{esc(alt)}"{wh} loading="lazy" decoding="async"><figcaption>{esc(cap)} {credit(fn, lang)}</figcaption></figure>'


def figs(text, lang):
    def rep(m):
        parts = [x.strip() for x in m.group(1).split("|")]
        fn, alt = parts[0], parts[1]
        cap = parts[2] if len(parts) > 2 else ""
        return "\n" + figure(fn, alt, cap, lang) + "\n"
    return re.sub(r"^!fig (.+)$", rep, text, flags=re.M)


def md(text, lang):
    text = figs(text, lang)
    h = markdown.markdown(text, extensions=["tables", "attr_list", "sane_lists"])
    # lista de fuentes con estilo .refs
    ref = T[lang]["refs"]
    h = re.sub(rf"(<h2[^>]*>{ref}</h2>\s*)<ol>", r'\1<ol class="refs">', h)
    h = re.sub(r"<table>", '<div class="table-scroll"><table>', h).replace("</table>", "</table></div>")
    # enlaces externos
    h = re.sub(r'<a href="(https?://[^"]+)">', r'<a href="\1" rel="noopener">', h)
    return h


def strip_tags(h):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()


def load_section(lang, slug):
    d = os.path.join(SRC, lang, slug)
    items = []
    if not os.path.isdir(d):
        return items
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".md"):
            meta, body = read_md(os.path.join(d, fn))
            mm = re.match(r"(\d{2,3})-(.+)\.md$", fn)
            meta["slug"] = mm.group(2) if mm else fn[:-3]
            meta["num"] = str(int(mm.group(1))) if mm else fn[:-3]
            meta["body"] = body
            items.append(meta)
    # «orden» permite colocar una ficha nueva junto a las relacionadas sin renumerar archivos
    items.sort(key=lambda m: float(m.get("orden") or (m["num"] if m["num"].isdigit() else 0)))
    return items


_GLOS = {}
_GLOS_SKIP = {"cáncer", "cancer", "tumor", "tumour", "célula", "cell", "adn", "dna", "gen", "gene"}


def glos_terms(lang):
    if lang not in _GLOS:
        import runpy, html as _h
        from build_extra import slugify as _sl
        fp = os.path.join(SRC, lang, "datos.py")
        terms = []
        if os.path.exists(fp):
            for term, d in runpy.run_path(fp)["GLOSARIO"]:
                if term.lower() in _GLOS_SKIP or len(term) < 3:
                    continue
                plain = _h.unescape(re.sub(r"<[^>]+>", "", d)).replace(" Leer más.", "").replace(" Read more.", "").strip()
                if len(plain) > 160:
                    plain = plain[:157].rsplit(" ", 1)[0] + "…"
                terms.append((term, _sl(term), plain))
        terms.sort(key=lambda x: -len(x[0]))
        _GLOS[lang] = terms
    return _GLOS[lang]


def glos_link(h, lang, maxn=14):
    """Enlaza la primera aparición de cada término del glosario en párrafos y listas."""
    gl = "../../glosario/" if lang == "es" else "../../glossary/"
    terms = glos_terms(lang)
    if not terms:
        return h
    parts = re.split(r"(<[^>]+>)", h)
    block = {"a": 0, "h": 0, "skip": 0}
    inside = 0
    used = set()
    n = 0
    for i, part in enumerate(parts):
        if part.startswith("<"):
            m = re.match(r"</?\s*([a-zA-Z0-9]+)", part)
            tag = m.group(1).lower() if m else ""
            close = part.startswith("</")
            dlt = -1 if close else 1
            if tag == "a": block["a"] += dlt
            elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"): block["h"] += dlt
            elif tag in ("table", "figcaption", "code", "pre", "aside", "blockquote", "summary"): block["skip"] += dlt
            elif tag in ("p", "li") and not part.endswith("/>"): inside += dlt
            continue
        if n >= maxn or inside <= 0 or any(v > 0 for v in block.values()) or not part.strip():
            continue
        for term, slug, plain in terms:
            if slug in used or n >= maxn:
                continue
            rx = re.compile(r"(?<![\w-])(" + re.escape(term) + r")(?![\w-])", re.I)
            mm = rx.search(part)
            if not mm:
                continue
            a = f'<a class="gl" href="{gl}#{slug}" title="{esc(plain)}">{mm.group(1)}</a>'
            parts[i] = part = part[:mm.start()] + "\x00" + str(len(used)) + "\x00" + part[mm.end():]
            used.add(slug)
            parts[i] = part
            parts[i] = parts[i]
            globals().setdefault("_GLREP", {})[(i, len(used) - 1)] = a
            n += 1
        # sustituir marcadores
        def rep(m2, i=i):
            return globals()["_GLREP"][(i, int(m2.group(1)))]
        parts[i] = re.sub(r"\x00(\d+)\x00", rep, parts[i])
    return "".join(parts)


AUTHOR_PATH = {"es": "quien-esta-detras/", "en": "en/about/"}
EDIT_PATH = {"es": "enfoque-editorial/#procedimiento", "en": "editorial-approach/#procedure"}
PUBLISHED = "2026-11-24"


def AUTHOR_LD(lang):
    return {"@type": "Person", "@id": SITE + "quien-esta-detras/#alejandro-rosas", "name": "Alejandro Rosàs",
            "url": SITE + AUTHOR_PATH[lang], "jobTitle": "Médico de familia" if lang == "es" else "Family physician",
            "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "Especialista en Medicina Preventiva y Salud Pública" if lang == "es" else "Specialist in Preventive Medicine and Public Health"}}


def _slugid(txt):
    import unicodedata
    t = unicodedata.normalize("NFKD", strip_tags(txt)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-") or "s"


def add_toc(h, lang, minimum=6):
    heads = re.findall(r"<h2>(.*?)</h2>", h)
    if len(heads) < minimum:
        return h, ""
    seen, items = set(), []
    def rep(m):
        sid = _slugid(m.group(1)); base_id = sid; k = 2
        while sid in seen:
            sid = f"{base_id}-{k}"; k += 1
        seen.add(sid); items.append((sid, m.group(1)))
        return f'<h2 id="{sid}">{m.group(1)}</h2>'
    h = re.sub(r"<h2>(.*?)</h2>", rep, h)
    lab = "En esta página" if lang == "es" else "On this page"
    toc = (f'<nav class="toc" aria-label="{lab}"><details open><summary class="toc-t">{lab} <small>· {len(items)} {"apartados" if lang == "es" else "sections"}</small></summary><ul>'
           + "".join(f'<li><a href="#{i}">{x}</a></li>' for i, x in items) + "</ul></details></nav>")
    return h, toc


def article_page(lang, sec, item, siblings, search):
    t = T[lang]
    lp = "en/" if lang == "en" else ""
    path = f"{lp}{sec[0]}/{item['slug']}/"
    r = prefix(path)
    base = r + lp
    body_html = glos_link(md(item["body"], lang), lang)
    body_html, toc = add_toc(body_html, lang)
    if item.get("medicapedia"):
        mu = f'https://medicapedia.org/{"en/" if lang == "en" else ""}enf/{item["medicapedia"]}.html'
        mb = (f'<section class="mpbox" aria-label="Medicapedia"><p class="mp-ey">{"Historia · Medicapedia" if lang == "es" else "History · Medicapedia"}</p>'
              f'<h2>{esc(item["title"])} {"en la historia de la medicina" if lang == "es" else "in the history of medicine"}</h2>'
              f'<p>{"Cómo se descubrió, quién lo investigó y cómo cambió su tratamiento a lo largo de los siglos, contado en Medicapedia, nuestra web hermana de historia de la medicina." if lang == "es" else "How it was discovered, who studied it and how its treatment changed over the centuries, told on Medicapedia, our sister site on the history of medicine."}</p>'
              f'<a class="mp-btn" href="{mu}" rel="noopener" target="_blank">{"Leer la historia en Medicapedia ↗" if lang == "es" else "Read the history on Medicapedia ↗"}</a></section>')
        ref = T[lang]["refs"]
        i = body_html.find(f">{ref}</h2>")
        if i > 0:
            j = body_html.rfind("<h2", 0, i)
            body_html = body_html[:j] + mb + body_html[j:]
        else:
            body_html += mb
    disc = f'<p class="disclaim">{t["disclaimer"]}</p>' if item.get("health") == "si" else ""
    hero = ficha = ""
    if item.get("vida"):
        rows = ([("Vida", "vida"), ("País", "pais"), ("Campo", "campo"), ("Aportación clave", "aporte"), ("Reconocimientos", "premio")] if lang == "es" else
                [("Life", "vida"), ("Country", "pais"), ("Field", "campo"), ("Key contribution", "aporte"), ("Honours", "premio")])
        img = f'<img src="{isrc(item["img"])}" alt="{esc(item["title"])}" loading="lazy">' if has_img(item.get("img")) else ""
        cred = f'<p class="fcred">{credit(item["img"], lang)}</p>' if has_img(item.get("img")) else ""
        ficha = f'<div class="box ficha">{img}<h4>{esc(item["title"])}</h4><dl>' + "".join(f'<dt>{a}</dt><dd>{esc(item[k])}</dd>' for a, k in rows if item.get(k)) + f'</dl>{cred}</div>'
    elif item.get("img"):
        hero = figure(item["img"], item.get("img_alt", item["title"]), item.get("img_pie", ""), lang, "fig hero")
    sibs = [s for s in siblings if s["slug"] != item["slug"] and (not item.get("grupo") or s.get("grupo") == item["grupo"])]
    sib = "".join(f'<li><a href="{base}{sec[0]}/{s["slug"]}/">{esc(s["title"])}</a></li>' for s in sibs)
    crumbs = f'<nav class="crumbs" aria-label="breadcrumb"><a href="{base}">{t["home"]}</a> › <a href="{base}{sec[0]}/">{esc(sec[1])}</a></nav>'
    rev = item.get("revisado", PUBLISHED)
    revline = (f' · {"Revisión clínica" if lang == "es" else "Clinical review"}: {esc(item["revisor"])}' if item.get("revisor") else "") + \
              (f' · {"Contenido clínico revisado" if lang == "es" else "Clinical content reviewed"}: {rev}' if item.get("health") == "si" else "")
    body = f"""<header class="phead wrap">{crumbs}<span class="eyebrow">{esc(sec[1])}</span><h1>{esc(item['title'])}</h1><p class="lead">{esc(item['desc'])}</p></header>
<div class="wrap article{' has-ficha' if ficha else ''}"><article class="prose">{disc}{hero}{toc}{body_html}<p class="meta"><a href="{base}{AUTHOR_PATH[lang].replace('en/', '', 1)}">{t['by']}</a>{revline} · {t['upd']}: {item.get('updated', TODAY)} · <a href="{base}{EDIT_PATH[lang]}">{"Cómo revisamos" if lang == "es" else "How we review"}</a> · {t['err']} <a href="mailto:{MAIL}">{MAIL}</a></p></article>
<aside class="aside">{ficha}<div class="box"><h4>{t['more']}: {esc(item.get('grupo') or sec[1])}</h4><ul>{sib}</ul></div></aside></div>"""
    body = body.replace("@@R@@", r)
    ldtype = "MedicalWebPage" if item.get("health") == "si" else "Article"
    extra = {"headline": item["title"], "author": AUTHOR_LD(lang), "datePublished": item.get("published", PUBLISHED), "dateModified": item.get("updated", TODAY)}
    if ldtype == "MedicalWebPage":
        extra["lastReviewed"] = item.get("revisado", PUBLISHED)
        if item.get("revisor"):
            extra["reviewedBy"] = {"@type": "Person", "name": item["revisor"]}
    write(path, page(lang, path, item["title"], item["desc"], body, ldtype=ldtype, extra_ld=extra, og_type="article", alt=item.get("alt")))
    search.append({"t": item["title"], "d": item["desc"], "u": path[len(lp):], "k": sec[1], "n": strip_tags(body_html.replace("@@R@@", ""))[:600]})


def section_index(lang, sec, items, search):
    t = T[lang]
    lp = "en/" if lang == "en" else ""
    path = f"{lp}{sec[0]}/"
    r = prefix(path)
    def thumb(it):
        if has_img(it.get("img")):
            return f'<img class="cimg" src="{isrc(it["img"], r)}" alt="" loading="lazy">'
        if it.get("vida"):
            ini = "".join(w[0] for w in it["title"].split()[:2])
            return f'<span class="cimg ph" aria-hidden="true">{esc(ini)}</span>'
        return ""
    def sub(it):
        return f'<span class="tag">{esc(it["vida"])}</span>' if it.get("vida") else ""
    def card(i, it):
        return f'<a class="card{" person" if it.get("vida") else ""}" href="./{it["slug"]}/">{thumb(it)}<span class="num">{i:02d}</span>{sub(it)}<h3>{esc(it["title"])}</h3><p>{esc(it["desc"])}</p><span class="more">{t["read"]}</span></a>'
    if any(it.get("grupo") for it in items):
        groups, gi = [], {}
        for i, it in enumerate(items, 1):
            g = it.get("grupo", "")
            if g not in gi:
                gi[g] = len(groups)
                groups.append((g, []))
            groups[gi[g]][1].append(card(i, it))
        gid = lambda g: "g-" + re.sub(r"[^a-z0-9]+", "-", g.lower().translate(str.maketrans("áéíóúñü", "aeiounu"))).strip("-")
        chips = "".join(f'<a class="gchip" href="#{gid(g)}">{esc(g)} <small>{len(c)}</small></a>' for g, c in groups)
        grids = "".join(f'<h2 class="ghead" id="{gid(g)}">{esc(g)}</h2><div class="grid">{"".join(c)}</div>' for g, c in groups)
        inner = f'<nav class="gchips" aria-label="{"Grupos" if lang == "es" else "Groups"}">{chips}</nav>{grids}'
    else:
        inner = f'<div class="grid">{"".join(card(i, it) for i, it in enumerate(items, 1))}</div>'
    body = f"""<header class="phead wrap"><span class="eyebrow">{esc(sec[1])}</span><h1>{esc(sec[2])}</h1><p class="lead">{esc(sec[3])}</p></header>
<section class="wrap section" style="padding-top:0">{inner}</section>"""
    write(path, page(lang, path, sec[2], sec[3], body, ldtype="CollectionPage"))
    search.append({"t": sec[2], "d": sec[3], "u": path[len(lp):], "k": sec[1], "n": " ".join(i["title"] for i in items)})


def topics_page(lang, allsec, search):
    t = T[lang]
    lp = "en/" if lang == "en" else ""
    slug = "temas" if lang == "es" else "topics"
    path = f"{lp}{slug}/"
    title = "Todos los temas" if lang == "es" else "All topics"
    desc = ("Todas las secciones de Oncolopedia: salud, ciencia básica, historia, sociedad y la genética de cada día." if lang == "es"
            else "Every section of Oncolopedia: health, basic science, history, society and everyday genetics.")
    word = "artículos" if lang == "es" else "articles"
    cards = "".join(f'<a class="card" href="../{s[0]}/"><span class="num">{i:02d}</span><span class="tag">{esc(s[1])}</span><h3>{esc(s[2])}</h3><p>{esc(s[3])}</p><span class="more">{len(allsec.get(s[0], []))} {word} →</span></a>'
                    for i, s in enumerate([s for s in SECTIONS[lang] if allsec.get(s[0])], 1))
    XD = {"atlas": ("Atlas de 273 entidades y subtipos", "Atlas of 273 entities and subtypes"), "historia": ("Cronología de la oncología", ""), "history": ("", "A timeline of oncology"),
          "glosario": ("Los términos de la oncología, explicados", ""), "glossary": ("", "Oncology terms, explained"), "quiz": ("Pon a prueba lo que sabes", "Test what you know"),
          "fuentes": ("Las fuentes que usamos", ""), "sources": ("", "The sources we use"), "blog": ("Novedades y artículos", "News and articles")}
    extra_cards = "".join(f'<a class="card" href="../{u}/"><span class="tag">{esc(n)}</span><h3>{esc(XD.get(u, ("", ""))[0 if lang == "es" else 1] or n)}</h3><span class="more">→</span></a>' for u, n in EXTRA[lang] if u in avail(lang))
    body = f"""<header class="phead wrap"><span class="eyebrow">{"Mapa del sitio" if lang == "es" else "Site map"}</span><h1>{title}</h1><p class="lead">{desc}</p></header>
<section class="wrap section" style="padding-top:0"><div class="grid">{cards}</div>
<h2 class="ghead" style="margin-top:36px">{"Herramientas y recursos" if lang == "es" else "Tools and resources"}</h2><div class="grid">{extra_cards}</div></section>"""
    write(path, page(lang, path, title, desc, body, ldtype="CollectionPage"))
    search.append({"t": title, "d": desc, "u": path[len(lp):], "k": title, "n": ""})


def simple_page(lang, slug, search, eyebrow=None):
    lp = "en/" if lang == "en" else ""
    meta, body = read_md(os.path.join(SRC, lang, "pages", slug + ".md"))
    path = f"{lp}{slug}/"
    h = md(body, lang)
    out = f"""<header class="phead wrap"><span class="eyebrow">{esc(meta.get('eyebrow', ''))}</span><h1>{esc(meta['title'])}</h1><p class="lead">{esc(meta['desc'])}</p></header>
<div class="wrap narrow prose">{h}</div>"""
    write(path, page(lang, path, meta["title"], meta["desc"], out))
    search.append({"t": meta["title"], "d": meta["desc"], "u": path[len(lp):], "k": meta.get("eyebrow", ""), "n": strip_tags(h)[:400]})
    return meta


# ----- hélice SVG de la portada -----
def helix_svg():
    W, H, n = 520, 390, 15
    a = []
    for k in range(n):
        y = 20 + k * (H - 40) / (n - 1)
        ph = k * 0.55
        x1 = W / 2 + 120 * math.sin(ph)
        x2 = W / 2 - 120 * math.sin(ph)
        op = 0.35 + 0.65 * (math.cos(ph) + 1) / 2
        col = ["#2f58a8", "#a3305f", "#2f8a6b", "#c98a1c"][k % 4]
        a.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="7" stroke-linecap="round" opacity="{op:.2f}"/>')
    p1 = " ".join(f"{W/2 + 120*math.sin(i*0.55/4):.1f},{20 + i*(H-40)/((n-1)*4):.1f}" for i in range((n - 1) * 4 + 1))
    p2 = " ".join(f"{W/2 - 120*math.sin(i*0.55/4):.1f},{20 + i*(H-40)/((n-1)*4):.1f}" for i in range((n - 1) * 4 + 1))
    return (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Doble hélice de ADN">'
            + "".join(a)
            + f'<polyline points="{p1}" fill="none" stroke="var(--accent)" stroke-width="9" stroke-linecap="round"/>'
            + f'<polyline points="{p2}" fill="none" stroke="var(--gold)" stroke-width="9" stroke-linecap="round"/></svg>')


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    for f in os.listdir(os.path.join(ROOT, "static")):
        shutil.copy(os.path.join(ROOT, "static", f), OUT)
    urls = []
    import build_extra
    # emparejar artículos es <-> en por sección y número de archivo
    for (a, *_), (b, *_) in zip(SECTIONS["es"], SECTIONS["en"]):
        en_items = {i["num"]: i["slug"] for i in load_section("en", b)}
        for i in load_section("es", a):
            if i["num"] in en_items:
                PAIR[f"{a}/{i['slug']}/"] = f"{b}/{en_items[i['num']]}/"
    bes, ben = (sorted(f for f in os.listdir(os.path.join(SRC, x, "blog")) if f.endswith(".md")) if os.path.isdir(os.path.join(SRC, x, "blog")) else [] for x in ("es", "en"))
    for fe, fn_ in zip(bes, ben):
        en_slug = read_md(os.path.join(SRC, "es", "blog", fe))[0].get("en") or fn_[11:-3]
        PAIR[f"blog/{fe[11:-3]}/"] = f"blog/{en_slug}/"
    for lang in ("es", "en"):
        search = []
        allsec = {}
        for sec in SECTIONS[lang]:
            items = load_section(lang, sec[0])
            allsec[sec[0]] = items
            if not items:
                continue
            section_index(lang, sec, items, search)
            for it in items:
                article_page(lang, sec, it, items, search)
        topics_page(lang, allsec, search)
        build_extra.build(lang, globals(), allsec, search)
        os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
        with open(os.path.join(OUT, "assets", f"search-{lang}.json"), "w", encoding="utf-8") as f:
            json.dump(search, f, ensure_ascii=False)
    # sitemap
    for dp, dn, fn in os.walk(OUT):
        for f in fn:
            if f == "index.html":
                rel = os.path.relpath(os.path.join(dp, f), OUT).replace("\\", "/")[:-10]
                urls.append(rel)
    urls.sort(key=lambda u: (u.startswith("en/"), u.count("/"), u))
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
    print(len(urls), "páginas")


if __name__ == "__main__":
    main()
