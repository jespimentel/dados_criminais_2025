import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell
def _():
    path_da_planilha = r'C:\Users\jepim\Desktop\projetos\gestao_dados\SPDadosCriminais_2025.xlsx'
    return (path_da_planilha,)


@app.cell
def _(path_da_planilha, pd):
    dados_criminais_1sem = pd.read_excel(path_da_planilha, sheet_name=1)
    return (dados_criminais_1sem,)


@app.cell
def _(path_da_planilha, pd):
    dados_criminais_2sem = pd.read_excel(path_da_planilha, sheet_name=2)
    return (dados_criminais_2sem,)


@app.cell
def _(dados_criminais_1sem, mo):
    # Lista de municípios
    municipios = sorted(dados_criminais_1sem['NOME_MUNICIPIO'].unique().tolist())

    # 2. Criação do componente de seleção
    filtro_municipio = mo.ui.dropdown(
        options=municipios, 
        label="Selecione um município: ",
        value="PIRACICABA" # Valor padrão
    )

    # 3. Exibição do filtro
    filtro_municipio
    return (filtro_municipio,)


@app.cell
def _(dados_criminais_1sem, dados_criminais_2sem, filtro_municipio, pd):
    # Filtragem dos dados
    dados_criminais_1sem_filtrados = dados_criminais_1sem[dados_criminais_1sem['NOME_MUNICIPIO'] == filtro_municipio.value]
    dados_criminais_2sem_filtrados = dados_criminais_2sem[dados_criminais_2sem['NOME_MUNICIPIO'] == filtro_municipio.value]

    # Concatenação dos dataframes
    dados_criminais_ano = pd.concat([dados_criminais_1sem_filtrados, dados_criminais_2sem_filtrados])

    dados_criminais_ano['NATUREZA_APURADA'].value_counts()
    return (dados_criminais_ano,)


@app.cell
def _(dados_criminais_ano, pd):
    dados_criminais_ano['LATITUDE'] = pd.to_numeric(dados_criminais_ano['LATITUDE'], errors='coerce')
    dados_criminais_ano['LONGITUDE'] = pd.to_numeric(dados_criminais_ano['LONGITUDE'], errors='coerce')
    return


@app.cell
def _(dados_criminais_ano):
    df_georreferenciado = dados_criminais_ano[(~dados_criminais_ano['LATITUDE'].isna()) & (dados_criminais_ano['LATITUDE'] != 0)]
    df_georreferenciado['NATUREZA_APURADA'].value_counts()
    return (df_georreferenciado,)


@app.cell
def _(df_georreferenciado):
    df_georreferenciado.to_csv('dados_criminais_geo.csv')
    return


if __name__ == "__main__":
    app.run()
