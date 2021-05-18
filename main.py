from flask import Flask, render_template
import folium
import csv
from csv import DictReader
# app = Flask(__name__)
import folium
import folium.plugins
import PopupCostum

loc = ' Piqures de tiques signalées depuis le site internet ou l’application pour smartphone signalement tique sur la région du Grand test de 2017-2019 '
title_html = '''
                 <h5 align="center" style="font-size:16px"><b>{}</b></h5>
                 '''.format(loc)


fond_carte = r'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'

map_france = folium.Map(location=[48.711, 6.680],
                            zoom_start=7,
                            tiles=fond_carte, attr= "basemap.cartocdn", name='Fond de Carte')


folium.GeoJson('./data/region-grand-est.geojson',
               name ='Region-grand-est'
              ).add_to(map_france)

fg1=folium.FeatureGroup(name='Signalements 2017', show=False).add_to(map_france)
fg2=folium.FeatureGroup(name='Signalements 2018', show=False).add_to(map_france)
fg3=folium.FeatureGroup(name='Signalements 2019', show=False).add_to(map_france)
fg5=folium.FeatureGroup(name='Signalements 2017-2019', show=True).add_to(map_france)

tiques_cluster17 = folium.plugins.MarkerCluster().add_to(fg1)
tiques_cluster18 = folium.plugins.MarkerCluster().add_to(fg2)
tiques_cluster19 = folium.plugins.MarkerCluster().add_to(fg3)
tiques_cluster1719 = folium.plugins.MarkerCluster().add_to(fg5)

with open('./data/humdata.csv', 'r',encoding='UTF-8') as fp :
    csv_dict_reader = DictReader(fp, delimiter='\t')
    # la liste des nom des attrbuts :
    column_names = csv_dict_reader.fieldnames

    for row in csv_dict_reader:

        latitude = row["lat"]
        longitude = row["lon"]

        valeurs_popup= PopupCostum.popup(row["annee_extract"], row["sex_pique"],
                                                            row["environnement"], row["raison_presence"],
                                                            row["departement"])
        folium.Marker([latitude, longitude],
                      popup=valeurs_popup,
                      icon=folium.Icon(color='green', icon='certificate'),
                      tooltip="Cliquez Ici"
                      ).add_to(tiques_cluster1719)
        if row["annee_extract"] == "2017":
            #valeurs_popup = PopupCostum.popup(row["annee_extract"])
            latitude = row["lat"]
            longitude = row["lon"]

            folium.Marker([latitude, longitude],
                          popup=valeurs_popup,
                          icon=folium.Icon(color='green', icon='certificate'),
                          tooltip= "Cliquez Ici"
                          ).add_to(tiques_cluster17)
        elif row["annee_extract"] == "2018":
            folium.Marker([latitude, longitude],
                          popup=valeurs_popup,
                          icon=folium.Icon(color='red', icon='certificate'),
                          tooltip="Cliquez Ici"
                          ).add_to(tiques_cluster18)
        elif row["annee_extract"] == "2019":
            #valeurs_popup = PopupCostum.popup(row["annee_extract"])
            folium.Marker([latitude, longitude],
                          popup=valeurs_popup,
                          icon=folium.Icon(color='red', icon='certificate'),
                          tooltip="Cliquez Ici"
                          ).add_to(tiques_cluster19)

map_france.add_child(fg1)

folium.LayerControl(position='bottomright', collapsed=False, autoZIndex=True).add_to(map_france)
folium.plugins.Geocoder(collapsed=True, position='topright', add_marker=False,).add_to(map_france)

map_france.get_root().html.add_child(folium.Element(title_html))
map_france.save("tique.html")









