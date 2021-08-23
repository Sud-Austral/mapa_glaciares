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
    df = pd.read_csv(datos, sep=";")

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

    geojson = folium.GeoJson(json.dumps(salida), 
                    name="Límite del complejo glaciar",
                    # tooltip=folium.GeoJsonTooltip(fields=["q1_SN", "q2_SN"])
                    tooltip = folium.GeoJsonTooltip(fields=["Nombre_Gla"],
                    aliases = ['GLACIAR: '])
                    ).add_to(m)

    popup = _popup
    popup.add_to(geojson)

    feature_group = FeatureGroup(name="Subdivisiones glaciar")

    for i in divi:
        
        _union = i
        # print(cut)
        
        df_ = pd.read_csv(datosDiv, sep=",")

        df_ = df_[df_["Id_Union"] == _union]
        indx_ = df_.index[0]

        output_dict_ = [x for x in input_dict_div['features'] if x['properties']['Id_Union'] == str(_union)]

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

    datosDiv = "https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/csv/R10_Lim_Glaciares_FINAL_ClipRegion.csv"
    dfDiv = pd.read_csv(datosDiv, sep=",")

    dfDiv = dfDiv[dfDiv["idZonGlac"] == id]
    indxDiv = dfDiv.index[0]

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
        <h3><center>""" + str(dfDiv["Nombre_GLA"][indxDiv]) + """</center></h3>
        <div>
            <ul>
                <li><b>REGIÓN:</b> """ + str(dfDiv["NOM_REGION"][indxDiv]) + """</li>
                <li><b>PROVINCIA</b> """ + str(dfDiv["NOM_PROVIN"][indxDiv]) + """</li>
                <li><b>COMUNA:</b> """ + str(dfDiv["NOM_COMUNA"][indxDiv]) + """</li>
                <br>
                <li><b>Código de glaciar:</b> """ + str(dfDiv["COD_GLA"][indxDiv]) + """</li>
                <li><b>SUBSUBCUENCA:</b> """ + str(dfDiv["NOM_SSUBC"][indxDiv]) + """</li>
                <br>
                <li><b>Época: </b>""" + str(qtext) + """</li>
                <li><b>Período:</b> """ + str(per) + """</li>
                <li><b>Superficie sin nieve (ha):</b> """ + str('{:,}'.format(round(dfDiv[sn][indxDiv]), 1).replace(',','.')) + """</li>
                <li><b>Superficie ganancia (ha):</b> """ + str('{:,}'.format(round(dfDiv[g][indxDiv]), 1).replace(',','.')) + """</li>
                <li><b>Superficie pérdida (ha):</b> """ + str('{:,}'.format(round(dfDiv[p][indxDiv]), 1).replace(',','.')) + """</li>
                <li><b>Superficie sin cambio (ha):</b> """ + str('{:,}'.format(round(dfDiv[sc][indxDiv]), 1).replace(',','.')) + """</li>
            </ul>
            <center><img src="https://raw.githubusercontent.com/Sud-Austral/mapa_glaciares/main/img/logo_DataIntelligence_normal.png" alt="Data Intelligence"/></center>
        </div>
    """

    iframe_div = folium.IFrame(html=html_div, width=290, height=400)
    _popup_div = folium.Popup(iframe_div, max_width=2650)

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

    popup_div = _popup_div
    popup_div.add_to(geojson_div)

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

    template = """
    {% macro html(this, kwargs) %}

    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dataintelligence</title>
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    
    <script>
    $( function() {
        $( "#maplegend" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });

    </script>
    </head>
    <body>

    
    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
        border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
        
    <div class='legend-title'><b>GLACIARES:</b> """ + str(dfDiv["NOM_REGION"][indxDiv]) + """</div>
    <div class='legend-scale'>
    <ul class='legend-labels'>
        <li><span style='background:#f78820;opacity:0.7;'></span>PÉRDIDA</li>
        <li><span style='background:#2099f7;opacity:0.7;'></span>GANANCIA</li>
    </ul>
    </div>
    </div>
    
    </body>
    </html>

    <style type='text/css'>
    .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
    .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
    .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
    .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
    .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
    .maplegend a {
        color: #777;
        }
    </style>
    {% endmacro %}"""

    macro = MacroElement()
    macro._template = Template(template)

    m.get_root().add_child(macro)

    return m._repr_html_()

if __name__ == '__main__':
    app.run()
