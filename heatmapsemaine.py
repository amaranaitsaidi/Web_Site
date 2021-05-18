import folium
import pandas as pd
from folium.plugins import HeatMap
from folium.plugins import HeatMapWithTime
import matplotlib.pyplot as plt

df = pd.read_csv("./data/humdata_sort.csv", encoding='UTF-8', delimiter=',')



loc = 'Carte de chaleur (Heat Map) des signalements des tiques sur la région du Grand test de 2017-2019 '
title_html = '''
                 <h6 align="center" style="font-size:16px"><b>{}</b></h6>
                 '''.format(loc)


df_copy = df.copy()

df_copy["count"] = 1

def generateBaseMap(default_location=[48.711, 6.680], default_zoom_start = 0,
                    fond_carte = r'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'):
    map_france = folium.Map(location = default_location,
                            zoom_start=default_zoom_start,
                            tiles=fond_carte, attr="fond_OSM")
    folium.GeoJson('./data/region-grand-est.geojson',
                   name ='geojson'
                   ).add_to(map_france)
    return map_france

df_copy['count'] = 1
base_map = generateBaseMap()
HeatMap(data=df_copy[['lat', 'lon', 'count']].groupby(['lat', 'lon']).sum().reset_index().values.tolist(), radius=8).add_to(base_map)
df_hour_list = []
for week in df_copy.week.sort_values().unique():
    df_hour_list.append(df_copy.loc[df_copy.week == week, ['lat', 'lon', 'count']].groupby(['lat', 'lon']).sum().reset_index().values.tolist())

base_map = generateBaseMap(default_zoom_start=7)
HeatMapWithTime(df_hour_list,min_speed= 3 ,radius=5, gradient={0.2: 'blue' , 0.4: 'lime', 0.6: 'orange', 1: 'red'}, min_opacity=0.5, max_opacity=0.8, use_local_extrema=True).add_to(base_map)
base_map.get_root().html.add_child(folium.Element(title_html))
base_map.save('heatmap_semaine2.html')
