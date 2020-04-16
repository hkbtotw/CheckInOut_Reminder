import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from Write_GoogleSheet_v4 import Update_Time

upTime=Update_Time()
sheet=upTime.Authorization()


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Title to appear at browser tab
app.title = 'WFH Check In-Out Monitor'

app.layout=html.Div(id='dcc-all',
            style={'marginLeft': '1.5%', 'marginRight': '1.5%', 'marginBottom': '.5%'},
            children=[
                html.Div(
                    id='refresh-button',
                    style={'textAlign': 'center','width': '48.0%',  'backgroundColor': '#ffffff',
                                'color': '#292929','marginLeft': '1.5%', 'marginRight': '1.5%', 'marginBottom': '4.5%', 'marginTop':'2.5%'},   
                    children=[
                    dbc.Button("Refresh", id='refresh',color='primary'), 
                    ]
                    ),             


                    html.Div( id='Update-button',
                    style={'marginLeft': '1.5%', 'marginRight': '1.5%', 'marginBottom': '.5%'},
                        children=[
                            html.Div(
                    id='Check-In-Update',
                    style={'textAlign': 'center','width': '48.0%',  'marginTop': '2.5%','marginLeft': '1.5%',  'verticalAlign': 'top',
                                     'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee',
                                     },
                    children=[
                                            ## start container
                    html.Div([
                        dbc.Container(
                        html.Div(id = 'graph-container-1')
                                )
                            ]),  ### container
                    dbc.Button("Check-In", id='C-In-1',color='primary'), 
                    
                    html.Table([
                        html.Tr([html.Td(' #Button Pressed : '), html.Td(id='tab-cin')]),
                        ]),
                    ]
                    ), 
                    html.Div(
                    id='Check-Out-Update',
                    style={'textAlign': 'center','width': '48.0%', 'marginTop': '2.5%','marginLeft': '1.5%', 'verticalAlign': 'top',
                                     'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee',
                                     },
                    children=[
                                            ## start container
                    html.Div([
                        dbc.Container(
                        html.Div(id = 'graph-container-2')
                                )
                            ]),  ### container
                    dbc.Button("Check-Out", id='C-Out-1',color='primary'),
                    html.Table([
                        html.Tr([html.Td(' #Button Pressed :'), html.Td(id='tab-cout')]),
                        ]),
                    ]
                    )
                    ####    
                        ]
                    )#### End button


                ] # children outside
            )  ### end

@app.callback(
    [Output('graph-container-1', component_property='children'),
    Output('graph-container-2', component_property='children')],
    [Input('refresh', 'n_clicks')])
def update_output_div(n_clicks):
    todayStr, nowDate, nowTime=upTime.GetDateTime()
    checkIn, checkOut, inTime, outTime=upTime.ReadCurrentStatus(todayStr, nowDate, nowTime, sheet)

    if(checkIn==0):
        colorLabel1="danger"
        message1="Go Check In : "+todayStr+" !!!"
    else:
        colorLabel1="success"
        message1="OK, Checked In at "+nowDate+", "+inTime+" ." 

    if(checkOut==0):
        colorLabel2="danger"
        message2="Go Check Out : "+todayStr+" !!!"
    else:
        colorLabel2="success"
        message2="OK, Checked Out at "+nowDate+", "+outTime+" ." 


    card1=dbc.Alert(message1, color=colorLabel1),    
    
    print(' C-In :: ',n_clicks)
    card2=dbc.Alert(message2, color=colorLabel2),
    
    #cards=dbc.Row(
    #    [
    #            dbc.Col(dbc.Card(card1, color=colorLabel1, inverse=True)),
    #            dbc.Col(dbc.Card(card2, color=colorLabel2, inverse=True)),
    #    ])

    return card1, card2
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