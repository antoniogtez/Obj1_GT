import os
import time
import random
import pandas as pd
from datetime import datetime
from trendspy import Trends

# ❌ Esta línea puede provocar bloqueos por tráfico mixto
# PROXIES.append(None)

# ✅ Solo proxies rotativos confiables
# ✅ Proxy con IP authentication (no requiere usuario:contraseña)
PROXY_URL = "http://xfjbuflz-rotate:emztbj4smng7@p.webshare.io:80/"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

# 🔧 CONFIGURACIÓN GLOBAL
BASE_PATH = r"C:\Users\34645\Desktop\projects\GoogleTrends\Data\raw_2"
LOG_FILE = os.path.join(BASE_PATH, "download_log.csv")
CONTROL_TERM = "wikipedia"
START_DATE = "2018-01-01"
END_DATE = "2025-01-01"
MAX_RETRIES = 5
SAMPLES = 50  # Puedes subir esto cuando confirmes estabilidad

# 🌍 Palabras clave por país
COUNTRIES_KEYWORDS = {
    "FR": [
        "voiture", "taxi", "vélo", "autobus",
        "télétravail", "supermarché proche", "restaurant proche", "achat en ligne",
        "voiture électrique", "borne de recharge", "consommation essence", "voiture hybride"
    ],
    "DE": ["auto", "taxi", "fahrrad", "bus", "homeoffice", "supermarkt in der nähe",
         "restaurant in der nähe", "online einkaufen", "elektroauto",
         "elektroauto aufladen", "benzinverbrauch", "hybridauto"],
    "US": [
        "car", "taxi", "bike", "bus",
        "work from home", "grocery store near me", "restaurant near me", "online shopping",
        "electric car", "charging station", "gas consumption", "hybrid car"
    ],
    "GB": [
        "car", "taxi", "bicycle", "bus",
        "work from home", "supermarket near me", "restaurant near me", "online shopping",
        "electric car", "charging point", "petrol consumption", "hybrid car"
    ],

    "ES": [
        "coche", "taxi", "bicicleta", "autobús",
        "teletrabajo", "supermercado cerca", "restaurante cerca", "compra online",
        "coche eléctrico", "electrolinera", "consumo gasolina", "coche híbrido"
    ],
    "PT": [
        "carro", "táxi", "bicicleta", "autocarro",
        "trabalho remoto", "supermercado perto", "restaurante perto", "compras online",
        "carro elétrico", "posto de carregamento", "consumo gasolina", "carro híbrido"
    ],
    }

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

    # Si el archivo ya existe, lo leemos y lo concatenamos
    if os.path.exists(LOG_FILE):
        df_prev = pd.read_csv(LOG_FILE)
        df_log = pd.concat([df_prev, df_log], ignore_index=True)

    df_log.to_csv(LOG_FILE, index=False)
    print(f"📄 Log actualizado (sin sobrescribir) en: {LOG_FILE}")


STOP_FLAG = False  # Bandera global para detener ejecución ante 429

def save_trend(keywords, country, folder, label="x", max_retries=MAX_RETRIES):
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

            # Nueva instancia con proxy y headers
           # Nueva instancia con proxy y user-agent (solo IP auth)
            headers = {
                 "User-Agent": get_random_user_agent()
                    }
            tr = Trends(request_delay=20.0, proxy=PROXY_URL, headers=headers)


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
                wait_long = random.uniform(120, 300)  # Espera larga (2 a 5 minutos)
                print(f"⚠️ Error 429 (rate limit). Esperando {wait_long:.0f}s antes de reintentar con nuevo proxy + User-Agent...")
                time.sleep(wait_long)
                attempt += 1  # ¡Y seguimos el bucle!

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

    for sample in range(1, SAMPLES + 1):
        for country, terms in COUNTRIES_KEYWORDS.items():
            if STOP_FLAG:
                break

            folder_path = os.path.join(BASE_PATH, "x")
            sorted_keywords = get_keywords_with_fewest_samples(country, terms, folder_path)

            for keyword in sorted_keywords:
                if STOP_FLAG:
                    break

                save_trend([keyword], country, folder_path, label="x")
                if STOP_FLAG: break
                time.sleep(random.uniform(60, 120))

                save_trend([CONTROL_TERM], country, folder_path, label="x")
                if STOP_FLAG: break
                time.sleep(random.uniform(60, 120))

                combined_term = f"{keyword} + {CONTROL_TERM}"
                save_trend([combined_term], country, folder_path, label="x")
                if STOP_FLAG: break
                time.sleep(random.uniform(60, 120))

    save_log()