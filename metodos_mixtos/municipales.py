import pandas as pd

def grafica_coca_municipio(cod_dane, vrds, emf=True, file_name='.'):
    '''Returns a chart with the hectares of coca in a municipality over the years
    Parameters:
        cod_dane (str): 5 digit unique municipality code from DANE
        vrds (gdf): base de veredas geodataframe
        emf (bool): True to ad the line for Erradicación Manual Forzada'''
    dfm = vrds[vrds['DPTOMPIO'] == cod_dane]
    s1 = dfm.filter(regex='coca').sum().transpose()
    df = pd.DataFrame(s1).reset_index()
    df['ano'] = range(2010,2010+df.shape[0])
    df.set_index("ano", inplace=True)
    df.drop('index', axis=1, inplace=True)
    df.columns = ['Cultivos de hoja de coca']
    ax = df.plot(figsize=(10,5))
    ax.set_ylabel("Hectáreas")
    nom_mpio = dfm['NOMB_MPIO'].unique()[0]
    ax.set_title("Hectáreas de coca en el municipio de {}".format(nom_mpio))
    ax.set_xlabel("Año")
    #Add the EMF line
    if emf == True:
        s2 = dfm.filter(regex='EMF').sum().transpose()
        df = pd.DataFrame(s2).reset_index()
        df['ano'] = range(2016,2016+df.shape[0])
        df.set_index("ano", inplace=True)
        df.drop('index', axis=1, inplace=True)
        df.columns = ['Erradicación Manual Forzada']
        df.plot(figsize=(10,5), ax=ax)  
    if file_name!='.':
        ax.savefig(file_name)
        
    return ax