import json,sys,re,os
sys.path.insert(0,'tools');import tipos100 as t
S=json.load(open('tools/elegidas.json'))
OV={
"cancer-de-apendice-y-pseudomixoma":("TC de abdomen de un pseudomixoma peritoneal","Abdominal CT of pseudomyxoma peritonei"),
"cancer-de-laringe":("Tumor de laringe visto por laringoscopia","Laryngeal tumour seen on laryngoscopy"),
"melanoma-uveal":("Melanoma del iris, una forma de melanoma uveal","Iris melanoma, a form of uveal melanoma"),
"retinoblastoma":("Retinoblastoma","Retinoblastoma"),
"tumores-cerebrales":("Resonancia magnética de un tumor cerebral","MRI of a brain tumour"),
"metastasis-cerebrales":("Resonancia magnética cerebral con metástasis","Brain MRI showing metastases"),
"cancer-infantil":("Niños recibiendo quimioterapia en un hospital","Children receiving chemotherapy in hospital"),
"metastasis-oseas":("Cabeza de fémur con una metástasis ósea (pieza quirúrgica)","Femoral head with a bone metastasis (surgical specimen)"),
"cancer-de-intestino-delgado":("Adenocarcinoma de intestino delgado (pieza quirúrgica)","Small intestine adenocarcinoma (surgical specimen)"),
"cancer-de-mama-en-el-hombre":("Cáncer de mama en el hombre: tinción de receptores hormonales","Male breast cancer: hormone receptor staining"),
"cancer-de-mama-her2-positivo":("Tinción de HER2 positiva en un cáncer de mama","Positive HER2 staining in breast cancer"),
"tricoleucemia":("Tricoleucemia al microscopio","Hairy cell leukaemia under the microscope"),
"cancer-de-vejiga-y-rinon":("Carcinoma urotelial de vejiga al microscopio","Urothelial bladder carcinoma under the microscope"),
"melanoma-y-cancer-de-piel":("Melanoma al microscopio","Melanoma under the microscope"),
"cancer-de-estomago-y-esofago":("Adenocarcinoma gástrico al microscopio","Gastric adenocarcinoma under the microscope"),
"leucemias":("Frotis de sangre en una leucemia aguda","Blood smear in acute leukaemia"),
"tumores-de-hipofisis":("Adenoma de hipófisis no funcionante al microscopio","Non-functioning pituitary adenoma under the microscope"),
}
def kind(ti):
    x=ti.lower()
    if re.search(r'immuno|ihc|gfap|stain|cd3|ki-67',x) and 'he stain' not in x: return 'ihc'
    if re.search(r'smear|cytolog|leukemia|leukaemia|neutrophil',x): return 'smear'
    return 'micro'
W={'micro':("{} al microscopio","{} under the microscope"),'ihc':("{}: tinción especial al microscopio","{}: special staining under the microscope"),'smear':("{}: frotis de sangre al microscopio","{}: blood smear under the microscope")}
IMG={}
for p in t.plan():
    s=p['slug']
    if s not in S: continue
    c=S[s]; fn=f"t-{s}.jpg"
    es,en=OV.get(s) or (W[kind(c['title'])][0].format(p['t']),W[kind(c['title'])][1].format(p['t_en']))
    IMG[fn]={"artist":c['artist'],"license":c['lic'],"license_url":c['lic_url'],"page":c['page'],"source":"Wikimedia Commons","w":c['w'],"h":c['h']}
    for d,slug,cap in (('src/es/tipos-de-cancer',s,es),('src/en/cancer-types',p['en'],en)):
        fp=f"{d}/{p['n']:03d}-{slug}.md"; txt=open(fp).read()
        fm,body=txt[4:].split('\n---\n',1)
        fm='\n'.join(l for l in fm.split('\n') if not l.startswith(('img:','img_alt:','img_pie:')))
        fm+=f"\nimg: {fn}\nimg_alt: {cap}\nimg_pie: {cap}."
        open(fp,'w').write('---\n'+fm+'\n---\n'+body)
json.dump(IMG,open('src/imagenes.json','w'),ensure_ascii=False,indent=1)
print(len(IMG))
