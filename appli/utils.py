import os
import requests
from dotenv import load_dotenv
import datetime

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer la clé API OpenWeatherMap
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# URL de base pour les requêtes API
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def obtenir_coordonnees(data):
    if "coord" in data:
        print("Coordonnées trouvées")
        return data["coord"]["lat"], data["coord"]["lon"]
    else:
        print("Coordonnées non trouvées")
        return None

def obtenir_temperature_actuelle(data):
    return data["main"]["temp"]

def obtenir_coordonnees(data):
    return data["coord"]["lat"], data["coord"]["lon"]

def obtenir_temperature_ressentie(data):
    return data["main"]["feels_like"]

def obtenir_temperature_min_max(data):
    return data["main"]["temp_min"], data["main"]["temp_max"]

def obtenir_pression_atmospherique(data):
    return data["main"]["pressure"]

def obtenir_humidite(data):
    return data["main"]["humidity"]

def obtenir_vitesse_vent(data):
    return data["wind"]["speed"]

def obtenir_direction_vent(data):
    return data["wind"]["deg"]

def obtenir_lever_soleil(data):
    timestamp = data["sys"]["sunrise"]
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def obtenir_coucher_soleil(data):
    timestamp = data["sys"]["sunset"]
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
def obtenir_donnees_meteo(ville):
    params = {
        "q": ville,
        "appid": API_KEY,
        "units": "metric",
        "lang": "fr"
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
        temperature_actuelle = obtenir_temperature_actuelle(data)
        temperature_ressentie = obtenir_temperature_ressentie(data)
        temp_min, temp_max = obtenir_temperature_min_max(data)
        pression = obtenir_pression_atmospherique(data)
        humidite = obtenir_humidite(data)
        vitesse_vent = obtenir_vitesse_vent(data)
        direction_vent = obtenir_direction_vent(data)
        lever_soleil = obtenir_lever_soleil(data)
        coucher_soleil = obtenir_coucher_soleil(data)
        coordonnees = obtenir_coordonnees(data)

        donnees_meteo = {
            "temperature_actuelle": temperature_actuelle,
            "temperature_ressentie": temperature_ressentie,
            "temp_minimum": temp_min,
            "temp_maximum": temp_max,
            "pression atmospherique": pression,
            "humidite": humidite,
            "vitesse_vent": vitesse_vent,
            "direction_vent": direction_vent,
            "lever_soleil": lever_soleil,
            "coucher_soleil": coucher_soleil,
            "latitude": coordonnees[0],
            "longitude": coordonnees[1]
        }
        
        print(donnees_meteo)
            
        return donnees_meteo
    else:
        print(f"Erreur lors de la récupération des données pour la ville {ville}. Code d'erreur : {response.status_code}")
        return None

# Prévisions météo
# URL de base pour les prévisions API
FORECAST_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

def obtenir_previsions_meteo(ville):
    params = {
        "q": ville,
        "appid": API_KEY,
        "units": "metric",
        "lang": "fr"
    }
    response = requests.get(FORECAST_BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        previsions = []
        for prevision in data["list"]:
            timestamp = prevision["dt"]
            timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            temperature = prevision["main"]["temp"]
            # mettre la température a 0 chiffre après la virgule
            temperature = "{:.0f}".format(temperature)
            temperature = temperature + "°C"
            temps = prevision["weather"][0]["description"]
            previsions.append({"timestamp": timestamp, "temperature": temperature, "temps": temps})
        
        return previsions
    else:
        print(f"Erreur lors de la récupération des prévisions pour la ville {ville}. Code d'erreur : {response.status_code}")
        return None

print(obtenir_previsions_meteo("Paris"))