import os
import pandas as pd
from datetime import datetime

ARQUIVO_FONTE = "transacoes.csv" 

def main():
    # Lê csv de origem -> agora sem acessar banco
    if not os.path.exists(ARQUIVO_FONTE):
        raise FileNotFoundError(f"Arquivo {ARQUIVO_FONTE} não encontrado na raiz do projeto.")

    df = pd.read_csv(ARQUIVO_FONTE)

    data_hoje = datetime.today().strftime("%Y-%m-%d")
    pasta_saida = os.path.join(data_hoje, "csv")
    os.makedirs(pasta_saida, exist_ok=True)

    destino = os.path.join(pasta_saida, "transacoes.csv")
    df.to_csv(destino, index=False, encoding="utf-8-sig")

    linhas = len(df)
    colunas = list(df.columns)
    print(f" Transacoes.csv salvo em: {destino}")
    print(f" Linhas: {linhas} | Colunas: {len(colunas)} -> OK")
    print(f" Cabeçalho: {colunas}")

if __name__ == "__main__":
    main()
