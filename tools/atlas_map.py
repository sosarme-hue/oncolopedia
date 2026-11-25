# entidad del atlas (nombre en español, minúsculas) -> número de ficha
import re
RULES = [
 (r'implante mamario', '84'), (r'rabdoide', '95'), (r'brenner', '7'), (r'astrocitoma de alto grado', '59'),
 (r'lobulillar', '5'), (r'mamari|filodes|tipo no especial', '1'),
 (r'microcítico pulmonar|neuroendocrino de células grandes pulmonar', '16'), (r'mesotelioma', '18'), (r'pulmon|nut torácico', '15'),
 (r'orofaringe', '50'), (r'nasofar', '51'), (r'laringe|hipofaringe', '49'), (r'lengua oral|suelo de boca|encía|yugal|labio', '48'),
 (r'sinonasal|olfatorio', '53'), (r'salival|ex adenoma pleomorfo', '52'),
 (r'esofágic', '102'), (r'gástric', '101'), (r'duodenal|yeyunal|ileal', '24'), (r'anal', '23'), (r'colorrectal', '21'), (r'ampular', '28'),
 (r'hepatoblastoma', '98'), (r'hepatocelular', '30'), (r'colangiocarcinoma', '31'), (r'vesícula biliar', '32'),
 (r'neuroendocrino pancreático', '29'), (r'pancreático|pancreatoblastoma', '28'),
 (r'tumor de wilms', '97'), (r'renal de células claras', '35'), (r'pelvis renal|uréter', '36'), (r'renal|riñón|colectores', '104'),
 (r'vejiga|vesical|uracal|uretra', '103'), (r'prostátic', '33'), (r'pene', '38'), (r'testicular', '37'),
 (r'granulosa|disgerminoma|saco vitelino ovárico|teratoma inmaduro ovárico', '8'), (r'ovárico', '7'),
 (r'leiomiosarcoma uterino|estroma endometrial|adenosarcoma uterino', '11'), (r'endometri|carcinosarcoma uterino', '10'),
 (r'cervical', '9'), (r'vulvar', '12'), (r'vaginal', '13'), (r'trofoblástico|coriocarcinoma gestacional', '14'),
 (r'medular de tiroides', '55'), (r'anaplásico de tiroides', '56'), (r'tiroid|tiroides', '54'), (r'adrenocortical', '39'),
 (r'basocelular', '42'), (r'escamoso cutáneo', '43'), (r'merkel', '44'), (r'kaposi', '45'), (r'micosis fungoide|sézary', '46'), (r'^melanoma (de extensión|nodular|lentiginoso|sobre|desmoplásico)', '41'),
 (r'coroideo|cuerpo ciliar|iris|conjuntival', '57'), (r'retinoblastoma', '58'),
 (r'glioblastoma', '60'), (r'astrocitoma, idh|oligodendroglioma', '61'), (r'ependimoma', '67'), (r'meduloblastoma', '66'), (r'glioma|teratoide|rosetas|pineoblastoma|plexo coroideo', '59'),
 (r'osteosarcoma', '90'), (r'ewing', '91'), (r'condrosarcoma', '92'), (r'rabdomiosarcoma', '93'), (r'angiosarcoma', '94'), (r'liposarcoma', '88'), (r'leiomiosarcoma', '89'),
 (r'cordoma|sarcoma|fibrosarcoma|vaina del nervio|mixofibrosarcoma|desmoplásico de células', '87'),
 (r'pml::rara', '71'), (r'leucemia mieloide aguda', '70'), (r'leucemia mieloide crónica', '73'), (r'leucemia linfoblástica', '69'), (r'leucemia linfocítica crónica', '72'), (r'células pilosas', '74'),
 (r'leucemia', '68'),
 (r'hodgkin', '78'), (r'folicular$', '80'), (r'células del manto', '81'), (r'difuso de células b grandes|mediastínico', '79'), (r'burkitt', '83'), (r'zona marginal', '82'), (r'linfoplasmocítico', '86'),
 (r'linfoma t|nk/t|leucemia/linfoma t', '84'), (r'mieloma|plasmocitoma', '85'), (r'linfoma', '77'),
 (r'neuroblastoma', '96'), (r'rabdoide', '95'),
]
def match(name):
    n = name.lower()
    for rx, num in RULES:
        if re.search(rx, n):
            return num
    return None
