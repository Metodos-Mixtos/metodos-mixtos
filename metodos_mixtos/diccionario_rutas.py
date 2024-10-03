#Esta función contiene las rutas de uso más común en Veredata

import os

def diccionario_rutas(path_OneDrive):
    """Retornan un diccionario con las rutas a los archivos
    ---
    path_OneDrive: Ruta al folder que contiene el folder de OneDrive.
    """
    user = path_OneDrive
    paths = {#PNIS
        'pagos': user+'programacion/geoinfo/Respuesta DCSI 3/Registro_2020_Noviembre.xlsx',
        'pagos_2021': user+'programacion/geoinfo/Respuesta DCSI 3/registro_2021.xlsx',
        'lotes' :user+'programacion/geoinfo/Respuesta DCSI 2/Monitoreo_UNODC/Lotes_Comprometidos_PNIS.shp',
        'lotes2020': user+'programacion/geoinfo/Respuesta DCSI 3/Lotes_PNIS_ErradicacionTotal_11112020.shp',
        'monitorio_pagos': user+'programacion/geoinfo/Respuesta DCSI 3/monitoreo_pagos.xlsx',
        'lotes_pagos_PNIS' : user+'programacion/geoinfo/Respuesta DCSI 2/Monitoreo_UNODC/Lotes_PNIS_pagos.shp',
        'veredas_pnis':user+'programacion/geoinfo/Respuesta DCSI 2/Monitoreo_UNODC/Vdas_PNIS.shp',
        #'pics':user+'programacion/geoinfo/PICs/Shapes PICS/Entregar_pres.shp', esta capa esta desactualizada
        'coca':user+'programacion/geoinfo/Colombia/Narcotrafico/densidad_coca/',   #Ruta al folder que tiene todos los shapes 
        # Acuerdos colectivos
        'acuerdos_art': user+'programacion/geoinfo/Respuesta DCSI 3/Vdas_AcuerdosColectivos_ART_10092019.shp',
        'acuerdos_dane': user+'programacion/geoinfo/Respuesta DCSI 3/Vdas_AcuerdosColectivos_DANE_10092019.shp',
        'acuerdos_otras': user+'programacion/geoinfo/Respuesta DCSI 3/Vdas_AcuerdosColectivos_OtrasDA_10092019.shp',
        'acuerdos_pnis': user+'programacion/geoinfo/Respuesta DCSI 3/Vdas_AcuerdosColectivos_PNIS_10092019.shp',

        #Conflicto
        #'armada':user+'programacion/geoinfo/Colombia/Conflicto/unidades_armada.shp',
        #'abolladuras':user+'programacion/geoinfo/Colombia/Conflicto/abolladura_1.shp',
        #'labs':user+'programacion/geoinfo/Colombia/Narcotrafico/Lab_1.shp',
        'emf': user+'programacion/geoinfo/Colombia/Narcotrafico/emf/EMF_2016_2020_Completo/EMF_2016_2020_Completo.shp',
        'zonas_futuro':user+'programacion/geoinfo/Colombia/Territoriales/zonas_futuro/zonas_futuro.shp',
        'map':user+'programacion/geoinfo/Colombia/Conflicto/map/map_2016_2020.shp',
        'map_base':user+'programacion/geoinfo/Colombia/Conflicto/map/map_octubre_31_2020.xlsx',
        'evoa':user+'programacion/geoinfo/Colombia/mineria_evoa/EVOA2019.shp',
        'evoa_veredas':user+'programacion/geoinfo/Colombia/mineria_evoa/evoa_veredas.xlsx',
        'grupos_armados':user+'geoinfo/Colombia/Conflicto/grupos_armados/grupos.shp',

        #Politico administrartivas
        #'caserios':user+'programacion/geoinfo/Colombia/Territoriales/Caseríos/Administrativo_P_Escala_1100.000_Cartografia_Base__IGAC.shp',
        #'aurbana':user+'programacion/geoinfo/Colombia/Territoriales/Área Urbana/Administrativo_R.shp',
        'colombia':user+'programacion/geoinfo/Colombia/ADMINISTRATIVO/colombia.shp',
        'veredas':user+'programacion/geoinfo/Colombia/Territoriales/CRVeredas_2017.shp',
        'municipios':user+'programacion/geoinfo/Colombia/ADMINISTRATIVO/VRDS_MPIO_POLITICO.shp',
        'mpios':user+'programacion/geoinfo/Colombia/ADMINISTRATIVO/MGN_MPIO_POLITICO.shp',
        'municipios_indices':user+'programacion/geoinfo/Colombia/ADMINISTRATIVO/VRDS_MPIO_INDEX.csv', #DF with indices and municipality codes to allow for a trageted import of the municipios shape file (based on row number)
        'deptos':user+'programacion/geoinfo/Colombia/ADMINISTRATIVO/MGN_DPTO_POLITICO.shp',
        'divipola':user+'programacion/geoinfo/Colombia/DIVIPOLA_MUN.xlsx',
        'pnn' : user+'programacion/geoinfo/Colombia/Territoriales/Parques_Nacionales_Naturales.shp',
        'resguardos':user+'programacion/geoinfo/Colombia/Territoriales/Resguardos_Indigenas.shp',
        'consejos':user+'programacion/geoinfo/Colombia/Territoriales/Consejos_comunitarios.shp',
        'runap':user+'programacion/geoinfo/Colombia/bosques/runap2/runap2Polygon.shp', #Registro único nacional de áreas protegidas.
        'humedales': user+'programacion/geoinfo/Colombia/bosques/Humedales_RAMSAR_Agosto_2018/Humedales_RAMSAR_Agosto_2018.shp', #Humedales
        'paramos':user+'programacion/geoinfo/Colombia/bosques/Paramos_Delimitados_Junio_2020/Paramos_Delimitados_Junio_2020.shp', #Páramos declarados
                       'sustracciones_reservas':user+'programacion/geoinfo/Colombia/Territoriales/Sustracciones_Definitivas_Ley2_marzo_2021/Sustracciones_Definitivas_Ley2_marzo_2021.shp',
        'zonificacion_reservas':user+'programacion/geoinfo/Colombia/Territoriales/Zonificacion_Ley2_marzo_2021/Zonificacion_Ley2_marzo_2021.shp',
        'reservas':user+'programacion/geoinfo/Colombia/Territoriales/Reserva_Ley2_marzo_2021/Reserva_Ley2_marzo_2021.shp',
        'jes': user+'programacion/geoinfo/Colombia/Territoriales/jurisdicciones_especiales.shp',
        'aurbana':user+'programacion/geoinfo/Colombia/ADMINISTRATIVO/MGN2020_URB_AREA_CENSAL/MGN_URB_AREA_CENSAL.shp',
        'panel_municipal_pgn':user+'programacion/bases/municipales/panel_municipales_pgn.xlsx',

        #Geograficas
        'rios':user+'programacion/geoinfo/Colombia/Geografia/rios/Rios_principales.shp',

        #Infraestructura
        #'redat':user+'programacion/geoinfo/Colombia/Infraestructura/Red_Alta_Tension/Red_Alta_Tension.shp',
        'vias':user+'programacion/geoinfo/Colombia/Infraestructura/Via/Via.shp',
        'aerodromos_aerocivil': user+'programacion/geoinfo/bases_tania/listado_aero_aerocivil.xlsx',
        'aerodromos_total': user+'programacion/geoinfo/bases_tania/listado_aero_pub_priv.xlsx',
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
        
        # Ovejas
        'fiso_ovejas': user+'LFP_compartido/sistemas_informacion/Insumos TetraTech/Piloto Modulo de Beneficiarios/Bases_Estandarizadas/Fisos Ovejas.xlsx',
        'app_cacao': user+'LFP_compartido/sistemas_informacion/Insumos TetraTech/Piloto Modulo de Beneficiarios/Bases_Estandarizadas/Caracterización APP Cacao.xlsx',
        'formalizados_lfp': user+'LFP_compartido/sistemas_informacion/Insumos TetraTech/Piloto Modulo de Beneficiarios/Bases_Estandarizadas/FormalizadosLFP.xlsx',
        'formalizados_lrdp': user+'LFP_compartido/sistemas_informacion/Insumos TetraTech/Piloto Modulo de Beneficiarios/Bases_Estandarizadas/FormalizadosLRDP.xlsx',       
        
        #Info municipal
        'info_municipal':user+'programacion/bases/municipales/27-01-2021 Caracterización municipios.xlsx', 
        
        #Cooperacion internacional
        
        'cooperacion_municipal': user+'LFP_compartido/cooperacion/cooperacion_municipal.xlsx',
        
        # DICAR
            # Archivos de stata, usar: pd.read_stata
        'delitos': user+'programacion/geoinfo/Colombia/delitos/Base/Delitos.dta',
        'estupefacientes': user+'programacion/geoinfo/Colombia/delitos/Base/2016-2019 Estupefacientes.dta',
        'armas': user+'programacion/geoinfo/Colombia/delitos/Base/2016-2019 Armas.dta',
        'capturas': user+'programacion/geoinfo/Colombia/delitos/Base/2016-2019 Capturas.dta',
        
        # Carpeta geoinfo
        
        'geoinfo':user+'programacion/geoinfo/',
        
        # Socioeconómicas
        'poblacion':user+'programacion/geoinfo/Colombia/socioeconomicas/proyeccion_poblacion.xlsx',
        
        # Deforestación
        
        'deforestacion_municipios': user+'programacion/geoinfo/deforestacion/forest_loss_mpios.xlsx',
        'deforestacion_veredas': user+'programacion/geoinfo/deforestacion/forest_loss_veredas.xlsx',
        
        }
    
    #Filepaths for the coca shapes
    
    def ano(year):
        """Returns a 2 digit year"""
        if i in (range(1,10)):
            return '0'+str(i)
        if i > 9:
            return str(i)
    
    for i in range(1,21):
        key = 'coca'+ano(i)
        paths[key] = user+'programacion/geoinfo/Colombia/Narcotrafico/densidad_coca/Densidad_Cultivos_Ilícitos_20{}.shp'.format(ano(i))
    
            
    #Paths OS agnostic paths
    for i in paths:
        paths[i] = os.path.abspath(paths[i])

    return paths

def indice_municipio(cod_mpio, path_OneDrive):
    """Retorna la fila que corresponde al municipio en el archivo 'municipos' del diccionario paths.
        Parametros:
            cod_mpio (str): Código del municipio en formato string"""
    paths = diccionario_rutas(path_OneDrive=path_OneDrive)
    inds = pd.read_csv(paths['municipios_indices'], 
                      dtype={'DPTOMPIO':str},
                      index_col=0)
    ind = inds[inds['DPTOMPIO']==cod_mpio]

    return ind.index.to_list()[0]+1

