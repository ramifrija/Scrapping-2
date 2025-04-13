import pandas as pd
import psycopg2

# Connexion à la base de données PostgreSQL
def load_data():
    conn = psycopg2.connect(
        dbname="scrapping",
        user="postgres",
        password="1",
        host="localhost",
        port="5432"
    )
    query = "SELECT * FROM tunisie_annonce"
    df = pd.read_sql(query, conn)
    conn.close()
    
   
    return df

data = load_data()
