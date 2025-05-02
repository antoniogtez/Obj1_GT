import os
import time
import random
import pandas as pd
import requests
from datetime import datetime
from trendspy import Trends

# --- Configuración proxies y headers ---
PROXY_URL = "http://xfjbuflz-rotate:emztbj4smng7@p.webshare.io:80/"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

# --- Configuración global ---
BASE_PATH = r"C:\Users\34645\Desktop\projects\GoogleTrends\Data\raw_2"
LOG_FILE = os.path.join(BASE_PATH, "download_log.csv")
CONTROL_TERM = "google"
START_DATE = "2018-01-01"
END_DATE = "2025-01-01"
MAX_RETRIES = 5
SAMPLES = 50
# 🌍 Palabras clave por país
COUNTRIES_KEYWORDS = {
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
    "DK": ["bil", "taxa","cykel", "bus", "hjemmearbejde", "supermarked i nærheden","restaurant i nærheden", 
       "online shopping",   "elbil", "ladestation", "benzinforbrug", "hybridbil" ],
    'NO': [
        "bil", "taxi", "sykkel", "buss",
        "hjemmekontor", "butikk i nærheten", "restaurant i nærheten", "netthandel",
        "elbil", "ladestasjon", "bensinforbruk", "hybridbil"
    ],
    "IT": ["auto", "taxi", "bicicletta", "autobus", "telelavoro",
    "supermercato vicino", "ristorante vicino", "acquisti online",
    "auto elettrica", "colonnina di ricarica", "consumo benzina", "auto ibrida"],
    'IE': [  # Irlanda: mismo que UK
        "car", "taxi", "bicycle", "bus",
        "remote work", "supermarket near me", "restaurant near me", "online shopping",
       "electric car", "electric charging station", "petrol consumption", "hybrid car"
    ],
    'SE': [
        "bil", "taxi", "cykel", "buss",
        "distansarbete", "mataffär nära mig", "restaurang nära mig", "online shopping",
        "elbil", "laddstation", "bensinförbrukning", "hybridbil"
    ],
    'BE': [
        "auto", "taxi", "fiets", "bus",
        "thuiswerken", "supermarkt in de buurt", "restaurant in de buurt", "online winkelen",
        "elektrische auto", "laadstation", "benzineverbruik", "hybride auto"
    ],
    
    'FI': [
        "auto", "taksi", "pyörä", "bussi",
        "etätyö", "lähikauppa", "ravintola lähellä", "verkkokauppa",
        "sähköauto", "latausasema", "polttoaineenkulutus", "hybridiauto"
    ],
    'NL': [
        "auto", "taxi", "fiets", "bus",
        "thuiswerken", "supermarkt in de buurt", "restaurant in de buurt", "online winkelen",
        "elektrische auto", "laadstation", "benzineverbruik", "hybride auto"
    ],
    'AT': [
        "auto", "taxi", "fahrrad", "bus",
        "homeoffice", "supermarkt in der nähe", "restaurant in der nähe", "online einkaufen",
        "elektroauto", "ladestation", "benzinverbrauch", "hybridauto"
    ],
    }

SESSION_LOG = []
STOP_FLAG = False

# --- Funciones auxiliares ---

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
    if os.path.exists(LOG_FILE):
        df_prev = pd.read_csv(LOG_FILE)
        df_log = pd.concat([df_prev, df_log], ignore_index=True)
    df_log.to_csv(LOG_FILE, index=False)
    print(f"📄 Log actualizado en: {LOG_FILE}")

last_ip = None  # Global para seguimiento

def check_proxy_ip(proxy_url):
    global last_ip
    try:
        proxies = {"http": proxy_url, "https": proxy_url}
        response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=10)
        ip = response.json().get("origin")
        if ip != last_ip:
            print(f"🌐 IP actual (nueva): {ip}")
            last_ip = ip
        else:
            print(f"🌐 IP no cambió: {ip}")
    except Exception as e:
        print(f"⚠️ Error verificando proxy: {e}")

def save_trend(keywords, country, folder, label="x", max_retries=MAX_RETRIES):
    global STOP_FLAG
    os.makedirs(folder, exist_ok=True)
    base_filename = f"{label}_{country}_{'_'.join(keywords).replace(' ', '_')}.csv"
    filepath = os.path.join(folder, base_filename)

    existing_df = pd.read_csv(filepath) if os.path.exists(filepath) else pd.DataFrame()
    last_sample = existing_df["muestra_n"].max() if not existing_df.empty else 0

    attempt = 0
    while attempt < max_retries:
        try:
            check_proxy_ip(PROXY_URL)  # ✅ Nueva línea: verificar IP actual del proxy

            muestra_n = last_sample + 1
            print(f"🌍 País: {country} | Palabra: {'+'.join(keywords)} | Muestra: {muestra_n} | Intento: {attempt+1}")

            headers = {"User-Agent": get_random_user_agent()}
            tr = Trends(request_delay=10.0, proxy=PROXY_URL, headers=headers)

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

            print(f"✅ Datos añadidos a: {filepath} (muestra_n = {muestra_n})")
            log_event(country, keywords, label, "success", f"Appended to {filepath}")
            return

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error al descargar '{keywords}' en {country}: {error_msg}")
            log_event(country, keywords, label, "error", error_msg)

            if "429" in error_msg:
                wait_long = random.uniform(60, 120)  #Funciona con 200-300
                print(f"⚠️ Error 429. Esperando {wait_long:.0f}s...")
                time.sleep(wait_long)

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
    
    return [kw for kw, _ in sorted(sample_counts, key=lambda x: x[1])]

# --- Programa principal ---

if __name__ == "__main__":
    try:
        last_ip = None

        for sample in range(1, SAMPLES + 1):
            for country, terms in COUNTRIES_KEYWORDS.items():
                if STOP_FLAG:
                    break

                folder_path = os.path.join(BASE_PATH, "x")
                sorted_keywords = get_keywords_with_fewest_samples(country, terms, folder_path)

                for i, keyword in enumerate(sorted_keywords):
                    if STOP_FLAG:
                        break

                    # Verificar proxy antes de cada descarga
                    current_ip = check_proxy_ip(PROXY_URL)

                    if last_ip is not None:
                        if current_ip == last_ip:
                            print("⚠️ IP NO ha cambiado respecto a la anterior.")
                        else:
                            print("✅ IP diferente detectada (rotación correcta).")
                    last_ip = current_ip

                    #save_trend([keyword], country, folder_path, label="x")
                    #if STOP_FLAG:
                    #    break
                    #time.sleep(random.uniform(5, 10)) #Funciona con 60-120

                    combined_term = f"{keyword} + {CONTROL_TERM}"
                    save_trend([combined_term], country, folder_path, label="x")
                    if STOP_FLAG:
                        break
                    time.sleep(random.uniform(5, 10)) #Funciona con 60-120

                    if i % 10 == 0:
                        save_trend([CONTROL_TERM], country, folder_path, label="x")
                        if STOP_FLAG:
                            break
                        time.sleep(random.uniform(5, 10)) #Funciona con 60-120

    except KeyboardInterrupt:
        print("🛑 Interrupción manual detectada (CTRL+C).")

    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

    finally:
        save_log()
        print("✅ Log de sesión guardado correctamente (final).")