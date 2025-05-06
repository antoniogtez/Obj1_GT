# config/keywords_mapping.py
import pandas as pd

# Diccionario principal con keywords por país
COUNTRIES_KEYWORDS = {
    "GB": [
        "car", "taxi", "bicycle", "bus", "work from home",
        "supermarket near me", "restaurant near me", "online shopping",
        "electric car", "petrol consumption", "hybrid car",
        "parking", "traffic", "car sharing", "uber"
    ],
    "ES": [
        "coche", "taxi", "bicicleta", "autobús", "teletrabajo",
        "supermercado cerca", "restaurante cerca", "compra online",
        "coche eléctrico", "consumo gasolina", "coche híbrido",
        "aparcamiento", "trafico", "car sharing", "uber", "cabify"
    ],
    "PT": [
        "carro", "táxi", "bicicleta", "autocarro", "trabalho remoto",
        "supermercado perto", "restaurante perto", "compras online",
        "carro elétrico", "consumo gasolina", "carro híbrido",
        "estacionamento", "trânsito", "car sharing", "uber", "cabify"
    ],
    "DK": [
        "bil", "taxa", "cykel", "bus", "hjemmearbejde",
        "supermarked i nærheden", "restaurant i nærheden", "online shopping",
        "elbil", "brændstofforbrug", "hybridbil",
        "parkering", "trafik", "delebil", "uber"
    ],
    "NO": [
        "bil", "taxi", "sykkel", "buss", "hjemmekontor",
        "butikk i nærheten", "restaurant i nærheten", "netthandel",
        "elbil", "bensinforbruk", "hybridbil",
        "parkering", "trafikk", "bildeling", "uber"
    ],
    "IT": [
        "auto", "taxi", "bicicletta", "autobus", "telelavoro",
        "supermercato vicino", "ristorante vicino", "acquisti online",
        "auto elettrica", "consumo benzina", "auto ibrida",
        "parcheggio", "traffico", "car sharing", "uber", "cabify"
    ],
    "IE": [
        "car", "taxi", "bicycle", "bus", "remote work",
        "supermarket near me", "restaurant near me", "online shopping",
        "electric car", "fuel consumption", "hybrid car",
        "parking", "traffic", "car sharing", "uber"
    ],
    "SE": [
        "bil", "taxi", "cykel", "buss", "distansarbete",
        "mataffär nära mig", "restaurang nära mig", "online shopping",
        "elbil", "bensinförbrukning", "hybridbil",
        "parkering", "trafik", "bilpool", "uber"
    ],
    "BE": [
        "auto", "taxi", "fiets", "bus", "thuiswerken",
        "supermarkt in de buurt", "restaurant in de buurt", "e-commerce",
        "elektrische auto",  "benzine verbruik", "hybride auto",
        "parking", "trafic", "car sharing", "uber", "cabify"
    ],
    "FI": [
        "auto", "taksi", "pyörä", "bussi", "etätyö",
        "lähikauppa", "ravintola lähellä", "verkkokauppa",
        "sähköauto", "polttoaineen kulutus", "hybridiauto",
        "pysäköinti", "liikenne", "yhteiskäyttöauto", "uber"
    ],
    "NL": [
        "auto", "taxi", "fiets", "bus", "thuiswerken",
        "supermarkt in de buurt", "restaurant in de buurt", "online winkelen",
        "elektrische auto", "benzineverbruik", "hybride auto",
        "parkeren", "verkeer", "car sharing", "uber"
    ],
    "AT": [
        "auto", "taxi", "fahrrad", "bus", "homeoffice",
        "supermarkt in der nähe", "restaurant in der nähe", "online einkaufen",
        "elektroauto",  "benzinverbrauch", "hybrid auto",
        "parkplatz", "verkehr", "car sharing", "uber"
    ],
    "FR": [
        "voiture", "taxi", "vélo", "autobus", "télétravail",
        "supermarché proche", "restaurant proche", "achat en ligne",
        "voiture électrique",  "consommation essence", "voiture hybride",
        "parking", "trafic", "autopartage", "uber", "cabify"
    ],
    "DE": [
        "auto", "taxi", "fahrrad", "bus", "homeoffice",
        "supermarkt in der nähe", "restaurant in der nähe", "online einkaufen",
        "elektroauto",  "benzinverbrauch", "hybridauto",
        "parkplatz", "verkehr", "carsharing", "uber"
    ],
    "US": [
        "car", "taxi", "bike", "bus", "work from home",
        "grocery store near me", "restaurant near me", "online shopping",
        "electric car", "gas consumption", "hybrid car",
        "parking", "traffic", "car sharing", "uber"
    ]
}



# --- Equivalencias comunes ---
# config/common_keywords.py

COMMON_KEYWORDS = {
    # 🚗 Car
    "auto": "car", "bil": "car", "car": "car", "voiture": "car",
    "carro": "car", "coche": "car",

    # 🚖 Taxi
    "taxi": "taxi", "táxi": "taxi", "taxa": "taxi", "taksi": "taxi",

    # 🚲 Bike
    "bicicleta": "bike", "bicycle": "bike", "vélo": "bike", "bicicletta": "bike",
    "fahrrad": "bike", "fiets": "bike", "sykkel": "bike", "cykel": "bike",
    "pyörä": "bike",

    # 🚌 Bus
    "autobús": "bus", "bus": "bus", "autocarro": "bus", "autobus": "bus",
    "buss": "bus", "bussi": "bus",

    # 🏠 Remote work
    "teletrabajo": "remote_work", "work from home": "remote_work",
    "trabalho remoto": "remote_work", "télétravail": "remote_work",
    "homeoffice": "remote_work", "telelavoro": "remote_work",
    "hjemmekontor": "remote_work", "distansarbete": "remote_work",
    "hjemmearbejde": "remote_work", "etätyö": "remote_work",
    "thuiswerken": "remote_work", "remote work": "remote_work",

    # 🛒 Supermarket
    "supermercado cerca": "supermarket", "supermercado perto": "supermarket",
    "supermarché proche": "supermarket", "supermarket near me": "supermarket",
    "supermarkt in der nähe": "supermarket", "supermercato vicino": "supermarket",
    "grocery store near me": "supermarket", "supermarked i nærheten": "supermarket",
    "supermarked i nærheden": "supermarket", "mataffär nära mig": "supermarket",
    "butikk i nærheten": "supermarket", "lähikauppa": "supermarket",
    "supermarkt in de buurt": "supermarket",

    # 🍽️ Restaurant
    "restaurante cerca": "restaurant", "restaurante perto": "restaurant",
    "restaurant proche": "restaurant", "restaurant near me": "restaurant",
    "restaurant in der nähe": "restaurant", "ristorante vicino": "restaurant",
    "restaurant i nærheten": "restaurant", "restaurang nära mig": "restaurant",
    "restaurant i nærheden": "restaurant", "ravintola lähellä": "restaurant",
    "restaurant in de buurt": "restaurant",

    # 🛍️ Online Shopping
    "compra online": "online_shopping", "compras online": "online_shopping",
    "online shopping": "online_shopping", "achat en ligne": "online_shopping",
    "online einkaufen": "online_shopping", "acquisti online": "online_shopping",
    "netthandel": "online_shopping", "verkkokauppa": "online_shopping",
    "online winkelen": "online_shopping", "e-commerce": "online_shopping",

    # ⚡ Electric Car
    "coche eléctrico": "electric_car", "electric car": "electric_car",
    "voiture électrique": "electric_car", "auto elettrica": "electric_car",
    "carro elétrico": "electric_car", "elektroauto": "electric_car",
    "elbil": "electric_car", "sähköauto": "electric_car",
    "elektrische auto": "electric_car",

    # 🔌 Charging Station (no usada actualmente pero mantenida por si se reutiliza)
    "electrolinera": "charging_station", "ladestasjon": "charging_station",
    "charging station": "charging_station", "borne de recharge": "charging_station",
    "posto de carregamento": "charging_station", "charging point": "charging_station",
    "colonnina di ricarica": "charging_station", "elektroauto aufladen": "charging_station",
    "ladestation": "charging_station", "laddstation": "charging_station",
    "latausasema": "charging_station", "laadstation": "charging_station",
    "electric charging station": "charging_station",

    # ⛽ Fuel Consumption (actualizado)
    "consumo gasolina": "fuel_consumption",
    "gas consumption": "fuel_consumption",
    "consommation essence": "fuel_consumption",
    "consumo benzina": "fuel_consumption",
    "petrol consumption": "fuel_consumption",
    "benzinverbrauch": "fuel_consumption",
    "bensinforbruk": "fuel_consumption",
    "bensinförbrukning": "fuel_consumption",
    "polttoaineen kulutus": "fuel_consumption",
    "benzineverbruik": "fuel_consumption",
    "benzine verbruik": "fuel_consumption",
    "benzinforbrug": "fuel_consumption",
    "fuel consumption": "fuel_consumption",         # ← 🔄 unificar
    "brændstofforbrug": "fuel_consumption",          # ← 🔄 unificar


    # 🔄 Hybrid Car
    "coche híbrido": "hybrid_car", "hybrid car": "hybrid_car",
    "voiture hybride": "hybrid_car", "auto ibrida": "hybrid_car",
    "carro híbrido": "hybrid_car", "hybridauto": "hybrid_car",
    "hybridbil": "hybrid_car", "hybridiauto": "hybrid_car",
    "hybride auto": "hybrid_car", "hybrid auto": "hybrid_car",

    # 🅿️ Parking
    "parking": "parking", "aparcamiento": "parking", "parcheggio": "parking",
    "estacionamento": "parking", "parkplatz": "parking", "parkeren": "parking",
    "parkering": "parking", "pysäköinti": "parking",

    # 🚦 Traffic
    "trafico": "traffic", "traffico": "traffic", "trafic": "traffic",
    "verkehr": "traffic", "traffic": "traffic", "trânsito": "traffic",
    "trafik": "traffic", "trafikk": "traffic", "liikenne": "traffic",
    "verkeer": "traffic",

    # 🚘 Car Sharing
    "car sharing": "car_sharing", "carsharing": "car_sharing",
    "autopartage": "car_sharing", "auto condiviso": "car_sharing",
    "compartir coche": "car_sharing", "bildeling": "car_sharing",
    "yhteiskäyttöauto": "car_sharing", "delebil": "car_sharing",
    "bilpool": "car_sharing",

    # 🚖 Ride-Hailing (Uber, Cabify)
    "uber": "ride_hailing", "cabify": "ride_hailing"
}

# Expandir a DataFrame con columnas por país
df_keywords = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in COUNTRIES_KEYWORDS.items()]))

# Ruta de guardado
output_path = r"C:\Users\34645\Desktop\projects\GoogleTrends\Data\keywords_by_country_vertical.csv"

# Guardar con codificación segura para tildes y caracteres especiales
df_keywords.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"CSV con acentos guardado correctamente en: {output_path}")