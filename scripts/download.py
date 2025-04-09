
import os
import time
import random
import pandas as pd
from datetime import datetime
from trendspy import Trends

# 🔧 CONFIGURACIÓN GLOBAL
BASE_PATH = r"C:\Users\34645\Desktop\projects\GoogleTrends\Data\raw_2"
LOG_FILE = os.path.join(BASE_PATH, "download_log.csv")
CONTROL_TERM = "wikipedia"
START_DATE = "2018-01-01"
END_DATE = "2025-01-01"
MAX_RETRIES = 5
SAMPLES = 3

# 🌍 Keywords por país
COUNTRIES_KEYWORDS = {
    "DE": ["auto", "taxi", "fahrrad", "bus", "homeoffice", "supermarkt in der nähe",
           "restaurant in der nähe", "online einkaufen", "elektroauto",
           "elektroauto aufladen", "benzinverbrauch", "hybridauto"],
    "IT": ["auto", "taxi", "bicicletta", "autobus", "telelavoro", "supermercato vicino",
           "ristorante vicino", "acquisti online", "auto elettrica", "colonnina di ricarica",
           "consumo benzina", "auto ibrida"],
    "PT": ["carro", "táxi", "bicicleta", "autocarro", "trabalho remoto",
           "supermercado perto", "restaurante perto", "compras online",
           "carro elétrico", "posto de carregamento", "consumo gasolina", "carro híbrido"],
    "ES": ["coche", "taxi", "bicicleta", "autobús", "teletrabajo", "supermercado cerca",
           "restaurante cerca", "compra online", "coche eléctrico", "electrolinera",
           "consumo gasolina", "coche híbrido"],
    "FR": ["voiture", "taxi", "vélo", "autobus", "télétravail", "supermarché proche",
           "restaurant proche", "achat en ligne", "voiture électrique", "borne de recharge",
           "consommation essence", "voiture hybride"],
    "US": ["car", "taxi", "bike", "bus", "work from home", "grocery store near me",
           "restaurant near me", "online shopping", "electric car", "charging station",
           "gas consumption", "hybrid car"],
    "GB": ["car", "taxi", "bicycle", "bus", "work from home", "supermarket near me",
           "restaurant near me", "online shopping", "electric car", "charging point",
           "petrol consumption", "hybrid car"]
}

SESSION_LOG = []
STOP_FLAG = False

def log_event(country, keywords, label, status, message):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "country": country,
        "keywords": "+".join(keywords),
        "label": label,
        "status": status,
        "message": message
    }
    SESSION_LOG.append(log_entry)

    df_log = pd.DataFrame([log_entry])
    file_exists = os.path.exists(LOG_FILE)
    df_log.to_csv(LOG_FILE, mode='a', index=False, header=not file_exists)

def save_trend(tr, keywords, country, folder, label="x", max_retries=MAX_RETRIES):
    global STOP_FLAG
    os.makedirs(folder, exist_ok=True)
    base_filename = f"{label}_{country}_{'_'.join(keywords).replace(' ', '_')}.csv"
    filepath = os.path.join(folder, base_filename)

    if os.path.exists(filepath):
        existing_df = pd.read_csv(filepath)
        last_sample = existing_df["muestra_n"].max()
    else:
        existing_df = pd.DataFrame()
        last_sample = 0

    attempt = 0
    while attempt < max_retries:
        try:
            muestra_n = last_sample + 1
            print(f"🌍 {country} | {keywords} | Muestra: {muestra_n}")
            df = tr.interest_over_time(keywords, geo=country, timeframe=f"{START_DATE} {END_DATE}")
            if df is None or df.empty:
                raise ValueError("Empty or None result")

            df = df.reset_index()
            df["keywords"] = "+".join(keywords)
            df["country"] = country
            df["muestra_n"] = muestra_n
            df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            full_df = pd.concat([existing_df, df], ignore_index=True)
            full_df.to_csv(filepath, index=False)

            log_event(country, keywords, label, "success", f"Appended to {filepath}")
            return

        except Exception as e:
            msg = str(e)
            print(f"❌ Error: {keywords} ({country}) -> {msg}")
            log_event(country, keywords, label, "error", msg)
            if "429" in msg:
                print("🛑 Error 429. Deteniendo ejecución.")
                STOP_FLAG = True
                return
            else:
                time.sleep(random.uniform(10, 25))
                attempt += 1

def build_global_keyword_list(folder):
    all_keywords = []
    for country, terms in COUNTRIES_KEYWORDS.items():
        for kw in terms:
            filename = f"x_{country}_{kw.replace(' ', '_')}.csv"
            filepath = os.path.join(folder, filename)
            if os.path.exists(filepath):
                try:
                    df = pd.read_csv(filepath)
                    num = df["muestra_n"].nunique()
                except Exception:
                    num = 0
            else:
                num = 0
            all_keywords.append((country, kw, num))
    sorted_all = sorted(all_keywords, key=lambda x: x[2])
    return sorted_all

if __name__ == "__main__":
    tr = Trends(request_delay=6.0)
    folder_path = os.path.join(BASE_PATH, "x")

    while not STOP_FLAG:
        sorted_global = build_global_keyword_list(folder_path)
        keyword_entry = next((entry for entry in sorted_global if entry[2] < SAMPLES), None)

        if not keyword_entry:
            print("🎉 ¡Todas las keywords tienen suficientes muestras!")
            break

        country, keyword, muestras = keyword_entry
        print(f"➡️ Próxima descarga: {keyword} ({country}) con {muestras} muestras")

        # 1. keyword sola
        save_trend(tr, [keyword], country, folder_path, label="x")
        if STOP_FLAG: break
        time.sleep(random.uniform(60, 300))

        # 2. control
        save_trend(tr, [CONTROL_TERM], country, folder_path, label="x")
        if STOP_FLAG: break
        time.sleep(random.uniform(60, 300))

        # 3. combinada
        combined = f"{keyword} + {CONTROL_TERM}"
        save_trend(tr, [combined], country, folder_path, label="x")
        if STOP_FLAG: break
        time.sleep(random.uniform(60, 300))