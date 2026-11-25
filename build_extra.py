"""Páginas especiales: portada, historia, glosario, quiz, blog, proyecto y 404."""
import html, json, os, re, runpy, unicodedata
from email.utils import format_datetime
from datetime import datetime, timezone
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
from atlas_map import match as atlas_match

esc = html.escape


def slugify(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


# Imagen de cada hito de la historia (por índice de HISTORIA; se usa la primera que exista)
HIST_IMG = {0: ['h-edwin-smith.jpg'], 2: ['h-hipocrates.jpg'], 3: ['h-galeno.jpg'], 5: ['h-vesalio.jpg'], 6: ['h-ramazzini.jpg'], 10: ['p-percivall-pott.jpg'], 12: ['h-hodgkin.jpg'], 14: ['p-rudolf-virchow.jpg'], 16: ['h-paget.jpg'], 17: ['p-william-halsted.jpg'], 18: ['h-rayos-x.jpg'], 20: ['marie-curie.jpg'], 21: ['p-peyton-rous.jpg'], 25: ['p-george-papanicolaou.jpg'], 27: ['p-charles-huggins.jpg'], 29: ['p-sidney-farber.jpg'], 31: ['h-hela.jpg'], 32: ['h-adn.jpg'], 35: ['p-janet-rowley.jpg'], 36: ['h-mamografia.jpg'], 37: ['h-surgeon-general.jpg'], 39: ['p-cicely-saunders.jpg'], 41: ['h-nixon.jpg'], 42: ['h-tac.jpg'], 44: ['p-harold-varmus-y-michael-bishop.jpg'], 45: ['h-tamoxifeno.jpg'], 49: ['p-mariano-barbacid.jpg'], 50: ['h-vph.jpg'], 51: ['p-bernard-fisher.jpg'], 52: ['p-mary-claire-king.jpg'], 57: ['p-brian-druker.jpg'], 58: ['h-genoma.jpg'], 60: ['p-harald-zur-hausen.jpg'], 62: ['p-james-allison-y-tasuku-honjo.jpg'], 64: ['h-car-t.jpg'], 65: ['h-honjo.jpg']}

QUIZ_ESO = set()

L = {
    "es": dict(hist="historia", glos="glosario", quiz="quiz", blog="blog", fuentes="fuentes", res_url="diagnostico/estadio-y-grado/", fam_url="vivir-con-cancer/apoyo-emocional/", src_note="Una fuente fiable no sustituye a tu equipo médico. Si un resultado o una noticia te preocupa, coméntalo con tu oncólogo o en tu centro de salud.",
               eyebrow="La enciclopedia de la oncología", h1="Comprender el cáncer.<br><em>Conocer las opciones.</em>",
               lead="Los tipos de cáncer, cómo se diagnostican, cómo se tratan y cómo se vive con ellos, explicados con claridad. De Marie Curie a la inmunoterapia, con fuentes oficiales en cada página.",
               note="Hacia 1921. Las investigaciones de Marie y Pierre Curie sobre la radiactividad, con el descubrimiento del radio en 1898, abrieron el camino a la radioterapia.",
               ph="Busca un cáncer, una prueba, un tratamiento…", btn="Buscar", start="Explorar los cánceres →", play="Entender el diagnóstico",
               trust=["Tipos de cáncer", "Diagnóstico", "Tratamientos", "Atlas, historia, glosario y quiz", "Bilingüe · Con fuentes · Gratuita"],
               core_e="El núcleo de Oncolopedia", core_h="Cánceres. Diagnóstico. Tratamiento.", core_p="Del nombre del tumor a las decisiones: lo que importa a los pacientes y a sus familias.",
               res_h="Un informe necesita<br>una explicación.", res_p="El estadio no es lo mismo que el grado. Una supervivencia a cinco años describe a un grupo, no a una persona. Una diana molecular no garantiza una respuesta.", res_btn="Estadio y grado, explicados",
               fam_e="Pacientes y familias", fam_h="No tienes que pasar por esto a solas", fam_p="El diagnóstico de un cáncer sacude a toda la familia. Hay apoyo psicológico, asociaciones de pacientes y servicios gratuitos de orientación. Pedir ayuda también forma parte del tratamiento.", fam_btn="Apoyo emocional",
               sci_e="Novedades y avances", sci_h="La investigación, con contexto", sci_p="Enlaces a las fuentes originales, con lo que conviene mirar en cada una. Ninguna noticia promete que un tratamiento esté disponible ni que sirva para todos.",
               sci=[("Ensayos clínicos", "Revisa a quién incluye, en qué fase está, con qué se compara y qué resultados tiene.", "https://clinicaltrials.gov/search?cond=Cancer", "ClinicalTrials.gov"),
                    ("Medicamentos autorizados", "Comprueba la indicación, quién puede recibirlo y si está autorizado en España.", "https://cima.aemps.es/cima/", "AEMPS · CIMA"),
                    ("Las cifras del cáncer", "Incidencia, mortalidad y supervivencia en el mundo y por país, con su metodología.", "https://gco.iarc.who.int/today/", "IARC · GCO")],
               consult="Consultar", fuentes_btn="Todas las fuentes →",
               fuentes_title="Fuentes y biblioteca", fuentes_desc="Dónde ampliar, contrastar y comprobar: fuentes fiables de oncología para pacientes, familias y profesionales, con lo que conviene saber de cada una.",
               libros_h="Biblioteca de referencia", libros_p="Manuales y libros en los que nos apoyamos para escribir y revisar los contenidos.",
               doors_e="Tres formas de entrar", doors_h="Comprender, decidir, descubrir",
               doors=[("Comprender", "Las bases", [("preguntas-frecuentes/que-es-el-cancer/", "Qué es el cáncer"), ("diagnostico/estadio-y-grado/", "Estadio y grado"), ("atlas/", "Atlas de 273 subtipos"), ("glosario/", "Glosario")]),
                      ("Decidir", "Diagnóstico y tratamiento", [("diagnostico/biopsia-y-anatomia-patologica/", "La biopsia"), ("tratamientos/inmunoterapia/", "Inmunoterapia"), ("tratamientos/cuidados-paliativos/", "Cuidados paliativos"), ("vivir-con-cancer/efectos-secundarios/", "Efectos secundarios")]),
                      ("Descubrir", "Historia y ciencia", [("historia/", "Historia de la oncología"), ("personajes/marie-curie/", "Marie Curie"), ("investigacion/como-leer-una-noticia-sobre-cancer/", "Cómo leer una noticia"), ("quiz/", "Quiz")])],
               map_e="Un mapa de la oncología", map_h="¿Qué te gustaría comprender?", map_p="Ocho secciones, de lo más básico a lo más nuevo.",
               hist_e="Historia", hist_h="Del papiro de Edwin Smith a la inmunoterapia", hist_btn="Ver la historia completa →",
               blog_e="Blog", blog_h="Entradas recientes", blog_btn="Todas las entradas →",
               who_t="Quién está detrás", who_h="Creada por un médico de familia",
               who_p="Alejandro Rosàs, médico de familia con <b>más de 38 años de experiencia en atención primaria</b> y especialista en Medicina Preventiva y Salud Pública. Colegiado en Barcelona, n.º 28574.",
               who_btn="Conocer al autor", ed_t="Oncología con contexto", ed_h="Sin falsas esperanzas ni alarmismo",
               ed_p="Explicamos la evidencia, sus límites y las incertidumbres. Separamos lo demostrado de lo que se investiga y de lo que se vende.", ed_btn="Nuestro enfoque editorial",
               hist_title="Historia de la oncología", hist_desc="Una línea de tiempo del cáncer y su tratamiento, del antiguo Egipto a la inmunoterapia y la medicina de precisión.",
               glos_title="Glosario de oncología", quiz_title="¿Cuánto sabes sobre el cáncer?", blog_title="Blog de Oncolopedia",
               blog_desc="Novedades, explicaciones de noticias y preguntas frecuentes sobre el cáncer, sin tecnicismos.",
               photo_alt="Retrato de Marie Curie hacia 1921", photo_t="Marie Curie, hacia 1921", photo_c="Underwood & Underwood / Wide World Photos · Dominio público en EE. UU. · <a href=\"https://commons.wikimedia.org/wiki/File:Portrait_of_Marie_Curie.jpg\" rel=\"noopener\">Wikimedia Commons</a> · <a href=\"personajes/marie-curie/\">Su historia</a>",
               q_daily="Quiz diario", q_all="Todas", p404="Página no encontrada", p404d="La página que buscas no existe o ha cambiado de dirección.", back="Volver a la portada",
               atlas_title="Atlas oncológico", atlas_desc="273 entidades y subtipos malignos agrupados por localización, con la clasificación de referencia y un perfil divulgativo de cada familia de tumores.",
               date_fmt=lambda d: f"{int(d[8:10])} de {['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'][int(d[5:7])-1]} de {d[:4]}"),
    "en": dict(hist="history", glos="glossary", quiz="quiz", blog="blog", fuentes="sources", res_url="diagnosis/stage-and-grade/", fam_url="living-with-cancer/emotional-support/", src_note="A reliable source does not replace your care team. If a result or a news story worries you, talk to your oncologist or your doctor.",
               eyebrow="The encyclopedia of oncology", h1="Understand cancer.<br><em>Know the options.</em>",
               lead="Cancer types, how they are diagnosed, how they are treated and how people live with them, clearly explained. From Marie Curie to immunotherapy, with official sources on every page.",
               note="Circa 1921. Marie and Pierre Curie's research on radioactivity, including the discovery of radium in 1898, paved the way for radiotherapy.",
               ph="Search a cancer, a test, a treatment…", btn="Search", start="Explore cancers →", play="Understand diagnosis",
               trust=["Cancer types", "Diagnosis", "Treatments", "Atlas, history, glossary and quiz", "Bilingual · Sourced · Free"],
               core_e="The core of Oncolopedia", core_h="Cancers. Diagnosis. Treatment.", core_p="From the name of the tumour to decisions: what matters to patients and their families.",
               res_h="A report needs<br>an explanation.", res_p="Stage is not the same as grade. Five-year survival describes a group, not a person. A molecular target does not guarantee a response.", res_btn="Stage and grade, explained",
               fam_e="Patients and families", fam_h="You do not have to face this alone", fam_p="A cancer diagnosis shakes the whole family. There is psychological support, patient organisations and free information services. Asking for help is part of treatment too.", fam_btn="Emotional support",
               sci_e="News and advances", sci_h="Research, in context", sci_p="Links to original sources, with what to look for in each. No news story promises that a treatment is available or that it works for everyone.",
               sci=[("Clinical trials", "Check who is included, which phase it is in, what it is compared with and what results it has.", "https://clinicaltrials.gov/search?cond=Cancer", "ClinicalTrials.gov"),
                    ("Authorised medicines", "Check the indication, who can receive it and whether it is authorised where you live.", "https://www.ema.europa.eu/en/medicines", "EMA"),
                    ("Cancer statistics", "Incidence, mortality and survival worldwide and by country, with their methods.", "https://gco.iarc.who.int/today/", "IARC · GCO")],
               consult="Look up", fuentes_btn="All sources →",
               fuentes_title="Sources and library", fuentes_desc="Where to read more, cross-check and verify: reliable oncology sources for patients, families and professionals, with what to know about each.",
               libros_h="Reference library", libros_p="Textbooks and books we rely on to write and review the content.",
               doors_e="Three ways in", doors_h="Understand, decide, discover",
               doors=[("Understand", "The basics", [("faq/what-is-cancer/", "What is cancer"), ("diagnosis/stage-and-grade/", "Stage and grade"), ("atlas/", "Atlas of 273 subtypes"), ("glossary/", "Glossary")]),
                      ("Decide", "Diagnosis and treatment", [("diagnosis/biopsy-and-pathology/", "The biopsy"), ("treatments/immunotherapy/", "Immunotherapy"), ("treatments/palliative-care/", "Palliative care"), ("living-with-cancer/side-effects/", "Side effects")]),
                      ("Discover", "History and science", [("history/", "History of oncology"), ("people/marie-curie/", "Marie Curie"), ("research/how-to-read-cancer-news/", "How to read the news"), ("quiz/", "Quiz")])],
               map_e="A map of oncology", map_h="What would you like to understand?", map_p="Eight sections, from the basics to the newest science.",
               hist_e="History", hist_h="From the Edwin Smith papyrus to immunotherapy", hist_btn="See the full history →",
               blog_e="Blog", blog_h="Latest posts", blog_btn="All posts →",
               who_t="About", who_h="Created by a family doctor",
               who_p="Alejandro Rosàs, a family physician with <b>over 38 years in primary care</b> and a specialist in Preventive Medicine and Public Health. Licensed in Barcelona, no. 28574.",
               who_btn="About the author", ed_t="Oncology in context", ed_h="No false hope, no alarmism",
               ed_p="We explain the evidence, its limits and the uncertainties. We separate what is proven from what is being studied and what is being sold.", ed_btn="Our editorial approach",
               hist_title="History of oncology", hist_desc="A timeline of cancer and its treatment, from ancient Egypt to immunotherapy and precision medicine.",
               glos_title="Oncology glossary", quiz_title="How much do you know about cancer?", blog_title="Oncolopedia blog",
               blog_desc="News, explainers and frequently asked questions about cancer, without the jargon.",
               photo_alt="Portrait of Marie Curie, circa 1921", photo_t="Marie Curie, circa 1921", photo_c="Underwood & Underwood / Wide World Photos · Public domain in the US · <a href=\"https://commons.wikimedia.org/wiki/File:Portrait_of_Marie_Curie.jpg\" rel=\"noopener\">Wikimedia Commons</a> · <a href=\"people/marie-curie/\">Her story</a>",
               q_daily="Daily quiz", q_all="All", p404="Page not found", p404d="The page you are looking for does not exist or has moved.", back="Back to the home page",
               atlas_title="Oncology atlas", atlas_desc="273 malignant entities and subtypes grouped by site, with the reference classification and a plain-language profile of each tumour family.",
               date_fmt=lambda d: datetime.strptime(d, "%Y-%m-%d").strftime("%-d %B %Y")),
}


def build(lang, g, allsec, search):
    T, page, write, md, prefix, SECTIONS, SRC, TODAY, MAIL, SITE = (g[k] for k in ("T", "page", "write", "md", "prefix", "SECTIONS", "SRC", "TODAY", "MAIL", "SITE"))
    l = L[lang]
    t = T[lang]
    lp = "en/" if lang == "en" else ""
    if not os.path.exists(os.path.join(SRC, lang, "datos.py")):
        return build_lite(lang, g, search)
    data = runpy.run_path(os.path.join(SRC, lang, "datos.py"))

    # ---------- blog ----------
    posts = []
    bdir = os.path.join(SRC, lang, "blog")
    for fn in sorted(os.listdir(bdir), reverse=True):
        if fn.endswith(".md"):
            meta, body = g["read_md"](os.path.join(bdir, fn))
            meta["slug"] = fn[11:-3]
            meta["date"] = fn[:10]
            meta["body"] = body
            posts.append(meta)
    brief_l = "Noticia breve" if lang == "es" else "News in brief"
    for p in posts:
        path = f"{lp}blog/{p['slug']}/"
        h = g["glos_link"](md(p["body"], lang), lang)
        crumbs = f'<nav class="crumbs" aria-label="breadcrumb"><a href="../../">{t["home"]}</a> › <a href="../">Blog</a></nav>' if not lp else f'<nav class="crumbs" aria-label="breadcrumb"><a href="../../">{t["home"]}</a> › <a href="../">Blog</a></nav>'
        others = "".join(f'<li><a href="../{o["slug"]}/">{esc(o["title"])}</a></li>' for o in posts if o is not p)
        out = f"""<header class="phead wrap">{crumbs}<span class="eyebrow">Blog · {(brief_l + " · ") if p.get("tipo") == "breve" else ""}<time datetime="{p['date']}">{l['date_fmt'](p['date'])}</time></span><h1>{esc(p['title'])}</h1><p class="lead">{esc(p['desc'])}</p></header>
<div class="wrap article"><article class="prose">{h}<p class="meta">{t['by']} · {t['err']} <a href="mailto:{MAIL}">{MAIL}</a></p></article>
<aside class="aside"><div class="box"><h4>{t['posts']}</h4><ul>{others}</ul><p style="margin:10px 0 0"><a href="../">{t['allposts']} →</a></p></div></aside></div>"""
        write(path, page(lang, path, p["title"], p["desc"], out, ldtype="BlogPosting", og_type="article", alt=p.get("alt"),
                         extra_ld={"headline": p["title"], "datePublished": p["date"], "author": {"@type": "Person", "name": "Alejandro Rosàs"}}))
        search.append({"t": p["title"], "d": p["desc"], "u": path[len(lp):], "k": "Blog", "n": g["strip_tags"](h)[:400]})
    brief_l = "Noticia breve" if lang == "es" else "News in brief"
    def _kind(p):
        return "breve" if p.get("tipo") == "breve" else "art"
    cards = "".join(f'<a class="card" data-kind="{_kind(p)}" href="./{p["slug"]}/"><span class="tag">{(brief_l + " · ") if _kind(p) == "breve" else ""}{l["date_fmt"](p["date"])}</span><h3>{esc(p["title"])}</h3><p>{esc(p["desc"])}</p><span class="more">{t["read"]}</span></a>' for p in posts)
    bopts = [("all", "Todo"), ("breve", "Noticias breves"), ("art", "Artículos")] if lang == "es" else [("all", "All"), ("breve", "News in brief"), ("art", "Articles")]
    bchips = "".join(f'<button type="button" class="chip{" on" if k == "all" else ""}" data-k="{k}">{v}</button>' for k, v in bopts)
    bjs = """<script>(function(){var c=document.querySelectorAll('.bchips .chip'),a=document.querySelectorAll('.bgrid .card');c.forEach(function(b){b.addEventListener('click',function(){var k=b.getAttribute('data-k');c.forEach(function(x){x.classList.toggle('on',x===b)});a.forEach(function(e){e.style.display=(k==='all'||e.getAttribute('data-kind')===k)?'':'none'})})});var q=location.hash.slice(1);c.forEach(function(b){if(b.getAttribute('data-k')===q)b.click()})})();</script>"""
    path = f"{lp}blog/"
    write(path, page(lang, path, l["blog_title"], l["blog_desc"], f'<header class="phead wrap"><span class="eyebrow">Blog</span><h1>{l["blog_title"]}</h1><p class="lead">{l["blog_desc"]}</p><p><a href="./feed.xml">RSS</a></p><div class="tlchips bchips" role="group">{bchips}</div></header><section class="wrap section" style="padding-top:0"><div class="grid bgrid">{cards}</div></section>{bjs}', ldtype="Blog"))
    items = "".join(f"<item><title>{esc(p['title'])}</title><link>{SITE}{lp}blog/{p['slug']}/</link><guid>{SITE}{lp}blog/{p['slug']}/</guid><pubDate>{format_datetime(datetime.strptime(p['date'], '%Y-%m-%d').replace(hour=8, tzinfo=timezone.utc))}</pubDate><description>{esc(p['desc'])}</description></item>" for p in posts)
    rss = f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Oncolopedia</title><link>{SITE}{lp}</link><description>{esc(l["blog_desc"])}</description><language>{lang}</language>{items}</channel></rss>\n'
    write(f"{lp}blog/feed.xml", rss)

    # ---------- historia ----------
    tl = data["HISTORIA"]
    path = f"{lp}{l['hist']}/"
    def _yr(y):
        m = re.search(r"\d{4}", y)
        return int(m.group()) if m else 0
    eras = ([("all", "Todo"), ("e1", "Antes de 1900"), ("e2", "1900-1952"), ("e3", "1953-1989"), ("e4", "1990-2009"), ("e5", "2010-hoy")] if lang == "es"
            else [("all", "All"), ("e1", "Before 1900"), ("e2", "1900-1952"), ("e3", "1953-1989"), ("e4", "1990-2009"), ("e5", "2010-today")])
    def _era(y):
        n = _yr(y)
        return "e1" if n < 1900 else "e2" if n < 1953 else "e3" if n < 1990 else "e4" if n < 2010 else "e5"
    more_l = "Leer más" if lang == "es" else "Read more"
    def _thumb(i, x):
        cands = [f.replace("@@L@@", lang) for f in HIST_IMG.get(i, [])]
        fn = next((f for f in cands if g["has_img"](f)), None)
        if not fn:
            return ""
        c = g["IMG"].get(fn, {})
        return (f'<figure class="tlimg"><img src="{g["isrc"](fn, "../" * path.count("/"))}" alt="{esc(x[1])}" loading="lazy" decoding="async">'
                f'<figcaption>{g["credit"](fn, lang)}</figcaption></figure>')
    lis = "".join(f'<li id="h{i}" data-era="{_era(x[0])}">{_thumb(i, x)}<span class="y">{esc(x[0])}</span><h3>{esc(x[1])}</h3><p class="sum">{x[2]}</p>' + (f'<details class="det"><summary>{more_l}</summary><p>{x[3]}</p></details>' if len(x) > 3 else '') + '</li>' for i, x in enumerate(tl))
    # tira visual: posición proporcional al año (1850-2030); lo anterior se agrupa al inicio
    dots = ""
    for i, x in enumerate(tl):
        n = _yr(x[0]); pos = 0 if n < 1850 else (n - 1850) / (2030 - 1850) * 100
        dots += f'<a class="tdot {_era(x[0])}" href="#h{i}" style="left:{pos:.1f}%" title="{esc(x[0])}: {esc(x[1])}"><span class="sr">{esc(x[0])}: {esc(x[1])}</span></a>'
    ticks = "".join(f'<span class="tick" style="left:{(y - 1850) / 180 * 100:.1f}%">{y}</span>' for y in (1850, 1900, 1950, 2000))
    chips = "".join(f'<button type="button" class="chip{" on" if k == "all" else ""}" data-era="{k}">{esc(v)}</button>' for k, v in eras)
    hint = "Toca un punto para ir al hito, o filtra por época." if lang == "es" else "Tap a dot to jump to a milestone, or filter by era."
    refs = "".join(f"<li>{r}</li>" for r in data["HISTORIA_FUENTES"])
    js = """<script>(function(){var c=document.querySelectorAll('.tlchips .chip'),li=document.querySelectorAll('ol.tl>li');c.forEach(function(b){b.addEventListener('click',function(){var e=b.getAttribute('data-era');c.forEach(function(x){x.classList.toggle('on',x===b)});li.forEach(function(l){l.style.display=(e==='all'||l.getAttribute('data-era')===e)?'':'none'})})});document.querySelectorAll('.tdot').forEach(function(d){d.addEventListener('click',function(){c[0].click();var t=document.querySelector(d.getAttribute('href'));if(t){var x=t.querySelector('details');if(x)x.open=true}})})})();</script>"""
    out = f"""<header class="phead wrap"><span class="eyebrow">{l['hist_e']}</span><h1>{l['hist_title']}</h1><p class="lead">{l['hist_desc']}</p></header>
<div class="wrap narrow"><div class="tlbar" aria-label="{'Cronología visual' if lang == 'es' else 'Visual timeline'}"><div class="track">{dots}</div><div class="ticks">{ticks}</div></div><p class="meta">{hint}</p><div class="tlchips">{chips}</div></div>
<div class="wrap narrow prose"><ol class="tl">{lis}</ol><h2>{t['refs']}</h2><ol class="refs">{refs}</ol><p class="meta">{t['by']} · {t['upd']}: {TODAY}</p></div>{js}"""
    write(path, page(lang, path, l["hist_title"], l["hist_desc"], out, ldtype="Article", extra_ld={"headline": l["hist_title"]}))
    search.append({"t": l["hist_title"], "d": l["hist_desc"], "u": path[len(lp):], "k": l["hist_e"], "n": " ".join(x[1] for x in tl)})

    # ---------- glosario ----------
    gl = sorted(data["GLOSARIO"], key=lambda x: slugify(x[0]))
    path = f"{lp}{l['glos']}/"
    letters = []
    blocks = ""
    cur = None
    for term, d in gl:
        L0 = slugify(term)[0].upper()
        if L0 != cur:
            if cur:
                blocks += "</dl>"
            cur = L0
            letters.append(L0)
            blocks += f'<h2 id="{L0}">{L0}</h2><dl class="gl-list">'
        _gl = data.get("GLOS_LINKS", {}) if isinstance(data, dict) else getattr(data, "GLOS_LINKS", {})
        if term in _gl and "<a " not in d:
            d = d + f' <a href="../{_gl[term]}">{"Leer más" if lang == "es" else "Read more"}</a>.'
        blocks += f'<dt id="{slugify(term)}">{esc(term)}</dt><dd>{d}</dd>'
        search.append({"t": term, "d": re.sub("<[^>]+>", "", d), "u": f"{l['glos']}/#{slugify(term)}", "k": t.get("glos", "Glosario" if lang == "es" else "Glossary")})
    blocks += "</dl>"
    gdesc = (f"{len(gl)} términos de oncología explicados de forma breve y clara, de adyuvante a TNM." if lang == "es"
             else f"{len(gl)} oncology terms explained briefly and clearly, from adjuvant to TNM.")
    nav = "".join(f'<a href="#{x}">{x}</a>' for x in letters)
    out = f"""<header class="phead wrap"><span class="eyebrow">{'Glosario' if lang=='es' else 'Glossary'}</span><h1>{l['glos_title']}</h1><p class="lead">{gdesc}</p></header>
<div class="wrap narrow prose"><p class="glletras" style="display:flex;flex-wrap:wrap;gap:6px 12px;font-weight:600">{nav}</p>{blocks}<p class="meta">{t['by']} · {t['upd']}: {TODAY}</p></div>"""
    write(path, page(lang, path, l["glos_title"], gdesc, out, ldtype="DefinedTermSet"))
    search.append({"t": l["glos_title"], "d": gdesc, "u": path[len(lp):], "k": "", "n": ""})

    # ---------- quiz ----------
    qs = [dict(x) for x in data["QUIZ"]]
    for i, x in enumerate(qs):
        x.setdefault("nivel", "eso" if i in QUIZ_ESO else "bach")
    temas = data["QUIZ_TEMAS"]
    path = f"{lp}quiz/"
    qdesc = (f"{len(qs)} preguntas con explicación. Juega al quiz diario de 10 preguntas, o elige un tema." if lang == "es"
             else f"{len(qs)} questions with explanations. Play the daily 10-question quiz, or pick a topic.")
    niv = []
    btns = f'<button class="on" data-m="diario">{l["q_daily"]}</button><button data-m="*">{l["q_all"]}</button>' + "".join(f'<button class="lvl" data-m="{k}">{v}</button>' for k, v in niv) + "".join(f'<button data-m="{k}">{esc(v)}</button>' for k, v in temas.items())
    out = f"""<header class="phead wrap"><span class="eyebrow">Quiz</span><h1>{l['quiz_title']}</h1><p class="lead">{qdesc}</p></header>
<div class="wrap narrow"><div class="filters" id="quiz-modes">{btns}</div>
<div class="quiz" id="bigquiz" data-all="{esc(json.dumps(qs, ensure_ascii=False))}"></div></div>"""
    write(path, page(lang, path, l["quiz_title"], qdesc, out))
    search.append({"t": l["quiz_title"], "d": qdesc, "u": path[len(lp):], "k": "Quiz", "n": ""})

    # ---------- proyecto ----------
    for slug, _ in g["PROJECT"][lang]:
        g["simple_page"](lang, slug, search)

    # ---------- fuentes ----------
    path = f"{lp}{l['fuentes']}/"
    groups = "".join(f'<h2>{esc(gname)}</h2><dl class="gl-list">' + "".join(f'<dt><a href="{u}" rel="noopener">{esc(nm)}</a> ↗</dt><dd>{esc(dd)}</dd>' for nm, u, dd in items) + "</dl>" for gname, items in data["FUENTES"])
    libros = "".join(f"<li>{b}</li>" for b in data["LIBROS"])
    out = f"""<header class="phead wrap"><span class="eyebrow">{t['refs']}</span><h1>{l['fuentes_title']}</h1><p class="lead">{l['fuentes_desc']}</p></header>
<div class="wrap narrow prose"><div class="note">{l['src_note']}</div>{groups}<h2>{l['libros_h']}</h2><p>{l['libros_p']}</p><ul>{libros}</ul><p class="meta">{t['upd']}: {TODAY}</p></div>"""
    write(path, page(lang, path, l["fuentes_title"], l["fuentes_desc"], out, ldtype="CollectionPage"))
    search.append({"t": l["fuentes_title"], "d": l["fuentes_desc"], "u": path[len(lp):], "k": t["refs"], "n": " ".join(nm for _, it in data["FUENTES"] for nm, _, _ in it)})

    # ---------- atlas ----------
    AT = json.load(open(os.path.join(SRC, "atlas.json"), encoding="utf-8"))
    PR = json.load(open(os.path.join(SRC, "profiles.json"), encoding="utf-8"))
    sec0 = SECTIONS[lang][0][0]
    PMAP = {  # perfil -> número de ficha en tipos de cáncer
        'breast': '1', 'lung': '15', 'digestive': '21', 'prostate': '33', 'skin': '41', 'pancreas': '28', 'liver': '30', 'urinary': '34', 'gynecology': '7', 'leukemia': '68', 'lymphoma': '77', 'pediatric': '95', 'cns': '59', 'headneck': '47', 'endocrine': '54', 'soft': '87', 'bone': '87', 'testis': '37'}
    bynum = {i["num"]: i for i in allsec.get(sec0, [])}
    i2 = 0 if lang == "es" else 1
    lab = (["Cómo se diagnostica", "Cómo se trata", "Qué influye en el pronóstico", "Cifras", "Ficha completa", "Fuente oficial", "entidades"] if lang == "es"
           else ["How it is diagnosed", "How it is treated", "What shapes the outlook", "Figures", "Full fact sheet", "Official source", "entities"])
    order = [k for k in PR if any(x["profile"] == k for x in AT)]
    fams = ""
    chips = f'<button type="button" class="chip on" data-f="all">{"Todas" if lang == "es" else "All"}</button>'
    for k in order:
        p = PR[k]
        ents = sorted([x for x in AT if x["profile"] == k], key=lambda x: slugify(x[lang]))
        art = bynum.get(PMAP.get(k, ""))
        link = f'<a class="btn primary" href="../{sec0}/{art["slug"]}/">{lab[4]}: {esc(art["title"])} →</a> ' if art else ""
        def ali(x):
            fa = bynum.get(atlas_match(x["es"]) or "")
            fl = f' <a class="alink" href="../{sec0}/{fa["slug"]}/">{"Ficha" if lang == "es" else "Fact sheet"}: {esc(fa["title"])} →</a>' if fa else ""
            return f'<li id="{esc(x["id"])}" data-s="{esc(slugify(x["es"] + " " + x["en"]))}"><b>{esc(x[lang])}</b><span class="meta"> · {esc(x["en" if lang == "es" else "es"])}</span>{fl}</li>'
        lis = "".join(ali(x) for x in ents)
        fams += (f'<section class="afam" id="{k}" data-f="{k}"><h2>{esc(p[lang])} <small style="font:500 15px var(--sans);color:var(--mute)">({len(ents)} {lab[6]})</small></h2>'
                 f'<div class="grid g2"><div class="door"><span class="tag">{lab[0]}</span><p>{esc(p["dx"][i2])}</p></div><div class="door"><span class="tag">{lab[1]}</span><p>{esc(p["tx"][i2])}</p></div>'
                 f'<div class="door"><span class="tag">{lab[2]}</span><p>{esc(p["pr"][i2])}</p></div><div class="door"><span class="tag">{lab[3]}</span><p>{esc(p["ep"][i2])}</p></div></div>'
                 f'<p style="margin:14px 0">{link}<a class="btn" href="{esc(p["source"])}" rel="noopener">{lab[5]}: NCI ↗</a></p>'
                 f'<details class="det"><summary>{"Ver las" if lang == "es" else "Show the"} {len(ents)} {lab[6]}</summary><ul class="alist">{lis}</ul></details></section>')
        chips += f'<button type="button" class="chip" data-f="{k}">{esc(p[lang])}</button>'
    ph = "Busca un subtipo (por ejemplo, «lobulillar» o «Hodgkin»)…" if lang == "es" else "Search a subtype (for example, “lobular” or “Hodgkin”)…"
    scope = ("<b>Cómo usar el atlas.</b> Cada subtipo se identifica por su nombre en la clasificación de referencia (OMS, CIE-O). El texto de cada familia es un perfil general, no una descripción de cada subtipo: el diagnóstico, el tratamiento y el pronóstico de una persona concreta dependen del informe de anatomía patológica, del estadio y de su situación. No sirve para elegir un tratamiento."
             if lang == "es" else
             "<b>How to use the atlas.</b> Each subtype is identified by its name in the reference classification (WHO, ICD-O). The text for each family is a general profile, not a description of each subtype: a person's diagnosis, treatment and outlook depend on the pathology report, the stage and their own situation. It cannot be used to choose a treatment.")
    ajs = """<script>(function(){var q=document.getElementById('aq'),c=document.querySelectorAll('.achips .chip'),f='all';function run(){var v=(q.value||'').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/[^a-z0-9]+/g,'-');document.querySelectorAll('.afam').forEach(function(s){var n=0;s.querySelectorAll('li').forEach(function(l){var ok=!v||l.getAttribute('data-s').indexOf(v)>-1;l.style.display=ok?'':'none';if(ok)n++});var show=(f==='all'||s.getAttribute('data-f')===f)&&n>0;s.style.display=show?'':'none';var d=s.querySelector('details');if(d)d.open=!!v})}function hash(){var id=decodeURIComponent(location.hash.slice(1));if(!id)return;var li=document.getElementById(id);if(!li||li.tagName!=='LI')return;var s=li.closest('.afam'),d=s.querySelector('details');d.open=true;document.querySelectorAll('.alist li.hit').forEach(function(x){x.classList.remove('hit')});li.classList.add('hit');setTimeout(function(){li.scrollIntoView({block:'center'})},60)}window.addEventListener('hashchange',hash);q.addEventListener('input',run);window.addEventListener('load',hash);c.forEach(function(b){b.addEventListener('click',function(){f=b.getAttribute('data-f');c.forEach(function(x){x.classList.toggle('on',x===b)});run()})})})();</script>"""
    path = f"{lp}atlas/"
    out = f"""<header class="phead wrap"><span class="eyebrow">Atlas</span><h1>{l['atlas_title']}</h1><p class="lead">{l['atlas_desc']}</p></header>
<div class="wrap"><div class="note">{scope}</div><form class="search" role="search" onsubmit="return false" style="margin:18px 0 12px"><input type="search" id="aq" placeholder="{ph}" aria-label="{ph}" autocomplete="off"></form><div class="tlchips achips">{chips}</div></div>
<div class="wrap section" style="padding-top:8px">{fams}<p class="meta">{"Clasificación" if lang == "es" else "Classification"}: <a href="https://tumourclassification.iarc.who.int/" rel="noopener">WHO Classification of Tumours</a> · <a href="https://seer.cancer.gov/icd-o-3/index.html" rel="noopener">SEER ICD-O-3</a> · {t['upd']}: {TODAY}</p></div>{ajs}"""
    write(path, page(lang, path, l["atlas_title"], l["atlas_desc"], out, ldtype="CollectionPage"))
    search.append({"t": l["atlas_title"], "d": l["atlas_desc"], "u": path[len(lp):], "k": "Atlas", "n": ""})
    for x in AT:
        search.append({"t": x[lang], "d": PR[x["profile"]][lang], "u": f"atlas/#{x['id']}", "k": "Atlas"})

    # ---------- portada ----------
    r = "./" if lang == "es" else "../"
    base = "./"
    secs = SECTIONS[lang]
    seccards = "".join(f'<a class="card" href="{base}{s[0]}/"><span class="num">{i:02d}</span><span class="tag">{esc(s[1])}</span><h3>{esc(s[2])}</h3><p>{esc(s[3])}</p><span class="more">{len(allsec.get(s[0], []))} {"artículos" if lang=="es" else "articles"} →</span></a>' for i, s in enumerate([s for s in secs if allsec.get(s[0])], 1))
    doors = "".join(f'<div class="door"><span class="tag">{a}</span><h3>{b}</h3><ul>' + "".join(f'<li><a href="{base}{u}">{n}</a></li>' for u, n in links) + "</ul></div>" for a, b, links in l["doors"])
    hl = data["HISTORIA"]
    pick = [hl[i] for i in data["HISTORIA_PORTADA"]]
    eras = "".join(f'<div class="era"><time>{esc(y)}</time><h3 style="color:#fff;margin:4px 0">{esc(h)}</h3><p>{re.sub("<[^>]+>", "", tx)[:150].rsplit(" ",1)[0].rstrip(".,;:")}…</p></div>' for y, h, tx, *_ in pick)
    pcards = "".join(f'<a class="card" href="{base}blog/{p["slug"]}/"><span class="tag">{l["date_fmt"](p["date"])}</span><h3>{esc(p["title"])}</h3><p>{esc(p["desc"])}</p><span class="more">{t["read"]}</span></a>' for p in posts[:3])
    n = lambda k: len(allsec.get(k, []))
    corecards = "".join(f'<a class="card big" href="{base}{s[0]}/"><span class="tag">{esc(s[1])}</span><h3>{esc(s[2])}</h3><p>{esc(s[3])}</p><span class="more">{n(s[0])} {"fichas" if lang=="es" else "entries"} →</span></a>' for s in secs[:3])
    basecards = "".join(f'<a class="card" href="{base}{s[0]}/"><span class="tag">{esc(s[1])}</span><h3>{esc(s[2])}</h3><p>{esc(s[3])}</p><span class="more">{n(s[0])} {"artículos" if lang=="es" else "articles"} →</span></a>' for s in secs[3:] if allsec.get(s[0]))
    scicards = "".join(f'<a class="card" href="{u}" rel="noopener"><span class="tag">{l["consult"]} · {esc(src)}</span><h3>{esc(h)}</h3><p>{esc(d)}</p><span class="more">{esc(src)} ↗</span></a>' for h, d, u, src in l["sci"])
    body = f"""<section class="wrap hero">
  <div>
    <span class="eyebrow">{l['eyebrow']}</span>
    <h1>{l['h1']}</h1>
    <p class="lead">{l['lead']}</p>
    <form class="search" role="search" onsubmit="return false"><input type="search" id="q" placeholder="{l['ph']}" aria-label="{l['btn']}" autocomplete="off"><button type="submit">{l['btn']}</button><div class="results" id="results" hidden></div></form>
    <div class="actions"><a class="btn primary" href="{base}{secs[0][0]}/">{l['start']}</a><a class="btn" href="{base}{secs[1][0]}/">{l['play']}</a></div>
    <p class="hnote">{l['note']}</p>
  </div>
  <figure class="arch"><img src="{r}assets/img/marie-curie.jpg" width="833" height="1100" alt="{l['photo_alt']}" decoding="async" fetchpriority="high" ><figcaption><b>{l['photo_t']}</b>{l['photo_c']}</figcaption></figure>
</section>
<div class="wrap"><div class="trust">{''.join(f'<span><b>{x}</b></span>' for x in l['trust'][:-1])}<span>{l['trust'][-1]}</span></div></div>

<section class="section wrap" id="mapa">
  <div class="shead"><div><span class="eyebrow">{l['core_e']}</span><h2>{l['core_h']}</h2></div><p>{l['core_p']}</p></div>
  <div class="grid core">{corecards}</div>
  <div class="grid g2" style="margin-top:16px">{basecards}</div>
</section>

<section class="wrap section"><div class="split2">
  <div class="dark2"><h2>{l['res_h']}</h2><p>{l['res_p']}</p><a class="btn" href="{base}{l['res_url']}">{l['res_btn']}</a></div>
  <div class="fam"><span class="eyebrow">{l['fam_e']}</span><h2>{l['fam_h']}</h2><p>{l['fam_p']}</p><a class="btn primary" href="{base}{l['fam_url']}">{l['fam_btn']}</a></div>
</div></section>

<section class="section wrap">
  <div class="shead"><div><span class="eyebrow">{l['doors_e']}</span><h2>{l['doors_h']}</h2></div></div>
  <div class="doors">{doors}</div>
</section>

<section class="darkband"><div class="wrap section">
  <div class="shead"><div><span class="eyebrow">{l['hist_e']}</span><h2 style="color:#fff">{l['hist_h']}</h2></div><a class="btn" href="{base}{l['hist']}/">{l['hist_btn']}</a></div>
  <div class="eras">{eras}</div>
</div></section>

<section class="section wrap">
  <div class="shead"><div><span class="eyebrow">{l['sci_e']}</span><h2>{l['sci_h']}</h2></div><a class="btn" href="{base}{l['fuentes']}/">{l['fuentes_btn']}</a></div>
  <p style="margin:-6px 0 16px;color:var(--mute);max-width:720px">{l['sci_p']}</p>
  <div class="grid">{scicards}</div>
</section>

<section class="section wrap">
  <div class="shead"><div><span class="eyebrow">{l['blog_e']}</span><h2>{l['blog_h']}</h2></div><a class="btn" href="{base}blog/">{l['blog_btn']}</a></div>
  <div class="grid">{pcards}</div>
</section>

<section class="wrap" style="margin-bottom:22px"><div class="door" style="background:var(--soft2);display:grid;grid-template-columns:auto 1fr auto;gap:22px;align-items:center" id="autor">
  <span class="sym" style="width:64px;height:64px;border:1.5px solid var(--accent2);border-radius:50%;display:grid;place-items:center;font:30px var(--serif);color:var(--accent2)">AR</span>
  <div><span class="tag">{l['who_t']}</span><h3 style="margin:6px 0">{l['who_h']}</h3><p style="margin:0;color:var(--mute)">{l['who_p']}</p></div>
  <a class="btn" href="{base}{g['PROJECT'][lang][0][0]}/">{l['who_btn']}</a>
</div></section>
<section class="wrap"><div class="door" style="display:flex;justify-content:space-between;gap:20px;align-items:center;flex-wrap:wrap">
  <div><span class="tag">{l['ed_t']}</span><h3>{l['ed_h']}</h3><p style="margin:0;color:var(--mute)">{l['ed_p']}</p></div>
  <a class="btn primary" href="{base}{g['PROJECT'][lang][1][0]}/">{l['ed_btn']}</a>
</div></section>"""
    title = "Oncolopedia · " + ("Comprender el cáncer, conocer las opciones" if lang == "es" else "Understand cancer, know the options")
    write(lp, page(lang, lp, title, t["desc"], body, full_title=True))

    # ---------- 404 ----------
    if lang == "es":
        out = f'<header class="phead wrap"><span class="eyebrow">404</span><h1>{l["p404"]}</h1><p class="lead">{l["p404d"]}</p><p><a class="btn primary" href="/">{l["back"]}</a> <a class="btn" href="/en/">English</a></p></header>'
        h = page(lang, "404.html", l["p404"], l["p404d"], out)
        # 404 se sirve desde cualquier ruta: rutas absolutas
        h = h.replace('href="./', 'href="/').replace('src="./', 'src="/')
        write("404.html", h)


def build_lite(lang, g, search):
    """Versión inicial en inglés: portada y páginas del proyecto; el resto enlaza a la versión en castellano."""
    T, page, write = g["T"], g["page"], g["write"]
    l = L[lang]
    t = T[lang]
    for slug, _ in g["PROJECT"][lang]:
        g["simple_page"](lang, slug, search)
    es_secs = g["SECTIONS"]["es"]
    cards = "".join(f'<a class="card" href="../{es[0]}/" hreflang="es"><span class="num">{i:02d}</span><span class="tag">{esc(en[1])}</span><h3>{esc(en[2])}</h3><p>{esc(en[3])}</p><span class="more">Read in Spanish →</span></a>' for i, (es, en) in enumerate(zip(es_secs, g["SECTIONS"][lang]), 1))
    body = f"""<section class="wrap hero">
  <div>
    <span class="eyebrow">{l['eyebrow']}</span>
    <h1>{l['h1']}</h1>
    <p class="lead">{l['lead']}</p>
    <div class="note" style="margin:18px 0 0">The English edition is on its way. All sections are already available in Spanish.</div>
    <div class="actions"><a class="btn primary" href="../" hreflang="es">Visit the Spanish edition →</a></div>
  </div>
  <figure class="arch"><img src="../assets/img/marie-curie.jpg" width="833" height="1100" alt="{l['photo_alt']}" decoding="async" fetchpriority="high" ><figcaption><b>{l['photo_t']}</b>{l['photo_c']}</figcaption></figure>
</section>
<section class="section wrap">
  <div class="shead"><div><span class="eyebrow">{l['map_e']}</span><h2>{l['map_h']}</h2></div><p>{l['map_p']}</p></div>
  <div class="grid">{cards}</div>
</section>
<section class="wrap" style="margin-bottom:22px"><div class="door" style="background:var(--soft2);display:grid;grid-template-columns:auto 1fr auto;gap:22px;align-items:center" id="autor">
  <span class="sym" style="width:64px;height:64px;border:1.5px solid var(--accent2);border-radius:50%;display:grid;place-items:center;font:30px var(--serif);color:var(--accent2)">AR</span>
  <div><span class="tag">{l['who_t']}</span><h3 style="margin:6px 0">{l['who_h']}</h3><p style="margin:0;color:var(--mute)">{l['who_p']}</p></div>
  <a class="btn" href="./about/">{l['who_btn']}</a>
</div></section>"""
    write("en/", page(lang, "en/", "Oncolopedia · DNA, clearly explained", t["desc"], body, full_title=True))
