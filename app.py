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
    
    datos = "https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/csv/R10_Lim_Glaciares_FINAL_ClipRegion.csv"
    df = pd.read_csv(datos)

    df = df[df["idZonGlac"] == id]
    indx = df.index[0]

    url = (
        "https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/json"
    )

    datosGlaciar = f"{url}/R10_Lim_Glaciares_FINAL_ClipRegion_30p.json"

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

        <h3>GLACIARES R10</h3>
        <div>
            <ul>
                <li><b>REGIÓN:</b> """ + str(df["NOM_REGION"][indx]) + """</li>
                <li><b>PROVINCIA</b> """ + str(df["NOM_PROVIN"][indx]) + """</li>
                <li><b>COMUNA:</b> """ + str(df["NOM_COMUNA"][indx]) + """</li>
                <br>
                <li><b>Q1 Mínima:</b> """ + str(df["q1_Min"][indx]) + """</li>
                <li><b>Q1 Máxima:</b> """ + str(df["q1_Max"][indx]) + """</li>
                <br>
                <li><b>Q2 Mínima:</b> """ + str(df["q2_Min"][indx]) + """</li>
                <li><b>Q2 Máxima:</b> """ + str(df["q2_Max"][indx]) + """</li>
            </ul>
        </div>
    """

    iframe = folium.IFrame(html=html, width=250, height=210)
    _popup = folium.Popup(iframe, max_width=2650)


    geojson = folium.GeoJson(json.dumps(salida), 
                    name="Glaciares R10",
                    # tooltip=folium.GeoJsonTooltip(fields=["q1_SN", "q2_SN"])
                    tooltip = folium.GeoJsonTooltip(fields=["Nombre_GLA"],
                    aliases = ['GLACIAR: '])
                    ).add_to(m)

    popup = _popup
    popup.add_to(geojson)

    folium.LayerControl().add_to(m)

    return m._repr_html_()


@app.route('/periodo')
def mapaPeriodo():

    try:
        id = request.args.get("id")
        id = int(id)

        q = request.args.get("q")
        periodo = request.args.get("p")

    except:
        id = 1
    
    if (str(q) == "Q1"):
        q = "Q1"
    elif (str(q) == "Q2"):
        q = "Q2"
    else:
        q = "Inválido"


    datos = "https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/csv/R10_Lim_Glaciares_FINAL_ClipRegion.csv"
    df = pd.read_csv(datos)

    df = df[df["idZonGlac"] == id]
    indx = df.index[0]

    url = (
        "https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/json"
    )

    datosGlaciar = f"{url}/R10_Lim_Glaciares_FINAL_ClipRegion_30p.json"

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

        <h3>GLACIARES R10</h3>
        <div>
            <ul>
                <li><b>REGIÓN:</b> """ + str(df["NOM_REGION"][indx]) + """</li>
                <li><b>PROVINCIA</b> """ + str(df["NOM_PROVIN"][indx]) + """</li>
                <li><b>COMUNA:</b> """ + str(df["NOM_COMUNA"][indx]) + """</li>
                <br>
                <li><b>Q1 Mínima:</b> """ + str(q) + """</li>
                <li><b>Q1 Mínima:</b> """ + str(df["q1_Min"][indx]) + """</li>
                <li><b>Q1 Máxima:</b> """ + str(df["q1_Max"][indx]) + """</li>
                <br>
                <li><b>Q2 Mínima:</b> """ + str(df["q2_Min"][indx]) + """</li>
                <li><b>Q2 Máxima:</b> """ + str(df["q2_Max"][indx]) + """</li>
            </ul>
        </div>
    """

    iframe = folium.IFrame(html=html, width=250, height=210)
    _popup = folium.Popup(iframe, max_width=2650)


    geojson = folium.GeoJson(json.dumps(salida), 
                    name="Glaciares R10",
                    # tooltip=folium.GeoJsonTooltip(fields=["q1_SN", "q2_SN"])
                    tooltip = folium.GeoJsonTooltip(fields=["Nombre_GLA"],
                    aliases = ['GLACIAR: '])
                    ).add_to(m)

    popup = _popup
    popup.add_to(geojson)

    folium.LayerControl().add_to(m)

    return m._repr_html_()

if __name__ == '__main__':
    app.run()
