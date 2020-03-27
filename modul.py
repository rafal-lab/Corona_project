
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
plt.rcParams['figure.figsize'] = [15, 5]
import pandas as pd
import datetime


today= datetime.date.today()
def day_to_string(day):
  return day.strftime('%m/%d/%y').lstrip("0").replace(" 0", " ")
def give_SUM(frame, country):
    nb_of_cases = frame.loc[frame['Countries and territories'] == f'{country}']

    lista = list(nb_of_cases["Cases"])


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


def table_of_country(df, ctr1, ctr2, ctr3):
    sp = df.loc[
        (df['Country/Region'] == f'{ctr1}'), ['Country/Region', f'{day_to_string(today + datetime.timedelta(days=-4))}',
                                              f'{day_to_string(today + datetime.timedelta(days=-3))}',
                                              f'{day_to_string(today + datetime.timedelta(days=-2))}',
                                              f'{day_to_string(today + datetime.timedelta(days=-1))}']]
    it = df.loc[
        (df['Country/Region'] == f'{ctr2}'), ['Country/Region', f'{day_to_string(today + datetime.timedelta(days=-4))}',
                                              f'{day_to_string(today + datetime.timedelta(days=-3))}',
                                              f'{day_to_string(today + datetime.timedelta(days=-2))}',
                                              f'{day_to_string(today + datetime.timedelta(days=-1))}']]
    us = df.loc[
        (df['Country/Region'] == f'{ctr3}'), ['Country/Region', f'{day_to_string(today + datetime.timedelta(days=-4))}',
                                              f'{day_to_string(today + datetime.timedelta(days=-3))}',
                                              f'{day_to_string(today + datetime.timedelta(days=-2))}',
                                              f'{day_to_string(today + datetime.timedelta(days=-1))}']]

    ass = sp.append(us, ignore_index=True)
    ass = ass.append(it, ignore_index=True)

    return ass


def find_country(frame, country):
    return frame.loc[frame['Countries and territories'] == f'{country}']
def sort_by_country(ramka):
    formated_gdf = ramka.groupby(['Countries and territories']).max()
    formated_gdf = formated_gdf.loc[formated_gdf['Deaths'] > 0]
    formated_gdf['size'] = formated_gdf['Deaths'].pow(0.3)
    formated_gdf = formated_gdf.reset_index()
    return formated_gdf

def main():
    url = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    df = pd.read_csv(url, error_bad_lines=False)
    xml=pd.read_excel(r'C:\Users\raffr\Downloads\COVID-19-geographic-disbtribution-worldwide-2020-03-24.xlsx') #po wrzucaniu na gita czyta inaczej.plik w repo pobrac i zmienic sciezke
    frame=pd.DataFrame(xml)
    allcountry=pd.read_csv(r'https://raw.githubusercontent.com/rafal-lab/Corona_project/master/word.csv')

    Poland = find_country(frame , 'Poland')
    rysunek = Poland.plot(y=['Cases', 'Deaths'], x='DateRep', figsize=(12, 8), marker='*', title='Liczba przypadków COVID-19 w Polsce danego dnia', grid=True)


    formated_gdf=sort_by_country(frame)
    fig = px.scatter_geo(formated_gdf, locations="Countries and territories", locationmode='country names',
                     color="Deaths", size='size', hover_name="Countries and territories",
                     range_color= [0, 80],
                     projection="natural earth",
                     title="Liczba smierci 24.03.2020 COVID-19 na swiecie"
                     )

    fig.show()

    fig2 = px.choropleth(formated_gdf, locations="Countries and territories", locationmode='country names',
                     color="Deaths", hover_name="Countries and territories",
                     range_color= [0, 150],
                     projection="natural earth",
                     title='Smiertelnosc COVID19 na swiecie w dniu 24.03.2020')
    fig2.show()

    USA=allcountry.loc[allcountry['Country/Region']=='US'].sort_values(by='3/23/20')
    USA=USA.fillna(value=0)
    us=pd.DataFrame(USA[["Province/State", "Country/Region", 'Lat','Long','3/23/20']].sort_values(by='3/23/20'))
    us=us.rename(columns={'3/23/20':'Deaths'}) #wybieramy dane z USA z określonych stanów


    fig3=px.scatter_geo(us,locations='Province/State',locationmode='USA-states',scope='usa',range_color=[0,20],color='Deaths',size='Deaths',title='Liczba zgonów w USA w dniu 23/03/2020')

    fig3.show()


    nb_of_cases_in_Italy=find_country(frame,'Italy')

    lista=list(nb_of_cases_in_Italy["Cases"]) #bierzemy tylko przypadki
    nb_cs=pd.DataFrame(nb_of_cases_in_Italy)

    lista.reverse()

    for i in range(len(lista)):# PĘTLA DO SUMOWANIA PRZYPADKOW
        if(i==0 ):
            pass
        else:
            lista[i] += lista[i-1]
    lista.reverse()
    lista = np.asarray(lista) #lista wszystkich przypadków


    nb_cs['sum_in_Italy']=lista #dodajemy liste do tabeli i rysujemy
    cases_Italy_print=nb_cs.plot(x='DateRep',y='sum_in_Italy',figsize=(12,8), marker='o', title="Liczba przypadkow we Włoszech",grid=True)


    #wybieranie poszczegolnych krajow i dodawanie do tabeli
    Hiszpania = pd.DataFrame(find_country(frame,'Spain'))
    cases_in_spain = np.array(Hiszpania['Cases'])
    death_in_spain = np.array(Hiszpania['Deaths'])
    nb_cs['cs_in_Spain'] = cases_in_spain
    nb_cs['dth_in_Spain'] = death_in_spain
    nb_cs = nb_cs.rename(columns={'Cases': "cs_in_Italy"})
    nb_cs = nb_cs.rename(columns={'Deaths': "dth_in_Italy"})
    USA = pd.DataFrame(find_country(frame, 'USA'))
    cases_in_USA = np.array(USA['Cases'])
    death_in_USA = np.array(USA['Deaths'])
    nb_cs['cs_in_USA'] = cases_in_USA
    nb_cs['dth_in_USA'] = death_in_USA


    #suma przypadkow z krajow i dodanie do tabeli
    sum_in_spain = give_SUM(frame,'Spain')
    sum_in_USA = give_SUM(frame,"USA")
    nb_cs['sum_in_USA'] = sum_in_USA
    nb_cs['sum_in_Spain'] = sum_in_spain

    sum_dth_Spain = give_Death(frame,"Spain")
    sum_dth_USA = give_Death(frame,"USA")
    sum_dth_Italy = give_Death(frame,"Italy")
    nb_cs['sum_dth_in_Spain'] = sum_dth_Spain
    nb_cs['sum_dth_in_Italy'] = sum_dth_Italy
    nb_cs['sum_dth_in_USA'] = sum_dth_USA

    #rysowanie poszczegolnych wykresow
    nb_cs.plot(y=['cs_in_Italy', 'cs_in_Spain', 'cs_in_USA'], x='DateRep', figsize=(12, 8), marker='o', title='Wykres ilości nowych przypadków w Hiszpani, Włoszech i USA,każdego dnia',grid=True)
    nb_cs.plot(y=['dth_in_Italy', 'dth_in_Spain', 'dth_in_USA'], x='DateRep', figsize=(12, 8), marker='o', title='Wykres ilości śmierci w Hiszpani, Włoszech i USA,każdego dnia',grid=True)

    nb_cs.plot(y=['sum_in_Spain', 'sum_in_USA', 'sum_in_Italy'], x='DateRep', figsize=(12, 8), marker='o', title='Wykres sumarycznej ilości przypadkow w Hiszpani, Włoszech i USA',grid=True)
    nb_cs.plot(y=['sum_dth_in_Spain', 'sum_dth_in_USA', 'sum_dth_in_Italy'], x='DateRep', figsize=(12, 8), marker='o', title='Wykres sumarycznej ilości śmierci w Hiszpani, Włoszech i USA',grid=True)
    plt.show()

    #kolowe tabele narysowane w colabie!
    tb=table_of_country(df,'Spain','US','Italy')
    print(tb)

if __name__ == '__main__':
    main()
