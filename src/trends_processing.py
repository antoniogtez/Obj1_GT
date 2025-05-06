# src/trends_processing.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config.keywords_mapping import COMMON_KEYWORDS


# --- 🔧 Funciones auxiliares de limpieza y carga --- #

def rename_value_column(df):
    """
    Renombra la columna de valor a 'value' si viene con otro nombre.
    También convierte 'time [UTC]' a 'date'.
    """
    if "time [UTC]" in df.columns:
        df = df.rename(columns={"time [UTC]": "date"})

    for c in df.columns:
        if c not in ["date", "keywords", "keyword", "country", "muestra_n", "timestamp", "value"]:
            df = df.rename(columns={c: "value"})
            break

    return df


def load_trend_data(base_folder, country, keyword, control_term="wikipedia"):
    """
    Carga los tres archivos CSV requeridos para una keyword:
    - keyword sola
    - keyword + control
    - control solo
    """
    def build_path(kw):
        filename = f"x_{country}_{kw.replace(' ', '_')}.csv"
        return os.path.join(base_folder, filename)

    df_x = rename_value_column(pd.read_csv(build_path(keyword)))
    df_comb = rename_value_column(pd.read_csv(build_path(f"{keyword} + {control_term}")))
    df_ctrl = rename_value_column(pd.read_csv(build_path(control_term)))

    return df_x, df_comb, df_ctrl


# --- 🔄 Imputación de muestras por regresión --- #

def get_common_samples(df_x, df_comb, df_ctrl):
    """
    Devuelve una lista ordenada de muestras que existen en los tres datasets.
    """
    samples_x = set(df_x["muestra_n"])
    samples_comb = set(df_comb["muestra_n"])
    samples_ctrl = set(df_ctrl["muestra_n"])
    return sorted(samples_x & samples_comb & samples_ctrl)


def clean_sample(df, sample_n, value_col="value"):
    """
    Filtra una muestra eliminando los valores extremos (0 y 100).
    """
    df_ = df[df["muestra_n"] == sample_n].copy()
    df_ = df_[~df_[value_col].isin([0, 100])]
    return df_


def imputar_muestra(df_x, df_comb, df_ctrl, sample_n):
    """
    Aplica regresión lineal para imputar la serie original a partir de:
    - keyword + control
    - control solo
    """
    dx = clean_sample(df_x, sample_n)
    dcomb = clean_sample(df_comb, sample_n)
    dctrl = clean_sample(df_ctrl, sample_n)

    # Solo rellenamos NaNs con 0 en la keyword (x), no en control ni combinada
    dx["value"] = dx["value"].fillna(0)

    df = dx[["date", "value"]].rename(columns={"value": "x"}).copy()
    df = df.merge(dcomb[["date", "value"]].rename(columns={"value": "combined"}), on="date", how="inner")
    df = df.merge(dctrl[["date", "value"]].rename(columns={"value": "control"}), on="date", how="inner")


    if len(df) < 3:
        return None  # Muy pocos puntos para modelar

    X = df[["combined", "control"]]
    y = df["x"]
    model = LinearRegression().fit(X, y)
    df["imputed"] = model.predict(X)

    return df[["date", "imputed"]]

# --- 📈 Serie imputada y normalizada por keyword --- #

def construir_serie_normalizada_con_imputaciones(base_folder, country, keyword, control_term="wikipedia"):
    """
    Construye una serie mensual normalizada (z-score) para una keyword específica.
    Combina muestras imputadas y las promedia.
    """
    try:
        df_x, df_comb, df_ctrl = load_trend_data(base_folder, country, keyword, control_term)
        muestras_validas = get_common_samples(df_x, df_comb, df_ctrl)
    except Exception as e:
        print(f"❌ Error cargando datos para {keyword} ({country}): {e}")
        return None

    imputaciones = []
    for m in muestras_validas:
        df_imp = imputar_muestra(df_x, df_comb, df_ctrl, m)
        if df_imp is not None:
            df_imp["sample_n"] = m
            imputaciones.append(df_imp)

    if not imputaciones:
        return None  # No hay datos suficientes

    df_all = pd.concat(imputaciones, ignore_index=True)
    df_all["date"] = pd.to_datetime(df_all["date"], errors="coerce")

    df_wide = df_all.pivot_table(index="date", columns="sample_n", values="imputed", aggfunc="mean")
    df_wide["mean_imputed"] = df_wide.mean(axis=1   )

    # 🔧 NUEVO: asegurar fechas completas
    fechas_completas = pd.date_range("2018-01-01", "2025-01-01", freq="MS")
    serie = df_wide["mean_imputed"].reindex(fechas_completas).fillna(0)

    z = (serie - serie.mean()) / serie.std()

    keyword_common = COMMON_KEYWORDS.get(keyword.lower(), keyword.lower())

    df_z = pd.DataFrame({
    "date": serie.index,
    "keyword": keyword,
    "keyword_common": keyword_common,
    "country": country,
    "imputed": serie.values,
    "zscore": z.values
    }).reset_index(drop=True)


    return df_z


# --- 🌍 Panel completo de todos los países y keywords --- #

def construir_panel_global(base_folder, country_keywords, control_term="wikipedia"):
    """
    Itera sobre países y keywords para construir un DataFrame panel completo.
    """
    panel = []
    for country, keywords in country_keywords.items():
        print(f"\n📦 Procesando país: {country}")
        for keyword in keywords:
            print(f"  🔍 Keyword: {keyword}")
            try:
                df_z = construir_serie_normalizada_con_imputaciones(
                    base_folder=base_folder,
                    country=country,
                    keyword=keyword,
                    control_term=control_term
                )
                if df_z is not None:
                    panel.append(df_z)
            except Exception as e:
                print(f"  ⚠️ Error con '{keyword}' en {country}: {e}")

    if panel:
        return pd.concat(panel, ignore_index=True)
    else:
        return None
def load_single_keyword_sample(base_folder, country, keyword):
    """
    Carga el archivo CSV original para una keyword sola.
    """
    filename = f"x_{country}_{keyword.replace(' ', '_')}.csv"
    filepath = os.path.join(base_folder, filename)
    if not os.path.exists(filepath):
        print(f"❌ Archivo no encontrado: {filepath}")
        return None
    df = pd.read_csv(filepath, encoding="utf-8")
    if "time [UTC]" in df.columns:
        df = df.rename(columns={"time [UTC]": "date"})
    for c in df.columns:
        if c not in ["date", "keywords", "keyword", "country", "muestra_n", "timestamp", "value"]:
            df = df.rename(columns={c: "value"})
            break
    df["date"] = pd.to_datetime(df["date"], format="mixed", errors="coerce")
    return df
