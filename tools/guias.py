"""Guías y documentos recientes (2024-2026), comprobados uno a uno, y su asignación a las fichas de tipos de cáncer."""
import os, re, glob, sys
L = lambda url, lab: f"[{lab}]({url})"
D = lambda d: L("https://doi.org/" + d, "doi:" + d)
ESMO = "ESMO Guidelines Committee"
# clave: (cita ES, cita EN, nombre corto ES, nombre corto EN, url principal)
G = {
 "cifras": ("SEOM y REDECAN. Las cifras del cáncer en España 2026. Madrid: SEOM; 2026. " + L("https://seom.org/info-sobre-el-cancer", "seom.org"),
            "SEOM and REDECAN. Las cifras del cáncer en España 2026 (Cancer figures in Spain 2026). Madrid: SEOM; 2026. " + L("https://seom.org/info-sobre-el-cancer", "seom.org"),
            "SEOM y REDECAN · Las cifras del cáncer en España 2026", "SEOM and REDECAN · Cancer figures in Spain 2026", "https://seom.org/info-sobre-el-cancer"),
 "mama_precoz": ("Loibl S, et al. Early breast cancer: ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up. *Ann Oncol*. 2024;35:159-182. " + D("10.1016/j.annonc.2023.11.016"), None,
            "ESMO · Cáncer de mama precoz (2024)", "ESMO · Early breast cancer (2024)", "https://doi.org/10.1016/j.annonc.2023.11.016"),
 "mama_met": (f"Loi S, Harbeck N, et al., on behalf of the {ESMO}. Metastatic breast cancer: ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up. *Ann Oncol*. 2026. " + D("10.1016/j.annonc.2026.05.707"), None,
            "ESMO · Cáncer de mama metastásico (2026)", "ESMO · Metastatic breast cancer (2026)", "https://doi.org/10.1016/j.annonc.2026.05.707"),
 "ovario": ("Ledermann JA, et al. ESGO-ESMO-ESP consensus conference recommendations on ovarian cancer. *Ann Oncol*. 2024;35:248-266. " + D("10.1016/j.annonc.2023.11.015"), None,
            "ESGO-ESMO-ESP · Cáncer de ovario (2024)", "ESGO-ESMO-ESP · Ovarian cancer (2024)", "https://doi.org/10.1016/j.annonc.2023.11.015"),
 "endometrio": ("Concin N, et al. ESGO-ESTRO-ESP guidelines for the management of patients with endometrial carcinoma: update 2025. *Lancet Oncol*. 2025;26:e423-e435. " + D("10.1016/S1470-2045(25)00167-6"), None,
            "ESGO-ESTRO-ESP · Cáncer de endometrio (2025)", "ESGO-ESTRO-ESP · Endometrial carcinoma (2025)", "https://doi.org/10.1016/S1470-2045(25)00167-6"),
 "endometrio_seom": ("SEOM-GEICO clinical guidelines on endometrial cancer (2025). *Clin Transl Oncol*. 2025;27:4368-4380. " + D("10.1007/s12094-025-04046-1"), None,
            "SEOM-GEICO · Cáncer de endometrio (2025)", "SEOM-GEICO · Endometrial cancer (2025)", "https://doi.org/10.1007/s12094-025-04046-1"),
 "pulmon_precoz": (f"{ESMO}. Early and locally advanced non-small-cell lung cancer: ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up. *Ann Oncol*. 2025;36:1245-1262. " + D("10.1016/j.annonc.2025.08.003"), None,
            "ESMO · Cáncer de pulmón no microcítico precoz y localmente avanzado (2025)", "ESMO · Early and locally advanced NSCLC (2025)", "https://doi.org/10.1016/j.annonc.2025.08.003"),
 "carcinoides": ("Baudin E, et al. European Society of Neuroendocrine Tumors (ENETS) 2025 guidance paper for lung and thymic carcinoids. *J Neuroendocrinol*. 2026. " + D("10.1111/jne.70174"), None,
            "ENETS · Carcinoides de pulmón y timo (2025)", "ENETS · Lung and thymic carcinoids (2025)", "https://doi.org/10.1111/jne.70174"),
 "meso": ("Treatment of pleural mesothelioma: ASCO guideline clinical insights. *JCO Oncol Pract*. 2025. " + L("https://pubmed.ncbi.nlm.nih.gov/40053896/", "PubMed"), None,
            "ASCO · Mesotelioma pleural (2025)", "ASCO · Pleural mesothelioma (2025)", "https://pubmed.ncbi.nlm.nih.gov/40053896/"),
 "crc_met": (f"Cremolini C, et al., on behalf of the {ESMO}. Metastatic colorectal cancer: ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up. *Ann Oncol*. 2026;37:759-776. " + L("https://www.annalsofoncology.org/article/S0923-7534(26)00108-0/fulltext", "annalsofoncology.org"), None,
            "ESMO · Cáncer colorrectal metastásico (2026)", "ESMO · Metastatic colorectal cancer (2026)", "https://www.annalsofoncology.org/article/S0923-7534(26)00108-0/fulltext"),
 "gastro": (f"Al-Batran SE, et al., on behalf of the {ESMO}. Gastric and oesophageal cancer: ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up. *Ann Oncol*. 2026. " + L("https://esmo.org/guidelines/gastrointestinal-cancers/gastric-cancer", "esmo.org"), None,
            "ESMO · Cáncer gástrico y de esófago (2026)", "ESMO · Gastric and oesophageal cancer (2026)", "https://esmo.org/guidelines/gastrointestinal-cancers/gastric-cancer"),
 "esof_eu": (f"{ESMO}. ESMO Clinical Practice Guideline interim update on the management of oesophageal cancer. *ESMO Open*. 2025;10:104134. " + L("https://esmo.org/guidelines/guidelines-by-topic/esmo-clinical-practice-guidelines-gastrointestinal-cancers/clinical-practice-guideline-oesophageal-cancer/eupdate-oesophageal-cancer", "esmo.org"), None,
            "ESMO · Actualización en cáncer de esófago (2025)", "ESMO · Oesophageal cancer update (2025)", "https://esmo.org/guidelines/guidelines-by-topic/esmo-clinical-practice-guidelines-gastrointestinal-cancers/clinical-practice-guideline-oesophageal-cancer/eupdate-oesophageal-cancer"),
 "asco_ge": ("Immunotherapy and targeted therapy for advanced gastroesophageal cancer: ASCO guideline update. *J Clin Oncol*. 2026. " + L("https://pubmed.ncbi.nlm.nih.gov/41747202/", "PubMed"), None,
            "ASCO · Cáncer gastroesofágico avanzado (2026)", "ASCO · Advanced gastroesophageal cancer (2026)", "https://pubmed.ncbi.nlm.nih.gov/41747202/"),
 "pancreas_eu": (f"Conroy T, Ducreux M, on behalf of the {ESMO}. ESMO Clinical Practice Guideline express update on the management of metastatic pancreatic cancer. *ESMO Open*. 2025. " + L("https://esmo.org/guidelines/guidelines-by-topic/esmo-clinical-practice-guidelines-gastrointestinal-cancers/cancer-of-the-pancreas-esmo-clinical-practice-guidelines/eupdate-metastatic-pancreatic-cancer", "esmo.org"), None,
            "ESMO · Actualización en cáncer de páncreas metastásico (2025)", "ESMO · Metastatic pancreatic cancer update (2025)", "https://esmo.org/guidelines/guidelines-by-topic/esmo-clinical-practice-guidelines-gastrointestinal-cancers/cancer-of-the-pancreas-esmo-clinical-practice-guidelines/eupdate-metastatic-pancreatic-cancer"),
 "hcc": ("Vogel A, et al. Hepatocellular carcinoma: ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up. *Ann Oncol*. 2025;36:491-506. " + D("10.1016/j.annonc.2025.02.006"), None,
            "ESMO · Hepatocarcinoma (2025)", "ESMO · Hepatocellular carcinoma (2025)", "https://doi.org/10.1016/j.annonc.2025.02.006"),
 "biliar_eu": (f"{ESMO}. ESMO Clinical Practice Guideline interim update on the management of biliary tract cancer. *ESMO Open*. 2025;10:104003. " + L("https://esmo.org/guidelines/guidelines-by-topic/esmo-clinical-practice-guidelines-gastrointestinal-cancers/clinical-practice-guideline-biliary-tract-cancer/eupdate-biliary-tract-cancer-recommendations", "esmo.org"), None,
            "ESMO · Actualización en cáncer de vías biliares (2025)", "ESMO · Biliary tract cancer update (2025)", "https://esmo.org/guidelines/guidelines-by-topic/esmo-clinical-practice-guidelines-gastrointestinal-cancers/clinical-practice-guideline-biliary-tract-cancer/eupdate-biliary-tract-cancer-recommendations"),
 "pros_local": (f"{ESMO}. Local and locoregional prostate cancer: ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up. *Ann Oncol*. 2026. " + D("10.1016/j.annonc.2025.12.009"), None,
            "ESMO · Cáncer de próstata localizado (2026)", "ESMO · Local and locoregional prostate cancer (2026)", "https://doi.org/10.1016/j.annonc.2025.12.009"),
 "pros_avz": (f"{ESMO}. Advanced and metastatic prostate cancer: ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up. *Ann Oncol*. 2026. " + D("10.1016/j.annonc.2026.01.015"), None,
            "ESMO · Cáncer de próstata avanzado y metastásico (2026)", "ESMO · Advanced and metastatic prostate cancer (2026)", "https://doi.org/10.1016/j.annonc.2026.01.015"),
 "eau_pros": ("European Association of Urology. EAU Guidelines on Prostate Cancer, edición 2026. " + L("https://uroweb.org/guidelines/prostate-cancer/summary-of-changes/2026", "uroweb.org"),
            "European Association of Urology. EAU Guidelines on Prostate Cancer, 2026 edition. " + L("https://uroweb.org/guidelines/prostate-cancer/summary-of-changes/2026", "uroweb.org"),
            "EAU · Cáncer de próstata (2026)", "EAU · Prostate cancer (2026)", "https://uroweb.org/guidelines/prostate-cancer/summary-of-changes/2026"),
 "eau": ("European Association of Urology. EAU Guidelines, edición 2026 (tumores urológicos). " + L("https://uroweb.org/guidelines", "uroweb.org"),
            "European Association of Urology. EAU Guidelines, 2026 edition (urological cancers). " + L("https://uroweb.org/guidelines", "uroweb.org"),
            "EAU · Guías de tumores urológicos (2026)", "EAU · Urological cancer guidelines (2026)", "https://uroweb.org/guidelines"),
 "rcc": ("Powles T, et al. Renal cell carcinoma: ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up. *Ann Oncol*. 2024;35:692-706. " + D("10.1016/j.annonc.2024.05.537"), None,
            "ESMO · Carcinoma de células renales (2024)", "ESMO · Renal cell carcinoma (2024)", "https://doi.org/10.1016/j.annonc.2024.05.537"),
 "vejiga_eu": (f"{ESMO}. ESMO Clinical Practice Guideline interim update on first-line therapy in advanced urothelial carcinoma. *Ann Oncol*. 2024;35:485-490. " + D("10.1016/j.annonc.2024.03.001"), None,
            "ESMO · Actualización en carcinoma urotelial avanzado (2024)", "ESMO · Advanced urothelial carcinoma update (2024)", "https://doi.org/10.1016/j.annonc.2024.03.001"),
 "melanoma": ("Amaral T, et al. Cutaneous melanoma: ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up. *Ann Oncol*. 2025;36:10-30. " + D("10.1016/j.annonc.2024.11.006"), None,
            "ESMO · Melanoma cutáneo (2025)", "ESMO · Cutaneous melanoma (2025)", "https://doi.org/10.1016/j.annonc.2024.11.006"),
 "uveal": ("Piperno-Neumann S, et al. Uveal melanoma: ESMO-EURACAN Clinical Practice Guideline for diagnosis, treatment and follow-up. *ESMO Open*. 2026;11:106888. " + D("10.1016/j.esmoop.2026.106888"), None,
            "ESMO-EURACAN · Melanoma uveal (2026)", "ESMO-EURACAN · Uveal melanoma (2026)", "https://doi.org/10.1016/j.esmoop.2026.106888"),
 "merkel": ("Lugowska I, et al. Merkel-cell carcinoma: ESMO-EURACAN Clinical Practice Guideline for diagnosis, treatment and follow-up. *ESMO Open*. 2024. " + L("https://pubmed.ncbi.nlm.nih.gov/38796285/", "PubMed"), None,
            "ESMO-EURACAN · Carcinoma de células de Merkel (2024)", "ESMO-EURACAN · Merkel-cell carcinoma (2024)", "https://pubmed.ncbi.nlm.nih.gov/38796285/"),
 "hn": ("NCCN Guidelines Insights: Head and Neck Cancers, version 2.2025. *J Natl Compr Canc Netw*. 2025. " + L("https://pubmed.ncbi.nlm.nih.gov/39938471/", "PubMed"), None,
            "NCCN · Cánceres de cabeza y cuello (2025)", "NCCN · Head and neck cancers (2025)", "https://pubmed.ncbi.nlm.nih.gov/39938471/"),
 "ata": ("Ringel MD, Sosa JA, et al. 2025 American Thyroid Association management guidelines for adult patients with differentiated thyroid cancer. *Thyroid*. 2025;35:841-. " + D("10.1177/10507256251363120"), None,
            "ATA · Cáncer diferenciado de tiroides (2025)", "ATA · Differentiated thyroid cancer (2025)", "https://doi.org/10.1177/10507256251363120"),
 "glioma": ("EANO guideline on molecular testing of gliomas, glioneuronal, and neuronal tumors in adults: update 1. *Neuro Oncol*. 2025;27:331-337. " + L("https://pubmed.ncbi.nlm.nih.gov/39387386/", "PubMed"), None,
            "EANO · Estudio molecular de los gliomas (2025)", "EANO · Molecular testing of gliomas (2025)", "https://pubmed.ncbi.nlm.nih.gov/39387386/"),
 "pcnsl": ("Ferreri AJM, et al. Primary central nervous system lymphomas: EHA-ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up. *HemaSphere*. 2024. " + L("https://pubmed.ncbi.nlm.nih.gov/38839484/", "PubMed"), None,
            "EHA-ESMO · Linfoma primario del SNC (2024)", "EHA-ESMO · Primary CNS lymphoma (2024)", "https://pubmed.ncbi.nlm.nih.gov/38839484/"),
 "linfomas": (f"{ESMO}. Lymphomas: ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up. *Ann Oncol*. 2025;36:1263-1284. " + D("10.1016/j.annonc.2025.07.014"), None,
            "ESMO · Linfomas (2025)", "ESMO · Lymphomas (2025)", "https://doi.org/10.1016/j.annonc.2025.07.014"),
 "lbcl": ("Large B-cell lymphoma (LBCL): EHA Clinical Practice Guidelines for diagnosis, treatment, and follow-up. *HemaSphere*. 2025;9:e70207. " + D("10.1002/hem3.70207"), None,
            "EHA · Linfoma B de células grandes (2025)", "EHA · Large B-cell lymphoma (2025)", "https://doi.org/10.1002/hem3.70207"),
 "llc": ("Eichhorst B, et al. ESMO Clinical Practice Guideline interim update on new targeted therapies in the first line and at relapse of chronic lymphocytic leukaemia. *Ann Oncol*. 2024;35:762-768. " + D("10.1016/j.annonc.2024.06.016"), None,
            "ESMO · Actualización en leucemia linfocítica crónica (2024)", "ESMO · Chronic lymphocytic leukaemia update (2024)", "https://doi.org/10.1016/j.annonc.2024.06.016"),
 "lmc": ("Apperley JF, et al. 2025 European LeukemiaNet recommendations for the management of chronic myeloid leukemia. *Leukemia*. 2025;39:1797-1813. " + D("10.1038/s41375-025-02664-w"), None,
            "ELN · Leucemia mieloide crónica (2025)", "ELN · Chronic myeloid leukaemia (2025)", "https://doi.org/10.1038/s41375-025-02664-w"),
 "lma": ("Genetic risk classification for adults with AML receiving less-intensive therapies: the 2024 ELN recommendations. *Blood*. 2024. " + L("https://pubmed.ncbi.nlm.nih.gov/39133932/", "PubMed"), None,
            "ELN · Riesgo genético en la leucemia mieloide aguda (2024)", "ELN · Genetic risk in acute myeloid leukaemia (2024)", "https://pubmed.ncbi.nlm.nih.gov/39133932/"),
 "mieloma": ("Dimopoulos MA, Terpos E, et al. EHA-EMN evidence-based guidelines for diagnosis, treatment and follow-up of patients with multiple myeloma. *Nat Rev Clin Oncol*. 2025;22:680-700. " + D("10.1038/s41571-025-01041-x"), None,
            "EHA-EMN · Mieloma múltiple (2025)", "EHA-EMN · Multiple myeloma (2025)", "https://doi.org/10.1038/s41571-025-01041-x"),
 "sts_geis": ("Vaz-Salgado MA, et al. Diagnosis and therapy of soft tissue sarcomas: Spanish Group for Research in Sarcomas (GEIS) guidelines. *Cancers*. 2025;17:3158. " + L("https://www.mdpi.com/2072-6694/17/19/3158", "mdpi.com"), None,
            "GEIS · Sarcomas de partes blandas (2025)", "GEIS · Soft tissue sarcomas (2025)", "https://www.mdpi.com/2072-6694/17/19/3158"),
 "sts_seom": ("SEOM-GEIS Spanish clinical guidelines for the management of soft-tissue sarcomas (2024). *Clin Transl Oncol*. 2025;27:1460-1471. " + L("https://pubmed.ncbi.nlm.nih.gov/39918719/", "PubMed"), None,
            "SEOM-GEIS · Sarcomas de partes blandas (2024)", "SEOM-GEIS · Soft tissue sarcomas (2024)", "https://pubmed.ncbi.nlm.nih.gov/39918719/"),
 "ped": ("SIOP Europe y Childhood Cancer International Europe. European Standards of Care for Children and Adolescents with Cancer 2025. Viena; 2025. " + L("https://ccieurope.eu/wp-content/uploads/2025/09/European-Standards-of-Care-for-Children-and-Adolescents-with-Cancer-2025.pdf", "ccieurope.eu"),
            "SIOP Europe and Childhood Cancer International Europe. European Standards of Care for Children and Adolescents with Cancer 2025. Vienna; 2025. " + L("https://ccieurope.eu/wp-content/uploads/2025/09/European-Standards-of-Care-for-Children-and-Adolescents-with-Cancer-2025.pdf", "ccieurope.eu"),
            "SIOPE y CCI Europe · Estándares europeos de atención al cáncer infantil y adolescente (2025)", "SIOPE and CCI Europe · European Standards of Care for Children and Adolescents with Cancer (2025)", "https://ccieurope.eu/wp-content/uploads/2025/09/European-Standards-of-Care-for-Children-and-Adolescents-with-Cancer-2025.pdf"),
 "hgg_ped": ("SIOPE HGG Working Group. European standard clinical practice recommendations for paediatric high-grade gliomas. *EJC Paediatric Oncology*. 2025. " + L("https://doaj.org/article/7dde28fa49ac4e54b05f8ed0ca5953c6", "doaj.org"), None,
            "SIOPE · Gliomas de alto grado pediátricos (2025)", "SIOPE · Paediatric high-grade gliomas (2025)", "https://doaj.org/article/7dde28fa49ac4e54b05f8ed0ca5953c6"),
}
M = {1: "mama_precoz mama_met", 2: "mama_precoz", 3: "mama_precoz mama_met", 4: "mama_precoz mama_met", 5: "mama_precoz mama_met", 6: "mama_precoz mama_met",
     7: "ovario", 10: "endometrio endometrio_seom", 15: "pulmon_precoz", 17: "carcinoides", 18: "meso", 20: "gastro esof_eu asco_ge", 21: "crc_met", 22: "crc_met",
     28: "pancreas_eu", 30: "hcc", 31: "biliar_eu", 32: "biliar_eu", 33: "pros_local pros_avz eau_pros", 34: "rcc vejiga_eu eau", 35: "rcc eau", 36: "eau", 37: "eau", 38: "eau",
     41: "melanoma", 44: "merkel", 47: "hn", 48: "hn", 49: "hn", 50: "hn", 51: "hn", 52: "hn", 53: "hn", 54: "ata", 57: "uveal", 58: "ped",
     59: "glioma", 60: "glioma", 61: "glioma", 64: "pcnsl linfomas", 66: "ped", 67: "ped", 68: "llc lmc lma", 70: "lma", 72: "llc", 73: "lmc",
     77: "linfomas", 78: "linfomas", 79: "linfomas lbcl", 80: "linfomas", 81: "linfomas", 82: "linfomas", 84: "linfomas", 85: "mieloma",
     87: "sts_geis sts_seom", 88: "sts_geis sts_seom", 89: "sts_geis sts_seom", 93: "ped", 94: "sts_geis sts_seom", 95: "ped hgg_ped", 96: "ped", 97: "ped", 98: "ped",
     101: "gastro asco_ge", 102: "gastro esof_eu asco_ge", 103: "vejiga_eu eau", 104: "rcc eau"}
HEAD = {"es": "**Guías y documentos recientes (2024-2026)**", "en": "**Recent guidelines and documents (2024-2026)**"}
FOOT = {"es": "*Fuentes revisadas y actualizadas en noviembre de 2026.*", "en": "*Sources reviewed and updated in November 2026.*"}
if __name__ == "__main__":
    n = 0
    for lang, d in (("es", "src/es/tipos-de-cancer"), ("en", "src/en/cancer-types")):
        for f in sorted(glob.glob(d + "/*.md")):
            num = int(os.path.basename(f).split("-")[0])
            t = open(f, encoding="utf8").read()
            if HEAD[lang] in t:
                t = t[:t.index("\n\n" + HEAD[lang])] + "\n"
            ids = lambda c: set(re.findall(r"10\.\d{4,}/[^\s)\]]+|https?://[^\s)\]]+", c))
            keys = [k for k in ["cifras"] + M.get(num, "").split() if not (ids(G[k][0]) & ids(t))]
            nums = [int(x) for x in re.findall(r"^(\d+)\. ", t.split("## Fuentes" if lang == "es" else "## Sources")[-1], re.M)]
            k = max(nums) if nums else 0
            lines = []
            for key in keys:
                es, en, *_ = G[key]
                k += 1; lines.append(f"{k}. {es if lang == 'es' or not en else en}")
            t = t.rstrip("\n") + "\n\n" + HEAD[lang] + "\n\n" + "\n".join(lines) + "\n\n" + FOOT[lang] + "\n"
            t = re.sub(r"^updated: .*$", "updated: 2026-11-27", t, count=1, flags=re.M)
            open(f, "w", encoding="utf8").write(t); n += 1
    print(n, "fichas actualizadas")
