import os
import random
import time
import pandas as pd
from trendspy import Trends
from datetime import datetime, timedelta

# 📌 Configuración de rutas
proxy_file_path = "C:/Users/34645/Desktop/projects/Obj1_GT/data/proxies.txt"
data_path = "C:/Users/34645/Desktop/projects/Obj1_GT/data/raw"
log_file = "C:/Users/34645/Desktop/projects/Obj1_GT/data/download_log.csv"

# 📌 Asegurar que el directorio de salida existe
os.makedirs(data_path, exist_ok=True)

# 📌 Leer la lista de proxies desde el archivo
with open(proxy_file_path, "r") as file:
    proxies_raw = file.readlines()

# 📌 Función para convertir los proxies al formato correcto
def convert_proxy_format(proxy_line):
    parts = proxy_line.strip().split(":")
    if len(parts) == 4:  # Formato: IP:PUERTO:USUARIO:CONTRASEÑA
        return f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
    return None  # Ignorar si no tiene el formato correcto

# 📌 Convertir y filtrar proxies válidos
proxy_list = list(filter(None, map(convert_proxy_format, proxies_raw)))

# 📌 Verificar que hay proxies válidos
if not proxy_list:
    raise ValueError("⚠️ No hay proxies válidos en el archivo.")

# 📌 Función para seleccionar un proxy aleatorio
def get_random_proxy(proxies):
    return random.choice(proxies)

# 📌 Función para obtener los rangos de fechas mensuales
def generate_monthly_ranges(start_date, end_date):
    date_ranges = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")

    while current_date < datetime.strptime(end_date, "%Y-%m-%d"):
        next_month = current_date + timedelta(days=32)
        next_month = next_month.replace(day=1)
        date_ranges.append((current_date.strftime("%Y-%m-%d"), (next_month - timedelta(days=1)).strftime("%Y-%m-%d")))
        current_date = next_month
    
    return date_ranges

# 📌 Función para probar `Trendspy` con un proxy y guardar en CSV
def download_trendspy_data(keyword, start_date="2023-01-01", end_date="2023-06-30"):
    date_ranges = generate_monthly_ranges(start_date, end_date)
    all_results = []

    for start, end in date_ranges:
        proxy = get_random_proxy(proxy_list)
        print(f"🔄 Usando proxy: {proxy} para descargar '{keyword}' del {start} al {end}")

        # 📌 Inicializar Trendspy con el proxy seleccionado
        tr = Trends(request_delay=4, proxy=proxy)

        try:
            # 📌 Intentar descargar datos de Google Trends
            df = tr.interest_over_time([keyword], timeframe=f"{start} {end}", geo="ES")

            # 📌 Si la consulta fue exitosa, procesar y guardar los datos
            if not df.empty:
                df["Keyword"] = keyword  # Agregar la columna de palabra clave
                df["Date"] = df.index.strftime("%Y-%m-%d")  # Convertir índice a fecha

                all_results.append(df)
                print(f"✅ Datos descargados correctamente para '{keyword}' del {start} al {end}.")

                # 📌 Registrar la descarga en el log
                with open(log_file, "a") as log:
                    log.write(f"{datetime.now()}, {keyword}, {start}, {end}, {proxy}\n")

            else:
                print(f"⚠️ No se encontraron datos para '{keyword}' en el rango {start} - {end}.")

        except Exception as e:
            print(f"❌ Error al descargar datos con el proxy {proxy}: {e}")

        # 📌 Esperar unos segundos antes de la siguiente descarga
        #time.sleep(random.randint(600, 180))

    # 📌 Guardar resultados en CSV si hay datos
    if all_results:
        final_df = pd.concat(all_results, ignore_index=True)
        output_file = os.path.join(data_path, f"{keyword}_diario.csv")
        final_df.to_csv(output_file, index=False)
        print(f"📁 Datos guardados en '{output_file}'.")
    else:
        print(f"⚠️ No se guardaron datos para '{keyword}'.")

# 📌 Lista de palabras clave a buscar
keywords = ["coche", "autobús", "bicicleta","metro", "tranvía"]

# 📌 Ejecutar la prueba con diferentes keywords
for keyword in keywords:
    download_trendspy_data(keyword)


