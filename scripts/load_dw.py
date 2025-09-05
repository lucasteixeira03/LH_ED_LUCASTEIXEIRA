import os
import sys
import psycopg2
from datetime import datetime

DW_HOST = "host.docker.internal"
DW_PORT = "56432"
DW_NAME = "banvic_warehouse"
DW_USER = "lucas_dw"
DW_PASS = "dr0w5sap&rucesyr3v" 

DATA_DIA = datetime.today().strftime("%Y-%m-%d")
BASE_DIR = os.path.join(os.getcwd(), DATA_DIA)
POSTGRES_DIR = os.path.join(BASE_DIR, "postgres")
CSV_DIR = os.path.join(BASE_DIR, "csv")

TABELAS_POSTGRES = [
    "agencias",
    "clientes",
    "colaborador_agencia",
    "colaboradores",
    "contas",
    "propostas_credito",
]

ARQUIVO_TRANSACOES = os.path.join(CSV_DIR, "transacoes.csv")

def get_dw_conn():
    return psycopg2.connect(
        host=DW_HOST, 
        port=DW_PORT, 
        dbname=DW_NAME, 
        user=DW_USER, 
        password=DW_PASS
    )

def truncate(cur, tabela):
    cur.execute(f'TRUNCATE TABLE "{tabela}";')

def copy_csv(cur, tabela, caminho_csv):
    with open(caminho_csv, "r", encoding="utf-8") as f:
        cur.copy_expert(
            sql=f'COPY "{tabela}" FROM STDIN WITH CSV HEADER',
            file=f
        )

def count_rows(cur, tabela):
    cur.execute(f'SELECT COUNT(*) FROM "{tabela}";')
    return cur.fetchone()[0]

def main():
    if not os.path.isdir(BASE_DIR):
        print(f" ERROR: PASTA DO DIA NÃO ENCONTRADA!: {BASE_DIR}")
        sys.exit(1)

    if not os.path.isdir(POSTGRES_DIR):
        print(f" ERROR: PASTA DE ORIGEM (postgres) NÃO ENCONTRADA!: {POSTGRES_DIR}")
        sys.exit(1)

    conn = get_dw_conn()
    cur  = conn.cursor()

    try:
        for tabela in TABELAS_POSTGRES:
            caminho_csv = os.path.join(POSTGRES_DIR, f"{tabela}.csv")
            if not os.path.exists(caminho_csv):
                print(f" ERROR: Arquivo não encontrado(pulando): {caminho_csv}")
                continue

            print(f"\n CARREGANDO: {tabela}")
            truncate(cur, tabela)
            copy_csv(cur, tabela, caminho_csv)
            conn.commit()

            qtd = count_rows(cur, tabela)
            print(f"   -> {qtd} linhas carregadas no DW")

        if os.path.exists(ARQUIVO_TRANSACOES):
            print(f"\n CARREGANDO: transacoes")
            truncate(cur, "transacoes")
            copy_csv(cur, "transacoes", ARQUIVO_TRANSACOES)
            conn.commit()

            qtd = count_rows(cur, "transacoes")
            print(f"   -> {qtd} linhas carregadas no DW")
        else:
            print(f" ERROR: transacoes.csv não encontrado em: {ARQUIVO_TRANSACOES}")

        print("\n Carga concluída com sucesso no DW!")

    except Exception as e:
        conn.rollback()
        print(" Erro durante a carga:", e)
        sys.exit(1)
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
