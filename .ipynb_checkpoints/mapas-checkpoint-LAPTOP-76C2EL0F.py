#Este archivo contiene funciones que facilitan la construcción de mapas
import pandas as pd
import geopandas as gpd
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import seaborn as sns
import sys
import numpy as np
import mapclassify
import contextily as ctx
from shapely.geometry import box
import mapclassify


#%%
def diccionario_rutas(path_OneDrive='/Users/Daniel/OneDrive - C- ANALISIS SAS/'):
    """Retornan un diccionario con las rutas a los archivos
    ---
    path_OneDrive: Ruta al folder que contiene el folder de OneDrive. Default es '/Users/Daniel/'
    """
    user = path_OneDrive
    paths = {#PNIS
        'pagos': user+'programacion/geoinfo/Respuesta DCSI 3/Registro_2020_Noviembre.xlsx',
        'lotes' :user+'programacion/geoinfo/Respuesta DCSI 2/Monitoreo_UNODC/Lotes_Comprometidos_PNIS.shp',
        'lotes2020': user+'programacion/geoinfo/Respuesta DCSI 3/Lotes_PNIS_ErradicacionTotal_11112020.shp',
        'lotes_pagos_PNIS' : user+'programacion/geoinfo/Respuesta DCSI 2/Monitoreo_UNODC/Lotes_PNIS_pagos.shp',
        'veredas_pnis':user+'programacion/geoinfo/Respuesta DCSI 2/Monitoreo_UNODC/Vdas_PNIS.shp',
        #'pics':user+'programacion/geoinfo/PICs/Shapes PICS/Entregar_pres.shp', esta capa esta desactualizada
        'coca':user+'programacion/geoinfo/Colombia/Narcotrafico/densidad_coca/',   #Ruta al folder que tiene todos los shapes      

        #Conflicto
        #'armada':user+'programacion/geoinfo/Colombia/Conflicto/unidades_armada.shp',
        #'abolladuras':user+'programacion/geoinfo/Colombia/Conflicto/abolladura_1.shp',
        #'labs':user+'programacion/geoinfo/Colombia/Narcotrafico/Lab_1.shp',
        'emf': user+'programacion/geoinfo/Colombia/Narcotrafico/emf/EMF_2016_2020_Completo/EMF_2016_2020_Completo.shp',
        'zonas_futuro':user+'programacion/geoinfo/Colombia/Territoriales/zonas_futuro/zonas_futuro.shp',
        'map':user+'programacion/geoinfo/Colombia/Conflicto/map_2016_2020.shp',
        'map_base':user+'programacion/geoinfo/Colombia/Conflicto/map/map_octubre_31_2020.xlsx',

        #Politico administrartivas
        #'caserios':user+'programacion/geoinfo/Colombia/Territoriales/Caseríos/Administrativo_P_Escala_1100.000_Cartografia_Base__IGAC.shp',
        #'aurbana':user+'programacion/geoinfo/Colombia/Territoriales/Área Urbana/Administrativo_R.shp',
        'veredas':user+'programacion/geoinfo/Colombia/Territoriales/CRVeredas_2017.shp',
        'municipios':user+'programacion/geoinfo/Colombia/ADMINISTRATIVO/VRDS_MPIO_POLITICO.shp',
        'municipios_indices':user+'programacion/geoinfo/Colombia/ADMINISTRATIVO/VRDS_MPIO_INDEX.csv', #DF with indices and municipality codes to allow for a trageted import of the municipios shape file (based on row number)
        'deptos':user+'programacion/geoinfo/Colombia/ADMINISTRATIVO/MGN_DPTO_POLITICO.shp',
        'pnn' : user+'programacion/geoinfo/Colombia/Territoriales/Parques_Nacionales_Naturales.shp',
        'resguardos':user+'programacion/geoinfo/Colombia/Territoriales/Resguardos_Indigenas.shp',
        'consejos':user+'programacion/geoinfo/Colombia/Territoriales/Consejos_comunitarios.shp',
        'jes': user+'programacion/geoinfo/Colombia/Territoriales/jurisdicciones_especiales.shp',
        'aurbana':user+'programacion/geoinfo/Colombia/Territoriales/perimetro_urbano/U_PERIMETRO.shp',
        'panel_municipal_pgn':user+'programacion/bases/municipales/panel_municipales_pgn.xlsx',

        #Geograficas
        'rios':user+'programacion/geoinfo/Colombia/Geografia/rios/Rios_principales.shp',

        #Infraestructura
        #'redat':user+'programacion/geoinfo/Colombia/Infraestructura/Red_Alta_Tension/Red_Alta_Tension.shp',
        'vias':user+'programacion/geoinfo/Colombia/Infraestructura/Via/Via.shp',
        #Agro
        'palma':user+'programacion/geoinfo/Agro/Palma/Lotes_18022019.shp',

        #Última versión de la base final ya procesada
        'vrds': user+'programacion/bases/base_veredas/base_veredas.shp',
        'vrds_pickle': user+'programacion/bases/base_veredas/vrds',
        
        # CNPV y CNA
        'mgn_cnpv': user+'programacion/bases/CNPV/ShapefileMGN_ANM_SECCION_RURAL/MGN_ANM_SECCION_RURAL.shp',
        'tabla_referencia_cnpv': user+'programacion/bases/CNPV/ShapefileMGN_ANM_SECCION_RURAL/tabla_referencia_cnpv.xlsx',
        'encabezado_cna': user+'programacion/bases/CNA/Total_nacional(csv)/S01_15(Unidad_productora).csv',
        'cultivos_cna': user+'programacion/bases/CNA/Total_nacional(csv)/S06A(Cultivos).csv',
        'maquinaria_cna': user+'programacion/bases/CNA/Total_nacional(csv)/S09(Maquinaria_uso_agropecuario).csv',
        'construcciones_cna': user+'programacion/bases/CNA/Total_nacional(csv)/S10(Construcciones_uso_agropecuario).csv',
        'referencias_cna': user+'programacion/bases/CNA/referencias.xlsx'
        
        }
    
    #Filepaths for the coca shapes
    
    def ano(year):
        """Returns a 2 digit year"""
        if i in (range(1,10)):
            return '0'+str(i)
        if i > 9:
            return str(i)
    
    for i in range(1,20):
        key = 'coca'+ano(i)
        paths[key] = user+'programacion/geoinfo/Colombia/Narcotrafico/densidad_coca/Densidad_Cultivos_Ilícitos_20{}.shp'.format(ano(i))
    
            
    #Paths OS agnostic paths
    for i in paths:
        paths[i] = os.path.abspath(paths[i])

    return paths

#%%Se crea una función para cargar una sola capa a la vez, en caso que se necesite
def cargar_capa_individual(filename, **kwargs):
    """Returns a gdf with the shape loaded and adjusted to the CRS:3116 (Bogota-centred metric system)
    Parameters:
        filename : str, path object or file-like object
            Either the absolute or relative path to the file or URL to
            be opened, or any object with a read() method (such as an open file
            or StringIO)
        mask : dict | GeoDataFrame or GeoSeries | shapely Geometry, default None 
            Filter for features that intersect with the given dict-like geojson
            geometry, GeoSeries, GeoDataFrame or shapely geometry.
            CRS mis-matches are resolved if given a GeoSeries or GeoDataFrame.
            Cannot be used with bbox.
        **kwargs :
            Keyword args to be passed to the `read_file` method
            in the geopandas library when opening the file. The mask and bbox arguments might be especially useful"""
      
    if filename[-3:] != 'shp':  # Se excluyen otros tipos de archivos
        return print('La ruta no apunta a un archivo Shape')
    capa = gpd.read_file(filename, encoding='utf-8', **kwargs)
   # print('Ajustando capa {}'.format(filename.split('/')[-1:][0]))
    # Se unifica todo en mismo crs
    capa = capa.to_crs({'init': 'EPSG:4326'})
    # Se corta para que los shapes no excedan las dimensiones de cobertura del crs métrico centrado en Bogotá
    capa = capa.cx[-79.1:-66.87, -4.23:13.68]
    # Se pasa todo a un crs métrico centrado en Bogotá, para aumentar la precisión de los cálculos y para que queden en metros
    capa = capa.to_crs({'init': 'EPSG:3116'})   
    #If a mask is used, clip the final layer to avoid possible inaccuracies in the read_file method of geopandas
    if 'mask' in kwargs.keys():
        mask = kwargs.get('mask').to_crs({'init': 'EPSG:3116'})
        mask['geometry'] = mask.buffer(0.01)
        if filename.split('/')[-1:][0] in ['VRDS_MPIO_POLITICO.shp', 
                                           'CRVeredas_2017.shp',
                                           'base_veredas.shp', 'Resguardos_Indigenas.shp', 
                                           'Consejos_comunitarios.shp', 
                                           'Lotes_18022019.shp']:
            capa = capa[capa.area>0] #Drop bordering polygons that have no area after clipping
    #        print('Empty polygons dropped')
            capa['geometry'] = capa.buffer(0.01) #Ajust geometries to avoid Rtree errors
            print('Buffer created to avoid errors while joining')
            capa = gpd.clip(capa, mask)
     #       print('Final layer clipped to the mask extent for accuracy')
            return capa    
        capa = gpd.clip(capa, mask)
      #  print('Final layer clipped to the mask extent for accuracy')
        return capa
    #print('Layer adjusted')
    return capa

#Utility functions to facilitate the creation of more complex ones

def indice_municipio(cod_mpio, **kwargs):
    """Retorna la fila que corresponde al municipio en el archivo 'municipos' del diccionario paths.
        Parametros:
            cod_mpio (str): Código del municipio en formato string"""
    paths = diccionario_rutas(**kwargs)
    inds = pd.read_csv(paths['municipios_indices'], 
                      dtype={'DPTOMPIO':str},
                      index_col=0)
    ind = inds[inds['DPTOMPIO']==cod_mpio]

    return ind.index.to_list()[0]+1

def get_bounding_box(gdf):
    """Returns a gdf with only one row that is box that encloses all geometries in the initial gdf
    ------
    Parameters:
        gdf (gdf): Geopandas.GeoDataFrame object"""
    bbx = box(*gdf.total_bounds)
    bbx = gpd.GeoDataFrame(geometry=[bbx])
    bbx.crs = gdf.crs
    return bbx

#This is a function to create custom, automatic maps for each municipality in Colombia

def mapa_general(shape,
                año='2019',
                coca='coca19', 
                emf_ano='2019', 
                vias=True, 
                figsize=(12, 12), 
                vrds=True, 
                rios=True,
                aurbana=True,
                pnn=True,
                minas=True,
                pnis=True,
                cca=True,
                rsg=True,
                zf=True,
                palma=False,
                title='.', 
                 **kwargs):
    """Retorna un mapa de matplot lib con el municipio y las diferentes capas resaltadas.
            Parametros:
                shape (gdf): Geodataframe with the zone of interest.
                coca (str): Nombre las capas de coca de 2001-19, escrito como cocaYY
                emf (str): Year for the EMF (manual erradication) layer (data from 2016)
                vrds (Bool): True to show the borders and names of veredas. Default is true. 
                minas (Bool): True to show the points with accidents due to Land Mines (last 5 years). Default is true. 
                figsize : tuple of integers (default None)
                        Size of the resulting matplotlib.figure.Figure. If the argument
                        axes is given explicitly, figsize is ignored."""
    paths = diccionario_rutas(**kwargs)
    df=shape
    bbx = get_bounding_box(shape)
    
    #df = mpios[mpios['DPTOMPIO']==cod_mpio]
    fig, ax = plt.subplots(figsize=figsize)

    #Get the bounding box to cut the other layers
    #df = cargar_capa_individual(paths['municipios'], maks=bbx)
    df.plot(ax=ax, color='white', alpha=0.01)
    #Load jurisdiction layers
    legend_patches = [] #List to store legend patches
    if pnn==True:
        pnn = cargar_capa_individual(paths['pnn'], mask=bbx)
        pnn.plot(ax=ax, color='limegreen', alpha=0.5)
        #Add label
        pnn.apply(lambda x: ax.annotate(s=x['NOM_PARQ'], 
                                         xy=x.geometry.centroid.coords[0], 
                                         ha='center', 
                                         color='forestgreen', 
                                         fontsize=10),
                   axis=1)
        pnn.boundary.plot(ax=ax, color='forestgreen')
        pnn_legend = mpatches.Patch(color='limegreen', label='Parque Nacional') 
        legend_patches = legend_patches + [pnn_legend]
    if cca==True:
        cca = cargar_capa_individual(paths['consejos'], mask=bbx)
        cca.plot(ax=ax, color='peru', alpha=0.5)
        #Add label
        cca.apply(lambda x: ax.annotate(s=x['NOMBRE'], 
                                         xy=x.geometry.centroid.coords[0], 
                                         ha='center', 
                                         color='saddlebrown', 
                                         fontsize=7, 
                                        alpha=0.7),
                   axis=1)
        cca.boundary.plot(ax=ax, color='saddlebrown')
        cca_legend = mpatches.Patch(color='peru', label='CC Afro') 
        legend_patches = legend_patches + [cca_legend]
    if rsg==True:
        rsg = cargar_capa_individual(paths['resguardos'], mask=bbx)
        rsg.plot(ax=ax, color='palevioletred', alpha=0.8)
        #Add label
        rsg.apply(lambda x: ax.annotate(s=x['NOM_RESG'], 
                                         xy=x.geometry.centroid.coords[0], 
                                         ha='center', 
                                         color='purple', 
                                         fontsize=7,
                                           alpha=0.7),
                   axis=1)
        rsg.boundary.plot(ax=ax, color='purple')
        rsg_legend = mpatches.Patch(color='palevioletred', label='Resguardo') 
        legend_patches = legend_patches + [rsg_legend]
    if zf==True:
        zf = cargar_capa_individual(paths['zonas_futuro'], mask=bbx)
        zf.plot(ax=ax, color='lightsteelblue', alpha=0.5)
        zf_legend = mpatches.Patch(color='lightsteelblue', label='Zona Futuro') 
        legend_patches = legend_patches + [zf_legend]
    #Se establecen los límites del mapa con base en los límites del municipio
    b = df.total_bounds
    ax.set_xlim(b[0]-100, b[2]+100)
    ax.set_ylim(b[1]-100, b[3]+100)

    #Se cargan las capas
    coca = cargar_capa_individual(paths[coca], mask=bbx) #Coca
    coca.plot(ax=ax, column='areacoca', cmap='Reds', alpha=0.5)
    sm = plt.cm.ScalarMappable(cmap='Reds', norm=mpl.colors.Normalize(0,100))
    fig.colorbar(sm, ax=ax, label='Hectáreas de coca', aspect=60, fraction=0.046, pad=0.04)
    if vrds==True:
        vrds = cargar_capa_individual(paths['vrds'], mask=df) #Veredas
        vrds.plot(ax=ax, edgecolor='grey', alpha=0.001)  
        #Labels for veredas
        vrds.apply(lambda x: ax.annotate(s=x['NOMBRE_VER'], xy=x.geometry.centroid.coords[0], ha='center', color='grey', fontsize=7),axis=1);
        vrds.boundary.plot(ax=ax, color='grey', linestyle='--') #Draw boundaries for veredas
    #EMF
    try:
        emf = cargar_capa_individual(paths['emf'], mask=bbx)
        emf['FECHA'] = pd.to_datetime(emf['FECHA'])
        emf.set_index('FECHA', inplace=True)
        emf = emf[emf_ano]
        emf.plot(ax=ax, color='green', marker=".",markersize=10, alpha=0.4)
        emf_legend = mpatches.Patch(color='green', label='EMF')
        legend_patches = legend_patches + [emf_legend]
    except:
        print('Area sin emf')
    #Add the rivers layer
    if rios==True:
        rios = cargar_capa_individual(paths['rios'], mask=bbx)
        rios.plot(ax=ax, color='turquoise')    
    if vias==True:
        vias = cargar_capa_individual(paths['vias'], mask=bbx)
        vias.plot(ax=ax, color='yellow')  
        vias_legend = mpatches.Patch(color='yellow', label='Vías')
        legend_patches = legend_patches + [vias_legend]
    if aurbana==True:
        aurbana = cargar_capa_individual(paths['aurbana'], mask=bbx)
        aurbana.plot(ax=ax, color='grey')
        aurbana_legend = mpatches.Patch(color='grey', label='Área Urbana') 
        legend_patches = legend_patches + [aurbana_legend]
    if minas == True:
        minas = cargar_capa_individual(paths['map'], mask=bbx)
        minas.plot(ax=ax, color='red', marker="*",markersize=30, alpha=1)
        red_star = mlines.Line2D([], [], color='red', marker='*', linestyle='None', markersize=10, label='Minas Ant.') #Add labels
        legend_patches = legend_patches + [red_star]
    if pnis == True:
        pnis = cargar_capa_individual(paths['lotes2020'], mask=bbx)
        pnis.plot(ax=ax, color='blue', marker=".",markersize=10, alpha=0.4)
        pnis_legend = mpatches.Patch(color='blue', label='Lotes PNIS')
        legend_patches = legend_patches + [pnis_legend] 
    if palma == True:
        palma = cargar_capa_individual(paths['palma'], mask=bbx)
        palma.plot(ax=ax, color='darkgreen', marker=".",markersize=10, alpha=0.8)
        palma_legend = mpatches.Patch(color='darkgreen', label='Cultivos palma')
        legend_patches = legend_patches + [palma_legend]
    #df2.plot(ax=fig, figsize=(10, 10), color='grey', alpha=0.5)

    #Titulo

    if title!= 'Mapa de diagnóstico zonal':
        ax.set_title(title, fontdict={'fontsize': 16})

    #Se grafica el lote con base en las coordenadas recibidas
    ctx.add_basemap(ax=ax, source=ctx.providers.Stamen.Terrain, crs=df.crs.to_string())
    ax.set_axis_off()
    df.boundary.plot(ax=ax, color='black')  #Bounds
    
    #Legenda
    #veredas_municipo = mpatches.Patch(color='green', label='Coca en 20'.format(coca[-2:]))
    #vereda = mpatches.Patch(color='grey', label='Vereda en la que se ubica el lote')
   
    plt.legend(handles=legend_patches)
    
    return ax   

def mapa_municipal(cod_mpio, año=2019, filename='.', dpi=100, **kwargs):
    """Retorna un mapa de diagnóstico del municipio seleccionado
    Parameters:
    -----------
        cod_mpio (str): Código del municipio en formato string.
        año:
        kwargs: All other arguments from mapa_general()
        """
    paths = diccionario_rutas(**kwargs)
    row= indice_municipio(cod_mpio, **kwargs)
    df = cargar_capa_individual(paths['municipios'], rows=slice(row-1,row))
    municipio = df['NOMB_MPIO'].iloc[0].capitalize()
    depto = df['NOM_DEP'].iloc[0].capitalize()
    if 'title' not in kwargs:
        kwargs['title'] = 'Mapa diagnóstico del municipio de {}, {} ({})'.format(municipio, depto, año)
    ax = mapa_general(df, **kwargs)
    if 'title' in kwargs:
        ax.set_title(kwargs.get('title', 'Mapa diagnóstico'), fontdict={'fontsize': 16})
    df.apply(lambda x: ax.annotate(s=x['NOMB_MPIO'], xy=x.geometry.centroid.coords[0], ha='center', color='black', fontsize=10),axis=1)
    if filename != '.':    
        plt.savefig(filename, dpi)
    return ax   
    

