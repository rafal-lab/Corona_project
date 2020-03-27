
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
plt.rcParams['figure.figsize'] = [15, 5]
from IPython import display
from ipywidgets import interact, widgets
import pandas as pd
import time

def give_SUM(frame,country):
    nb_of_cases_in_Italy = frame.loc[frame['Countries and territories'] == f'{country}']

    lista = list(nb_of_cases_in_Italy["Cases"])


    lista.reverse()

    for i in range(len(lista)):
        if (i == 0):
            pass
        else:
            lista[i] += lista[i - 1]
    lista.reverse()
    lista = np.asarray(lista)

    return lista
def give_Death(frame,country):
    nb_of_cases_in_Italy = frame.loc[frame['Countries and territories'] == f'{country}']

    lista = list(nb_of_cases_in_Italy["Deaths"])


    lista.reverse()

    for i in range(len(lista)):
        if (i == 0):
            pass
        else:
            lista[i] += lista[i - 1]
    lista.reverse()
    lista = np.asarray(lista)

    return lista



xml=pd.read_excel(r'https://github.com/rafal-lab/Corona_project/blob/master/COVID-19-geographic-disbtribution-worldwide-2020-03-24.xlsx')
frame=pd.DataFrame(xml)
df=frame
zh=df.loc[df["Countries and territories"]=="Poland",:].sort_values(by='Cases').tail(10).head(9).style.background_gradient(cmap='magma').highlight_null('red')
print(zh)
time.sleep(50)

Poland=frame.loc[frame['Countries and territories']=='Poland']


rysunek=Poland.plot(y='Cases',x='DateRep', figsize=(12,8), marker='*', title='Liczba przypadków COVID-19 w Polsce danego dnia', grid=True)
#plt.show()

deathPoland=Poland[['DateRep','Deaths']]
wskazniksmierci=deathPoland.plot(y='Deaths',x='DateRep', figsize=(12,8), marker='o', title="Liczba zgonów każdego dnia")
#plt.show()


formated_gdf=frame.groupby(['Countries and territories']).max()
formated_gdf=formated_gdf.loc[formated_gdf['Deaths']>0]
formated_gdf['size'] = formated_gdf['Deaths'].pow(0.3)
formated_gdf =  formated_gdf.reset_index()

fig = px.scatter_geo(formated_gdf, locations="Countries and territories", locationmode='country names',
                     color="Deaths", size='size', hover_name="Countries and territories",
                     range_color= [0, 80],
                     projection="natural earth",
                     title="Liczba smierci 24.03.2020 COVID-19 na swiecie"
                     )

#fig.show()

fig2 = px.choropleth(formated_gdf, locations="Countries and territories", locationmode='country names',
                     color="Deaths", hover_name="Countries and territories",
                     range_color= [0, 150],
                     projection="natural earth",
                     title='Smiertelnosc COVID19 na swiecie')
#fig2.show()

nb_of_cases_in_Italy=frame.loc[frame['Countries and territories']=='Italy']

lista=list(nb_of_cases_in_Italy["Cases"])
nb_cs=pd.DataFrame(nb_of_cases_in_Italy)

lista.reverse()

for i in range(len(lista)):
    if(i==0):
        pass
    else:
        lista[i]+=lista[i-1]
lista.reverse()
lista=np.asarray(lista)


nb_cs['sum_in_Italy']=lista

cases_Italy_print=nb_cs.plot(x='DateRep',y='sum_in_Italy',figsize=(12,8), marker='o', title="Liczba przypadkow we Włoszech",grid=True)


Hiszpania=pd.DataFrame(frame.loc[frame['Countries and territories']=='Spain'])

cases_in_spain=np.array(Hiszpania['Cases'])
death_in_spain=np.array(Hiszpania['Deaths'])
nb_cs['cs_in_Spain']=cases_in_spain
nb_cs['dth_in_Spain']=death_in_spain
nb_cs=nb_cs.rename(columns={'Cases':"cs_in_Italy"})
nb_cs=nb_cs.rename(columns={'Deaths':"dth_in_Italy"})

USA=pd.DataFrame(frame.loc[frame['Countries and territories']=='USA'])
cases_in_USA=np.array(USA['Cases'])
death_in_USA=np.array(USA['Deaths'])
nb_cs['cs_in_USA']=cases_in_USA
nb_cs['dth_in_USA']=death_in_USA



sum_in_spain=give_SUM(frame,'Spain')
sum_in_USA=give_SUM(frame,"USA")
nb_cs['sum_in_USA']=sum_in_USA
nb_cs['sum_in_Spain']=sum_in_spain


sum_dth_Spain=give_Death(frame,"Spain")
sum_dth_USA=give_Death(frame,"USA")
sum_dth_Italy=give_Death(frame,"Italy")
nb_cs['sum_dth_in_Spain']=sum_dth_Spain
nb_cs['sum_dth_in_Italy']=sum_dth_Italy
nb_cs['sum_dth_in_USA']=sum_dth_USA
#print(nb_cs)
nb_cs.plot(y=['cs_in_Italy', 'cs_in_Spain','cs_in_USA'], x='DateRep',figsize=(12,8), marker='o', title='Wykres ilości nowych przypadków w Hiszpani, Włoszech i USA,każdego dnia',grid=True)
nb_cs.plot(y=['dth_in_Italy', 'dth_in_Spain','dth_in_USA'], x='DateRep',figsize=(12,8), marker='o', title='Wykres ilości śmierci w Hiszpani, Włoszech i USA,każdego dnia',grid=True)

nb_cs.plot(y=['sum_in_Spain', 'sum_in_USA','sum_in_Italy'], x='DateRep',figsize=(12,8), marker='o', title='Wykres sumarycznej ilości przypadkow w Hiszpani, Włoszech i USA')
nb_cs.plot(y=['sum_dth_in_Spain', 'sum_dth_in_USA','sum_dth_in_Italy'], x='DateRep',figsize=(12,8), marker='o', title='Wykres sumarycznej ilości śmierci w Hiszpani, Włoszech i USA')
#plt.show()

allcountry=pd.read_csv('word.csv')
USA=allcountry.loc[allcountry['Country/Region']=='US'].sort_values(by='3/23/20')
USA=USA.fillna(value=0)
us=pd.DataFrame(USA[["Province/State", "Country/Region", 'Lat','Long','3/23/20']].sort_values(by='3/23/20'))

us=us.rename(columns={'3/23/20':'Deaths'})

print(us)
fig=px.scatter_geo(us,locations='Province/State',locationmode='USA-states',scope='usa',range_color=[0,20],color='Deaths',size='Deaths',title='Liczba zgonów w USA w dniu 23/03/2020')

fig.show()
