from flask import Flask
from flask import request
import pandas as pd
import numpy as np
import folium
import json
import random
import requests
from folium.plugins import HeatMapWithTime
from branca.element import Template, MacroElement
from folium import FeatureGroup, LayerControl, Map, Marker

app = Flask(__name__)

@app.route('/')
def mapa():
   
    try:
        id = request.args.get("id")
        id = int(id)
    except:
        id = 1
    
    datos = "https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/csv/R10_AREA_Glac_ZONA_glac.csv"
    df = pd.read_csv(datos, sep=",")

    df = df[df["idZonGlac"] == id]
    indx = df.index[0]

    datosDiv = "https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/csv/R10_Lim_Glaciares_FINAL_ClipRegion.csv"
    dfDiv = pd.read_csv(datosDiv, sep=",")

    dfSubc = dfDiv[dfDiv["idZonGlac"] == id]
    divi = dfSubc["Id_Union"].unique().tolist()
    divi

    url = (
        "https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/json"
    )

    datosGlaciar = f"{url}/R10_AREA_Glac_ZONA_glac.json"

    input_dict = json.loads(requests.get(datosGlaciar).content)
    output_dict = [x for x in input_dict['features'] if x['properties']['idZonGlac'] == id]

    salida = {'type':'FeatureCollection','features':output_dict}

    # JSON Glaciar divisiones

    glaciarDivisiones = f"{url}/R10_Lim_Glaciares_FINAL_ClipRegion.json"

    input_dict_div = json.loads(requests.get(glaciarDivisiones).content)
    
    if (id != ""):
        ubicacion = [float(df["Y"][indx]), float(df["X"][indx])]
    else:
        ubicacion = [-33.48621795345005, -70.66557950912359]

    m = folium.Map(
        location=ubicacion,
        zoom_start=13,
        
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

            img{
                width: 70%;
                height: auto;
            }

            .banner{
                width: 100%;
                height: auto;
            }
        </style>
        <center><img class="banner" src="https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/img/Glaciares.jpg" alt="Data Intelligence"/></center>
        <br>
        <h3><center>""" + str(df["Nombre_Gla"][indx]) + """</center></h3>
        <div>
            <ul>
                <li><b>REGIÓN:</b> """ + str(df["NOM_REGION"][indx]) + """</li>
                <li><b>PROVINCIA: </b> """ + str(df["NOM_PROVIN"][indx]) + """</li>
                <li><b>COMUNA:</b> """ + str(df["NOM_COMUNA"][indx]) + """</li>
                <br>
                <li><b>Q1 (Ene-Abr) Mínima (ha):</b> """ + str('{:,}'.format(round(df["q1_Min"][indx]), 1).replace(',','.')) + """</li>
                <li><b>Q1 (Ene-Abr) Máxima (ha):</b> """ + str('{:,}'.format(round(df["q1_Max"][indx]), 1).replace(',','.')) + """</li>
                <br>
                <li><b>Q2 (May-Dic) Mínima (ha):</b> """ + str('{:,}'.format(round(df["q2_Min"][indx]), 1).replace(',','.')) + """</li>
                <li><b>Q2 (May-Dic) Máxima (ha):</b> """ + str('{:,}'.format(round(df["q2_Max"][indx]), 1).replace(',','.')) + """</li>
            </ul>
            <center><img src="https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/img/logo_DataIntelligence_normal.png" alt="Data Intelligence"/></center>
        </div>
    """

    iframe = folium.IFrame(html=html, width=290, height=350)
    _popup = folium.Popup(iframe, max_width=2650)

    geojson = folium.GeoJson(json.dumps(salida), 
                    name="Complejo glaciar",
                    # tooltip=folium.GeoJsonTooltip(fields=["q1_SN", "q2_SN"])
                    tooltip = folium.GeoJsonTooltip(fields=["Nombre_Gla"],
                    aliases = ['GLACIAR: '])
                    ).add_to(m)

    popup = _popup
    popup.add_to(geojson)

    feature_group = FeatureGroup(name="Sectores del complejo glaciar")

    for i in divi:
        
        _union = i
        # print(cut)
        
        df_ = pd.read_csv(datosDiv, sep=",")

        df_ = df_[df_["Id_Union"] == _union]
        indx_ = df_.index[0]

        output_dict_ = [x for x in input_dict_div['features'] if x['properties']['Id_Union'] == _union]

        salida_ = {'type':'FeatureCollection','features':output_dict_}

        if(df_["COD_GLA"][indx_] is np.nan):
            codGla = "No definido"
        else:
            codGla = df_["COD_GLA"][indx_]

        htmlDiv="""

            <style>
                *{
                    font-family: Arial, Tahoma;
                    font-size: 13px;
                }
                
                li{
                    list-style:none;
                    margin-left: -40px;
                }

                img{
                    width: 70%;
                    height: auto;
                }

                .banner{
                    width: 100%;
                    height: auto;
                }
            </style>
            <center><img class="banner" src="https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/img/Glaciares.jpg" alt="Data Intelligence"/></center>
            <br>
            <h3><center>""" + str(df_["Nombre_GLA"][indx_]) + """</center></h3>
            <div>
                <ul>
                    <li><b>REGIÓN:</b> """ + str(df_["NOM_REGION"][indx_]) + """</li>
                    <li><b>PROVINCIA</b> """ + str(df_["NOM_PROVIN"][indx_]) + """</li>
                    <li><b>COMUNA:</b> """ + str(df_["NOM_COMUNA"][indx_]) + """</li>
                    <br>
                    <li><b>CÓDIGO GLACIAR:</b> """ + str(codGla) + """</li>
                    <li><b>SUBSUBCUENCA:</b> """ + str(df_["NOM_SSUBC"][indx_]) + """</li>
                    <br>
                    <li><b>Q1 (Ene-Abr) Mínima (ha):</b> """ + str('{:,}'.format(round(df_["q1_Min"][indx_]), 1).replace(',','.')) + """</li>
                    <li><b>Q1 (Ene-Abr) Máxima (ha):</b> """ + str('{:,}'.format(round(df_["q1_Max"][indx_]), 1).replace(',','.')) + """</li>
                    <br>
                    <li><b>Q2 (May-Dic) Mínima (ha):</b> """ + str('{:,}'.format(round(df_["q2_Min"][indx_]), 1).replace(',','.')) + """</li>
                    <li><b>Q2 (May-Dic) Máxima (ha):</b> """ + str('{:,}'.format(round(df_["q2_Max"][indx_]), 1).replace(',','.')) + """</li>
                </ul>
                <center><img src="https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/img/logo_DataIntelligence_normal.png" alt="Data Intelligence"/></center>
            </div>
        """

        iframeDiv = folium.IFrame(html=htmlDiv, width=290, height=400)
        _popupDiv = folium.Popup(iframeDiv, max_width=2650)

        def colormap(feature):
            if feature["properties"]["idZonGlac"] > 0:
                r = lambda: random.randint(0,255)
                hexaColor = '#%02X%02X%02X' % (r(),r(),r())
            else:
                hexaColor = 'transparent'

            return hexaColor

        geojsonDiv = folium.GeoJson(json.dumps(salida_),
                       tooltip = folium.GeoJsonTooltip(fields=["NOM_SSUBC"],
                       aliases = ['SUBSUBCUENCA: ']),
                       style_function=lambda feature: {
                            "fillColor": colormap(feature)
                        },
                        ).add_to(feature_group)

        popupDiv = _popupDiv
        popupDiv.add_to(geojsonDiv)

    feature_group.add_to(m)
    folium.LayerControl().add_to(m)

    return m._repr_html_()


if __name__ == '__main__':
    app.run()
