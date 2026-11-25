import json,sys,re,os,time,urllib.request
sys.path.insert(0,'tools');import tipos100 as t
C=json.load(open('tools/candidatas.json'))
CH={"cancer-de-mama":("",2),"cancer-de-mama-triple-negativo":("#r",0),"cancer-de-vulva":None,"cancer-de-vagina":None,"cancer-de-recto":("#r",0),
"timoma-y-carcinoma-timico":("#r",0),"tumores-neuroendocrinos-de-pancreas":None,"cancer-de-higado":("#r",1),"cancer-de-vejiga-y-rinon":("#r",0),
"leucemias":("#r",0),"leucemia-linfocitica-cronica":("#r",1),"leucemia-mieloide-cronica":("#r",0),"linfoma-difuso-de-celulas-b-grandes":("#r",0),
"macroglobulinemia-de-waldenstrom":None,"condrosarcoma":("#r",2),"gliomas-de-bajo-grado":("#r",0),"cancer-de-orofaringe":("cancer-de-cabeza-y-cuello",2),
"cancer-de-origen-desconocido":("",1),"metastasis-oseas":("",3),"cancer-infantil":("",1),"linfomas-cutaneos":("",1),"melanoma-y-cancer-de-piel":("",5),
"tumores-de-hipofisis":("",2),"linfomas-de-la-zona-marginal":("",5),"linfomas":("",1),"cancer-de-pulmon":("",1)}
sel={}
for p in t.plan():
    s=p['slug']; ch=CH.get(s,("",0))
    if ch is None: continue
    k,i=ch; key=s+k if k in("","#r") else k
    L=C.get(key) or []
    if len(L)>i: sel[s]=L[i]
for s,c in sel.items(): print(s,'|',c['title'][5:90],'|',c['lic'],c['w'],c['h'])
json.dump(sel,open('tools/elegidas.json','w'),ensure_ascii=False,indent=1)
print(len(sel))
