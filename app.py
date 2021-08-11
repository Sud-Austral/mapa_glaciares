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
        id = request.args.get("id")
        id = int(id)
    except:
        id = 1
    
    datos = "https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/csv/R10_AREA_Glac_ZONA_glac.csv"
    df = pd.read_csv(datos)

    df = df[df["idZonGlac"] == id]
    indx = df.index[0]

    url = (
        "https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/json/"
    )

    datosGlaciar = f"{url}/R10_AREA_Glac_ZONA_glac.json"

    input_dict = json.loads(requests.get(datosGlaciar).content)
    output_dict = [x for x in input_dict['features'] if x['properties']['idZonGlac'] == id]

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
                <li><b>Q1 SN:</b> """ + str(df["q1_SN"][indx]) + """</li>
                <li><b>Q1 Mínimo:</b> """ + str(df["q1_Min"][indx]) + """</li>
                <li><b>Q1 Máximo:</b> """ + str(df["q1_Max"][indx]) + """</li>
                <li><b>Q1 Sin nieve, 2017 - 2018:</b> """ + str(df["SN_1718q1"][indx]) + """</li>
                <li><b>Q1 Ganancia, 2017 - 2018:</b> """ + str(df["G_1718q1"][indx]) + """</li>
                <li><b>Q1 Pérdida, 2017 - 2018:</b> """ + str(df["P_1718q1"][indx]) + """</li>
                <li><b>Q1 SC, 2017 - 2018:</b> """ + str(df["SC_1718q1"][indx]) + """</li>
            </ul>
        </div>
    """

    iframe = folium.IFrame(html=html, width=250, height=210)
    _popup = folium.Popup(iframe, max_width=2650)

    geojson = folium.GeoJson(json.dumps(salida), 
                    name="Glaciares",
                    # tooltip=folium.GeoJsonTooltip(fields=["q1_SN", "q2_SN"])
                    tooltip = folium.GeoJsonTooltip(fields=["q1_SN", "q2_SN"],
                    aliases = ['Q1 sin nieve:', 'Q2 sin nieve:']),
                    popup="Soy un popup",
                     style_function = lambda feature: {
                        'fillOpacity': 0.5,
                        'weight': 0.5,
                        'color': "#8b0000",
                        'fillColor': "#d4d4d4"
                    }
                    ).add_to(m)

    popup = _popup
    popup.add_to(geojson)

    folium.LayerControl().add_to(m)

    return m._repr_html_()

if __name__ == '__main__':
    app.run()
