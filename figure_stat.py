import pandas as pd 
import matplotlib.pyplot as plt 
import plotly.express as px
#Import data
df = pd.read_csv("./data/humdata_sort.csv", encoding='UTF-8', delimiter=',')

#Grouper et compter le nombre de signalement par départements 
dept_emp_num =  df.groupby('departement')['departement'].count()

#pourcentage de piqure par départements 
fig = px.pie(df, values='nbr_tique', names='departement')
fig.show()

#pourcentage de piqure par sex
groupe_femme_homme = df.groupby('sex_pique')['sex_pique'].count()
fig = px.pie(df, values='nbr_tique', names='sex_pique')
fig.show()
#raison de présences des individus piqués par les tiques 
groupe_raison_presence = df.groupby('environnement')['environnement'].count()
fig = px.pie(df, values='nbr_tique', names='environnement')
fig.show()
