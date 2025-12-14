# people-analytics/attrition/export_figures_eda.py
from __future__ import annotations

import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# =========================
# CONFIG
# =========================
REPO_ROOT = Path(__file__).resolve().parents[2]  # remonte à la racine du repo
DATA_PATH = REPO_ROOT / "people-analytics" / "data" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"

# On réutilise ton dossier d'images déjà référencé dans eda_resultats.qmd
OUTPUT_DIR = REPO_ROOT / "assets" / "images" / "people-analytics" / "attrition_hr"

# Noms de fichiers attendus par eda_resultats.qmd (on garde les mêmes)
OUT_H1 = OUTPUT_DIR / "H1_satisfaction_taux_depart.png"
OUT_H2 = OUTPUT_DIR / "H2_anciennete_taux_depart.png"
OUT_H3 = OUTPUT_DIR / "H3_distance_taux_depart.png"
OUT_H4 = OUTPUT_DIR / "H4_heures_supp_taux_depart.png"
OUT_H5 = OUTPUT_DIR / "H5_heures_supp_anciennete.png"
OUT_H6 = OUTPUT_DIR / "H6_postes_taux_depart.png"

# Mapping FR minimal (ceux utiles à l'EDA)
RENAME_FR = {
    "Attrition": "Départ",
    "JobSatisfaction": "Satisfaction au travail",
    "YearsAtCompany": "Ancienneté dans l’entreprise",
    "DistanceFromHome": "Distance domicile-travail",
    "OverTime": "Heures supplémentaires",
    "JobRole": "Poste",
}

YES_NO_FR = {"Yes": "Oui", "No": "Non"}


# =========================
# UTILS
# =========================
def ensure_outdir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"CSV introuvable: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

    # Renommage FR (seulement colonnes utiles)
    df = df.rename(columns=RENAME_FR)

    # Harmonisation Oui/Non (pour les variables catégorielles concernées)
    if "Départ" in df.columns:
        df["Départ"] = df["Départ"].map(YES_NO_FR).fillna(df["Départ"])
    if "Heures supplémentaires" in df.columns:
        df["Heures supplémentaires"] = df["Heures supplémentaires"].map(YES_NO_FR).fillna(df["Heures supplémentaires"])

    return df


def savefig(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def tenure_bucket(years: float) -> str:
    # Buckets alignés avec ce que tu montres dans technique.qmd (0-3, 4-6, 7-10, 10+)
    if pd.isna(years):
        return "Inconnu"
    if years <= 3:
        return "0-3 ans"
    if years <= 6:
        return "4-6 ans"
    if years <= 10:
        return "7-10 ans"
    return "10+ ans"


# =========================
# FIGURES (style = proche de technique.qmd : proportions empilées, boxplot, etc.)
# =========================
def fig_h1(df: pd.DataFrame) -> None:
    # Proportions empilées Départ (Oui/Non) par niveau de satisfaction
    col_x = "Satisfaction au travail"
    col_y = "Départ"

    tab = pd.crosstab(df[col_x], df[col_y], normalize="index").sort_index()
    # Assure ordre colonnes
    for c in ["Non", "Oui"]:
        if c not in tab.columns:
            tab[c] = 0.0
    tab = tab[["Non", "Oui"]]

    ax = tab.plot(kind="bar", stacked=True)
    ax.set_title("Répartition des départs selon la satisfaction au travail")
    ax.set_xlabel("Satisfaction au travail (1 = très faible, 4 = très élevée)")
    ax.set_ylabel("Proportion d'employés")
    ax.legend(title="Départ")
    savefig(OUT_H1)


def fig_h2(df: pd.DataFrame) -> None:
    # Boxplot Ancienneté selon Départ (proche de technique.qmd)
    x = "Départ"
    y = "Ancienneté dans l’entreprise"

    data_oui = df.loc[df[x] == "Oui", y].dropna().values
    data_non = df.loc[df[x] == "Non", y].dropna().values

    plt.figure()
    plt.boxplot([data_oui, data_non], labels=["Oui", "Non"], showfliers=True)
    plt.title("Ancienneté dans l'entreprise selon le statut de départ")
    plt.xlabel("Départ de l'entreprise")
    plt.ylabel("Ancienneté dans l'entreprise (en années)")
    savefig(OUT_H2)


def fig_h3(df: pd.DataFrame) -> None:
    # Histogrammes superposés Distance selon Départ (proche de technique.qmd)
    x = "Distance domicile-travail"
    y = "Départ"

    d_non = df.loc[df[y] == "Non", x].dropna().values
    d_oui = df.loc[df[y] == "Oui", x].dropna().values

    plt.figure()
    plt.hist(d_non, bins=20, alpha=0.6, label="Non")
    plt.hist(d_oui, bins=20, alpha=0.6, label="Oui")
    plt.title("Distribution de la distance domicile-travail selon le départ")
    plt.xlabel("Distance domicile-travail")
    plt.ylabel("Nombre d'employés")
    plt.legend(title="Départ")
    savefig(OUT_H3)


def fig_h4(df: pd.DataFrame) -> None:
    # Proportions empilées Départ selon Heures supplémentaires
    col_x = "Heures supplémentaires"
    col_y = "Départ"

    tab = pd.crosstab(df[col_x], df[col_y], normalize="index")
    for c in ["Non", "Oui"]:
        if c not in tab.columns:
            tab[c] = 0.0
    tab = tab[["Non", "Oui"]]

    ax = tab.plot(kind="bar", stacked=True)
    ax.set_title("Répartition des départs selon les heures supplémentaires")
    ax.set_xlabel("Heures supplémentaires")
    ax.set_ylabel("Proportion d'employés")
    ax.legend(title="Départ")
    savefig(OUT_H4)


def fig_h5(df: pd.DataFrame) -> None:
    # Proportions empilées Heures sup selon tranche d'ancienneté
    x_years = "Ancienneté dans l’entreprise"
    x_ot = "Heures supplémentaires"

    tmp = df[[x_years, x_ot]].copy()
    tmp["Tranche ancienneté"] = tmp[x_years].apply(tenure_bucket)

    tab = pd.crosstab(tmp["Tranche ancienneté"], tmp[x_ot], normalize="index")
    for c in ["Non", "Oui"]:
        if c not in tab.columns:
            tab[c] = 0.0
    tab = tab[["Non", "Oui"]]

    # Ordre des tranches
    order = ["0-3 ans", "4-6 ans", "7-10 ans", "10+ ans"]
    tab = tab.reindex(order)

    ax = tab.plot(kind="bar", stacked=True)
    ax.set_title("Répartition des heures supplémentaires par tranche d'ancienneté")
    ax.set_xlabel("Tranche d'ancienneté")
    ax.set_ylabel("Proportion d'employés (%)")
    ax.legend(title="Heures supplémentaires")
    savefig(OUT_H5)


def fig_h6(df: pd.DataFrame) -> None:
    # Proportions empilées Départ par poste (top 10 postes par effectif)
    x = "Poste"
    y = "Départ"

    # garde top 10 postes
    top = df[x].value_counts().head(10).index
    d = df[df[x].isin(top)].copy()

    tab = pd.crosstab(d[x], d[y], normalize="index")
    for c in ["Non", "Oui"]:
        if c not in tab.columns:
            tab[c] = 0.0
    tab = tab[["Non", "Oui"]]

    ax = tab.plot(kind="bar", stacked=True, figsize=(8, 4))
    ax.set_title("Taux de départ par poste (barres empilées)")
    ax.set_xlabel("Poste")
    ax.set_ylabel("Proportion d'employés")
    ax.legend(title="Départ")
    plt.xticks(rotation=35, ha="right")
    savefig(OUT_H6)


def main() -> None:
    ensure_outdir()
    df = load_data()

    required = [
        "Départ",
        "Satisfaction au travail",
        "Ancienneté dans l’entreprise",
        "Distance domicile-travail",
        "Heures supplémentaires",
        "Poste",
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes après renommage: {missing}")

    fig_h1(df)
    fig_h2(df)
    fig_h3(df)
    fig_h4(df)
    fig_h5(df)
    fig_h6(df)

    print("✅ Figures EDA (FR) générées dans:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
