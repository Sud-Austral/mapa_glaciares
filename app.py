from os import stat
from flask import Flask
import folium
import folium.plugins as plugins
import numpy as np
import pandas as pd
from flask import request
from datetime import datetime, timedelta
from folium.plugins import FloatImage
from folium.plugins import Draw
from folium.plugins import MiniMap
import random
import requests
import geopandas
import json
import requests
import geopandas as gpd
from shapely.geometry import shape
import branca.colormap as cm
from branca.element import Template, MacroElement

app = Flask(__name__)

@app.route('/')
def hello_world():

    codigo = request.args.get("codigo")
    codigo = str(codigo)
    
    url = (
        "https://github.com/Sud-Austral/mapa_glaciares/blob/main/json/"
    )

    datosGlaciar = f"{url}/R10_AREA_Glac_ZONA_glac.json"
    
    m = folium.Map(
        location=[-33.48621795345005, -70.66557950912359],
        zoom_start=8,
        
        )
    
    folium.GeoJson(datosGlaciar, 
                    name="Glaciares",
                    tooltip=folium.GeoJsonTooltip(fields=["idZonGlac", "SUM_Shape_"])
                    ).add_to(m)

    folium.LayerControl().add_to(m)

    return m._repr_html_()

if __name__ == '__main__':
    app.run()
