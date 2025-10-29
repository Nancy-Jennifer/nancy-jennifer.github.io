# France 2024 — QoS Voix vs Standards Internationaux (ARCEP – ITU – WB)

**Objectif**  
Positionner la qualité de service Voix en France (2024) face aux benchmarks internationaux (ITU, World Bank), identifier les écarts structurants (notamment en transport) et prioriser les actions réseau à impact expérience client.

**Datasets (répertoire `data/`)**
- ARCEP 2024 (voix habitat / transport)
- ITU — indicateurs clés, mobile broadband
- World Bank — cellular, WDI

**Méthode**
- Ingestion/clean Python ; **EDA** et visualisations **R** (R Markdown/Quarto).
- Normalisation des KPI Voix en **score 0–100**.
- Comparaisons opérateurs × environnement (habitat vs transport).

**Livrables**
- `EDA_version-definitive_Projet-ARCEP_Internationa_FIXED11_MERGE.Rmd` (knit → HTML)
- Section Résultats (recruteur-ready) + Annexe technique courte (Q/C)

**Insights clés**
- Habitat solide, **mobilité fragile** : chute de performance en transport.
- Priorité réseau : **TGV / RER / Métros** + poches rurales.
- Suivi KPI ciblé et mesure **avant/après** (NPS mobilité, réclamations).

**Repro**
1. Placer les CSV dans `data/` (voir noms dans le Rmd).
2. Ouvrir le `.Rmd` et **Knit**.
3. Si besoin, exécuter l’EDA (Section 3) avant de knitter.

**Auteur** : Nancy — Data Analyst Technique (Télécoms & People Analytics)  
_Portfolio_ : (ajouter le lien GitHub Pages)
