import folium
import pandas as pd
from folium.plugins import HeatMap
from folium.plugins import HeatMapWithTime
import matplotlib.pyplot as plt

df = pd.read_csv("./data/humdata.csv", encoding='UTF-8', delimiter='\t').drop(columns = ["utilisateur", "apparenttemperaturemintime",
                                                                                         "apparenttemperaturemintime", "apparenttemperaturemax",
                                                                                         "apparenttemperaturemaxtime", "apparenttemperaturehigh",
                                                                                         "apparenttemperaturehightime", "apparenttemperaturelow",
                                                                                         "apparenttemperaturelow",
                                                                                         "apparenttemperaturelowtime",
                                                                                         "datasource",
                                                                                         "temperatureoffset2", "cloudcover","cloudcovererror","uvindex",
                                                                                         "uvindextime","temperaturemintime","temperaturemaxtime","apparenttemperaturemin","windgust",
                                                                                         "windgusttime","windspeed","windbearing",
                                                                                         "temperaturemin","temperaturemax",
                                                                                         "visibility", "geom","precipaccumulation","precipintensitymaxtime",
                                                                                         "precipprobability","precipintensity","precipintensitymax",
                                                                                         "temperaturehightime","temperaturelow","temperaturelowtime",
                                                                                         "dewpoint","summary","icon","sunrisetime","sunsettime","moonphase",
                                                                                         "timezone","autre_info","Unnamed: 0","pressure","village","environnement_precision","date_server","age","precision_geo"])




loc = 'Carte de chaleur (Heat Map) des signalements des tiques sur la région du Grand test de 2017-2019 '
title_html = '''
                 <h6 align="center" style="font-size:16px"><b>{}</b></h6>
                 '''.format(loc)
df.time = pd.to_datetime(df.time, format='%Y-%m-%d %H:%M:%S')
df['year'] = df.time.apply(lambda x: x.year)
df['month'] = df.time.apply(lambda x: x.month)
df['week'] = df.time.apply(lambda x: x.week)
df['day'] = df.time.apply(lambda x: x.day)
df['hour'] = df.time.apply(lambda x: x.hour)
df["moisannee"] = df.time.map(lambda x: x.strftime('%Y-%m'))

df_copy = df.copy()



print(plt.hist(df_copy.month))

print(df_copy.head(5))

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
for moisannee in df_copy.moisannee.sort_values().unique():
    df_hour_list.append(df_copy.loc[df_copy.moisannee == moisannee, ['lat', 'lon', 'count']].groupby(['lat', 'lon']).sum().reset_index().values.tolist())

base_map = generateBaseMap(default_zoom_start=7)
HeatMapWithTime(df_hour_list,min_speed= 3 ,radius=5,index= [str(i) for i in df_copy["moisannee"]], gradient={0.2: 'blue' , 0.4: 'lime', 0.6: 'orange', 1: 'red'}, min_opacity=0.5, max_opacity=0.8, use_local_extrema=True).add_to(base_map)
base_map.get_root().html.add_child(folium.Element(title_html))
base_map.save('heatmap_semaine2.html')
