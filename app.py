from flask import Flask
from flask import request
import pandas as pd
import folium
import json
import requests
from folium.plugins import HeatMapWithTime

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
