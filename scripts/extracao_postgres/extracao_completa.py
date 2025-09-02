import os
import psycopg2
import pandas as pd
from datetime import datetime

DB_HOST = "localhost"
DB_PORT = "55432"
DB_NAME = "banvic"
DB_USER = "data_engineer"
DB_PASS = "v3rysecur&pas5w0rd"

conn = psycopg2.connect(
    host=DB_HOST, 
    port=DB_PORT, 
    dbname=DB_NAME, 
    user=DB_USER, 
    password=DB_PASS
)
cur = conn.cursor()

cur.execute("""
    SELECT tablename
    FROM pg_catalog.pg_tables
    WHERE schemaname = 'public'
    ORDER BY tablename;
""")
tabelas = [linha[0] for linha in cur.fetchall()]

print("Tabelas encontradas:", tabelas)

data_hoje = datetime.today().strftime("%Y-%m-%d")
pasta_saida = os.path.join(data_hoje, "postgres")
os.makedirs(pasta_saida, exist_ok=True)

# Extração de cada tabela e salva em CSV
for tabela in tabelas:
    print(f"\nExtraindo: {tabela}")

    df = pd.read_sql(f'select * from "{tabela}";', conn)
    caminho_csv = os.path.join(pasta_saida, f"{tabela}.csv")
    df.to_csv(caminho_csv, index=False, encoding="utf-8")

    cur.execute(f'select COUNT(*) from "{tabela}";')
    qtd_db = cur.fetchone()[0]
    qtd_csv = len(df)

    if qtd_csv == qtd_db:
        status = "OK" 
    else:
        status = "ERRO"

    print(f"Linhas DB: {qtd_db} | Linhas CSV: {qtd_csv} -> {status}")
    print(f"Arquivo salvo: {caminho_csv}")

cur.close()
conn.close()

print("\nFinalizado! Todos os CSVs foram gerados na pasta:", pasta_saida)

