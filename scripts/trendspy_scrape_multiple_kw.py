import pandas as pd 
import os
import time
import random
from datetime import datetime, timedelta
from trendspy import Trends

# 🔹 CONFIGURACIÓN GLOBAL
PAIS = "ES"
# 🔹 Uso de término de control en Google Trends
# Google Trends normaliza cada consulta individualmente, por lo que los valores no son directamente comparables
# cuando se extraen más de 5 palabras clave en diferentes consultas.
# Para solucionar esto, agregamos un término de control ("Google") en todas las consultas.
# Este término debe ser estable en el tiempo y más popular que cualquier otro en el conjunto de palabras clave.
# De esta manera, se asegura que todas las consultas estén en la misma escala y puedan ser comparadas.
#
# 🔹 Selección del término de control:
# "Google" fue elegido porque tiene un volumen de búsqueda alto y estable en el tiempo.
# Otras opciones podrían haber sido "Wikipedia" o "Tiempo", pero Google es el más seguro para asegurar la normalización correcta.

KEYWORDS = ["coche", "taxi", "bus", "bicicleta", "google"]
LOG_FILE = r"C:\Users\34645\Desktop\projects\Obj1_GT\data\error_log.csv"
DATA_FOLDER = r"C:\Users\34645\Desktop\projects\Obj1_GT\data"

# 🔹 Verificar que la carpeta existe, si no, crearla
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def get_file_path(filename):
    return os.path.join(DATA_FOLDER, filename)

START_DATE = "2015-01-01"
END_DATE = "2023-12-31"

PROXIES = ["http://xfjbuflz-rotate:emztbj4smng7@p.webshare.io:80"]
PROXIES.append(None)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
]

def get_random_proxy():
    return random.choice(PROXIES)

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def get_wait_time(attempt):
    return random.uniform(5, 15) * (2 ** attempt)

def log_error(timeframe, country, error_message):
    log_df = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "timeframe": timeframe,
        "country": country,
        "error_message": error_message
    }])
    
    if os.path.exists(LOG_FILE):
        log_df.to_csv(LOG_FILE, mode='a', header=False, index=False)
    else:
        log_df.to_csv(LOG_FILE, index=False)

def get_timeframes(start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    timeframes = []
    while start_date < end_date:
        next_date = start_date + timedelta(days=30)
        if next_date > end_date:
            next_date = end_date
        timeframes.append(f"{start_date.strftime('%Y-%m-%d')} {next_date.strftime('%Y-%m-%d')}")
        start_date = next_date
    return timeframes

def get_extraction_number(df, timeframe, country):
    """ Devuelve el número de extracción para una combinación única de periodo y país """
    if df.empty:
        return 1
    subset = df[(df["timeframe"] == timeframe) & (df["country"] == country)]
    if subset.empty:
        return 1
    return subset["extraction_number"].max() + 1

def get_trends_and_save(keywords, country, start_date, end_date):
    attempts = 0
    tr = Trends(request_delay=5.0)  

    timeframes = get_timeframes(start_date, end_date)  
    filename_multiple = get_file_path(f"panel_trends_ES_multiple.csv")  # 🔹 Nuevo CSV para consultas múltiples

    # 🔹 Cargar datos previos si el archivo existe
    if os.path.exists(filename_multiple):
        existing_df = pd.read_csv(filename_multiple)
    else:
        existing_df = pd.DataFrame()

    while attempts < 5:
        try:
            proxy = get_random_proxy()
            tr.set_proxy(proxy)  
            HEADERS = {
                "User-Agent": get_random_user_agent(),
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.google.com/"
            }

            for timeframe in timeframes:
                wait_time = random.uniform(60, 300)
                print(f"⌛ Esperando {wait_time:.2f} segundos antes de la siguiente solicitud a Google Trends...")
                time.sleep(wait_time)  

                print(f"📊 Descargando datos para {keywords} en {country} - Período: {timeframe}")
                df = tr.interest_over_time(keywords, geo=country, timeframe=timeframe, headers=HEADERS)

                print("📥 Respuesta de Google Trends (primeras 5 filas):")
                print(df.head() if df is not None else "❌ No se recibieron datos.")

                if df is None or df.empty:
                    print(f"⚠ No se encontraron datos para {keywords} en {timeframe}, continuando...")
                    continue

                df = df.reset_index().rename(columns={"time [UTC]": "date"})

                df = df.melt(id_vars=["date"], var_name="keyword", value_name="interest")
                df["country"] = country
                df["timeframe"] = timeframe  # Guardar el periodo de extracción
                df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # 🔹 Asignar número de extracción
                df["extraction_number"] = get_extraction_number(existing_df, timeframe, country)

                # 🔹 Guardar datos progresivamente en el CSV de múltiples palabras clave
                existing_df = pd.concat([existing_df, df], ignore_index=True)
                existing_df.to_csv(filename_multiple, index=False)
                
                print(f"✅ Datos guardados en '{filename_multiple}' - Extracción #{df['extraction_number'].max()}")

            return df  

        except Exception as e:
            print(f"❌ Error en la extracción: {e}")
            log_error(timeframe, country, str(e))
            attempts += 1
            time.sleep(get_wait_time(attempts))

# 🔹 Ejecutar para todas las palabras clave a la vez y guardarlo en el nuevo CSV
get_trends_and_save(KEYWORDS, PAIS, START_DATE, END_DATE)
