import json,sys,os,time,urllib.request
S=json.load(open('tools/elegidas.json'))
UA={"User-Agent":"Mozilla/5.0 (compatible; OncolopediaBot/1.0; +https://oncolopedia.com)"}
D=sys.argv[1]
for s,c in S.items():
    out=os.path.join(D,f"t-{s}.img")
    if os.path.exists(out) and os.path.getsize(out)>1000: continue
    u=c['thumb'].replace('thumb.wikimedia.org','upload.wikimedia.org').split('?')[0]
    for i in range(4):
        try:
            b=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read(); open(out,'wb').write(b); break
        except Exception as e: print(s,e,flush=True); time.sleep(5*(i+1))
    time.sleep(0.5)
print('ok')
