"""Descarga las fotos elegidas (tools/fotos_pick.json) a assets/img y registra créditos en src/imagenes.json."""
import json, os, re, time, io, urllib.request
from PIL import Image
UA = {"User-Agent": "OncolopediaBot/1.0 (https://oncolopedia.com/quien-esta-detras/)"}
C = json.load(open('tools/fotos_cand.json')); P = json.load(open('tools/fotos_pick.json'))
IMG = json.load(open('src/imagenes.json'))
PEOPLE = {"theodor-boveri", "richard-doll", "peyton-rous", "judah-folkman", "mary-claire-king", "dennis-slamon"}
for k, sel in P.items():
    ck, i = (sel.split('@') if isinstance(sel, str) else (k, sel))
    c = C[ck][int(i)]
    fn = ("p-" if k in PEOPLE else ("t-" if k.startswith(("cancer-de", "tumores-", "macroglob")) else "a-")) + k + ".jpg"
    out = "assets/img/" + fn
    if os.path.exists(out): continue
    t = c['thumb'].replace('thumb.wikimedia.org', 'upload.wikimedia.org').split('?')[0]
    m = re.match(r'(.*)/thumb/(.*)/[0-9]+px-[^/]+$', t)
    url = (m.group(1) + '/thumb/' + m.group(2) + '/500px-' + m.group(2).split('/')[-1]) if (m and c['w'] > 500) else (m.group(1) + '/' + m.group(2) if m else t)
    b = None
    for n in range(6):
        try:
            b = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read(); break
        except Exception as e:
            print(k, e, flush=True); time.sleep(10 * (n + 1))
    if not b: continue
    from PIL import ImageOps
    im = ImageOps.exif_transpose(Image.open(io.BytesIO(b)))
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[-1]); im = bg
    else: im = im.convert('RGB')
    if im.width > 960: im = im.resize((960, round(im.height * 960 / im.width)), Image.LANCZOS)
    im.save(out, 'JPEG', quality=82, optimize=True, progressive=True)
    IMG[fn] = {"artist": c["artist"] or "Unknown author", "license": c['lic'], "license_url": c['lic_url'], "page": c['page'], "source": "Wikimedia Commons", "w": im.width, "h": im.height, "url": url}
    json.dump(IMG, open('src/imagenes.json', 'w'), ensure_ascii=False, indent=1)
    print('ok', fn, flush=True); time.sleep(2)
