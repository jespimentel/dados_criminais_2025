import marimo

__generated_with = "0.18.4"
app = marimo.App(width="full")


@app.cell
def _(mo):
    mo.md(r"""
    ## Promotoria de Justiça de Piracicaba

    ### Dados Criminais - 2025 (plotagem com os dados da SSP/SP)
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import folium
    from folium.plugins import MarkerCluster
    from folium.plugins import HeatMap
    return HeatMap, MarkerCluster, folium, mo, pd


@app.cell
def _(pd):
    # Lê o arquivo CSV
    df = pd.read_csv('dados_criminais_geo.csv')
    return (df,)


@app.cell
def _(df, mo):
    # Cria o dropdown
    filtro_crime = mo.ui.dropdown(
        options=sorted(list(df['NATUREZA_APURADA'].unique())), 
        label="Selecione: ", 
        value = 'TRÁFICO DE ENTORPECENTES' # Valor padrão
    )

    # Exibe o dropdown
    filtro_crime
    return (filtro_crime,)


@app.cell
def _(mo):
    # Cria o dropdown
    tipo_mapa = mo.ui.dropdown(
       options=["Clusters", "Calor"],
       label="Selecione:",
       value="Calor"
    )

    # Exibe o dropdown
    tipo_mapa
    return (tipo_mapa,)


@app.cell
def _(df, filtro_crime):
    # Filtra os dados
    df_filtrado = df[df['NATUREZA_APURADA'] == filtro_crime.value]
    return (df_filtrado,)


@app.cell
def _(HeatMap, folium):
    def gera_mapa_calor(dados):
        if dados.empty:
            return None

        lat_media = dados['LATITUDE'].mean()
        lon_media = dados['LONGITUDE'].mean()

        mapa_obj = folium.Map(location=[lat_media, lon_media], zoom_start=12)

        # Prepara a lista de coordenadas [[lat, lon], [lat, lon], ...]
        coordenadas = dados[['LATITUDE', 'LONGITUDE']].values.tolist()

        # Adiciona a camada de calor ao mapa
        HeatMap(coordenadas).add_to(mapa_obj)

        return mapa_obj
    return (gera_mapa_calor,)


@app.cell
def _(MarkerCluster, folium):
    def gera_mapa_clusterizado(dados):
        if dados.empty:
            return None

        lat_media = dados['LATITUDE'].mean()
        lon_media = dados['LONGITUDE'].mean()

        mapa_obj = folium.Map(location=[lat_media, lon_media], zoom_start=12)
        marker_cluster = MarkerCluster().add_to(mapa_obj)

        for _, row in dados.iterrows():
            html_popup = f"""
            <strong>{row['NATUREZA_APURADA']}</strong> <br>
            <strong>BO nº {row['NUM_BO']}</strong> <br>
            {row['DATA_OCORRENCIA_BO']}<br>
            {row['NOME_DELEGACIA']}
            """
            folium.Marker(
                location=[row['LATITUDE'], row['LONGITUDE']],
                popup=html_popup,
                icon=folium.Icon(icon='info-sign')
            ).add_to(marker_cluster)

        return mapa_obj
    return (gera_mapa_clusterizado,)


@app.cell
def _(df_filtrado, gera_mapa_calor, gera_mapa_clusterizado, tipo_mapa):
    if tipo_mapa.value == 'Calor':
        mapa_final = gera_mapa_calor(df_filtrado)
    else:
        mapa_final = gera_mapa_clusterizado(df_filtrado)   
    return (mapa_final,)


@app.cell
def _(mapa_final, mo):
    if mapa_final is not None:
        saida = mo.Html(mapa_final._repr_html_())
    else:
        saida = mo.md("Selecione um crime acima para visualizar o mapa.")

    saida
    return


if __name__ == "__main__":
    app.run()
