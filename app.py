import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from Write_GoogleSheet_v4 import Update_Time

upTime=Update_Time()
sheet=upTime.Authorization()

# Title to appear at browser tab
app.title = 'WFH Check In-Out Monitor'

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout=html.Div(id='dcc-all',
            style={'marginLeft': '1.5%', 'marginRight': '1.5%', 'marginBottom': '.5%'},
            children=[
                html.Div(
                    id='refresh-button',
                    style={'textAlign': 'center', 'backgroundColor': '#ffffff',
                                'color': '#292929','marginLeft': '1.5%', 'marginRight': '1.5%', 'marginBottom': '4.5%', 'marginTop':'2.5%'},   
                    children=[
                    #html.Button('Refresh', id='refresh'),  
                    dbc.Button("Refresh", id='refresh',color='primary'), 
                    ]
                    ),             
                    ## start container
                    html.Div([
                        dbc.Container(
                        html.Div(id = 'graph-container')
                                )
                            ]),  ### container
                    html.Div( id='Update-button',
                    style={'marginLeft': '1.5%', 'marginRight': '1.5%', 'marginBottom': '.5%'},
                        children=[
                            html.Div(
                    id='Check-In-Update',
                    style={'textAlign': 'center','width': '48.0%',  'marginTop': '2.5%','marginLeft': '1.5%', 'display': 'inline-block', 'verticalAlign': 'top',
                                     'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee',
                                     },
                    children=[
                    dbc.Button("Check-In", id='C-In-1',color='primary'), 
                    
                    html.Table([
                        html.Tr([html.Td('=>'), html.Td(id='tab-cin')]),
                        ]),
                    ]
                    ), 
                    html.Div(
                    id='Check-Out-Update',
                    style={'textAlign': 'center','width': '48.0%', 'marginTop': '2.5%','marginLeft': '1.5%', 'display': 'inline-block', 'verticalAlign': 'top',
                                     'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee',
                                     },
                    children=[
                    dbc.Button("Check-Out", id='C-Out-1',color='primary'),
                    html.Table([
                        html.Tr([html.Td('=>'), html.Td(id='tab-cout')]),
                        ]),
                    ]
                    )
                    ####    
                        ]
                    )#### End button


                ] # children outside
            )  ### end

@app.callback(
    Output('graph-container', component_property='children'),
    [Input('refresh', 'n_clicks')])
def update_output_div(n_clicks):
    todayStr, nowDate, nowTime=upTime.GetDateTime()
    checkIn, checkOut=upTime.ReadCurrentStatus(todayStr, nowDate, nowTime, sheet)

    if(checkIn==0):
        colorLabel1="danger"
        message1="Go Check In : "+todayStr+" !!!"
    else:
        colorLabel1="success"
        message1="Go RELAX."

    if(checkOut==0):
        colorLabel2="danger"
        message2="Go Check Out : "+todayStr+" !!!"
    else:
        colorLabel2="success"
        message2="Go RELAX."


    card1=dbc.Alert(message1, color=colorLabel1),    
    #card1 =[dbc.CardHeader("Check-In"),
    #    dbc.CardBody(
    #        [
    #            html.H4("Status", className="card-title"),
    #            html.P(                    
    #                "Ha Ha Ha",
    #                className="card-text",
    #            ),
    #        ]
    #    ),
    #]#### card1
    print(' C-In :: ',n_clicks)
    card2=dbc.Alert(message2, color=colorLabel2),
    #card2 = [ dbc.CardHeader("Check_Out"),
    #    dbc.CardBody(
    #        [
    #            html.H4("Status", className="card-title"),
    #            html.P(
    #                "C-Out",
    #                className="card-text",
    #            ),
    #        ]
    #        ),
    #] #### card2
    #cards=dbc.Row(
    #    [
    #            dbc.Col(dbc.Card(card1, color="secondary", inverse=True)),
    #            dbc.Col(dbc.Card(card2, color="secondary", inverse=True)),
    #    ])
    cards=dbc.Row(
        [
                dbc.Col(dbc.Card(card1, color=colorLabel1, inverse=True)),
                dbc.Col(dbc.Card(card2, color=colorLabel2, inverse=True)),
        ])

    return cards

@app.callback(
    Output('tab-cout', 'children'),
    [Input('C-Out-1', 'n_clicks')])
def update_Checkout(n_clicks):
    if(n_clicks==0):
        print(' not call at open ')
    else:
        print(' call update ')
        todayStr, nowDate, nowTime=upTime.GetDateTime()
        upTime.InsertNewValue_Out(todayStr, nowDate, nowTime, sheet)

    return n_clicks 

@app.callback(
    Output('tab-cin', 'children'),
    [Input('C-In-1', 'n_clicks')])
def update_Checkin(n_clicks):
    if(n_clicks==0):
        print(' not call at open ')
    else:
        print(' call update ')
        todayStr, nowDate, nowTime=upTime.GetDateTime()
        upTime.InsertNewValue_In(todayStr, nowDate, nowTime,sheet)
    return n_clicks



server = app.server

if __name__ == '__main__':
    app.run_server(debug=False)