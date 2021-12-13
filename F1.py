import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np



st.set_page_config(page_title = "Formula One Dashboard",
                   page_icon = ":bar_chart:",
                   layout = 'wide')

race_year = pd.read_csv("C:\\Users\\33761\\Desktop\\Projets Perso\\Formula One Dashboard\\Race_Year.csv")
race_year = race_year.drop(race_year[race_year.year == 2021].index)
constructors = pd.read_csv("C:\\Users\\33761\\Desktop\\Projets Perso\\Formula One Dashboard\\constructors.csv")
constructor_standings = pd.read_csv("C:\\Users\\33761\\Desktop\\Projets Perso\\Formula One Dashboard\\constructor_standings.csv")
drivers = pd.read_csv("C:\\Users\\33761\\Desktop\\Projets Perso\\Formula One Dashboard\\drivers.csv")
drivers['counter'] = 1
drivers['delta color'] = np.where(drivers['delta'] < 0, "#FF1801", '#00FF00')
drivers_standing = pd.read_csv("C:\\Users\\33761\\Desktop\\Projets Perso\\Formula One Dashboard\\driver_standings.csv")
drivers_infos = pd.read_csv("C:\\Users\\33761\\Desktop\\Projets Perso\\Formula One Dashboard\\drivers_infos.csv")



#---SIDEBAR---

st.sidebar.image("https://i.imgur.com/FNaBuuW.png")

choix = st.sidebar.selectbox("Que voulez vous analyser", ("Championnat", "Ecurie","Comparer 2 écuries", "Pilote","Comparer 2 pilotes"))

if choix == 'Championnat': 
    #year selection
    year_list = list(race_year["year"].unique())
    year_list.sort(reverse = True)

    year = st.sidebar.selectbox(
        "Selectionnez une année",
        options = year_list)

    year_selection = race_year.query("year == @year")
    
    raceId_list = list(year_selection["raceId"].unique())
    points_ecurie_championnat = constructor_standings[constructor_standings['raceId'].isin(raceId_list)]
    points_ecurie_championnat = points_ecurie_championnat[['racename', 'raceId','name','points']].sort_values(by=['raceId'])
    
    points_drivers_championnat = drivers_standing[drivers_standing['raceId'].isin(raceId_list)]
    points_drivers_championnat = points_drivers_championnat[['racename', 'raceId','driver_name','points','round']].sort_values(by=['raceId'])
    
    
    
    ecurie_championnat = px.line(points_ecurie_championnat, x='racename', y='points', color = 'name')
    
    ecurie_championnat.update_layout(
                   paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)',
                   xaxis = dict(showgrid = False),
                   yaxis = dict(showgrid = False),
                   width = 800,
                   height = 500)
    
    driver_championnat = px.line(points_drivers_championnat, x='racename', y='points', color = 'driver_name')
    
    driver_championnat.update_layout(
                   paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)',
                   xaxis = dict(showgrid = False),
                   yaxis = dict(showgrid = False),
                   width = 800,
                   height = 500)
    

    #---MainPage---
    
    full_map = go.Figure(data=go.Scattergeo(
        lon = year_selection["lng"],
        lat = year_selection["lat"],
        mode = 'markers'))

    full_map.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        width= 500,
        height = 500)

    full_map.update_traces(marker = dict(color = '#FF1801', size = 7), line = dict(color = '#FF1801'))
    
    full_map.update_geos(showocean = True,
                    oceancolor = "Black",
                    projection_type="orthographic",
                    bgcolor = '#0E1117')
    
    st.title("Championnat de " + str(year))
    

    st.plotly_chart(full_map)
    
    st.subheader("Evolution des points par écurie")
    st.plotly_chart(ecurie_championnat)
    
    st.subheader("Evolution des points par pilote")
    st.plotly_chart(driver_championnat)


    #Infos sur les Grands Prix
    st.subheader("Informations par Grand Prix")
    race_list = year_selection["name_number"]
    race = st.selectbox(
            "Sélectionnez un Grand Prix",
            options = race_list)

    expander1 = st.expander("Voir les données")
    with expander1:
        clicked = st.dataframe(year_selection)

    st.markdown('---')

    year_race_selection = year_selection.query("name_number == @race")

    raceId = year_race_selection.iloc[0]["raceId"]
    country = year_race_selection.iloc[0]["Country"]
    Location = year_race_selection.iloc[0]["Location"]
    date = year_race_selection.iloc[0]["date"]
    time = year_race_selection.iloc[0]["time"]
    wiki_link = year_race_selection.iloc[0]["url"]
    latitude = float(year_race_selection.iloc[0]["lat"])
    longitude = float(year_race_selection.iloc[0]["lng"])


    constructors_selection = constructors.query("raceId ==@raceId")

    fig = go.Figure(data=go.Scattergeo(
        lon = year_race_selection["lng"],
        lat = year_race_selection["lat"],
        mode = 'markers'))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        width= 400,
        height = 400)

    fig.update_traces(marker = dict(color = '#FF1801', size = 10), line = dict(color = '#FF1801'))
    
    fig.update_geos(showocean = True,
                    oceancolor = "Black",
                    projection_type="orthographic",
                    bgcolor = '#0E1117')

    col1, col2 = st.columns(2)

    with col1:
        st.header(str(race))
        st.text(" ")
        st.markdown("Pays : " + str(country))
        st.markdown("Ville : " + str(Location))
        st.markdown("Date : " + str(date))
        st.markdown("Heure : " + str(time))
        st.markdown("Lien wikipedia pour plus d'infos !")
        st.markdown(wiki_link)

    
    with col2:
        st.plotly_chart(fig)
    
    expander2 = st.expander("Voir les données")  
    with expander2:
        clicked = st.dataframe(year_race_selection)

    st.markdown('---')


    #points par écurie
    constructor_points = px.bar(constructors_selection,
              x = 'points',
              y = 'name',
              text = 'points')

    constructor_points.update_traces(marker_color = '#FF1801',
                   textposition = 'outside')

    constructor_points.update_layout(barmode='stack',
                   yaxis={'categoryorder':'total ascending'},
                   paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)',
                   xaxis = dict(showgrid = False, range = [0,50]),
                   width = 400,
                   height = 400,
                   font = dict(size = 10))

    drivers_selection = drivers.query("raceId == @raceId")
    
    #points par écurie
    driver_points = px.bar(drivers_selection,
              x = 'points',
              y = 'Driver',
              text = 'points')

    driver_points.update_traces(marker_color = '#FF1801',
                   textposition = 'outside')

    driver_points.update_layout(barmode='stack',
                   yaxis={'categoryorder':'total ascending'},
                   paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)',
                   xaxis = dict(showgrid = False, range = [0,50]),
                   width = 400,
                   height = 400,
                   font = dict(size = 10))

    #finale position driver
    driver_chart1 = px.bar(drivers_selection,
              x = 'positionOrder',
              y = 'Driver',
              text = 'positionOrder')

    driver_chart1.update_traces(marker_color = '#FF1801',
                   textposition='outside')

    driver_chart1.update_layout(barmode='stack',
                   yaxis={'categoryorder':'total descending'},
                   paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)',
                   width = 350,
                   height = 400,
                   xaxis = dict(showgrid = False, range = [0,24]),
                   font = dict(size = 10))

    #grid position driver
    driver_chart2 = px.bar(drivers_selection,
              x = 'grid',
              y = 'Driver',
              text = 'grid')

    driver_chart2.update_traces(marker_color = '#FF1801',
                   textposition = 'outside')

    driver_chart2.update_layout(barmode='stack',
                   paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)',
                   width = 350,
                   height = 400,
                   xaxis = dict(showgrid = False,range = [0,24]),
                   yaxis = dict(autorange = "reversed"),
                   font = dict(size = 10))

    #delta driver
    driver_chart3 = px.bar(drivers_selection,
              x = 'delta',
              y = 'Driver',
              text = 'delta')

    driver_chart3.update_traces(marker_color = drivers_selection['delta color'],
                   textposition = 'outside')

    driver_chart3.update_layout(barmode='stack',
                   paper_bgcolor='rgba(0,0,0,0)',
                   plot_bgcolor='rgba(0,0,0,0)',
                   width = 350,
                   height = 400,
                   xaxis = dict(showgrid = False,range = [-25,25]),
                   yaxis = dict(autorange = "reversed"),
                   font = dict(size = 10))


    y = drivers_selection['Driver']
    x_grid = drivers_selection['grid']
    x_finale = drivers_selection['positionOrder']

    pyramid_chart = [go.Bar(y=y,
               x=x_grid,
               orientation='h',
               name='Grid',
               hoverinfo='x',
               marker=dict(color='green')
               ),
        go.Bar(y=y,
               x=-x_finale,
               orientation='h',
               name='Finale',
               text=1 * x_finale.astype('int'),
               hoverinfo='text',
               marker=dict(color='red')
               )]

    ecurie_point, driver_point = st.columns(2) 

    with ecurie_point:
        st.markdown('#### Points par écurie')
        st.plotly_chart(constructor_points)
    
    with driver_point:
        st.markdown('#### Points par pilotes')
        st.plotly_chart(driver_points)

    expander3 = st.expander("Voir les données")
    with expander3:
        clicked = st.dataframe(constructors_selection)

    col5, col6, col7 = st.columns(3)

    with col5:
        st.markdown("Position Finale")
        st.plotly_chart(driver_chart1)

    with col6:
        st.markdown("Position sur la grille")
        st.plotly_chart(driver_chart2)
 
    with col7:
        st.markdown("Delta")
        st.plotly_chart(driver_chart3)

    expander4 = st.expander("Voir les données")
    with expander4:
        clicked = st.dataframe(drivers_selection)

    driver_list = drivers_selection["Driver"]
    driver = st.selectbox(
        "Sélectionnez un Pilot",
        options = driver_list)
    

    drivers2_selection = drivers_selection.query("Driver ==@driver")

    grid = drivers2_selection.iloc[0]["grid"]
    positionOrder = drivers2_selection.iloc[0]["positionOrder"]
    delta = drivers2_selection.iloc[0]["delta"]
    points = drivers2_selection.iloc[0]["points"]
    laps = drivers2_selection.iloc[0]["laps"]
    fastestLap = drivers2_selection.iloc[0]["fastestLap"]
    fastestLapTime = drivers2_selection.iloc[0]["fastestLapTime"]
    fastestLapSpeed = drivers2_selection.iloc[0]["fastestLapSpeed"]
    constructor = drivers2_selection.iloc[0]["constructor"]

    st.subheader(str(driver) + " (écurie " + str(constructor) + " )")

    driver_rank, driver_lap = st.columns(2)

    with driver_rank:
        st.markdown("Position sur la Grille : " + str(grid))
        st.markdown("Position Finale : " + str(positionOrder))
        st.markdown("Delta : " + str(delta))
        st.markdown("Points remportés : " + str(points))

    with driver_lap:
        st.markdown("Nombre de tours effectués : " + str(laps))
        st.markdown("Tour le plus rapide : " + str(fastestLap))
        st.markdown("Temps du tour le plus rapide en minute : " + str(fastestLapTime))
        st.markdown("Vitesse moyenne sur le tour le plus rapide : " + str(fastestLapSpeed)) 

    expander5 = st.expander("Voir les données")
    with expander5:
        clicked = st.dataframe(drivers2_selection)

if choix == 'Pilote': 
    
    drivers_list = drivers_infos["Full_name"].unique()
    drivers_list.sort()

    drivers_selectbox = st.sidebar.selectbox(
        "Selectionnez un pilote",
        options = drivers_list)

    drivers_infos_selection = drivers_infos.query("Full_name == @drivers_selectbox")
    
    Full_name = drivers_infos_selection.iloc[0]["Full_name"]
    dob = drivers_infos_selection.iloc[0]["dob"]
    nationality = drivers_infos_selection.iloc[0]["nationality"]
    wiki = drivers_infos_selection.iloc[0]["url"]
    driverID = drivers_infos_selection.iloc[0]["driverId"]
    
    driverID_selection = drivers.query("driverId == @driverID")

    constructor_pie_chart = px.pie(driverID_selection, values = 'counter', names = 'constructor')
        
    constructor_pie_chart.update_layout(
                       width = 350,
                       height = 350,
                       showlegend = False)
        
    constructor_pie_chart.update_traces(textposition='inside',
                                        textinfo='percent+label',
                                        marker = dict(line = dict(color = '#FFFFFF', width = 1)),
                                        hole = 0.5)
    
    
    st.title(str(Full_name))
    
    col1, col2 = st.columns(2)
     
    with col1:

        st.plotly_chart(constructor_pie_chart)
        
    with col2:

        st.text(" ")
        st.text(" ")
        st.markdown("Nationalité : " + str(nationality))
        st.markdown("---")
        st.markdown("Date de naissance : " + str(dob))
        st.markdown("---")
        st.markdown("Plus d'info sur sa page wikipedia :point_down:")
        st.markdown(wiki)
 
    
    expander6 = st.expander("Voir les données")
    with expander6:
        clicked = st.dataframe(drivers_infos_selection)
        
    st.markdown("---")

    ecuries = st.multiselect("informations en fonction des écuries sélectionnées",
                             options = driverID_selection['constructor'].unique(),
                             default = driverID_selection['constructor'].unique()
                             )
    
    driverID_ecurie_selection = drivers.query("driverId == @driverID & constructor == @ecuries")
    
    nb_course = len(np.unique(driverID_ecurie_selection['raceId']))
    pts_gagnes = driverID_ecurie_selection['points'].sum()
    victoires1 = (driverID_ecurie_selection['positionOrder'] == 1).sum()
    victoires2 = (driverID_ecurie_selection['positionOrder'] == 2).sum()
    victoires3 = (driverID_ecurie_selection['positionOrder'] == 3).sum()
    finale_mean = (driverID_ecurie_selection['positionOrder']).mean().round(0)  
    grid_mean = (driverID_ecurie_selection['grid']).mean().round(0)                        
                                                          
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("Courses effectuées")
        st.title(nb_course)

    
    with col2:
        st.markdown("Points total remportés")
        st.title(pts_gagnes)
    with col3:
        st.markdown("Positions moyennes")
        st.text(" ")
        st.markdown("Position finale : " + str(finale_mean))
        st.markdown("Position sur la grille : " + str(grid_mean))
        
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader(":medal: 1ier : " + str(victoires1))
    with col2:
        st.subheader(":medal: 2ème : " + str(victoires2))
    with col3:
        st.subheader(":medal: 3ème : " + str(victoires3))
        
    max_position = int((driverID_ecurie_selection['positionOrder']).max())
    max_grid = int((driverID_ecurie_selection['grid']).max())
    max_points = int((driverID_ecurie_selection['points']).max())
    
    final_histogram = px.histogram(driverID_ecurie_selection,
                                   x = 'positionOrder',
                                   nbins = 25,
                                   labels = {'positionOrder' : 'Position Finale'},
                                   color = 'constructor',
                                   )
    
    #final_histogram.update_traces(marker_color = '#FF1801')
        
    final_histogram.update_layout(
                       width = 400,
                       height = 350,
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       yaxis = dict(showgrid = False),
                       bargap = 0.2)
    
    grid_histogram = px.histogram(driverID_ecurie_selection,
                                   x = 'grid',
                                   nbins = 25,
                                   labels = {'grid' : 'Position sur la grille'},
                                   color = 'constructor',
                                   )
    
    #grid_histogram.update_traces(marker_color = '#FF1801')
        
    grid_histogram.update_layout(
                       width = 400,
                       height = 350,
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       yaxis = dict(showgrid = False),
                       bargap = 0.2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("Distribution des positions finales")
        st.plotly_chart(final_histogram)
    
    with col2:
        st.markdown("Distribution des positions sur la grille")
        st.plotly_chart(grid_histogram)
    
    expander7 = st.expander("Voir les données")
    with expander7:
        clicked = st.dataframe(driverID_ecurie_selection)
        
if choix == 'Comparer 2 pilotes':  

    col1, col2 = st.columns(2)
    
    with col1:
        
        drivers_list1 = drivers_infos["Full_name"].unique()
        drivers_list1.sort()

        drivers_selectbox1 = st.selectbox(
            "Selectionnez le 1ier pilote",
            options = drivers_list1)
        
        st.markdown("---")

        drivers_infos_selection1 = drivers_infos.query("Full_name == @drivers_selectbox1")
        
        Full_name1 = drivers_infos_selection1.iloc[0]["Full_name"]
        dob1 = drivers_infos_selection1.iloc[0]["dob"]
        nationality1 = drivers_infos_selection1.iloc[0]["nationality"]
        wiki1 = drivers_infos_selection1.iloc[0]["url"]
        driverID1 = drivers_infos_selection1.iloc[0]["driverId"]
        
        driverID_selection1 = drivers.query("driverId == @driverID1")

        constructor_pie_chart1 = px.pie(driverID_selection1, values = 'counter', names = 'constructor')
            
        constructor_pie_chart1.update_layout(
                           width = 300,
                           height = 300,
                           showlegend = False)
            
        constructor_pie_chart1.update_traces(textposition='inside',
                                             textinfo='percent+label',
                                             marker = dict(line = dict(color = '#FFFFFF', width = 1)),
                                             hole = 0.5)
        
        st.subheader(str(Full_name1))
        st.plotly_chart(constructor_pie_chart1)
        
        st.markdown("Nationalité : " + str(nationality1))
        st.markdown("Date de naissance : " + str(dob1))
        st.markdown("Plus d'info sur sa page wikipedia :point_down:")
        st.markdown(wiki1)
 
    
        expander6 = st.expander("Voir les données")
        with expander6:
            clicked = st.dataframe(drivers_infos_selection1)
            
        ecuries1 = st.multiselect("Ecuries avec lesquelles il a couru",
                                     options = driverID_selection1['constructor'].unique(),
                                     default = driverID_selection1['constructor'].unique()
                                     )
        driverID_ecurie_selection1 = drivers.query("driverId == @driverID1 & constructor == @ecuries1")
            
    
    with col2:
        
        drivers_list2 = drivers_infos["Full_name"].unique()
        drivers_list2.sort()

        drivers_selectbox2 = st.selectbox(
            "Selectionnez le 2ème pilote",
            options = drivers_list2)
        
        st.markdown("---")

        drivers_infos_selection2 = drivers_infos.query("Full_name == @drivers_selectbox2")
        
        Full_name2 = drivers_infos_selection2.iloc[0]["Full_name"]
        dob2 = drivers_infos_selection2.iloc[0]["dob"]
        nationality2 = drivers_infos_selection2.iloc[0]["nationality"]
        wiki2 = drivers_infos_selection2.iloc[0]["url"]
        driverID2 = drivers_infos_selection2.iloc[0]["driverId"]
        
        driverID_selection2 = drivers.query("driverId == @driverID2")

        constructor_pie_chart2 = px.pie(driverID_selection2, values = 'counter', names = 'constructor')
            
        constructor_pie_chart2.update_layout(
                           width = 300,
                           height = 300,
                           showlegend = False)
            
        constructor_pie_chart2.update_traces(textposition='inside',
                                             textinfo='percent+label',
                                             marker = dict(line = dict(color = '#FFFFFF', width = 1)),
                                             hole = 0.5)
        
        st.subheader(str(Full_name2))
        st.plotly_chart(constructor_pie_chart2)
        
        st.markdown("Nationalité : " + str(nationality2))
        st.markdown("Date de naissance : " + str(dob2))
        st.markdown("Plus d'info sur sa page wikipedia :point_down:")
        st.markdown(wiki2)
 
    
        expander6 = st.expander("Voir les données")
        with expander6:
            clicked = st.dataframe(drivers_infos_selection2)

        ecuries2 = st.multiselect("Ecuries avec lesquelles il a couru",
                                     options = driverID_selection2['constructor'].unique(),
                                     default = driverID_selection2['constructor'].unique(), key = 'écurie2'
                                     )
            
        driverID_ecurie_selection2 = drivers.query("driverId == @driverID2 & constructor == @ecuries2")
            
    st.markdown("---")
    
    col1, col2 = st.columns(2)
        
    with col1: 
        nb_course1 = len(np.unique(driverID_ecurie_selection1['raceId']))
        pts_gagnes1 = driverID_ecurie_selection1['points'].sum()
        victoires11 = (driverID_ecurie_selection1['positionOrder'] == 1).sum()
        victoires21 = (driverID_ecurie_selection1['positionOrder'] == 2).sum()
        victoires31 = (driverID_ecurie_selection1['positionOrder'] == 3).sum()
        finale_mean1 = (driverID_ecurie_selection1['positionOrder']).mean().round(0)  
        grid_mean1 = (driverID_ecurie_selection1['grid']).mean().round(0)
        
        st.markdown("Nombre de Grands Prix : " + str(nb_course1))
        st.markdown("Nombre de points gagnés : " + str(pts_gagnes1))
        st.markdown("1ier :medal: : " + str(victoires11))
        st.markdown("2ème :medal: : " + str(victoires21))
        st.markdown("3ème :medal: : " + str(victoires31))
        st.markdown("Position finale moyenne : " + str(finale_mean1))
        st.markdown("Position sur la grille moyenne : " + str(grid_mean1))
        
        final_histogram1 = px.histogram(driverID_ecurie_selection1,
                                       x = 'positionOrder',
                                       nbins = 30,
                                       labels = {'positionOrder' : 'Position Finale'},
                                       color = 'constructor',
                                       )
        
            
        final_histogram1.update_layout(
                           width = 400,
                           height = 300,
                           paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)',
                           yaxis = dict(showgrid = False),
                           bargap = 0.2)
        
        final_histogram1.update_yaxes(visible = False, showticklabels = True)
        
        grid_histogram1 = px.histogram(driverID_ecurie_selection1,
                                       x = 'grid',
                                       nbins = 30,
                                       labels = {'grid' : 'Position sur la grille'},
                                       color = 'constructor',
                                       )
            
        grid_histogram1.update_layout(
                           width = 400,
                           height = 300,
                           paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)',
                           yaxis = dict(showgrid = False),
                           bargap = 0.2)
        
        grid_histogram1.update_yaxes(visible = False, showticklabels = True)
        

        st.plotly_chart(final_histogram1)
        st.plotly_chart(grid_histogram1)        
        
    with col2:
        nb_course2 = len(np.unique(driverID_ecurie_selection2['raceId']))
        pts_gagnes2 = driverID_ecurie_selection2['points'].sum()
        victoires12 = (driverID_ecurie_selection2['positionOrder'] == 1).sum()
        victoires22 = (driverID_ecurie_selection2['positionOrder'] == 2).sum()
        victoires32 = (driverID_ecurie_selection2['positionOrder'] == 3).sum()
        finale_mean2 = (driverID_ecurie_selection2['positionOrder']).mean().round(0)  
        grid_mean2 = (driverID_ecurie_selection2['grid']).mean().round(0)   
        
        st.markdown("Nombre de Grands Prix : " + str(nb_course2))
        st.markdown("Nombre de points gagnés : " + str(pts_gagnes2))
        st.markdown("1ier :medal: : " + str(victoires12))
        st.markdown("2ème :medal: : " + str(victoires22))
        st.markdown("3ème :medal: : " + str(victoires32))
        st.markdown("Position finale moyenne : " + str(finale_mean2))
        st.markdown("Position sur la grille moyenne : " + str(grid_mean2))

        final_histogram2 = px.histogram(driverID_ecurie_selection2,
                                       x = 'positionOrder',
                                       nbins = 30,
                                       labels = {'positionOrder' : 'Position Finale'},
                                       color = 'constructor',
                                       )
        
            
        final_histogram2.update_layout(
                           width = 400,
                           height = 300,
                           paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)',
                           yaxis = dict(showgrid = False),
                           bargap = 0.2)
        
        final_histogram2.update_yaxes(visible = False, showticklabels = True)
        
        grid_histogram2 = px.histogram(driverID_ecurie_selection2,
                                       x = 'grid',
                                       nbins = 30,
                                       labels = {'grid' : 'Position sur la grille'},
                                       color = 'constructor',
                                       )
            
        grid_histogram2.update_layout(
                           width = 400,
                           height = 300,
                           paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)',
                           yaxis = dict(showgrid = False),
                           bargap = 0.2)
        
        grid_histogram2.update_yaxes(visible = False, showticklabels = True)
        

        st.plotly_chart(final_histogram2)
        st.plotly_chart(grid_histogram2)
        
        
if choix == 'Ecurie': 

    constructor_list = constructor_standings["name"].unique()
    constructor_list.sort()

    constructor_selectbox = st.sidebar.selectbox(
        "Selectionnez une écurie",
        options = constructor_list)

    constructor_selection = constructor_standings.query("name == @constructor_selectbox")
    
    nb_course_constructor = len(np.unique(constructor_selection['raceId']))
    wiki_constructor = constructor_selection.iloc[0]['wiki']
    constructor_points = constructor_selection['points'].sum()
    podium1 = (constructor_selection['position'] == 1).sum()
    podium2 = (constructor_selection['position'] == 2).sum()
    podium3 = (constructor_selection['position'] == 3).sum()
    mean_constructor = constructor_selection['position'].mean().round()

    st.title(constructor_selectbox)
    st.markdown(wiki_constructor)
    st.markdown('---')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("Participation aux Grands Prix")
        st.title(str(nb_course_constructor))

    
    with col2:
        st.markdown("Nombre total de points remportés")
        st.title(str(constructor_points))
        
    with col3: 
        st.markdown("Resultat final moyen")
        st.title(str(mean_constructor))
        
    st.markdown('---')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader(":medal: 1ier : " + str(podium1))
    with col2:
        st.subheader(":medal: 2ème : " + str(podium2))
    with col3:
        st.subheader(":medal: 3ème : " + str(podium3))
        

    ecurie_histo = px.histogram(constructor_selection,
                                       x = 'position',
                                       nbins = 30,
                                       labels = {'positionOrder' : 'Position Finale'}
                                       )
        
            
    ecurie_histo.update_layout(
                           width = 700,
                           height = 300,
                           paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)',
                           yaxis = dict(showgrid = False),
                           xaxis = dict(showgrid = False),
                           bargap = 0.2)
    
    ecurie_histo.update_traces(marker_color = '#FF1801')
        
    #ecurie_histo.update_yaxes(visible = False, showticklabels = True)
    st.markdown('---')
    st.subheader('Distribution des Positions Finales aux Grands Prix')
    st.plotly_chart(ecurie_histo)
    
    
    expander6 = st.expander("Voir les données")
    with expander6:
        clicked = st.dataframe(constructor_selection)
        
if choix == 'Comparer 2 écuries':  
        
    col1, col2 = st.columns(2)
        
    with col1:
            
        ecurie_list1 = constructor_standings["name"].unique()
        ecurie_list1.sort()

        ecurie_selectbox1 = st.selectbox(
                "Selectionnez la 1ère écurie",
                options = ecurie_list1)
            
        st.markdown("---")

        constructor_selection1 = constructor_standings.query("name == @ecurie_selectbox1")
        
        nb_course_constructor1 = len(np.unique(constructor_selection1['raceId']))
        wiki_constructor1 = constructor_selection1.iloc[0]['wiki']
        constructor_points1 = constructor_selection1['points'].sum()
        podium11 = (constructor_selection1['position'] == 1).sum()
        podium21 = (constructor_selection1['position'] == 2).sum()
        podium31= (constructor_selection1['position'] == 3).sum()
        mean_constructor1 = constructor_selection1['position'].mean().round()
    
    
        st.title(ecurie_selectbox1)
        
        st.markdown('---')
        
        st.markdown("Participation aux Grands Prix : " + str(nb_course_constructor1))
        
        st.markdown("Nombre total de points remportés : " + str(constructor_points1))
            
        st.markdown("Resultat final moyen : " + str(mean_constructor1))
            
        st.markdown('---')
        
        st.subheader(":medal: 1ier : " + str(podium11))

        st.subheader(":medal: 2ème : " + str(podium21))

        st.subheader(":medal: 3ème : " + str(podium31))
        
        ecurie_histo1 = px.histogram(constructor_selection1,
                                           x = 'position',
                                           nbins = 30,
                                           labels = {'positionOrder' : 'Position Finale'}
                                           )
            
                
        ecurie_histo1.update_layout(
                               width = 350,
                               height = 300,
                               paper_bgcolor='rgba(0,0,0,0)',
                               plot_bgcolor='rgba(0,0,0,0)',
                               yaxis = dict(showgrid = False),
                               xaxis = dict(showgrid = False),
                               bargap = 0.2)
        
        ecurie_histo1.update_traces(marker_color = '#FF1801')
            
        #ecurie_histo.update_yaxes(visible = False, showticklabels = True)
        st.markdown('---')
        st.markdown('Distribution des Positions Finales aux Grands Prix')
        st.plotly_chart(ecurie_histo1)
            
        
    with col2: 
        ecurie_list2 = constructor_standings["name"].unique()
        ecurie_list2.sort()

        ecurie_selectbox2 = st.selectbox(
                "Selectionnez la 2ème écurie",
                options = ecurie_list2)
            
        st.markdown("---")

        constructor_selection2 = constructor_standings.query("name == @ecurie_selectbox2")
        
        nb_course_constructor2 = len(np.unique(constructor_selection2['raceId']))
        wiki_constructor2 = constructor_selection2.iloc[0]['wiki']
        constructor_points2 = constructor_selection2['points'].sum()
        podium12 = (constructor_selection2['position'] == 1).sum()
        podium22 = (constructor_selection2['position'] == 2).sum()
        podium32= (constructor_selection2['position'] == 3).sum()
        mean_constructor2 = constructor_selection2['position'].mean().round()
        
        st.title(ecurie_selectbox2)
        st.markdown('---')
        
        st.markdown("Participation aux Grands Prix : " + str(nb_course_constructor2))
        
        st.markdown("Nombre total de points remportés : " + str(constructor_points2))
            
        st.markdown("Resultat final moyen : " + str(mean_constructor2))
            
        st.markdown('---')
        
        st.subheader(":medal: 1ier : " + str(podium12))

        st.subheader(":medal: 2ème : " + str(podium22))

        st.subheader(":medal: 3ème : " + str(podium32))
        
        ecurie_histo2 = px.histogram(constructor_selection2,
                                           x = 'position',
                                           nbins = 30,
                                           labels = {'positionOrder' : 'Position Finale'}
                                           )
            
                
        ecurie_histo2.update_layout(
                               width = 350,
                               height = 300,
                               paper_bgcolor='rgba(0,0,0,0)',
                               plot_bgcolor='rgba(0,0,0,0)',
                               yaxis = dict(showgrid = False),
                               xaxis = dict(showgrid = False),
                               bargap = 0.2)
        
        ecurie_histo2.update_traces(marker_color = '#FF1801')
            
        #ecurie_histo.update_yaxes(visible = False, showticklabels = True)
        st.markdown('---')
        st.markdown('Distribution des Positions Finales aux Grands Prix')
        st.plotly_chart(ecurie_histo2)


