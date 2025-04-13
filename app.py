import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from data_loader import load_data

# Charger les données
df = load_data()

df = df.rename(columns={"date_publication": "date"})  
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["date"]) 

if "prix" in df.columns:
    df["prix"] = pd.to_numeric(df["prix"], errors="coerce")  

app = dash.Dash(__name__)

# Répartition des types de biens
fig_type = px.pie(df, names="type_bien", title="Répartition des types de biens")

# Distribution des prix
fig_prix = px.histogram(df, x="prix", title="Distribution des prix", nbins=50)

# Répartition des annonces par ville
fig_ville = px.bar(df, x="localisation", title="Nombre d'annonces par localisation", color="localisation")

# Évolution du nombre d'annonces
if not df.empty:
    df_evolution = df.groupby("date").size().reset_index(name="count")
    fig_evolution = px.line(df_evolution, x="date", y="count", title="Évolution des annonces")
else:
    fig_evolution = px.line(title="Aucune donnée disponible")

app.layout = html.Div(children=[
    html.H1("Tableau de Bord des Annonces", style={'textAlign': 'center'}),
    
    html.Div([
        dcc.Graph(figure=fig_type),
        dcc.Graph(figure=fig_prix)
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'flex-wrap': 'wrap'}),
    
    html.Div([
        dcc.Graph(figure=fig_ville),
        dcc.Graph(figure=fig_evolution)
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'flex-wrap': 'wrap'})
])

# Lancer l'application
if __name__ == '__main__':
    app.run(debug=True)
