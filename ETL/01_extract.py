import pandas as pd
import os

# Mapeamento dos nomes do Bacen para nomes padronizados
MAPEAMENTO_BANCOS = {
    'NUBANK (conglomerado)': 'Nubank',
    'C6 BANK (conglomerado)': 'C6 Bank',
    'INTER (conglomerado)': 'Inter',
    'ITAU (conglomerado)': 'Itaú',
    'BRADESCO (conglomerado)': 'Bradesco',
    'SANTANDER (conglomerado)': 'Santander',
    'BB (conglomerado)': 'Banco do Brasil',
    'PAGBANK-PAGSEGURO (conglomerado)': 'PagBank',
    'MERCADO PAGO (conglomerado)': 'Mercado Pago',
    'PICPAY (conglomerado)': 'PicPay'
}

def extrair_dados(pasta_raw: str) -> pd.DataFrame:
    """
    Lê todos os CSVs da pasta raw, filtra os 10 bancos
    e retorna um único DataFrame consolidado.
    """
    arquivos = sorted(os.listdir(pasta_raw))
    dfs = []

    for arquivo in arquivos:
        caminho = os.path.join(pasta_raw, arquivo)
        df = pd.read_csv(caminho, sep=';', encoding='latin-1')

        # Filtra só os 10 bancos
        df = df[df['Instituição financeira'].isin(MAPEAMENTO_BANCOS.keys())]

        # Renomeia para nome padronizado
        df['banco'] = df['Instituição financeira'].map(MAPEAMENTO_BANCOS)

        # Mantém só as colunas que existem em todos os arquivos
        df = df[['Ano', 'Trimestre', 'banco', 'Índice', 
                 'Quantidade total de clientes \x96 CCS e SCR']]

        dfs.append(df)

    # Junta todos os trimestres num único DataFrame
    df_final = pd.concat(dfs, ignore_index=True)
    return df_final


if __name__ == '__main__':
    pasta = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
    df = extrair_dados(pasta)
    print(f"Shape: {df.shape}")
    print(df.head(10))