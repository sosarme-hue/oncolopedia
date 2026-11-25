import os,re,sys,urllib.parse
root=sys.argv[1]; bad={}
for d,_,fs in os.walk(root):
  for f in fs:
    if not f.endswith('.html'): continue
    p=os.path.join(d,f); s=open(p,encoding='utf8').read()
    for h in re.findall(r'(?:href|src)="([^"#?]+)',s):
      if h.startswith(('http','mailto:','data:','//','tel:')): continue
      t=os.path.normpath(os.path.join(root,h.lstrip('/')) if h.startswith('/') else os.path.join(d,h))
      t=urllib.parse.unquote(t)
      if os.path.isdir(t): t=os.path.join(t,'index.html')
      if not os.path.exists(t): bad.setdefault(h,[]).append(os.path.relpath(p,root))
for h,ps in sorted(bad.items()): print(h, len(ps), ps[:2])
print(len(bad),'rotos')
