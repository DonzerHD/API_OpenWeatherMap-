import streamlit as st
from .utils import obtenir_donnees_meteo
import pandas as pd

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

        if meteo_ville is not None:
            st.write(f"Température actuelle à {selected_city}: {meteo_ville['temperature_actuelle']} °C ")
            # Affichez les autres informations météorologiques ici

            coordonnees = meteo_ville["latitude"], meteo_ville["longitude"]
            if coordonnees is not None:
                df = pd.DataFrame({'latitude': [coordonnees[0]], 'longitude': [coordonnees[1]]})
                st.map(df)
        else:
            st.write("Aucune donnée météo disponible pour cette ville.")
    else:
        # Afficher la carte centrée sur la France avec le zoom par défaut
        st.map(pd.DataFrame({'latitude': france_center[0], 'longitude': france_center[1]}, index=[0]), zoom=default_zoom)

