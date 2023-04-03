import streamlit as st
from .utils import obtenir_donnees_meteo , obtenir_previsions_meteo
import pandas as pd
import sqlite3
import datetime

def main():
    # Titre de l'application
    st.title("Météo des villes")

    # Saisie de la ville
    selected_city = st.text_input("Entrez le nom de la ville:")

    # Coordonnées et zoom par défaut pour la France
    france_center = [46.603354, 1.888334]
    default_zoom = 4

    if st.button("Valider"):
        meteo_ville = obtenir_donnees_meteo(selected_city)
        prevision_meteo = obtenir_previsions_meteo(selected_city)

        if meteo_ville is not None:
            # Informations météorologiques
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Température actuelle: {meteo_ville['temperature_actuelle']} °C ")
                st.write(f"Température ressentie: {meteo_ville['temperature_ressentie']} °C ")
                st.write(f"Température minimale: {meteo_ville['temp_minimum']} °C ")
                st.write(f"Température maximale: {meteo_ville['temp_maximum']} °C ")
            with col2:
                st.write(f"Pression atmosphérique: {meteo_ville['pression atmospherique']} hPa ")
                st.write(f"Humidité: {meteo_ville['humidite']} % ")
                st.write(f"Vitesse du vent: {meteo_ville['vitesse_vent']} m/s ")
                st.write(f"Direction du vent: {meteo_ville['direction_vent']} ° ")
                st.write(f"Lever du soleil: {meteo_ville['lever_soleil']} ")
                st.write(f"Coucher du soleil: {meteo_ville['coucher_soleil']} ")
                
            # faire les prévisions pour la ville sélectionnée
            # afficher les prévisions sous forme de graphique
            st.write("Prévisions météo :")
            # Création d'un dataframe à partir des prévisions
            df = pd.DataFrame(prevision_meteo)
            # fait un tableau avec les prévisions
            st.table(df)
    

            # Carte
            coordonnees = meteo_ville["latitude"], meteo_ville["longitude"]
            if coordonnees is not None:
                st.map(pd.DataFrame({'latitude': [coordonnees[0]], 'longitude': [coordonnees[1]]}))

            # Enregistrement des données dans la base de données
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn = sqlite3.connect('appli/meteo.db')
            conn.execute("CREATE TABLE IF NOT EXISTS meteo (ville TEXT, date TEXT, temperature_actuelle REAL, temperature_ressentie REAL, temp_minimum REAL, temp_maximum REAL, pression REAL, humidite REAL, vitesse_vent REAL, direction_vent REAL, lever_soleil TEXT, coucher_soleil TEXT)")
            conn.execute("INSERT INTO meteo VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                         (selected_city, date, meteo_ville['temperature_actuelle'], meteo_ville['temperature_ressentie'], 
                          meteo_ville['temp_minimum'], meteo_ville['temp_maximum'], meteo_ville['pression atmospherique'], 
                          meteo_ville['humidite'], meteo_ville['vitesse_vent'], meteo_ville['direction_vent'], 
                          meteo_ville['lever_soleil'], meteo_ville['coucher_soleil']))
            conn.commit()
            conn.close()

        else:
            st.write("Aucune donnée météo disponible pour cette ville.")

    else:
    # Afficher la carte centrée sur la France avec le zoom par défaut
        st.map(pd.DataFrame({'latitude': [france_center[0]], 'longitude': [france_center[1]]}), zoom=default_zoom)