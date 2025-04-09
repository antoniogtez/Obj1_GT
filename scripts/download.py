
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
SAMPLES = 3  # Puedes subir esto cuando confirmes estabilidad

# 🌍 Palabras clave por país
COUNTRIES_KEYWORDS = {
     "DE": [
        "auto", "taxi", "fahrrad", "bus",
        "homeoffice", "supermarkt in der nähe", "restaurant in der nähe", "online einkaufen",
        "elektroauto", "elektroauto aufladen", "benzinverbrauch", "hybridauto"
    ],
    "IT": [
        "auto", "taxi", "bicicletta", "autobus",
        "telelavoro", "supermercato vicino", "ristorante vicino", "acquisti online",
        "auto elettrica", "colonnina di ricarica", "consumo benzina", "auto ibrida"
    ],
    "PT": [
        "carro", "táxi", "bicicleta", "autocarro",
        "trabalho remoto", "supermercado perto", "restaurante perto", "compras online",
        "carro elétrico", "posto de carregamento", "consumo gasolina", "carro híbrido"
    ],
    "ES": [
        "coche", "taxi", "bicicleta", "autobús",
        "teletrabajo", "supermercado cerca", "restaurante cerca", "compra online",
        "coche eléctrico", "electrolinera", "consumo gasolina", "coche híbrido"
    ],
    "FR": [
        "voiture", "taxi", "vélo", "autobus",
        "télétravail", "supermarché proche", "restaurant proche", "achat en ligne",
        "voiture électrique", "borne de recharge", "consommation essence", "voiture hybride"
    ],
    "US": [
        "car", "taxi", "bike", "bus",
        "work from home", "grocery store near me", "restaurant near me", "online shopping",
        "electric car", "charging station", "gas consumption", "hybrid car"
    ],
    "GB": [
        "car", "taxi", "bicycle", "bus",
        "work from home", "supermarket near me", "restaurant near me", "online shopping",
        "electric car", "charging point", "petrol consumption", "hybrid car"
    ]}

# 🧾 LOG DE SESIÓN
SESSION_LOG = []

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

def save_log():
    df_log = pd.DataFrame(SESSION_LOG)
    df_log.to_csv(LOG_FILE, index=False)
    print(f"📄 Log guardado en: {LOG_FILE}")

STOP_FLAG = False  # Bandera global para detener ejecución ante 429

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
            print(f"🌍 País: {country} | Palabra: {'+'.join(keywords)} | Muestra: {muestra_n} | Intento: {attempt+1}")
            df = tr.interest_over_time(
                keywords,
                geo=country,
                timeframe=f"{START_DATE} {END_DATE}"
            )
            if df is None or df.empty:
                raise ValueError("Empty or None result")

            df = df.reset_index()
            df["keywords"] = "+".join(keywords)
            df["country"] = country
            df["muestra_n"] = muestra_n
            df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            full_df = pd.concat([existing_df, df], ignore_index=True)
            full_df.to_csv(filepath, index=False)

            print(f"✅ Datos añadidos a: {filepath} (muestra_n = {muestra_n})")
            log_event(country, keywords, label, "success", f"Appended to {filepath}")
            return

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al descargar '{keywords}' en {country}: {error_msg}")
            log_event(country, keywords, label, "error", error_msg)

            if "429" in error_msg:
                print("🛑 Error 429 detectado. Deteniendo ejecución inmediatamente.")
                STOP_FLAG = True
                return  # sin más intentos
            else:
                wait_time = random.uniform(10, 25)
                print(f"⏳ Esperando {wait_time:.2f} segundos antes de reintentar...")
                time.sleep(wait_time)
                attempt += 1

def get_keywords_with_fewest_samples(country, keywords, folder):
    sample_counts = []
    for kw in keywords:
        filename = f"x_{country}_{kw.replace(' ', '_')}.csv"
        filepath = os.path.join(folder, filename)
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath)
                count = df["muestra_n"].nunique()
            except Exception:
                count = 0
        else:
            count = 0
        sample_counts.append((kw, count))
    
    sorted_keywords = sorted(sample_counts, key=lambda x: x[1])
    return [kw for kw, _ in sorted_keywords]

if __name__ == "__main__":
    tr = Trends(request_delay=6.0)

    for sample in range(1, SAMPLES + 1):
        for country, terms in COUNTRIES_KEYWORDS.items():
            if STOP_FLAG:
                break

            folder_path = os.path.join(BASE_PATH, "x")
            sorted_keywords = get_keywords_with_fewest_samples(country, terms, folder_path)

            for keyword in sorted_keywords:
                if STOP_FLAG:
                    break

                save_trend(tr, [keyword], country, folder_path, label="x")
                if STOP_FLAG: break
                time.sleep(random.uniform(60, 300))

                save_trend(tr, [CONTROL_TERM], country, folder_path, label="x")
                if STOP_FLAG: break
                time.sleep(random.uniform(60, 300))

                combined_term = f"{keyword} + {CONTROL_TERM}"
                save_trend(tr, [combined_term], country, folder_path, label="x")
                if STOP_FLAG: break
                time.sleep(random.uniform(60, 300))

    save_log()
