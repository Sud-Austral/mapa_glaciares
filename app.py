from flask import Flask
from flask import request
import pandas as pd
import folium
import json
import requests
from folium.plugins import HeatMapWithTime

app = Flask(__name__)

@app.route('/')
def mapa():

    try:
        id = request.args.get("cod")
        id = str(id)
    except:
        id = 1
    
    datos = "https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/csv/R10_Lim_Glaciares_FINAL_ClipRegion.csv"
    df = pd.read_csv(datos)

    df = df[df["COD_GLA"] == id]
    indx = df.index[0]

    url = (
        "https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/json/"
    )

    datosGlaciar = f"{url}/R10_Lim_Glaciares_FINAL_ClipRegion_30p.json"

    input_dict = json.loads(requests.get(datosGlaciar).content)
    output_dict = [x for x in input_dict['features'] if x['properties']['COD_GLA'] == id]

    salida = {'type:':'FeatureCollection','features':output_dict}
    
    m = folium.Map(
        location=[-33.48621795345005, -70.66557950912359],
        zoom_start=8,
        
        )
    
    html="""

        <style>
            *{
                font-family: Arial, Tahoma;
                font-size: 13px;
            }
            
            li{
                list-style:none;
                margin-left: -40px;
            }

        </style>

        <h3>Datos e información</h3>
        <div>
            <ul>
                <li><b>Q1 SN:</b> """ + str(df["REGION"][indx]) + """</li>
            </ul>
        </div>
    """

    iframe = folium.IFrame(html=html, width=250, height=210)
    _popup = folium.Popup(iframe, max_width=2650)


    geojson = folium.GeoJson(json.dumps(salida), 
                    name="Glaciares R10",
                    # tooltip=folium.GeoJsonTooltip(fields=["q1_SN", "q2_SN"])
                    tooltip = folium.GeoJsonTooltip(fields=["REGION", "COMUNA"],
                    aliases = ['REGIÓN:', 'COMUNA:'])
                    ).add_to(m)

    popup = _popup
    popup.add_to(geojson)

    folium.LayerControl().add_to(m)

    return m._repr_html_()

if __name__ == '__main__':
    app.run()
