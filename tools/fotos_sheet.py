"""Hojas de contacto: descarga miniaturas de candidatas y monta una imagen por grupo de páginas."""
import json, os, sys, time, urllib.request, io
from PIL import Image, ImageDraw
UA = {"User-Agent": "OncolopediaBot/1.0 (https://oncolopedia.com/quien-esta-detras/)"}
C = json.load(open('tools/fotos_cand.json'))
D = sys.argv[1]; os.makedirs(D, exist_ok=True)
keys = [k for k in C if C[k]]
if len(sys.argv) > 2: keys = [k for k in keys if k in sys.argv[2].split(',')]
TW, TH = 260, 190
def thumb(u):
    for i in range(3):
        try:
            u = u.replace('thumb.wikimedia.org', 'upload.wikimedia.org').split("?")[0].replace("/500px-", "/330px-")
            return Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20).read())).convert('RGB')
        except Exception:
            time.sleep(8)
for g in range(0, len(keys), 8):
    if os.path.exists(f'{D}/hoja{g // 8:02d}.jpg'): continue
    ks = keys[g:g + 8]
    sheet = Image.new('RGB', (TW * 6 + 10, (TH + 22) * len(ks)), 'white'); dr = ImageDraw.Draw(sheet)
    for r, k in enumerate(ks):
        y = r * (TH + 22)
        dr.text((4, y + 4), k, fill='red')
        for i, c in enumerate(C[k][:6]):
            im = thumb(c['thumb'])
            if im is None: continue
            im.thumbnail((TW - 6, TH - 4))
            sheet.paste(im, (i * TW + 4, y + 20))
            dr.text((i * TW + 6, y + 22), str(i), fill='yellow')
    sheet.save(f'{D}/hoja{g // 8:02d}.jpg', quality=80)
    print('hoja', g // 8, flush=True)
