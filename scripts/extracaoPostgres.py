import os
import psycopg2
import pandas as pd
from datetime import datetime

DB_HOST = "localhost"
DB_PORT = "55432"
DB_NAME = "banvic"
DB_USER = "data_engineer"
DB_PASS = "v3rysecur&pas5w0rd"

def extracao_tabela(nome_tabela: str):
    conn = psycopg2.connect(
        host = DB_HOST,
        port = DB_PORT,
        dbname = DB_NAME,
        user = DB_USER,
        password = DB_PASS
    )

    query = f"select * from {nome_tabela};"
    df = pd.read_sql(query, conn)
    conn.close()

    today = datetime.today().strftime("%Y-%m-%d")
    output_dir = os.path.join(today, "postgres")
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{nome_tabela}.csv")
    df.to_csv(output_file, index=False, encoding="utf-8")

    print(f"Tabela {nome_tabela} extraída e salva em: {output_file}")

if __name__ == "__main__":
    extracao_tabela("clientes")