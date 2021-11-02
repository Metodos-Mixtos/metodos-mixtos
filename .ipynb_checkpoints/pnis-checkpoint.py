def ubicar_otros_beneficiarios_pnis(vrds, lts, df2):
    
    """Retorna el df de pagos del PNIS con algunos de los beneficiarios que no tienen lotes ubicados
        ---
        Parámetros:
            vrds (gdf): geopandas dataframe con la capa de veredas del DANE
            lts (gdf): geopandas dataframe con los lotes georreferenciados del PNIS
            df2: (df): Dataframe general de registro recibido de la DSCI con información de los beneficiarios del PNIS
    """
   

    lts = gpd.sjoin(lts, vrds[['CODIGO_VER', 'geometry']]) #Se le pega la información de las veredas a los lotes

    #Seleccionar unicamente el lote mas grande de cada beneficiario
    ids = lts.groupby(['CUB'])['A_ERRA'].idxmax()
    lts = lts.loc[ids]

    #Se crea una nueva variable con la vereda y el código DANE juntos para evitar errores
    def vereda_unida(x):
        return str(x['CODIGO DANE']) + '_' + x['VEREDA']
    
    df2['VEREDA_PNIS'] = df2.apply(vereda_unida, axis=1)

    #Asignar las veredas del DANE al df de general de registro
    df4 = df2[['CUB', 'VEREDA_PNIS']].merge(lts[['CUB', 'CODIGO_VER']], on='CUB', how='left')
    df5 = df4[['VEREDA_PNIS','CODIGO_VER']].dropna().drop_duplicates()
    df6 = df4[['VEREDA_PNIS','CODIGO_VER']].dropna()
    df7 = df6.groupby(['VEREDA_PNIS', 'CODIGO_VER']).size().reset_index() #df con la frequencia de veredas DANE por veredas PNIS
    df7.columns=['VEREDA_PNIS', 'CODIGO_VER', 'FRECUENCIA']
    df7 = df7.loc[df7.groupby('CODIGO_VER')['FRECUENCIA'].idxmax()] #Unicamente las observaciones mas frecuentes
    vrds_pnis_dane = dict(zip(df7['VEREDA_PNIS'], df7['CODIGO_VER'])) #Se crea un diccionario para asignar las veredas PNIS a veredas DANE cuando no hay cruce geografico

    #Nota: La DSCI también suministró un Shape de las veredas PNIS que el programa a definido. Sin embargo, la siguiente tabla muestra que hay veredas PNIS que tienen beneficiarios que están hasta en 16 veredas DANE diferentes. Esto indica que las veredas PNIS son mucho más grandes que las del DANE. Por lo tanto, utilizar las veredas PNIS produciría calculos más imprecisos que con las veredas del DANE, de manera que se trabaja con esta última.

    reg = df2.merge(lts[['CUB', 'CODIGO_VER']], on='CUB', how='left')
    reg['CODIGO_VER'].fillna(True, inplace=True)

    def asignar_veredas(x, dic):
        """Esta función asigna veredas para los casos en los que no hay cruce geográfico pero sí hay otro beneficiario asignado a la misma vereda PNIS que tenía un lote."""
        if x['CODIGO_VER']!=True:
            return x['CODIGO_VER']
        if x['VEREDA_PNIS'] in dic.keys():
            return dic[x['VEREDA_PNIS']]
        else:
            return np.nan

    reg['CODIGO_VER'] = reg.apply(lambda x: asignar_veredas(x, vrds_pnis_dane), axis=1)
    return reg