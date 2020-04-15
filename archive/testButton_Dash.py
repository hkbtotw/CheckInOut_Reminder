import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


card1 =[dbc.CardHeader("Check-In"),
        dbc.CardBody(
            [
                html.H4("Status", className="card-title"),
                html.P(                    
                    "-",
                    className="card-text",
                ),
                dbc.Button("Check-In", color="primary"),
            ]
        ),
    ]#### card1

card2 = [ dbc.CardHeader("Check_Out"),
        dbc.CardBody(
            [
                html.H4("Status", className="card-title"),
                html.P(
                    "-",
                    className="card-text",
                ),
                dbc.Button("Check-Out", color="primary"),
            ]
        ),
    ] #### card2

cards=dbc.Row(
        [
                dbc.Col(dbc.Card(card1, color="primary", inverse=True)),
                dbc.Col(dbc.Card(card2, color="secondary", inverse=True)),
        ])

app.layout= html.Div( id='number-plate',
           style={ 'marginLeft':'1.5%','marginRight':'1.5%','marginBottom':'0.8%','marginTop':'1.5%'  },
           children=[cards
            ]
       )


#@app.callback(
#    Output(component_id='my-div', component_property='children'),
#    [Input('button', 'n_clicks')],
#    state=[State(component_id='my-id', component_property='value')]
#)
#def update_output_div(n_clicks, input_value):
#    return 'You\'ve entered "{}" and clicked {} times'.format(input_value, n_clicks)

if __name__ == '__main__':
    app.run_server()