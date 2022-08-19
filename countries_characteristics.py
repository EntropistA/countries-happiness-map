import pandas as pd # library for data analysis
import numpy as np
import json # library to handle JSON files
from geopy.geocoders import Nominatim 

import requests
import folium # map rendering library
import streamlit as st # creating an app
from streamlit_folium import folium_static 

add_select = st.sidebar.selectbox("What data do you want to see?",("OpenStreetMap", "Stamen Terrain","Stamen Toner"))


map_sby = folium.Map(tiles=add_select, zoom_start=12)
st.title('World Map')

happiness_data = pd.read_parquet("happiness_rank_score_by_country_2022.parquet")
with open("all_countries.geo.json") as f:
    countries_polygons = json.load(f)
happiness_scale = np.linspace(happiness_data["score"].min(), happiness_data["score"].max(), 10).tolist()


def show_maps(threshold_scale):
    folium.Choropleth(geo_data = countries_polygons,
        data = happiness_data,
        columns=['country', "score"],
        key_on='feature.properties.name',
        threshold_scale=threshold_scale,
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Happiness",
        highlight=True,
        reset=True).add_to(map_sby)
    folium_static(map_sby)

show_maps(happiness_scale)