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
    df = pd.read_csv(datos, sep=";")

    df = df[df["idZonGlac"] == id]
    indx = df.index[0]

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
    output_dict_div = [x for x in input_dict_div['features'] if x['properties']['idZonGlac'] == id]

    salida_div = {'type':'FeatureCollection','features':output_dict_div}
    
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
                <li><b>PROVINCIA</b> """ + str(df["NOM_PROVIN"][indx]) + """</li>
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

    # POPUP PARA SUBDIVISIONES

    html_div="""

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
                <li><b>PROVINCIA</b> """ + str(df["NOM_PROVIN"][indx]) + """</li>
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

    iframe_div = folium.IFrame(html=html_div, width=290, height=350)
    _popup_div = folium.Popup(iframe_div, max_width=2650)

    geojson = folium.GeoJson(json.dumps(salida), 
                    name="Glaciar",
                    # tooltip=folium.GeoJsonTooltip(fields=["q1_SN", "q2_SN"])
                    tooltip = folium.GeoJsonTooltip(fields=["Nombre_Gla"],
                    aliases = ['GLACIAR: '])
                    ).add_to(m)

    popup = _popup
    popup.add_to(geojson)

    geojson_div = folium.GeoJson(json.dumps(salida_div), 
                    name="Glaciar (subdisivión)",
                    tooltip = folium.GeoJsonTooltip(fields=["NOM_SSUBC"],
                    aliases = ['SUBCUENCA: '])
                    ).add_to(m)

    popup_div = _popup_div
    popup_div.add_to(geojson_div)

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
        qtext = "Q1 (Ene-Abr)"
    elif (str(q) == "Q2"):
        q = "Q2"
        qtext = "Q2 (May-Dic)"
    else:
        q = "Inválido"

    

    if (str(periodo) == "17-18" and str(q) == "Q1"):
        per = "2017 - 2018"
        sn = "SN_1718q1"
        g = "G_1718q1"
        p = "P_1718q1"
        sc = "SC_1718q1"
        capa = "glaciares_r10:1718q1"
        nombre = "Q1 (Ene-Abr) 2017-2018"

    elif (str(periodo) == "18-19" and str(q) == "Q1"):
        per = "P2018 - 2019"
        sn = "SN_1819q1"
        g = "G_1819q1"
        p = "P_1819q1"
        sc = "SC_1819q1"
        capa = "glaciares_r10:1819q1"
        nombre = "Q1 (Ene-Abr) 2018-2019"

    elif (str(periodo) == "19-20" and str(q) == "Q1"):
        per = "2019 - 2020"
        sn = "SN_1920q1"
        g = "G_1920q1"
        p = "P_1920q1"
        sc = "SC_1920q1"
        capa = "glaciares_r10:1920q1"
        nombre = "Q1 (Ene-Abr) 2019-2020"

    elif (str(periodo) == "20-21" and str(q) == "Q1"):
        per = "2020 - 2021"
        sn = "SN_2021q1"
        g = "G_2021q1"
        p = "P_2021q1"
        sc = "SC_2021q1"
        capa = "glaciares_r10:2021q1"
        nombre = "Q1 (Ene-Abr) 2020-2021"

    elif (str(periodo) == "17-18" and str(q) == "Q2"):
        per = "2017 - 2018"
        sn = "SN_1718q2"
        g = "G_1718q2"
        p = "P_1718q2"
        sc = "SC_1718q2"
        capa = "glaciares_r10:1718q2"
        nombre = "Q2 (May-Dic) 2017-2018"

    elif (str(periodo) == "18-19" and str(q) == "Q2"):
        per = "2018 - 2019"
        sn = "SN_1819q2"
        g = "G_1819q2"
        p = "P_1819q2"
        sc = "SC_1819q2"
        capa = "glaciares_r10:1819q2"
        nombre = "Q2 (May-Dic) 2018-2019"

    elif (str(periodo) == "19-20" and str(q) == "Q2"):
        per = "2019 - 2020"
        sn = "SN_1920q2"
        g = "G_1920q2"
        p = "P_1920q2"
        sc = "SC_1920q2"
        capa = "glaciares_r10:1920q2"
        nombre = "Q2 (May-Dic) 2020-2021"

    else:
        pass

    datos = "https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/csv/R10_AREA_Glac_ZONA_glac.csv"
    df = pd.read_csv(datos, sep=";")

    df = df[df["idZonGlac"] == id]
    indx = df.index[0]

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
    output_dict_div = [x for x in input_dict_div['features'] if x['properties']['idZonGlac'] == id]

    salida_div = {'type':'FeatureCollection','features':output_dict_div}

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
                width: 50%;
                height: auto;
            }

            .banner{
                width: 100%;
                height: auto;
            }
        </style>

        <center><img class="banner" src="https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/img/Glaciares_top.jpg" alt="Data Intelligence"/></center>
        <br>
        <h3><center>""" + str(df["Nombre_Gla"][indx]) + """</center></h3>
        <div>
            <ul>
                <li><b>REGIÓN:</b> """ + str(df["NOM_REGION"][indx]) + """</li>
                <li><b>PROVINCIA</b> """ + str(df["NOM_PROVIN"][indx]) + """</li>
                <li><b>COMUNA:</b> """ + str(df["NOM_COMUNA"][indx]) + """</li>
                <br>
                <li><b>Época: </b>""" + str(qtext) + """</li>
                <li><b>Período:</b> """ + str(per) + """</li>
                <li><b>Superficie sin nieve (ha):</b> """ + str('{:,}'.format(round(df[sn][indx]), 1).replace(',','.')) + """</li>
                <li><b>Superficie ganancia (ha):</b> """ + str('{:,}'.format(round(df[g][indx]), 1).replace(',','.')) + """</li>
                <li><b>Superficie pérdida (ha):</b> """ + str('{:,}'.format(round(df[p][indx]), 1).replace(',','.')) + """</li>
                <li><b>Superficie sin cambio (ha):</b> """ + str('{:,}'.format(round(df[sc][indx]), 1).replace(',','.')) + """</li>
            </ul>
            <br>
            <center><img class="banner" src="https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/img/Glaciares_bottom.jpg" alt="Data Intelligence"/></center>
        </div>
    """

    iframe = folium.IFrame(html=html, width=280, height=400)
    _popup = folium.Popup(iframe, max_width=2650)


    geojson = folium.GeoJson(json.dumps(salida), 
                    name="Glaciar",
                    style_function = lambda feature: {
                                "fillColor": "transparent"
                                if feature["properties"]["idZonGlac"] > 0
                                else "transparent",
                                "color": "#b2ff00",
                                "weight": 3,
                                "dashArray": "5, 5",
                            },
                    tooltip = folium.GeoJsonTooltip(fields=["Nombre_Gla"],
                    aliases = ['GLACIAR: '])
                    ).add_to(m)

    popup = _popup
    popup.add_to(geojson)

    geojson_div = folium.GeoJson(json.dumps(salida_div), 
                    name="Glaciar (subdisivión)",
                    style_function = lambda feature: {
                                "fillColor": "transparent"
                                if feature["properties"]["idZonGlac"] > 0
                                else "transparent",
                                "color": "#edff37",
                                "weight": 3,
                            },
                    tooltip = folium.GeoJsonTooltip(fields=["NOM_SSUBC"],
                    aliases = ['SUBCUENCA: '])
                    ).add_to(m)

    # GEOSERVICIOS

    # codComuna = "CQL_FILTER=COMUNA=" + idGeo
    # geoq11718 = folium.WmsTileLayer(url = 'https://ide.dataintelligence-group.com/geoserver/glaciares_r10/wms?' + codComuna,
    geoq11718 = folium.WmsTileLayer(url = 'https://ide.dataintelligence-group.com/geoserver/glaciares_r10/wms?',
                        layers = capa,
                        fmt ='image/png',
                        transparent = True,
                        name = nombre,
                        control = True,
                        attr = "Mapa de Chile"
                        )

    
    geoq11718.add_to(m)

    folium.LayerControl().add_to(m)

    return m._repr_html_()

if __name__ == '__main__':
    app.run()
