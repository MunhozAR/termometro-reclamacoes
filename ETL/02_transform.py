import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
import importlib
extract = importlib.import_module('01_extract')
extrair_dados = extract.extrair_dados

def transformar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe o DataFrame bruto do 01_extract.py e retorna limpo e pronto pra análise.
    """
    df = df.rename(columns={
        'Ano': 'ano',
        'Trimestre': 'trimestre',
        'Índice': 'indice',
        'Quantidade total de clientes \x96 CCS e SCR': 'total_clientes'
    })

    df['indice'] = df['indice'].astype(str).str.replace(',', '.').astype(float)
    df['total_clientes'] = pd.to_numeric(df['total_clientes'], errors='coerce').astype('Int64')
    df['periodo'] = df['ano'].astype(str) + ' ' + df['trimestre'].str.replace('º', '')

    digitais = ['Nubank', 'C6 Bank', 'Inter']
    tradicionais = ['Itaú', 'Bradesco', 'Santander', 'Banco do Brasil']

    def categorizar(banco):
        if banco in digitais:
            return 'Digital'
        elif banco in tradicionais:
            return 'Tradicional'
        else:
            return 'Fintech Pgto.'

    df['categoria'] = df['banco'].apply(categorizar)
    df = df.drop_duplicates()
    df = df.sort_values(['banco', 'ano', 'trimestre']).reset_index(drop=True)

    return df


if __name__ == '__main__':
    pasta = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
    df_raw = extrair_dados(pasta)
    df_clean = transformar_dados(df_raw)
    print(f"Shape: {df_clean.shape}")
    print(df_clean.head(10))
    print(f"\nCategorias: {df_clean['categoria'].unique()}")
    print(f"Tipos de índice: {df_clean['indice'].dtype}")