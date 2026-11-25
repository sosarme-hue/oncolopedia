import sys,os,json
from PIL import Image
D=sys.argv[1]; IMG=json.load(open('src/imagenes.json')); n=0
for f in sorted(os.listdir(D)):
    if not f.endswith('.img'): continue
    out=f"assets/img/{f[:-4]}.jpg"
    if os.path.exists(out): continue
    im=Image.open(os.path.join(D,f))
    if im.mode in('RGBA','LA','P'):
        im=im.convert('RGBA'); bg=Image.new('RGB',im.size,(255,255,255)); bg.paste(im,mask=im.split()[-1]); im=bg
    else: im=im.convert('RGB')
    if im.width>960: im=im.resize((960,round(im.height*960/im.width)),Image.LANCZOS)
    im.save(out,'JPEG',quality=82,optimize=True,progressive=True); n+=1
    k=f[:-4]+'.jpg'
    if k in IMG: IMG[k]['w'],IMG[k]['h']=im.width,im.height
json.dump(IMG,open('src/imagenes.json','w'),ensure_ascii=False,indent=1)
print(n,'convertidas')
