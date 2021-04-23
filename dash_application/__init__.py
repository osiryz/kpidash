import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import requests
import json
from dash.dependencies import Input, Output
from flask_login import LoginManager, login_user, login_required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#GET KPI1
KPI1 = "https://dkffsfbetbpbvzd-tipdata.adb.ap-osaka-1.oraclecloudapps.com/ords/tip/kpi1/incvol/"
r = requests.get(KPI1)
KPI1JSON = r.json()["items"]

#KPI 1
kpi1_months = []
kpi1_incidences_numbers = []
kpi1_priorities = []

for dict in KPI1JSON:
    if dict['month'] == '201801':
        dict['month'] = 'Jan 2018'
        kpi1_months.append(dict["month"])
        kpi1_incidences_numbers.append(dict["incidences_number"])
        kpi1_priorities.append(dict["priority"])
for dict in KPI1JSON:
    if dict['month'] == '201802':
        dict['month'] = 'Feb 2018'
        kpi1_months.append(dict["month"])
        kpi1_incidences_numbers.append(dict["incidences_number"])
        kpi1_priorities.append(dict["priority"])

for dict in KPI1JSON:
    if dict['month'] == '201803':
        dict['month'] = 'Mar 2018'
        kpi1_months.append(dict["month"])
        kpi1_incidences_numbers.append(dict["incidences_number"])
        kpi1_priorities.append(dict["priority"])

kpi1_df = pd.DataFrame({
    "Months": kpi1_months,
    "Number of incidents": kpi1_incidences_numbers,
    "Priority": kpi1_priorities
})

def create_kpi1(flask_app):
    dash_app = dash.Dash(server=flask_app, name="kpi1", url_base_pathname='/kpi1/')
    
    dash_app.layout = html.Div(
        dcc.Graph(
            id='kpi1-graph',
            figure= px.bar(kpi1_df, x="Months", y="Number of incidents", color="Priority", barmode="group"),
        ),  
        
    )
    for view_function in dash_app.server.view_functions:
        if view_function.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_function] = login_required(
                dash_app.server.view_functions[view_function]
                )    
    return dash_app


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Month": ["201801", "201802", "201803", "201801", "201802", "201803", "201801", "201802", "201803", "201801", "201802", "201803"],
    "Incidences": [300, 287, 292, 7706, 6486, 6630, 2382, 2344, 2353, 13, 18, 9],
    "Priority": ["Alta", "Alta", "Alta", "Baja", "Baja", "Baja", "Media", "Media", "Media", "Crit", "Crit", "Crit"]
})

def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash/")

    

    dash_app.layout = html.Div(children=[
        html.H1(children='Hello MCSBT'),

        html.Div(children='''
            Term Integration Platform - Iberia.
        '''),
        dcc.Graph(
            id='example-graph',
            figure=px.bar(df, x="Month", y="Incidences", color="Priority", barmode="group")
        )
    ])
    return dash_app


#GET KPI2
KPI2 = "https://dkffsfbetbpbvzd-tipdata.adb.ap-osaka-1.oraclecloudapps.com/ords/tip/kpi2/incsolved/"
r2 = requests.get(KPI2)
KPI2JSON = r2.json()["items"]

#KPI2
kpi2_months = []
kpi2_incidences_numbers = []

for dict in KPI2JSON:
   if dict["month"] == '201801':
       dict["month"] = 'Jan 2018'
       kpi2_months.append(dict["month"])
       kpi2_incidences_numbers.append(dict["incidences_number"])
   elif dict["month"] == '201802':
       dict["month"] = 'Feb 2018'
       kpi2_months.append(dict["month"])
       kpi2_incidences_numbers.append(dict["incidences_number"])
   elif dict["month"] == '201803':
       dict["month"] = 'Mar 2018'
       kpi2_months.append(dict["month"])
       kpi2_incidences_numbers.append(dict["incidences_number"])
    

kpi2_df = pd.DataFrame({
    "Months": kpi2_months,
    "Number of incidents": kpi2_incidences_numbers,
})

def create_kpi2(flask_app):
    dash_app = dash.Dash(server=flask_app, name="kpi2", url_base_pathname='/kpi2/')
    
    dash_app.layout = html.Div(
        dcc.Graph(
            id='kpi2-graph',
            figure= px.bar(kpi2_df, x="Months", y="Number of incidents", barmode="group")
        ),    
    )  

    for view_function in dash_app.server.view_functions:
        if view_function.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_function] = login_required(dash_app.server.view_functions[view_function]
            )

    return dash_app

#GET KPI3
KPI3 = "https://qovo4nsf3oonbax-db202103111252.adb.eu-frankfurt-1.oraclecloudapps.com/ords/tip_rose/kpi3/sla/"
r3 = requests.get(KPI3)
KPI3JSON = r3.json()["items"]

#GET KPI3 Fancy Version

sla= {}
for i in KPI3JSON:
    if i['month'] in sla:
        sla[i['month']].append(i['brbaja'],i['mtbaja'],i['brmedia'],i['mtmedia'],i['bralta'],i['mtalta'],i['brcritica'],i['mtcritica'])
    else: 
        sla[i['month']]= [i["brbaja"],i['mtbaja'],i['brmedia'],i['mtmedia'],i['bralta'],i['mtalta'],i['brcritica'],i['mtcritica']]

def create_kpi3(flask_app):
    dash_app = dash.Dash(server=flask_app, name="SLA", url_base_pathname='/kpi3/')    
    
    dash_app.layout = html.Div(children=[
        #KPI3
        dcc.Dropdown(
            id="month",
            options=[{"label": 'January 2018', "value":'201801'},
                    {"label": 'February 2018', "value":'201802'},
                    {"label": 'March 2018', "value":'201803'}
                    ],
            value="201801"
        ),
        dcc.Graph(
            id='kpi3',
            figure={
                'data':[],           
            }
        )  
    ])
   
    @dash_app.callback(
        Output(component_id="kpi3",component_property="figure"),
        [Input(component_id="month", component_property="value")]
    )
    def update_KPI3(value):
        return {
            "data": [
            {'x': ['BR BAJA','MT BAJA','BR MEDIA','MT MEDIA','BR ALTA','MT ALTA','BT CRITICA','MT CRITICA'], 'y': sla[value], 'type': 'bar', 'name': value},            
            ]
        }
        for view_function in dash_app.server.view_functions:
            if view_function.startswith(dash_app.config.url_base_pathname):
                dash_app.server.view_functions[view_function] = login_required(dash_app.server.view_functions[view_function]
                )

        return dash_app

#GET KPI4
KPI4 = "https://qovo4nsf3oonbax-db202103111252.adb.eu-frankfurt-1.oraclecloudapps.com/ords/tip_rose/kpi4/BL/"
r4 = requests.get(KPI4)
KPI4JSON = r4.json()["items"]

#KPI4
k4_months = []
k4_incidences_numbers = []

for dict in KPI4JSON:
   if dict["month"] == '201801':
       dict["month"] = 'Jan 2018'
       k4_months.append(dict["month"])
       k4_incidences_numbers.append(dict["incidences_number"])
   elif dict["month"] == '201802':
       dict["month"] = 'Feb 2018'
       k4_months.append(dict["month"])
       k4_incidences_numbers.append(dict["incidences_number"])
   elif dict["month"] == '201803':
       dict["month"] = 'Mar 2018'
       k4_months.append(dict["month"])
       k4_incidences_numbers.append(dict["incidences_number"])

k4_df = pd.DataFrame({
    "Months": k4_months,
    "Number of incidents": k4_incidences_numbers,
})

def create_kpi4(flask_app):
    dash_app = dash.Dash(server=flask_app, name="kpi4", url_base_pathname='/kpi4/')
        
    dash_app.layout = html.Div(
        dcc.Graph(
            id='kpi4-graph',
            figure= px.bar(k4_df, x="Months", y="Number of incidents", barmode="group")
        ),  
            
    )
    for view_function in dash_app.server.view_functions:
        if view_function.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_function] = login_required(dash_app.server.view_functions[view_function]
            )

    return dash_app