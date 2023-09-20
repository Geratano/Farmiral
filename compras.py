import pandas as pd 
import streamlit as st 
from PIL import Image
import altair as alt
import numpy as np
from datetime import datetime,timedelta
import re
import math

st.set_page_config(layout="wide")

def main():

    img = Image.open('logo_farmiral.jpg')
    col1, col2, col3 = st.columns([5,10,1])

    with col1:
        st.write("")
    with col2:
        st.image(img,width=250)
    with col3:
        st.write("")

    #cargo la base compras 
    @st.cache_resource
    def load_compras():
        compras = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/compras.csv',encoding='latin-1')
        return compras
    compras = load_compras()
    @st.cache_resource
    def Forecast():
        base8 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/Plan2023.csv',encoding='latin-1')
        return base8
    forecast = Forecast()
    @st.cache_resource
    def Formulas():
        base9 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/formulas.csv',encoding='latin-1')
        return base9
    df_formulas = Formulas()
    @st.cache_resource
    def Productos():
        base10 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/productos.csv',encoding='latin-1')
        return base10
    productos = Productos()
    @st.cache_resource
    def Existencias():
        base6 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/existencias.csv',encoding='latin-1')
        return base6
    existencias = Existencias()
    @st.cache_resource
    def Forecast_victor():
        base11 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/fcst_victor.csv',encoding='latin-1')
        return base11
    fcst_victor = Forecast_victor() 
    @st.cache_resource
    def moq():
        base12 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/moq.csv',encoding='latin-1')
        return base12
    moq = moq()
    def a1():
        base13 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/ingresosa1.csv',encoding='latin-1')
        return base13
    a1 = a1()

    #quito los espacios 
    compras.columns = compras.columns.str.strip()
    existencias.columns = existencias.columns.str.strip()
    df_formulas.columns = df_formulas.columns.str.strip()
    productos.columns = productos.columns.str.strip()
    fcst_victor.columns = fcst_victor.columns.str.strip()
    fcst_victor['Codigo'] = fcst_victor['Codigo'].str.strip()
    fcst_victor['Producto'] = fcst_victor['Producto'].str.strip()
    productos['Cve_prod'] = productos['Cve_prod'].str.strip()
    productos['Desc_prod'] = productos['Desc_prod'].str.strip()
    df_productos = productos[['Cve_prod', 'Desc_prod']]
    df_productos.columns = ['SKU', 'Producto']
    forecast.columns = forecast.columns.str.strip()
    forecast.columns = ['Cve_prod', 'Producto', 'Tamano lotes', 'Presentacion', 'Cliente', 'Stock', 'Plan Julio', 'Forecast', 'Lotes origin', 'Lotes', 'Nota','NO']
    forecast = forecast[['Cve_prod', 'Producto', 'Plan Julio', 'Forecast', 'Lotes origin']]
    compras['Cve_prod'] = compras['Cve_prod'].str.strip()
    compras['Desc_prod'] = compras['Desc_prod'].str.strip()
    compras['Nom_prov'] = compras['Nom_prov'].str.strip()
    compras['F_ent'] = compras['F_ent'].str.strip()
    existencias['Lugar'] = existencias['Lugar'].str.strip()
    moq.columns = moq.columns.str.strip()
    moq['SKU'] = moq['SKU'].str.strip()
    moq['MP'] = moq['MP'].str.strip()
    a1.columns = a1.columns.str.strip()
    a1['Cve_prod'] = a1['Cve_prod'].str.strip()
    a1['Desc_prod'] = a1['Desc_prod'].str.strip()

    #########EXTRACCION INGRESOS A1#########################
    a1 = a1[['Cve_prod', 'Desc_prod', 'Cant_prod']]
    a1.columns = ['SKU', 'MP', 'Ingreso']
    a1 = a1.groupby(['SKU']).agg({'Ingreso':'sum'}).reset_index()
    ###################################EXTRACTO APP DE VENTAS##################################################################
    ###TRATAMIENTO BASE EXISTENCIAS###
    ##########
    fcst_victor.columns = ['Codigo', 'Producto', 'Unidad', 'Lote', 'sep23', 'oct23', 'nov23', 'dic23', 'ene24', 'feb24', 'Almacen']
    fcst_victor = fcst_victor.fillna(0)
    fcst_victor2 = fcst_victor.copy()
    fcst_victor2['Forecast anual'] = (fcst_victor2['sep23'] + fcst_victor2['oct23'] + fcst_victor2['nov23'] + fcst_victor2['dic23'] + fcst_victor2['ene24'] + fcst_victor2['feb24'])
    
    #fcst_victor2 = fcst_victor2.groupby(['Codigo','Producto']).agg({'Forecast anual':'sum'}).reset_index()
    #st.write(fcst_victor2)
    ##########
    df_existencias = existencias[['Cve_prod', 'Lote', 'Lugar', 'Cto_ent', 'Existencia', 'Fech_venc', 'Desc_prod', 'Uni_med']]
    df_existencias.columns = ['SKU', 'Lote', 'Lugar', 'Costo', 'Existencia', 'Vencimiento', 'Producto', 'Unidad']
    #df_existencias['Lugar'] = df_existencias['Lugar'].str.strip()
    ###############ALMACENES DIFERENCIADOS##########################################################################################
    df_existencias = df_existencias[(df_existencias['Lugar']=='5') | (df_existencias['Lugar']=='4')] 
    df_existencias2 = df_existencias[(df_existencias['Lugar']=='A1') | (df_existencias['Lugar']=='A2') | (df_existencias['Lugar']=='A3')]
    df_existenciasaspen = df_existencias[(df_existencias['Lugar']=='ASPEN')]
    df_existenciasgrisi = df_existencias[(df_existencias['Lugar']=='G1')|(df_existencias['Lugar']=='G2')]
    df_existenciassimi = df_existencias[(df_existencias['Lugar']=='SIMILARES')]
    #############################################################################################################################33
    df_existencias_4 = df_existencias[(df_existencias['Lugar']=='4')]
    df_existencias_5 = df_existencias[(df_existencias['Lugar']=='5')]
    df_existencias_a1 = df_existencias2[(df_existencias2['Lugar']=='A1')]
    df_existencias_a2 = df_existencias2[(df_existencias2['Lugar']=='A2')]
    df_existencias_a3 = df_existencias2[(df_existencias2['Lugar']=='A3')]
    df_existencias_4 = df_existencias_4.groupby(['Producto']).agg({'Costo':'mean', 'Existencia':'sum'}).reset_index()
    df_existencias_4.columns = ['Producto', 'Costo', 'Existencia proceso']
    df_existencias_5 = df_existencias_5.groupby(['Producto']).agg({'Costo':'mean', 'Existencia':'sum'}).reset_index()
    df_existencias_5.columns = ['Producto', 'Costo', 'Existencia pt']
    df_existencias_a1 = df_existencias_a1.groupby(['Producto']).agg({'Costo':'mean', 'Existencia':'sum'}).reset_index()
    df_existencias_a1.columns = ['Producto', 'Costo', 'Existencia mp a1']
    df_existencias_a2 = df_existencias_a2.groupby(['Producto']).agg({'Costo':'mean', 'Existencia':'sum'}).reset_index()
    df_existencias_a2.columns = ['Producto', 'Costo', 'Existencia mp a2']
    df_existencias_a3 = df_existencias_a3.groupby(['Producto']).agg({'Costo':'mean', 'Existencia':'sum'}).reset_index()
    df_existencias_a3.columns = ['Producto', 'Costo', 'Existencia mp a3']
    df_existenciasaspen = df_existenciasaspen.groupby(['Producto']).agg({'Costo':'mean', 'Existencia':'sum'}).reset_index()
    df_existenciasaspen.columns = ['Producto', 'Costo', 'Existencia mp aspen']
    df_existenciasgrisi = df_existenciasgrisi.groupby(['Producto']).agg({'Costo':'mean', 'Existencia':'sum'}).reset_index()
    df_existenciasgrisi.columns = ['Producto', 'Costo', 'Existencia mp grisi']
    df_existenciassimi = df_existenciassimi.groupby(['Producto']).agg({'Costo':'mean', 'Existencia':'sum'}).reset_index()
    df_existenciassimi.columns = ['Producto', 'Costo', 'Existencia mp simi']
    ###TRATAMIENTO BASE FORMULAS####Quitamos los posibles espacios sobrantes de cada columna
    formulas = df_formulas[['Cve_copr', 'Cve_prod', 'Can_copr', 'New_med', 'New_copr', 'Undfor', 'Desc_prod', 'Ren_copr', 'Uncfor']]
    formulas.columns = ['SKU', 'Cve_prod', 'Cantidad rendimiento', 'New_med', 'New_copr', 'Unidad mp', 'MP', 'Rendimiento', 'Unidad']
    formulas['Cantidad'] = formulas['Cantidad rendimiento']/formulas['Rendimiento']

    formulas['SKU'] = formulas['SKU'].str.strip()
    formulas['New_copr'] = formulas['New_copr'].str.strip()
    formulas = formulas.loc[(formulas['New_copr'] != 'V1') & (formulas['New_copr'] != 'V2') & (formulas['New_copr'] != 'V3') & (formulas['New_copr'] != 'V4')]
    formulas = formulas.merge(df_productos, on='SKU', how='left')
    #st.write(formulas)
    existe = df_existencias.groupby(['Producto','SKU']).agg({'Existencia':'sum'
                                                       }).reset_index()
    existemp = df_existencias2.groupby(['Producto', 'SKU']).agg({'Existencia':'sum'}).reset_index()
    #forecast = forecast.fillna(0)
    #forecast = forecast[forecast['Cve_prod'] != 0]
    existe['SKU'] = existe['SKU'].str.strip()
    #forecast['SKU'] = forecast['Cve_prod'].str.strip()
    #forecast = forecast[['SKU', 'Producto', 'Forecast']]
    fcst_victor2['SKU'] = fcst_victor2['Codigo'].str.strip()
    fcst_victor2 = fcst_victor2[['SKU', 'Producto', 'sep23', 'oct23', 'nov23', 'dic23', 'ene24', 'feb24', 'Forecast anual', 'Almacen']]
    fcst_comp = fcst_victor2.copy()
    #st.write(fcst_comp)
    ################################FORECAST GENERAL########################################################################
    forecast = fcst_comp[['SKU', 'Producto', 'sep23', 'oct23', 'nov23', 'dic23', 'ene24', 'feb24', 'Forecast anual', 'Almacen']]
    forecast.columns = ['SKU', 'Producto', 'Sep23', 'Oct23', 'Nov23', 'Dic23', 'Ene23', 'Feb24', 'Forecast anual', 'Almacen']
    #st.write(forecast)
    ####################################################################################################################

    ###Pegamos la existencia del producto terminado para obtener los faltantes generales de PT
    t_existe = existe.fillna(0)
    t_existemp = existemp.fillna(0)

    t_existe = t_existe[['SKU', 'Producto', 'Existencia']]
    t_existemp = t_existemp[['SKU', 'Producto', 'Existencia']]

    t_forecast = forecast.merge(t_existe, on='SKU', how='outer').fillna(0)
    
    t_forecast['Producto'] = t_forecast['Producto_x']


    for i in range(len(t_forecast['Producto'])):
        if t_forecast.loc[i,'Producto_x']==0:
            t_forecast.loc[i,'Producto'] = t_forecast.loc[i,'Producto_y']
            #t_forecast.loc[i,'Forecast'] = str(t_forecast.loc[i,'Forecast']).strip().replace('-','0')

    t_forecast = t_forecast[['SKU', 'Producto','Sep23', 'Oct23', 'Nov23', 'Dic23', 'Ene23', 'Feb24', 'Forecast anual', 'Existencia', 'Almacen']]
    t_forecast['Faltantes'] = t_forecast['Sep23'] - t_forecast['Existencia']
    t_forecast = t_forecast[t_forecast['Faltantes'] != 0]
    #st.write(t_forecast)
    #Forecast faltantes Completo
    fcst_faltantes = t_forecast[['SKU', 'Producto','Sep23', 'Oct23', 'Nov23', 'Dic23', 'Ene23', 'Feb24', 'Forecast anual', 'Faltantes', 'Existencia', 'Almacen']]
    fcst_faltantes = fcst_faltantes[fcst_faltantes['Faltantes']>0]
    #st.write(fcst_faltantes)
    ############################
    #Forecast faltantes A1-A3
    fcst_faltantesa = fcst_faltantes[fcst_faltantes['Almacen']==1]
    #Forecast faltantes Aspen
    fcst_faltantesaspen = fcst_faltantes[fcst_faltantes['Almacen']==3]
    #Forecast faltantes Simi
    fcst_faltantessimi = fcst_faltantes[fcst_faltantes['Almacen']==2]
    #orecast faltantes Grisi
    fcst_faltantesgrisi = fcst_faltantes[fcst_faltantes['Almacen']==4]
    #st.write(fcst_faltantes)
    #st.write(fcst_faltantesgrisi)
    ###############fcst faltantes es el forecast con sus faltantes a nivel pt

    ### EXISTENCIAS MATERIAS PRIMAS ###
    existeN = existencias[['Cve_prod', 'Lugar', 'Desc_prod','Existencia']]
    existeN['Lugar'] = existeN['Lugar'].str.strip()
    existeN.columns=existeN.columns.str.strip()
    existeN['Cve_prod'] = existeN['Cve_prod'].str.strip()
    existeN['Lugar'] = existeN['Lugar'].str.strip()
    existeN['Desc_prod'] = existeN['Desc_prod'].str.strip()
    existeN_comp =existeN[(existeN['Lugar'] == 'A1') | 
                          (existeN['Lugar'] == 'A2') | 
                          (existeN['Lugar'] == 'A3') |
                          (existeN['Lugar'] == 'ASPEN') |
                          (existeN['Lugar'] == 'SIMILARES') |
                          (existeN['Lugar'] == 'G2') |
                          (existeN['Lugar'] == 'G1')]

    ####CONTRUCCION PARTICULAR######################
    existeN_a = existeN[(existeN['Lugar'] == 'A1') |
                        (existeN['Lugar'] == 'A2') |
                        (existeN['Lugar'] == 'A3')] 
    existeN_aspen = existeN[(existeN['Lugar'] == 'ASPEN')]                        
    existeN_simi = existeN[(existeN['Lugar'] == 'SIMILARES')]  
    existeN_grisi = existeN[(existeN['Lugar'] == 'G2') |
                          (existeN['Lugar'] == 'G1')]
    ###############################################
    nomprod = productos.copy()
    nomprod = nomprod[['Cve_prod', 'Desc_prod']]
    nomprod.columns = ['SKU', 'MP']
    ###############################################
    #General
    existeN_comp.columns = ['SKU', 'Lugar', 'MP', 'Existencia']
    existeN_comp['SKU'] = existeN_comp['SKU'].str.strip()
    existeN_comp = existeN_comp.groupby(['SKU']).agg({'Existencia':'sum'}).reset_index()
    #A1-A3
    existeN_a.columns = ['SKU', 'Lugar', 'MP', 'Existencia']
    existeN_a['SKU'] = existeN_a['SKU'].str.strip()
    existeN_a = existeN_a.groupby(['SKU']).agg({'Existencia':'sum'}).reset_index()
    #Aspen
    existeN_aspen.columns = ['SKU', 'Lugar', 'MP', 'Existencia']
    existeN_aspen['SKU'] = existeN_aspen['SKU'].str.strip()
    existeN_aspen = existeN_aspen.groupby(['SKU']).agg({'Existencia':'sum'}).reset_index()
    easpen = existeN_aspen.copy()
    easpen = easpen.merge(nomprod, on='SKU', how='left')
    easpen = easpen[['SKU', 'MP', 'Existencia']]
    #Simi
    existeN_simi.columns = ['SKU', 'Lugar', 'MP', 'Existencia']
    existeN_simi['SKU'] = existeN_simi['SKU'].str.strip()
    existeN_simi = existeN_simi.groupby(['SKU']).agg({'Existencia':'sum'}).reset_index()
    esimi = existeN_simi.copy()
    esimi = esimi.merge(nomprod, on='SKU', how='left')
    esimi = esimi[['SKU', 'MP', 'Existencia']]
    #grisi
    existeN_grisi.columns = ['SKU', 'Lugar', 'MP', 'Existencia']
    existeN_grisi['SKU'] = existeN_grisi['SKU'].str.strip()
    existeN_grisi = existeN_grisi.groupby(['SKU']).agg({'Existencia':'sum'}).reset_index()
    egrisi = existeN_grisi.copy()
    egrisi = egrisi.merge(nomprod, on='SKU', how='left')
    egrisi = egrisi[['SKU', 'MP', 'Existencia']]
    #st.write(existeN_comp)
    ###############
    #st.write(formulas)
    ####################PEDIR GENERAL#####################################################

    pedir_fcst = fcst_faltantes.merge(formulas, on='SKU', how='left')
    #st.write(pedir_fcst)
    pedir_fcst = pedir_fcst.dropna()
    #st.write(pedir_fcst)
    pedir_fcstme = pedir_fcst[pedir_fcst['Cve_prod'].str.startswith('M')].reset_index(drop=True)
    
    pedir_fcstme['Faltantes me'] = pedir_fcstme['Faltantes'] * pedir_fcstme['Cantidad']    
    pedir_fcstme['Faltantes me Oct23'] = pedir_fcstme['Oct23'] * pedir_fcstme['Cantidad']
    pedir_fcstme['Faltantes me Nov23'] = pedir_fcstme['Nov23'] * pedir_fcstme['Cantidad']
    pedir_fcstme['Faltantes me Dic23'] = pedir_fcstme['Dic23'] * pedir_fcstme['Cantidad']
    pedir_fcstme['Faltantes me Ene24'] = pedir_fcstme['Ene23'] * pedir_fcstme['Cantidad']
    pedir_fcstme['Faltantes me Feb24'] = pedir_fcstme['Feb24'] * pedir_fcstme['Cantidad']
    #st.write(pedir_fcstme)
    pedir_fcstst = pedir_fcst[pedir_fcst['Cve_prod'].str.startswith('41')].reset_index(drop=True)
    pedir_fcstst.rename(columns = {'SKU':'SKU_f', 'Cve_prod':'SKU'}, inplace=True)
    pedir_fcstst['SKU'] = pedir_fcstst['SKU'].str.strip()
    pedir_fcstst = pedir_fcstst.merge(formulas, on='SKU', how='left')
    #st.write(pedir_fcstst)
    #Cantidad por pieza
    pedir_fcstst['Cantidad_y'] = pedir_fcstst['Cantidad rendimiento_y'] / pedir_fcstst['Rendimiento_x']
    pedir_fcstst['Cantidad mp'] = pedir_fcstst['Cantidad_y'] * pedir_fcstst['Faltantes']
    #st.write(pedir_fcstst)
    pedir_fcstst['Cantidad mp Oct23'] = pedir_fcstst['Cantidad_y'] * pedir_fcstst['Oct23']
    pedir_fcstst['Cantidad mp Nov23'] = pedir_fcstst['Cantidad_y'] * pedir_fcstst['Nov23']
    pedir_fcstst['Cantidad mp Dic23'] = pedir_fcstst['Cantidad_y'] * pedir_fcstst['Dic23']
    pedir_fcstst['Cantidad mp Ene24'] = pedir_fcstst['Cantidad_y'] * pedir_fcstst['Ene23']
    pedir_fcstst['Cantidad mp Feb24'] = pedir_fcstst['Cantidad_y'] * pedir_fcstst['Feb24']
    #st.write(pedir_fcstst)
    pedir_fcstst = pedir_fcstst[['Producto_x', 'Faltantes', 'MP_y', 'Cantidad mp', 'Sep23', 'Cantidad mp Oct23', 'Cantidad mp Nov23', 'Cantidad mp Dic23', 'Cantidad mp Ene24', 'Cantidad mp Feb24', 'Forecast anual']]
    pedir_fcstst.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'Sep23', 'Cantidad Oct23', 'Cantidad Nov23', 'Cantidad Dic23', 'Cantidad Ene24', 'Cantidad Feb24', 'Forecast anual']
    #st.write(pedir_fcstst)
    pedir_fcstme = pedir_fcstme[['Producto_x', 'Faltantes', 'MP', 'Faltantes me', 'Sep23', 'Faltantes me Oct23', 'Faltantes me Nov23', 'Faltantes me Dic23', 'Faltantes me Ene24', 'Faltantes me Feb24', 'Forecast anual']]
    pedir_fcstme.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'Sep23', 'Cantidad Oct23', 'Cantidad Nov23', 'Cantidad Dic23', 'Cantidad Ene24', 'Cantidad Feb24', 'Forecast anual']
    #st.write(pedir_fcstme)
    pedir2 = pd.concat([pedir_fcstst, pedir_fcstme])
    #st.write(pedir2)
    pedir2['MP'] = pedir2['MP'].str.strip()
    prods = productos[['Cve_prod', 'Desc_prod']]
    prods.columns = ['SKU', 'MP']
    pedir2 = pedir2.merge(prods, on='MP', how='left')
    #Columnas a pegar en la explosión
    pedir2t = pedir2.groupby(['SKU']).agg({'Cantidad Oct23':'sum',
                                  'Cantidad Nov23':'sum',
                                  'Cantidad Dic23':'sum',
                                  'Cantidad Ene24':'sum',
                                  'Cantidad Feb24':'sum'}).reset_index()
    #st.write(pedir2t)
    ######################################################################################################
    ####################PEDIR A1-A3#####################################################
    pedir_fcsta = fcst_faltantesa.merge(formulas, on='SKU', how='left')
    #st.write(pedir_fcst)
    pedir_fcsta = pedir_fcsta.dropna()
    #st.write(pedir_fcst)
    pedir_fcstmea = pedir_fcsta[pedir_fcsta['Cve_prod'].str.startswith('M')].reset_index(drop=True)
    pedir_fcstmea['Faltantes me'] = pedir_fcstmea['Faltantes'] * pedir_fcstmea['Cantidad']
    pedir_fcstmea['Faltantes me Oct23'] = pedir_fcstmea['Oct23'] * pedir_fcstmea['Cantidad']
    pedir_fcstmea['Faltantes me Nov23'] = pedir_fcstmea['Nov23'] * pedir_fcstmea['Cantidad']
    pedir_fcstmea['Faltantes me Dic23'] = pedir_fcstmea['Dic23'] * pedir_fcstmea['Cantidad']
    pedir_fcstmea['Faltantes me Ene24'] = pedir_fcstmea['Ene23'] * pedir_fcstmea['Cantidad']
    pedir_fcstmea['Faltantes me Feb24'] = pedir_fcstmea['Feb24'] * pedir_fcstmea['Cantidad']
    #st.write(pedir_fcstmea)
    pedir_fcststa = pedir_fcsta[pedir_fcsta['Cve_prod'].str.startswith('41')].reset_index(drop=True)
    pedir_fcststa.rename(columns = {'SKU':'SKU_f', 'Cve_prod':'SKU'}, inplace=True)
    pedir_fcststa['SKU'] = pedir_fcststa['SKU'].str.strip()
    pedir_fcststa = pedir_fcststa.merge(formulas, on='SKU', how='left')
    pedir_fcststa['Cantidad_y'] = pedir_fcststa['Cantidad rendimiento_y'] / pedir_fcststa['Rendimiento_x']
    pedir_fcststa['Cantidad mp'] = pedir_fcststa['Cantidad_y'] * pedir_fcststa['Faltantes']
    pedir_fcststa['Cantidad mp Oct23'] = pedir_fcststa['Cantidad_y'] * pedir_fcststa['Oct23']
    pedir_fcststa['Cantidad mp Nov23'] = pedir_fcststa['Cantidad_y'] * pedir_fcststa['Nov23']
    pedir_fcststa['Cantidad mp Dic23'] = pedir_fcststa['Cantidad_y'] * pedir_fcststa['Dic23']
    pedir_fcststa['Cantidad mp Ene24'] = pedir_fcststa['Cantidad_y'] * pedir_fcststa['Ene23']
    pedir_fcststa['Cantidad mp Feb24'] = pedir_fcststa['Cantidad_y'] * pedir_fcststa['Feb24']
    pedir_fcststa = pedir_fcststa[['Producto_x', 'Faltantes', 'MP_y', 'Cantidad mp', 'Sep23', 'Cantidad mp Oct23', 'Cantidad mp Nov23', 'Cantidad mp Dic23', 'Cantidad mp Ene24', 'Cantidad mp Feb24', 'Forecast anual']]
    pedir_fcststa.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'Sep23', 'Cantidad Oct23', 'Cantidad Nov23', 'Cantidad Dic23', 'Cantidad Ene24', 'Cantidad Feb24', 'Forecast anual']
    #st.write(pedir_fcstst)
    pedir_fcstmea = pedir_fcstmea[['Producto_x', 'Faltantes', 'MP', 'Faltantes me', 'Sep23', 'Faltantes me Oct23', 'Faltantes me Nov23', 'Faltantes me Dic23', 'Faltantes me Ene24', 'Faltantes me Feb24', 'Forecast anual']]
    pedir_fcstmea.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'Sep23', 'Cantidad Oct23', 'Cantidad Nov23', 'Cantidad Dic23', 'Cantidad Ene24', 'Cantidad Feb24', 'Forecast anual']
    #st.write(pedir_fcstme)
    pedir2a = pd.concat([pedir_fcststa, pedir_fcstmea])
    #st.write(pedir2a)
    pedir2a['MP'] = pedir2a['MP'].str.strip()
    prods = productos[['Cve_prod', 'Desc_prod']]
    prods.columns = ['SKU', 'MP']
    pedir2a = pedir2a.merge(prods, on='MP', how='left')
    #Columnas a pegar en la explosión
    pedir2ta = pedir2a.groupby(['SKU']).agg({'Cantidad Oct23':'sum',
                                  'Cantidad Nov23':'sum',
                                  'Cantidad Dic23':'sum',
                                  'Cantidad Ene24':'sum',
                                  'Cantidad Feb24':'sum'}).reset_index()
    #st.write(pedir2a)
    ######################################################################################################
    ####################PEDIR ASPEN#####################################################
    pedir_fcstaspen = fcst_faltantesaspen.merge(formulas, on='SKU', how='left')
    #st.write(pedir_fcst)
    pedir_fcstaspen = pedir_fcstaspen.dropna()
    #st.write(pedir_fcst)
    pedir_fcstmeaspen = pedir_fcstaspen[pedir_fcstaspen['Cve_prod'].str.startswith('M')].reset_index(drop=True)
    pedir_fcstmeaspen['Faltantes me'] = pedir_fcstmeaspen['Faltantes'] * pedir_fcstmeaspen['Cantidad']
    pedir_fcstmeaspen['Faltantes me Oct23'] = pedir_fcstmeaspen['Oct23'] * pedir_fcstmeaspen['Cantidad']
    pedir_fcstmeaspen['Faltantes me Nov23'] = pedir_fcstmeaspen['Nov23'] * pedir_fcstmeaspen['Cantidad']
    pedir_fcstmeaspen['Faltantes me Dic23'] = pedir_fcstmeaspen['Dic23'] * pedir_fcstmeaspen['Cantidad']
    pedir_fcstmeaspen['Faltantes me Ene24'] = pedir_fcstmeaspen['Ene23'] * pedir_fcstmeaspen['Cantidad']
    pedir_fcstmeaspen['Faltantes me Feb24'] = pedir_fcstmeaspen['Feb24'] * pedir_fcstmeaspen['Cantidad']
    #st.write(pedir_fcstmea)
    pedir_fcststaspen = pedir_fcstaspen[pedir_fcstaspen['Cve_prod'].str.startswith('41')].reset_index(drop=True)
    pedir_fcststaspen.rename(columns = {'SKU':'SKU_f', 'Cve_prod':'SKU'}, inplace=True)
    pedir_fcststaspen['SKU'] = pedir_fcststaspen['SKU'].str.strip()
    pedir_fcststaspen = pedir_fcststaspen.merge(formulas, on='SKU', how='left')
    pedir_fcststaspen['Cantidad_y'] = pedir_fcststaspen['Cantidad rendimiento_y'] / pedir_fcststaspen['Rendimiento_x']
    pedir_fcststaspen['Cantidad mp'] = pedir_fcststaspen['Cantidad_y'] * pedir_fcststaspen['Faltantes']
    pedir_fcststaspen['Cantidad mp Oct23'] = pedir_fcststaspen['Cantidad_y'] * pedir_fcststaspen['Oct23']
    pedir_fcststaspen['Cantidad mp Nov23'] = pedir_fcststaspen['Cantidad_y'] * pedir_fcststaspen['Nov23']
    pedir_fcststaspen['Cantidad mp Dic23'] = pedir_fcststaspen['Cantidad_y'] * pedir_fcststaspen['Dic23']
    pedir_fcststaspen['Cantidad mp Ene24'] = pedir_fcststaspen['Cantidad_y'] * pedir_fcststaspen['Ene23']
    pedir_fcststaspen['Cantidad mp Feb24'] = pedir_fcststaspen['Cantidad_y'] * pedir_fcststaspen['Feb24']
    pedir_fcststaspen = pedir_fcststaspen[['Producto_x', 'Faltantes', 'MP_y', 'Cantidad mp', 'Sep23', 'Cantidad mp Oct23', 'Cantidad mp Nov23', 'Cantidad mp Dic23', 'Cantidad mp Ene24', 'Cantidad mp Feb24', 'Forecast anual']]
    pedir_fcststaspen.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'Sep23', 'Cantidad Oct23', 'Cantidad Nov23', 'Cantidad Dic23', 'Cantidad Ene24', 'Cantidad Feb24', 'Forecast anual']
    #st.write(pedir_fcstst)
    pedir_fcstmeaspen = pedir_fcstmeaspen[['Producto_x', 'Faltantes', 'MP', 'Faltantes me', 'Sep23', 'Faltantes me Oct23', 'Faltantes me Nov23', 'Faltantes me Dic23', 'Faltantes me Ene24', 'Faltantes me Feb24', 'Forecast anual']]
    pedir_fcstmeaspen.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'Sep23', 'Cantidad Oct23', 'Cantidad Nov23', 'Cantidad Dic23', 'Cantidad Ene24', 'Cantidad Feb24', 'Forecast anual']
    #st.write(pedir_fcstme)
    pedir2aspen = pd.concat([pedir_fcststaspen, pedir_fcstmeaspen])
    #st.write(pedir2a)
    pedir2aspen['MP'] = pedir2aspen['MP'].str.strip()
    prods = productos[['Cve_prod', 'Desc_prod']]
    prods.columns = ['SKU', 'MP']
    pedir2aspen = pedir2aspen.merge(prods, on='MP', how='left')
    #Columnas a pegar en la explosión
    pedir2taspen = pedir2aspen.groupby(['SKU']).agg({'Cantidad Oct23':'sum',
                                  'Cantidad Nov23':'sum',
                                  'Cantidad Dic23':'sum',
                                  'Cantidad Ene24':'sum',
                                  'Cantidad Feb24':'sum'}).reset_index()
    ######################################################################################################
    ####################PEDIR SIMILARES#####################################################
    pedir_fcstsimi = fcst_faltantessimi.merge(formulas, on='SKU', how='left')
    #st.write(pedir_fcst)
    pedir_fcstsimi = pedir_fcstsimi.dropna()
    #st.write(pedir_fcst)
    pedir_fcstmesimi = pedir_fcstsimi[pedir_fcstsimi['Cve_prod'].str.startswith('M')].reset_index(drop=True)
    pedir_fcstmesimi['Faltantes me'] = pedir_fcstmesimi['Faltantes'] * pedir_fcstmesimi['Cantidad']
    pedir_fcstmesimi['Faltantes me Oct23'] = pedir_fcstmesimi['Oct23'] * pedir_fcstmesimi['Cantidad']
    pedir_fcstmesimi['Faltantes me Nov23'] = pedir_fcstmesimi['Nov23'] * pedir_fcstmesimi['Cantidad']
    pedir_fcstmesimi['Faltantes me Dic23'] = pedir_fcstmesimi['Dic23'] * pedir_fcstmesimi['Cantidad']
    pedir_fcstmesimi['Faltantes me Ene24'] = pedir_fcstmesimi['Ene23'] * pedir_fcstmesimi['Cantidad']
    pedir_fcstmesimi['Faltantes me Feb24'] = pedir_fcstmesimi['Feb24'] * pedir_fcstmesimi['Cantidad']
    #st.write(pedir_fcstmea)
    pedir_fcststsimi = pedir_fcstsimi[pedir_fcstsimi['Cve_prod'].str.startswith('41')].reset_index(drop=True)
    pedir_fcststsimi.rename(columns = {'SKU':'SKU_f', 'Cve_prod':'SKU'}, inplace=True)
    pedir_fcststsimi['SKU'] = pedir_fcststsimi['SKU'].str.strip()
    pedir_fcststsimi = pedir_fcststsimi.merge(formulas, on='SKU', how='left')
    pedir_fcststsimi['Cantidad_y'] = pedir_fcststsimi['Cantidad rendimiento_y'] / pedir_fcststsimi['Rendimiento_x']
    pedir_fcststsimi['Cantidad mp'] = pedir_fcststsimi['Cantidad_y'] * pedir_fcststsimi['Faltantes']
    pedir_fcststsimi['Cantidad mp Oct23'] = pedir_fcststsimi['Cantidad_y'] * pedir_fcststsimi['Oct23']
    pedir_fcststsimi['Cantidad mp Nov23'] = pedir_fcststsimi['Cantidad_y'] * pedir_fcststsimi['Nov23']
    pedir_fcststsimi['Cantidad mp Dic23'] = pedir_fcststsimi['Cantidad_y'] * pedir_fcststsimi['Dic23']
    pedir_fcststsimi['Cantidad mp Ene24'] = pedir_fcststsimi['Cantidad_y'] * pedir_fcststsimi['Ene23']
    pedir_fcststsimi['Cantidad mp Feb24'] = pedir_fcststsimi['Cantidad_y'] * pedir_fcststsimi['Feb24']
    #st.write(pedir_fcststsimi)
    pedir_fcststsimi = pedir_fcststsimi[['Producto_x', 'Faltantes', 'MP_y', 'Cantidad mp', 'Sep23', 'Cantidad mp Oct23', 'Cantidad mp Nov23', 'Cantidad mp Dic23', 'Cantidad mp Ene24', 'Cantidad mp Feb24', 'Forecast anual']]
    pedir_fcststsimi.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'Sep23', 'Cantidad Oct23', 'Cantidad Nov23', 'Cantidad Dic23', 'Cantidad Ene24', 'Cantidad Feb24', 'Forecast anual']
    #st.write(pedir_fcstst)
    pedir_fcstmesimi = pedir_fcstmesimi[['Producto_x', 'Faltantes', 'MP', 'Faltantes me', 'Sep23', 'Faltantes me Oct23', 'Faltantes me Nov23', 'Faltantes me Dic23', 'Faltantes me Ene24', 'Faltantes me Feb24', 'Forecast anual']]
    pedir_fcstmesimi.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'Sep23', 'Cantidad Oct23', 'Cantidad Nov23', 'Cantidad Dic23', 'Cantidad Ene24', 'Cantidad Feb24', 'Forecast anual']
    #st.write(pedir_fcstme)
    pedir2simi = pd.concat([pedir_fcststsimi, pedir_fcstmesimi])
    #st.write(pedir2a)
    pedir2simi['MP'] = pedir2simi['MP'].str.strip()
    prods = productos[['Cve_prod', 'Desc_prod']]
    prods.columns = ['SKU', 'MP']
    pedir2simi = pedir2simi.merge(prods, on='MP', how='left')
    #Columnas a pegar en la explosión
    pedir2tsimi = pedir2simi.groupby(['SKU']).agg({'Cantidad Oct23':'sum',
                                  'Cantidad Nov23':'sum',
                                  'Cantidad Dic23':'sum',
                                  'Cantidad Ene24':'sum',
                                  'Cantidad Feb24':'sum'}).reset_index()
    ######################################################################################################
    ####################PEDIR GRISI#####################################################
    pedir_fcstgrisi = fcst_faltantesgrisi.merge(formulas, on='SKU', how='left')
    #st.write(pedir_fcstgrisi)
    pedir_fcstgrisi = pedir_fcstgrisi.dropna()
    #st.write(pedir_fcst)
    pedir_fcstmegrisi = pedir_fcstgrisi[pedir_fcstgrisi['Cve_prod'].str.startswith('M')].reset_index(drop=True)
    pedir_fcstmegrisi['Faltantes me'] = pedir_fcstmegrisi['Faltantes'] * pedir_fcstmegrisi['Cantidad']
    pedir_fcstmegrisi['Faltantes me Oct23'] = pedir_fcstmegrisi['Oct23'] * pedir_fcstmegrisi['Cantidad']
    pedir_fcstmegrisi['Faltantes me Nov23'] = pedir_fcstmegrisi['Nov23'] * pedir_fcstmegrisi['Cantidad']
    pedir_fcstmegrisi['Faltantes me Dic23'] = pedir_fcstmegrisi['Dic23'] * pedir_fcstmegrisi['Cantidad']
    pedir_fcstmegrisi['Faltantes me Ene24'] = pedir_fcstmegrisi['Ene23'] * pedir_fcstmegrisi['Cantidad']
    pedir_fcstmegrisi['Faltantes me Feb24'] = pedir_fcstmegrisi['Feb24'] * pedir_fcstmegrisi['Cantidad']
    #st.write(pedir_fcstmea)
    pedir_fcststgrisi = pedir_fcstgrisi[pedir_fcstgrisi['Cve_prod'].str.startswith('41')].reset_index(drop=True)
    pedir_fcststgrisi.rename(columns = {'SKU':'SKU_f', 'Cve_prod':'SKU'}, inplace=True)
    pedir_fcststgrisi['SKU'] = pedir_fcststgrisi['SKU'].str.strip()
    pedir_fcststgrisi = pedir_fcststgrisi.merge(formulas, on='SKU', how='left')
    pedir_fcststgrisi['Cantidad_y'] = pedir_fcststgrisi['Cantidad rendimiento_y'] / pedir_fcststgrisi['Rendimiento_x']
    pedir_fcststgrisi['Cantidad mp'] = pedir_fcststgrisi['Cantidad_y'] * pedir_fcststgrisi['Faltantes']
    pedir_fcststgrisi['Cantidad mp Oct23'] = pedir_fcststgrisi['Cantidad_y'] * pedir_fcststgrisi['Oct23']
    pedir_fcststgrisi['Cantidad mp Nov23'] = pedir_fcststgrisi['Cantidad_y'] * pedir_fcststgrisi['Nov23']
    pedir_fcststgrisi['Cantidad mp Dic23'] = pedir_fcststgrisi['Cantidad_y'] * pedir_fcststgrisi['Dic23']
    pedir_fcststgrisi['Cantidad mp Ene24'] = pedir_fcststgrisi['Cantidad_y'] * pedir_fcststgrisi['Ene23']
    pedir_fcststgrisi['Cantidad mp Feb24'] = pedir_fcststgrisi['Cantidad_y'] * pedir_fcststgrisi['Feb24']
    pedir_fcststgrisi = pedir_fcststgrisi[['Producto_x', 'Faltantes', 'MP_y', 'Cantidad mp', 'Sep23', 'Cantidad mp Oct23', 'Cantidad mp Nov23', 'Cantidad mp Dic23', 'Cantidad mp Ene24', 'Cantidad mp Feb24', 'Forecast anual']]
    pedir_fcststgrisi.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'Sep23', 'Cantidad Oct23', 'Cantidad Nov23', 'Cantidad Dic23', 'Cantidad Ene24', 'Cantidad Feb24', 'Forecast anual']
    #st.write(pedir_fcstst)
    pedir_fcstmegrisi = pedir_fcstmegrisi[['Producto_x', 'Faltantes', 'MP', 'Faltantes me', 'Sep23', 'Faltantes me Oct23', 'Faltantes me Nov23', 'Faltantes me Dic23', 'Faltantes me Ene24', 'Faltantes me Feb24', 'Forecast anual']]
    pedir_fcstmegrisi.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'Sep23', 'Cantidad Oct23', 'Cantidad Nov23', 'Cantidad Dic23', 'Cantidad Ene24', 'Cantidad Feb24', 'Forecast anual']
    #st.write(pedir_fcstme)
    pedir2grisi = pd.concat([pedir_fcststgrisi, pedir_fcstmegrisi])
    #st.write(pedir2a)
    pedir2grisi['MP'] = pedir2grisi['MP'].str.strip()
    prods = productos[['Cve_prod', 'Desc_prod']]
    prods.columns = ['SKU', 'MP']
    pedir2grisi = pedir2grisi.merge(prods, on='MP', how='left')
    #Columnas a pegar en la explosión
    pedir2tgrisi = pedir2grisi.groupby(['SKU']).agg({'Cantidad Oct23':'sum',
                                  'Cantidad Nov23':'sum',
                                  'Cantidad Dic23':'sum',
                                  'Cantidad Ene24':'sum',
                                  'Cantidad Feb24':'sum'}).reset_index()
    ######################################################################################################
    #############REQUI GENERAL##########################################################################
    pedir2 = pedir2.merge(existeN_comp, on='SKU', how='left')
    pedir2 = pedir2.fillna(0)
    #st.write(pedir2)
    pedir2['Faltante mp'] = pedir2['Cantidad'] - pedir2['Existencia']
    #st.write(pedir2)
    ###COSTO FOR
    costo_for = df_formulas[['Desc_prod', 'Cto_rep']]
    costo_for.columns = ['MP', 'Costo']
    costo_for =costo_for.groupby(['MP']).agg({'Costo':'mean'}).reset_index()
    costo_for['MP'] = costo_for['MP'].str.strip()
    ###
    pedir2['Faltante mp'][(pedir2['Faltante mp'] < 0)] = 0
    requi2 = pedir2.groupby(['MP']).agg({'Cantidad':'sum', 'Existencia':'max', 'Faltante mp':'sum'}).reset_index()
    #st.write(requi2)
    requi2 = requi2.merge(costo_for, on='MP', how='left')
    requi2['Costo total'] = requi2['Faltante mp'] * requi2['Costo']
    total_requi2 = requi2['Costo total'].sum()
    ######################################################################################################
    #############REQUI A1-A3##########################################################################
    pedira = pedir2a.merge(existeN_a, on='SKU', how='left')
    pedira = pedira.fillna(0)
    #st.write(pedira)
    pedira['Faltante mp'] = pedira['Cantidad'] - pedira['Existencia']
    #st.write(pedira)
    ###COSTO FOR
    costo_fora = df_formulas[['Desc_prod', 'Cto_rep']]
    costo_fora.columns = ['MP', 'Costo']
    costo_fora =costo_fora.groupby(['MP']).agg({'Costo':'mean'}).reset_index()
    costo_fora['MP'] = costo_fora['MP'].str.strip()
    ###
    pedira['Faltante mp'][(pedira['Faltante mp'] < 0)] = 0
    requia = pedira.groupby(['MP']).agg({'Cantidad':'sum', 'Existencia':'max', 'Faltante mp':'sum'}).reset_index()
    #st.write(requi2)
    requia = requia.merge(costo_fora, on='MP', how='left')
    requia['Costo total'] = requia['Faltante mp'] * requia['Costo']
    total_requia = requia['Costo total'].sum()
    ######################################################################################################
    #############REQUI ASPEN##########################################################################
    pediraspen = pedir2aspen.merge(existeN_aspen, on='SKU', how='left')
    pediraspen = pediraspen.fillna(0)
    #st.write(pedir2)
    pediraspen['Faltante mp'] = pediraspen['Cantidad'] - pediraspen['Existencia']
    #st.write(pedir2)
    ###COSTO FOR
    costo_foraspen = df_formulas[['Desc_prod', 'Cto_rep']]
    costo_foraspen.columns = ['MP', 'Costo']
    costo_foraspen =costo_foraspen.groupby(['MP']).agg({'Costo':'mean'}).reset_index()
    costo_foraspen['MP'] = costo_foraspen['MP'].str.strip()
    ###
    pediraspen['Faltante mp'][(pediraspen['Faltante mp'] < 0)] = 0
    requiaspen = pediraspen.groupby(['MP']).agg({'Cantidad':'sum', 'Existencia':'max', 'Faltante mp':'sum'}).reset_index()
    #st.write(requi2)
    requiaspen = requiaspen.merge(costo_foraspen, on='MP', how='left')
    requiaspen['Costo total'] = requiaspen['Faltante mp'] * requiaspen['Costo']
    total_requiaspen = requiaspen['Costo total'].sum()
    ######################################################################################################
    #############REQUI SIMI##########################################################################
    pedirsimi = pedir2simi.merge(existeN_simi, on='SKU', how='left')
    pedirsimi = pedirsimi.fillna(0)
    #st.write(pedir2)
    pedirsimi['Faltante mp'] = pedirsimi['Cantidad'] - pedirsimi['Existencia']
    #st.write(pedir2)
    ###COSTO FOR
    costo_forsimi = df_formulas[['Desc_prod', 'Cto_rep']]
    costo_forsimi.columns = ['MP', 'Costo']
    costo_forsimi =costo_forsimi.groupby(['MP']).agg({'Costo':'mean'}).reset_index()
    costo_forsimi['MP'] = costo_forsimi['MP'].str.strip()
    ###
    pedirsimi['Faltante mp'][(pedirsimi['Faltante mp'] < 0)] = 0
    requisimi = pedirsimi.groupby(['MP']).agg({'Cantidad':'sum', 'Existencia':'max', 'Faltante mp':'sum'}).reset_index()
    #st.write(requi2)
    requisimi = requisimi.merge(costo_forsimi, on='MP', how='left')
    requisimi['Costo total'] = requisimi['Faltante mp'] * requisimi['Costo']
    total_requisimi = requisimi['Costo total'].sum()
    ######################################################################################################
    #############REQUI GRISI##########################################################################
    pedirgrisi = pedir2grisi.merge(existeN_grisi, on='SKU', how='left')
    pedirgrisi = pedirgrisi.fillna(0)
    #st.write(pedir2)
    pedirgrisi['Faltante mp'] = pedirgrisi['Cantidad'] - pedirgrisi['Existencia']
    #st.write(pedir2)
    ###COSTO FOR
    costo_forgrisi = df_formulas[['Desc_prod', 'Cto_rep']]
    costo_forgrisi.columns = ['MP', 'Costo']
    costo_forgrisi =costo_forgrisi.groupby(['MP']).agg({'Costo':'mean'}).reset_index()
    costo_forgrisi['MP'] = costo_forgrisi['MP'].str.strip()
    ###
    pedirgrisi['Faltante mp'][(pedirgrisi['Faltante mp'] < 0)] = 0
    requigrisi = pedirgrisi.groupby(['MP']).agg({'Cantidad':'sum', 'Existencia':'max', 'Faltante mp':'sum'}).reset_index()
    #st.write(requi2)
    requigrisi = requigrisi.merge(costo_forgrisi, on='MP', how='left')
    requigrisi['Costo total'] = requigrisi['Faltante mp'] * requigrisi['Costo']
    total_requigrisi = requigrisi['Costo total'].sum()
    ######################################################################################################
    #st.write(requi2)

#####################################################################################################################################
    # creo un dataframe vacio con una columna llamada mes
    mes= pd.DataFrame(columns=['Mes'])
    anio = pd.DataFrame(columns=['Anio'])
    #Filtro las columnas que necesito
    #st.write(compras)
    df_compras = compras[['No_pedc', 'F_alta_ped','Cve_prod','Desc_prod', 'Nom_prov', 'F_ent','Cant_prod','Cant_surtp','Valor_prod',
                          'Des_mon', 'Status', 'Status_aut']]
    # hago un substring que me de solo los numeros del mes 
    mes['Mes'] = df_compras['F_ent'].str[3:5]
    anio['Anio'] = df_compras['F_ent'].str[6:10]
    #st.write(anio)

    # concateno el mes con mi dataframe df_compras
    df_compras = pd.concat([df_compras,mes,anio], axis=1)

    # Cant_prod - Cant_surtp
    x_entregar = df_compras['Cant_prod'] - df_compras['Cant_surtp']
    df_compras = pd.concat([df_compras,x_entregar], axis=1)
    df_compras.columns=['# Orden', 'F_alta_ped','Cve_prod','Desc_prod', 'Nom_prov', 'F_ent','Cant_prod','Cant_surtp','Valor_prod',
                        'Des_mon', 'Status', 'Status_aut', 'Mes', 'Anio', 'X_Entregar']
    
    df_compras = df_compras[['# Orden', 'F_alta_ped', 'Cve_prod','Desc_prod', 'Nom_prov','X_Entregar','Cant_surtp','Cant_prod',
                             'Status', 'Status_aut', 'F_ent','Mes', 'Anio', 'Valor_prod','Des_mon']]
    for i in range(len(df_compras.loc[:,'F_ent'])):
        try:
            df_compras.loc[i,'F_ent'] = pd.to_datetime(df_compras.loc[i,'F_ent'], format='%d/%m/%Y')
        except ValueError:
            df_compras.loc[i, 'F_ent'] = pd.to_datetime(df_compras.loc[i, 'F_alta_ped'], format='%d/%m/%Y')
    
    df_compras = df_compras[['# Orden', 'Cve_prod','Desc_prod', 'Nom_prov','X_Entregar','Cant_surtp','Cant_prod', 
                             'Status', 'Status_aut', 'F_ent','Mes', 'Anio', 'Valor_prod','Des_mon']]
    #start_date = df_compras['F_ent'].min()
    #start_date = datetime(start_date.year, start_date.month, start_date.day)
    #end_date = df_compras['F_ent'].max()
    #end_date = datetime(end_date.year, end_date.month, end_date.day)
    
    st.sidebar.title("Filtros ordenes de compra")
    proov = st.sidebar.multiselect("Proveedor",df_compras['Nom_prov'].unique())
    #Filtro de fecha de entrega#
    #selected_date = st.sidebar.slider(
    #    "Selecciona un rango en fecha de entrega",
    #    min_value = start_date,
    #    max_value = end_date,
    #    value = (start_date, end_date),
    #    step = timedelta(days=1),
    #    )
    Autorizacion = st.sidebar.multiselect('Autorización', df_compras['Status_aut'].unique())
    Estatus = st.sidebar.multiselect('Estatus', df_compras['Status'].unique())
    if not proov:
        proov = df_compras['Nom_prov'].unique()
    if not Autorizacion:
        Autorizacion = df_compras['Status_aut'].unique()
    if not Estatus:
        Estatus = df_compras['Status'].unique()
    
    #df_compras = df_compras[(df_compras['Nom_prov'].isin(proov)) & (df_compras['F_ent']<selected_date[1]) & 
    #    (df_compras['F_ent']>selected_date[0]) & (df_compras['Status_aut'].isin(Autorizacion)) & (df_compras['Status'].isin(Estatus))]

    df_compras = df_compras[(df_compras['Nom_prov'].isin(proov)) & (df_compras['Status_aut'].isin(Autorizacion)) 
                            & (df_compras['Status'].isin(Estatus))]
    #st.write(fcst_victor2['Forecast'])
    if st.checkbox('Formulas'):
        st.write(formulas)
    if st.checkbox('Forecast original'):
        st.write(fcst_faltantes)
    if st.checkbox('Desglose materias primas por PT'):
        st.write(pedir2)
    if st.checkbox('Almacenes Grisi'):
        st.write(egrisi)
    if st.checkbox('Almacenes Aspen'):
        st.write(easpen)
    if st.checkbox('Almacenes Similares'):
        st.write(esimi)
    if st.checkbox('Ordenes de compra'):
        st.write(df_compras)

    recepcion = df_compras.copy()
    recepcion.columns = recepcion.columns.str.strip()
    recepcion['Status'] = recepcion['Status'].str.strip()
    recepcion['Status_aut'] = recepcion['Status_aut'].str.strip()
    recepcion = recepcion[(recepcion['Status'] !='Surtido') & (recepcion['Status_aut'] == 'Aceptada')] 
    recepcion['Rec Sep23'] = recepcion['X_Entregar'][(recepcion['Mes'] == '09')]
    recepcion['Rec Oct23'] = recepcion['X_Entregar'][(recepcion['Mes'] == '10')]
    recepcion['Rec Nov23'] = recepcion['X_Entregar'][(recepcion['Mes'] == '11')]
    recepcion['Rec Dic23'] = recepcion['X_Entregar'][(recepcion['Mes'] == '12')]
    recepcion['Rec Ene24'] = recepcion['X_Entregar'][(recepcion['Mes'] == '1') & (recepcion['Anio']) == '2024']
    recepcion['Rec Feb24'] = recepcion['X_Entregar'][(recepcion['Mes'] == '2') & (recepcion['Anio']) == '2024']
    recepcion = recepcion.fillna(0)
    #st.write(recepcion)
    recepcion = recepcion.groupby(['Cve_prod']).agg({'X_Entregar':'sum',
                                                     'Rec Sep23':'sum',
                                                     'Rec Oct23':'sum',
                                                     'Rec Nov23':'sum',
                                                     'Rec Dic23':'sum',
                                                     'Rec Ene24':'sum',
                                                     'Rec Feb24':'sum'}).reset_index()
    recepcion.columns = ['SKU', 'X_Entregar', 'Rec Sep23', 'Rec Oct23', 'Rec Nov23', 'Rec Dic23', 'Rec Ene24', 'Rec Feb24']
    prods = productos[['Cve_prod', 'Desc_prod', 'Cve_monc']]
    prods.columns = ['SKU', 'MP', 'Moneda']
    tc = st.text_input('Tipo de cambio', '17.00')
    tc = float(tc)
    ##########EXPLOSION FINAL GENERAL################################################
    explosion = requi2.copy()
    explosion = explosion.merge(prods, on='MP', how='left')
    #st.write(requi2)
    explosion = explosion.fillna(0)
    
    explosion = explosion[['SKU', 'MP', 'Moneda', 'Costo', 'Existencia', 'Cantidad', 'Faltante mp']]
    explosion = explosion.merge(pedir2t, on='SKU', how='left')
    explosion['Faltante mp'] = explosion['Cantidad'] - explosion['Existencia']
    explosion['Faltante mp'][(explosion['Faltante mp'] < 0)] = 0
    for i in range(len(explosion['SKU'])):
        if explosion.loc[i,'Moneda'] == 2:
            explosion.loc[i,'Costo'] = tc * explosion.loc[i,'Costo']
    explosion = explosion.merge(recepcion, on='SKU', how='left')
    explosion = explosion.fillna(0)
    explosion['Costo total'] = explosion['Faltante mp'] * explosion['Costo']
    #st.write(explosion)
    
    ##################################################################################################3333
    explosion['Inv inicial'] = (explosion['Cantidad'] - explosion['Existencia']) - explosion['Rec Sep23']
    explosion['Inv inicial'][(explosion['Inv inicial'] >0)] = 0
    explosion['Inv inicial'][(explosion['Inv inicial'] <0)] = (-1)*explosion['Inv inicial']
    
    #Faltantes Octubre
    explosion['Fal Oct23'] = explosion['Cantidad Oct23'] - explosion['Inv inicial']
    explosion['Fal Oct23'][(explosion['Fal Oct23'] <0)] = 0
    explosion['Costo Oct23'] = explosion['Fal Oct23'] * explosion['Costo']
    #Inventario inicial Noviembre
    explosion['Inv inicial Nov23'] = (explosion['Cantidad Oct23'] - explosion['Inv inicial']) - explosion['Rec Oct23']
    explosion['Inv inicial Nov23'][(explosion['Inv inicial Nov23'] >0)] = 0
    explosion['Inv inicial Nov23'][(explosion['Inv inicial Nov23'] <0)] = (-1)*explosion['Inv inicial Nov23']
    #Faltantes Noviembre
    explosion['Fal Nov23'] = explosion['Cantidad Nov23'] - explosion['Inv inicial Nov23']
    explosion['Fal Nov23'][(explosion['Fal Nov23'] <0)] = 0
    explosion['Costo Nov23'] = explosion['Fal Nov23'] * explosion['Costo']
    #Inventario inicial diciembre
    explosion['Inv inicial Dic23'] = (explosion['Cantidad Nov23'] - explosion['Inv inicial Nov23']) - explosion['Rec Nov23']
    explosion['Inv inicial Dic23'][(explosion['Inv inicial Dic23'] >0)] = 0
    explosion['Inv inicial Dic23'][(explosion['Inv inicial Dic23'] <0)] = (-1)*explosion['Inv inicial Dic23']
    #Faltantes diciembre
    explosion['Fal Dic23'] = explosion['Cantidad Dic23'] - explosion['Inv inicial Dic23']
    explosion['Fal Dic23'][(explosion['Fal Dic23'] <0)] = 0
    explosion['Costo Dic23'] = explosion['Fal Dic23'] * explosion['Costo']
    #Inventario inicial Enero
    explosion['Inv inicial Ene24'] = (explosion['Cantidad Dic23'] - explosion['Inv inicial Dic23']) - explosion['Rec Dic23']
    explosion['Inv inicial Ene24'][(explosion['Inv inicial Ene24'] >0)] = 0
    explosion['Inv inicial Ene24'][(explosion['Inv inicial Ene24'] <0)] = (-1)*explosion['Inv inicial Ene24']
    #Faltantes Enero
    explosion['Fal Ene24'] = explosion['Cantidad Ene24'] - explosion['Inv inicial Ene24']
    explosion['Fal Ene24'][(explosion['Fal Ene24'] <0)] = 0
    explosion['Costo Ene24'] = explosion['Fal Ene24'] * explosion['Costo']
    #Inventario inicial Febrero
    explosion['Inv inicial Feb24'] = (explosion['Cantidad Ene24'] - explosion['Inv inicial Ene24']) - explosion['Rec Ene24']
    explosion['Inv inicial Feb24'][(explosion['Inv inicial Feb24'] >0)] = 0
    explosion['Inv inicial Feb24'][(explosion['Inv inicial Feb24'] <0)] = (-1)*explosion['Inv inicial Feb24']
    #Faltantes Febrero
    explosion['Fal Feb24'] = explosion['Cantidad Feb24'] - explosion['Inv inicial Feb24']
    explosion['Fal Feb24'][(explosion['Fal Feb24'] <0)] = 0
    explosion['Costo Feb24'] = explosion['Fal Feb24'] * explosion['Costo']
    #for i in range(len(explosion['SKU'])):
    #    if explosion.loc[i,'Inv inicial']>0:
    #        explosion.loc[i,'Inv inicial'] = 0
    #    else:
    #        explosion.loc[i,'Inv inicial'] = (-1)*explosion.loc[i,'Inv inicial']
    explosion = explosion[['SKU', 'MP', 'Moneda', 'Costo', 'Existencia', 'Cantidad', 'Faltante mp', 'Costo total', 'Rec Sep23', 
               'Inv inicial', 'Cantidad Oct23', 'Fal Oct23', 'Costo Oct23', 'Rec Oct23', 
               'Inv inicial Nov23', 'Cantidad Nov23', 'Fal Nov23', 'Costo Nov23' , 'Rec Nov23',
               'Inv inicial Dic23', 'Cantidad Dic23', 'Fal Dic23', 'Costo Dic23', 'Rec Dic23',
               'Inv inicial Ene24', 'Cantidad Ene24', 'Fal Ene24', 'Costo Ene24', 'Rec Ene24',
               'Inv inicial Feb24', 'Cantidad Feb24', 'Fal Feb24', 'Costo Feb24', 'Rec Feb24']]
    #############################################################################################################
    
    inversionmes = explosion['Costo total'].sum()
    frase = 'Inversión total del mes $' + str(round(inversionmes,2))

    ####################################################################################
    ##########EXPLOSION FINAL A1-A3################################################
    explosiona = requia.copy()
    explosiona = explosiona.merge(prods, on='MP', how='left')
    #st.write(requi2)
    
    explosiona = explosiona.fillna(0)
    
    explosiona = explosiona[['SKU', 'MP', 'Moneda', 'Costo', 'Existencia', 'Cantidad', 'Faltante mp']]
    
    explosiona['Faltante mp'] = explosiona['Cantidad'] - explosiona['Existencia']
    explosiona['Faltante mp'][(explosiona['Faltante mp'] < 0)] = 0
    explosiona = explosiona.merge(pedir2ta, on='SKU', how='left')
    for i in range(len(explosiona['SKU'])):
        if explosiona.loc[i,'Moneda'] == 2:
            explosiona.loc[i,'Costo'] = tc * explosiona.loc[i,'Costo']
    explosiona = explosiona.merge(recepcion, on='SKU', how='left')
    explosiona = explosiona.fillna(0)
    explosiona['Costo total'] = explosiona['Faltante mp'] * explosiona['Costo']
    
    #####################################################################################################
    explosiona['Inv inicial'] = (explosiona['Cantidad'] - explosiona['Existencia']) - explosiona['Rec Sep23']
    explosiona['Inv inicial'][(explosiona['Inv inicial'] >0)] = 0
    explosiona['Inv inicial'][(explosiona['Inv inicial'] <0)] = (-1)*explosiona['Inv inicial']
    
    #Faltantes Octubre
    explosiona['Fal Oct23'] = explosiona['Cantidad Oct23'] - explosiona['Inv inicial']
    explosiona['Fal Oct23'][(explosiona['Fal Oct23'] <0)] = 0
    explosiona['Costo Oct23'] = explosiona['Fal Oct23'] * explosiona['Costo']
    #Inventario inicial Noviembre
    explosiona['Inv inicial Nov23'] = (explosiona['Cantidad Oct23'] - explosiona['Inv inicial']) - explosiona['Rec Oct23']
    explosiona['Inv inicial Nov23'][(explosiona['Inv inicial Nov23'] >0)] = 0
    explosiona['Inv inicial Nov23'][(explosiona['Inv inicial Nov23'] <0)] = (-1)*explosiona['Inv inicial Nov23']
    #Faltantes Noviembre
    explosiona['Fal Nov23'] = explosiona['Cantidad Nov23'] - explosiona['Inv inicial Nov23']
    explosiona['Fal Nov23'][(explosiona['Fal Nov23'] <0)] = 0
    explosiona['Costo Nov23'] = explosiona['Fal Nov23'] * explosiona['Costo']
    #Inventario inicial diciembre
    explosiona['Inv inicial Dic23'] = (explosiona['Cantidad Nov23'] - explosiona['Inv inicial Nov23']) - explosiona['Rec Nov23']
    explosiona['Inv inicial Dic23'][(explosiona['Inv inicial Dic23'] >0)] = 0
    explosiona['Inv inicial Dic23'][(explosiona['Inv inicial Dic23'] <0)] = (-1)*explosiona['Inv inicial Dic23']
    #Faltantes diciembre
    explosiona['Fal Dic23'] = explosiona['Cantidad Dic23'] - explosiona['Inv inicial Dic23']
    explosiona['Fal Dic23'][(explosiona['Fal Dic23'] <0)] = 0
    explosiona['Costo Dic23'] = explosiona['Fal Dic23'] * explosiona['Costo']
    #Inventario inicial Enero
    explosiona['Inv inicial Ene24'] = (explosiona['Cantidad Dic23'] - explosiona['Inv inicial Dic23']) - explosiona['Rec Dic23']
    explosiona['Inv inicial Ene24'][(explosiona['Inv inicial Ene24'] >0)] = 0
    explosiona['Inv inicial Ene24'][(explosiona['Inv inicial Ene24'] <0)] = (-1)*explosiona['Inv inicial Ene24']
    #Faltantes Enero
    explosiona['Fal Ene24'] = explosiona['Cantidad Ene24'] - explosiona['Inv inicial Ene24']
    explosiona['Fal Ene24'][(explosiona['Fal Ene24'] <0)] = 0
    explosiona['Costo Ene24'] = explosiona['Fal Ene24'] * explosiona['Costo']
    #Inventario inicial Febrero
    explosiona['Inv inicial Feb24'] = (explosiona['Cantidad Ene24'] - explosiona['Inv inicial Ene24']) - explosiona['Rec Ene24']
    explosiona['Inv inicial Feb24'][(explosiona['Inv inicial Feb24'] >0)] = 0
    explosiona['Inv inicial Feb24'][(explosiona['Inv inicial Feb24'] <0)] = (-1)*explosiona['Inv inicial Feb24']
    #Faltantes Febrero
    explosiona['Fal Feb24'] = explosiona['Cantidad Feb24'] - explosiona['Inv inicial Feb24']
    explosiona['Fal Feb24'][(explosiona['Fal Feb24'] <0)] = 0
    explosiona['Costo Feb24'] = explosiona['Fal Feb24'] * explosiona['Costo']
    explosiona = explosiona[['SKU', 'MP', 'Moneda', 'Costo', 'Existencia', 'Cantidad', 'Faltante mp', 'Costo total', 'Rec Sep23', 
               'Inv inicial', 'Cantidad Oct23', 'Fal Oct23', 'Costo Oct23', 
               'Inv inicial Nov23', 'Cantidad Nov23', 'Fal Nov23', 'Costo Nov23',
               'Inv inicial Dic23', 'Cantidad Dic23', 'Fal Dic23', 'Costo Dic23',
               'Inv inicial Ene24', 'Cantidad Ene24', 'Fal Ene24', 'Costo Ene24',
               'Inv inicial Feb24', 'Cantidad Feb24', 'Fal Feb24', 'Costo Feb24']]

    #######################################################################################################
    
    inversionmesa = explosiona['Costo total'].sum()
    frasea = 'Inversión total del mes $' + str(round(inversionmesa,2))
    ####################################################################################
    ##########EXPLOSION FINAL ASPEN################################################
    explosionaspen = requiaspen.copy()
    explosionaspen = explosionaspen.merge(prods, on='MP', how='left')
    
    #st.write(requi2)
    explosionaspen = explosionaspen.fillna(0)
    explosionaspen = explosionaspen[['SKU', 'MP', 'Moneda', 'Costo', 'Existencia', 'Cantidad', 'Faltante mp']]
    explosionaspen['Faltante mp'] = explosionaspen['Cantidad'] - explosionaspen['Existencia']
    explosionaspen['Faltante mp'][(explosionaspen['Faltante mp'] < 0)] = 0
    explosionaspen = explosionaspen.merge(pedir2taspen, on='SKU', how='left')
    for i in range(len(explosionaspen['SKU'])):
        if explosionaspen.loc[i,'Moneda'] == 2:
            explosionaspen.loc[i,'Costo'] = tc * explosionaspen.loc[i,'Costo']
    explosionaspen = explosionaspen.merge(recepcion, on='SKU', how='left')
    explosionaspen = explosionaspen.fillna(0)
    explosionaspen['Costo total'] = explosionaspen['Faltante mp'] * explosionaspen['Costo']
    
    #########################################################################################################
    explosionaspen['Inv inicial'] = (explosionaspen['Cantidad'] - explosionaspen['Existencia']) - explosionaspen['Rec Sep23']
    explosionaspen['Inv inicial'][(explosionaspen['Inv inicial'] >0)] = 0
    explosionaspen['Inv inicial'][(explosionaspen['Inv inicial'] <0)] = (-1)*explosionaspen['Inv inicial']
    #st.write(explosionaspen)
    #Faltantes Octubre
    explosionaspen['Fal Oct23'] = explosionaspen['Cantidad Oct23'] - explosionaspen['Inv inicial']
    explosionaspen['Fal Oct23'][(explosionaspen['Fal Oct23'] <0)] = 0
    explosionaspen['Costo Oct23'] = explosionaspen['Fal Oct23'] * explosionaspen['Costo']
    #Inventario inicial Noviembre
    explosionaspen['Inv inicial Nov23'] = (explosionaspen['Cantidad Oct23'] - explosionaspen['Inv inicial']) - explosionaspen['Rec Oct23']
    explosionaspen['Inv inicial Nov23'][(explosionaspen['Inv inicial Nov23'] >0)] = 0
    explosionaspen['Inv inicial Nov23'][(explosionaspen['Inv inicial Nov23'] <0)] = (-1)*explosionaspen['Inv inicial Nov23']
    #Faltantes Noviembre
    explosionaspen['Fal Nov23'] = explosionaspen['Cantidad Nov23'] - explosionaspen['Inv inicial Nov23']
    explosionaspen['Fal Nov23'][(explosionaspen['Fal Nov23'] <0)] = 0
    explosionaspen['Costo Nov23'] = explosionaspen['Fal Nov23'] * explosionaspen['Costo']
    #Inventario inicial diciembre
    explosionaspen['Inv inicial Dic23'] = (explosionaspen['Cantidad Nov23'] - explosionaspen['Inv inicial Nov23']) - explosionaspen['Rec Nov23']
    explosionaspen['Inv inicial Dic23'][(explosionaspen['Inv inicial Dic23'] >0)] = 0
    explosionaspen['Inv inicial Dic23'][(explosionaspen['Inv inicial Dic23'] <0)] = (-1)*explosionaspen['Inv inicial Dic23']
    #Faltantes diciembre
    explosionaspen['Fal Dic23'] = explosionaspen['Cantidad Dic23'] - explosionaspen['Inv inicial Dic23']
    explosionaspen['Fal Dic23'][(explosionaspen['Fal Dic23'] <0)] = 0
    explosionaspen['Costo Dic23'] = explosionaspen['Fal Dic23'] * explosionaspen['Costo']
    #Inventario inicial Enero
    explosionaspen['Inv inicial Ene24'] = (explosionaspen['Cantidad Dic23'] - explosionaspen['Inv inicial Dic23']) - explosionaspen['Rec Dic23']
    explosionaspen['Inv inicial Ene24'][(explosionaspen['Inv inicial Ene24'] >0)] = 0
    explosionaspen['Inv inicial Ene24'][(explosionaspen['Inv inicial Ene24'] <0)] = (-1)*explosionaspen['Inv inicial Ene24']
    #Faltantes Enero
    explosionaspen['Fal Ene24'] = explosionaspen['Cantidad Ene24'] - explosionaspen['Inv inicial Ene24']
    explosionaspen['Fal Ene24'][(explosionaspen['Fal Ene24'] <0)] = 0
    explosionaspen['Costo Ene24'] = explosionaspen['Fal Ene24'] * explosionaspen['Costo']
    #Inventario inicial Febrero
    explosionaspen['Inv inicial Feb24'] = (explosionaspen['Cantidad Ene24'] - explosionaspen['Inv inicial Ene24']) - explosionaspen['Rec Ene24']
    explosionaspen['Inv inicial Feb24'][(explosionaspen['Inv inicial Feb24'] >0)] = 0
    explosionaspen['Inv inicial Feb24'][(explosionaspen['Inv inicial Feb24'] <0)] = (-1)*explosionaspen['Inv inicial Feb24']
    #Faltantes Febrero
    explosionaspen['Fal Feb24'] = explosionaspen['Cantidad Feb24'] - explosionaspen['Inv inicial Feb24']
    explosionaspen['Fal Feb24'][(explosionaspen['Fal Feb24'] <0)] = 0
    explosionaspen['Costo Feb24'] = explosionaspen['Fal Feb24'] * explosionaspen['Costo']
    explosionaspen = explosionaspen[['SKU', 'MP', 'Moneda', 'Costo', 'Existencia', 'Cantidad', 'Faltante mp', 'Costo total', 'Rec Sep23', 
               'Inv inicial', 'Cantidad Oct23', 'Fal Oct23', 'Costo Oct23', 
               'Inv inicial Nov23', 'Cantidad Nov23', 'Fal Nov23', 'Costo Nov23',
               'Inv inicial Dic23', 'Cantidad Dic23', 'Fal Dic23', 'Costo Dic23',
               'Inv inicial Ene24', 'Cantidad Ene24', 'Fal Ene24', 'Costo Ene24',
               'Inv inicial Feb24', 'Cantidad Feb24', 'Fal Feb24', 'Costo Feb24']]
    ########################################################################################################
    
    inversionmesaspen = explosionaspen['Costo total'].sum()
    fraseaspen = 'Inversión total del mes $' + str(round(inversionmesaspen,2))
    ####################################################################################
    ##########EXPLOSION FINAL SIMI################################################
    explosionsimi = requisimi.copy()
    explosionsimi = explosionsimi.merge(prods, on='MP', how='left')
    
    #st.write(requi2)
    explosionsimi = explosionsimi.fillna(0)
    explosionsimi = explosionsimi[['SKU', 'MP', 'Moneda', 'Costo', 'Existencia', 'Cantidad', 'Faltante mp']]
    explosionsimi['Faltante mp'] = explosionsimi['Cantidad'] - explosionsimi['Existencia']
    explosionsimi['Faltante mp'][(explosionsimi['Faltante mp'] < 0)] = 0
    explosionsimi = explosionsimi.merge(pedir2tsimi, on='SKU', how='left')
    for i in range(len(explosionsimi['SKU'])):
        if explosionsimi.loc[i,'Moneda'] == 2:
            explosionsimi.loc[i,'Costo'] = tc * explosionsimi.loc[i,'Costo']
    explosionsimi = explosionsimi.merge(recepcion, on='SKU', how='left')
    explosionsimi = explosionsimi.fillna(0)
    explosionsimi['Costo total'] = explosionsimi['Faltante mp'] * explosionsimi['Costo']
    
    ########################################################################################################
    #st.write(explosionsimi)
    explosionsimi['Inv inicial'] = (explosionsimi['Cantidad'] - explosionsimi['Existencia']) - explosionsimi['Rec Sep23']
    explosionsimi['Inv inicial'][(explosionsimi['Inv inicial'] >0)] = 0
    explosionsimi['Inv inicial'][(explosionsimi['Inv inicial'] <0)] = (-1)*explosionsimi['Inv inicial']
    
    #Faltantes Octubre
    explosionsimi['Fal Oct23'] = explosionsimi['Cantidad Oct23'] - explosionsimi['Inv inicial']
    explosionsimi['Fal Oct23'][(explosionsimi['Fal Oct23'] <0)] = 0
    explosionsimi['Costo Oct23'] = explosionsimi['Fal Oct23'] * explosionsimi['Costo']
    #Inventario inicial Noviembre
    explosionsimi['Inv inicial Nov23'] = (explosionsimi['Cantidad Oct23'] - explosionsimi['Inv inicial']) - explosionsimi['Rec Oct23']
    explosionsimi['Inv inicial Nov23'][(explosionsimi['Inv inicial Nov23'] >0)] = 0
    explosionsimi['Inv inicial Nov23'][(explosionsimi['Inv inicial Nov23'] <0)] = (-1)*explosionsimi['Inv inicial Nov23']
    #Faltantes Noviembre
    explosionsimi['Fal Nov23'] = explosionsimi['Cantidad Nov23'] - explosionsimi['Inv inicial Nov23']
    explosionsimi['Fal Nov23'][(explosionsimi['Fal Nov23'] <0)] = 0
    explosionsimi['Costo Nov23'] = explosionsimi['Fal Nov23'] * explosionsimi['Costo']
    #Inventario inicial diciembre
    explosionsimi['Inv inicial Dic23'] = (explosionsimi['Cantidad Nov23'] - explosionsimi['Inv inicial Nov23']) - explosionsimi['Rec Nov23']
    explosionsimi['Inv inicial Dic23'][(explosionsimi['Inv inicial Dic23'] >0)] = 0
    explosionsimi['Inv inicial Dic23'][(explosionsimi['Inv inicial Dic23'] <0)] = (-1)*explosionsimi['Inv inicial Dic23']
    #Faltantes diciembre
    explosionsimi['Fal Dic23'] = explosionsimi['Cantidad Dic23'] - explosionsimi['Inv inicial Dic23']
    explosionsimi['Fal Dic23'][(explosionsimi['Fal Dic23'] <0)] = 0
    explosionsimi['Costo Dic23'] = explosionsimi['Fal Dic23'] * explosionsimi['Costo']
    #Inventario inicial Enero
    explosionsimi['Inv inicial Ene24'] = (explosionsimi['Cantidad Dic23'] - explosionsimi['Inv inicial Dic23']) - explosionsimi['Rec Dic23']
    explosionsimi['Inv inicial Ene24'][(explosionsimi['Inv inicial Ene24'] >0)] = 0
    explosionsimi['Inv inicial Ene24'][(explosionsimi['Inv inicial Ene24'] <0)] = (-1)*explosionsimi['Inv inicial Ene24']
    #Faltantes Enero
    explosionsimi['Fal Ene24'] = explosionsimi['Cantidad Ene24'] - explosionsimi['Inv inicial Ene24']
    explosionsimi['Fal Ene24'][(explosionsimi['Fal Ene24'] <0)] = 0
    explosionsimi['Costo Ene24'] = explosionsimi['Fal Ene24'] * explosionsimi['Costo']
    #Inventario inicial Febrero
    explosionsimi['Inv inicial Feb24'] = (explosionsimi['Cantidad Ene24'] - explosionsimi['Inv inicial Ene24']) - explosionsimi['Rec Ene24']
    explosionsimi['Inv inicial Feb24'][(explosionsimi['Inv inicial Feb24'] >0)] = 0
    explosionsimi['Inv inicial Feb24'][(explosionsimi['Inv inicial Feb24'] <0)] = (-1)*explosionsimi['Inv inicial Feb24']
    #Faltantes Febrero
    explosionsimi['Fal Feb24'] = explosionsimi['Cantidad Feb24'] - explosionsimi['Inv inicial Feb24']
    explosionsimi['Fal Feb24'][(explosionsimi['Fal Feb24'] <0)] = 0
    explosionsimi['Costo Feb24'] = explosionsimi['Fal Feb24'] * explosionsimi['Costo']
    #for i in range(len(explosion['SKU'])):
    #    if explosion.loc[i,'Inv inicial']>0:
    #        explosion.loc[i,'Inv inicial'] = 0
    #    else:
    #        explosion.loc[i,'Inv inicial'] = (-1)*explosion.loc[i,'Inv inicial']
    explosionsimi = explosionsimi[['SKU', 'MP', 'Moneda', 'Costo', 'Existencia', 'Cantidad', 'Faltante mp', 'Costo total', 'Rec Sep23', 
               'Inv inicial', 'Cantidad Oct23', 'Fal Oct23', 'Costo Oct23', 
               'Inv inicial Nov23', 'Cantidad Nov23', 'Fal Nov23', 'Costo Nov23',
               'Inv inicial Dic23', 'Cantidad Dic23', 'Fal Dic23', 'Costo Dic23',
               'Inv inicial Ene24', 'Cantidad Ene24', 'Fal Ene24', 'Costo Ene24',
               'Inv inicial Feb24', 'Cantidad Feb24', 'Fal Feb24', 'Costo Feb24']]
    
    ########################################################################################################

    
    inversionmessimi = explosionsimi['Costo total'].sum()
    frasesimi = 'Inversión total del mes $' + str(round(inversionmessimi,2))
    ####################################################################################
    ##########EXPLOSION FINAL GRISI################################################
    explosiongrisi = requigrisi.copy()
    explosiongrisi = explosiongrisi.merge(prods, on='MP', how='left')
    
    #st.write(requi2)
    explosiongrisi = explosiongrisi.fillna(0)
    explosiongrisi = explosiongrisi[['SKU', 'MP', 'Moneda', 'Costo', 'Existencia', 'Cantidad', 'Faltante mp']]
    explosiongrisi['Faltante mp'] = explosiongrisi['Cantidad'] - explosiongrisi['Existencia']
    explosiongrisi['Faltante mp'][(explosiongrisi['Faltante mp'] < 0)] = 0
    explosiongrisi = explosiongrisi.merge(pedir2tgrisi, on='SKU', how='left')
    for i in range(len(explosiongrisi['SKU'])):
        if explosiongrisi.loc[i,'Moneda'] == 2:
            explosiongrisi.loc[i,'Costo'] = tc * explosiongrisi.loc[i,'Costo']
    explosiongrisi = explosiongrisi.merge(recepcion, on='SKU', how='left')
    explosiongrisi = explosiongrisi.fillna(0)
    explosiongrisi['Costo total'] = explosiongrisi['Faltante mp'] * explosiongrisi['Costo']
    
    ##########################################################################################################3

    explosiongrisi['Inv inicial'] = (explosiongrisi['Cantidad'] - explosiongrisi['Existencia']) - explosiongrisi['Rec Sep23']
    explosiongrisi['Inv inicial'][(explosiongrisi['Inv inicial'] >0)] = 0
    explosiongrisi['Inv inicial'][(explosiongrisi['Inv inicial'] <0)] = (-1)*explosiongrisi['Inv inicial']
    
    #Faltantes Octubre
    explosiongrisi['Fal Oct23'] = explosiongrisi['Cantidad Oct23'] - explosiongrisi['Inv inicial']
    explosiongrisi['Fal Oct23'][(explosiongrisi['Fal Oct23'] <0)] = 0
    explosiongrisi['Costo Oct23'] = explosiongrisi['Fal Oct23'] * explosiongrisi['Costo']
    #Inventario inicial Noviembre
    explosiongrisi['Inv inicial Nov23'] = (explosiongrisi['Cantidad Oct23'] - explosiongrisi['Inv inicial']) - explosiongrisi['Rec Oct23']
    explosiongrisi['Inv inicial Nov23'][(explosiongrisi['Inv inicial Nov23'] >0)] = 0
    explosiongrisi['Inv inicial Nov23'][(explosiongrisi['Inv inicial Nov23'] <0)] = (-1)*explosiongrisi['Inv inicial Nov23']
    #Faltantes Noviembre
    explosiongrisi['Fal Nov23'] = explosiongrisi['Cantidad Nov23'] - explosiongrisi['Inv inicial Nov23']
    explosiongrisi['Fal Nov23'][(explosiongrisi['Fal Nov23'] <0)] = 0
    explosiongrisi['Costo Nov23'] = explosiongrisi['Fal Nov23'] * explosiongrisi['Costo']
    #Inventario inicial diciembre
    explosiongrisi['Inv inicial Dic23'] = (explosiongrisi['Cantidad Nov23'] - explosiongrisi['Inv inicial Nov23']) - explosiongrisi['Rec Nov23']
    explosiongrisi['Inv inicial Dic23'][(explosiongrisi['Inv inicial Dic23'] >0)] = 0
    explosiongrisi['Inv inicial Dic23'][(explosiongrisi['Inv inicial Dic23'] <0)] = (-1)*explosiongrisi['Inv inicial Dic23']
    #Faltantes diciembre
    explosiongrisi['Fal Dic23'] = explosiongrisi['Cantidad Dic23'] - explosiongrisi['Inv inicial Dic23']
    explosiongrisi['Fal Dic23'][(explosiongrisi['Fal Dic23'] <0)] = 0
    explosiongrisi['Costo Dic23'] = explosiongrisi['Fal Dic23'] * explosiongrisi['Costo']
    #Inventario inicial Enero
    explosiongrisi['Inv inicial Ene24'] = (explosiongrisi['Cantidad Dic23'] - explosiongrisi['Inv inicial Dic23']) - explosiongrisi['Rec Dic23']
    explosiongrisi['Inv inicial Ene24'][(explosiongrisi['Inv inicial Ene24'] >0)] = 0
    explosiongrisi['Inv inicial Ene24'][(explosiongrisi['Inv inicial Ene24'] <0)] = (-1)*explosiongrisi['Inv inicial Ene24']
    #Faltantes Enero
    explosiongrisi['Fal Ene24'] = explosiongrisi['Cantidad Ene24'] - explosiongrisi['Inv inicial Ene24']
    explosiongrisi['Fal Ene24'][(explosiongrisi['Fal Ene24'] <0)] = 0
    explosiongrisi['Costo Ene24'] = explosiongrisi['Fal Ene24'] * explosiongrisi['Costo']
    #Inventario inicial Febrero
    explosiongrisi['Inv inicial Feb24'] = (explosiongrisi['Cantidad Ene24'] - explosiongrisi['Inv inicial Ene24']) - explosiongrisi['Rec Ene24']
    explosiongrisi['Inv inicial Feb24'][(explosiongrisi['Inv inicial Feb24'] >0)] = 0
    explosiongrisi['Inv inicial Feb24'][(explosiongrisi['Inv inicial Feb24'] <0)] = (-1)*explosiongrisi['Inv inicial Feb24']
    #Faltantes Febrero
    explosiongrisi['Fal Feb24'] = explosiongrisi['Cantidad Feb24'] - explosiongrisi['Inv inicial Feb24']
    explosiongrisi['Fal Feb24'][(explosiongrisi['Fal Feb24'] <0)] = 0
    explosiongrisi['Costo Feb24'] = explosiongrisi['Fal Feb24'] * explosiongrisi['Costo']
    #for i in range(len(explosion['SKU'])):
    #    if explosion.loc[i,'Inv inicial']>0:
    #        explosion.loc[i,'Inv inicial'] = 0
    #    else:
    #        explosion.loc[i,'Inv inicial'] = (-1)*explosion.loc[i,'Inv inicial']
    explosiongrisi = explosiongrisi[['SKU', 'MP', 'Moneda', 'Costo', 'Existencia', 'Cantidad', 'Faltante mp', 'Costo total', 'Rec Sep23', 
               'Inv inicial', 'Cantidad Oct23', 'Fal Oct23', 'Costo Oct23', 
               'Inv inicial Nov23', 'Cantidad Nov23', 'Fal Nov23', 'Costo Nov23',
               'Inv inicial Dic23', 'Cantidad Dic23', 'Fal Dic23', 'Costo Dic23',
               'Inv inicial Ene24', 'Cantidad Ene24', 'Fal Ene24', 'Costo Ene24',
               'Inv inicial Feb24', 'Cantidad Feb24', 'Fal Feb24', 'Costo Feb24']]
    
    ################################################################################################################
    
    inversionmesgrisi = explosiongrisi['Costo total'].sum()
    frasegrisi = 'Inversión total del mes $' + str(round(inversionmesgrisi,2))
    ####################################################################################
    uno, dos = st.columns([1, 1])
    with uno:
        st.title('Almacén A1-A3')
        st.write(explosiona)
        st.download_button(label="Descargar", data=explosiona.to_csv(), mime="text/csv")
        st.info(frasea, icon='💵')
        st.title('Almacén ASPEN')
        st.write(explosionaspen)
        st.download_button(label="Descargar", data=explosionaspen.to_csv(), mime="text/csv")
        st.info(fraseaspen, icon='💵')
    with dos:
        st.title('Almacén SIMILARES')
        st.write(explosionsimi)
        st.download_button(label="Descargar", data=explosionsimi.to_csv(), mime="text/csv")
        st.info(frasesimi, icon='💵')
        st.title('Almacén GRISI')
        st.write(explosiongrisi)
        st.download_button(label="Descargar", data=explosiongrisi.to_csv(), mime="text/csv")
        st.info(frasegrisi, icon='💵')

    if st.checkbox('Requerimientos general'):
        explosion_temp = explosion.merge(moq, on='SKU', how='left')
        explosion_temp = explosion_temp.fillna(0)
        #st.write(explosion_temp)
        explosion_temp['OC NUEVA'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC NUEVAOCT'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC NUEVANOV'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC NUEVADIC'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC NUEVAENE'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC NUEVAFEB'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['div'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['divoct'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['divnov'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['divdic'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['divene'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['divfeb'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC temp'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC tempoct'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC tempnov'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC tempdic'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC tempene'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC tempfeb'] = pd.Series(0, index=range(len(explosion['SKU'])))
        #hola = math.ceil(explosion_temp.loc[22,'Faltante mp'] / explosion_temp.loc[22, 'MOQ'])
        #hola = (math.ceil(explosion_temp.loc[22,'Faltante mp'] / explosion_temp.loc[22,'MOQ']))*(explosion_temp.loc[22,'MOQ'])-(explosion_temp.loc[22,'Rec Sep23'])
        #st.write(hola)
        for i in range(len(explosion_temp['SKU'])):
            explosion_temp.loc[i, 'MOQ'] = float(explosion_temp.loc[i, 'MOQ'])
            explosion_temp = explosion_temp.fillna(0)
            if explosion_temp.loc[i,'MOQ'] != 0:
                explosion_temp.loc[i, 'div'] = math.ceil(explosion_temp.loc[i,'Faltante mp'] / explosion_temp.loc[i,'MOQ'])
            else:
                explosion_temp.loc[i, 'div'] = 0

            explosion_temp.loc[i,'OC temp'] = (explosion_temp.loc[i,'div'])*(explosion_temp.loc[i,'MOQ'])-(explosion_temp.loc[i,'Rec Sep23'])
        
            if (explosion_temp.loc[i,'Faltante mp']>0) & (explosion_temp.loc[i,'OC temp']>0):
                explosion_temp.loc[i,'OC NUEVA'] = explosion_temp.loc[i,'OC temp']
            else:
                explosion_temp.loc[i, 'OC NUEVA'] = 0  
        

        explosion_temp['TOTAL OC'] = explosion_temp['Rec Sep23'] + explosion_temp['OC NUEVA']
        explosion_temp = explosion_temp.merge(a1, on='SKU', how='left')
        explosion_temp = explosion_temp.fillna(0)
        explosion_temp['INV_OCT'] = (explosion_temp['Cantidad'] - explosion_temp['Existencia']) - explosion_temp['TOTAL OC'] 
        explosion_temp['INV_OCT'][(explosion_temp['INV_OCT'] >0)] = 0
        explosion_temp['INV_OCT'][(explosion_temp['INV_OCT'] <0)] = (-1)*explosion_temp['INV_OCT']
        
        #################################MES OCT################################################################################
        explosion_temp['Fal Oct23'] = explosion_temp['Cantidad Oct23'] - explosion_temp['INV_OCT']
        explosion_temp['Fal Oct23'][(explosion_temp['Fal Oct23']<0)] = 0
        for i in range(len(explosion_temp['SKU'])):
            if explosion_temp.loc[i, 'MOQ'] != 0:
                explosion_temp.loc[i, 'divoct'] = math.ceil(explosion_temp.loc[i,'Fal Oct23'] / explosion_temp.loc[i,'MOQ'])
            else:
                explosion_temp.loc[i, 'divoct'] = 0        
            explosion_temp.loc[i,'OC tempoct'] = (explosion_temp.loc[i,'divoct'])*(explosion_temp.loc[i,'MOQ'])-(explosion_temp.loc[i,'Rec Oct23'])
            if (explosion_temp.loc[i,'Fal Oct23']>0) & (explosion_temp.loc[i,'OC tempoct']>0):
                explosion_temp.loc[i,'OC NUEVAOCT'] = explosion_temp.loc[i,'OC tempoct']
            else:
                explosion_temp.loc[i, 'OC NUEVAOCT'] = 0
        explosion_temp['TOTAL OC_OCT'] = explosion_temp['Rec Oct23'] + explosion_temp['OC NUEVAOCT']
        explosion_temp['INV_NOV'] = (explosion_temp['Cantidad Oct23'] - explosion_temp['INV_OCT']) - explosion_temp['TOTAL OC_OCT']
        explosion_temp['INV_NOV'][(explosion_temp['INV_NOV'] >0)] = 0
        explosion_temp['INV_NOV'][(explosion_temp['INV_NOV'] <0)] = (-1)*explosion_temp['INV_NOV']
        ##################################################################################################################################

        #################################MES NOV################################################################################
        explosion_temp['Fal Nov23'] = explosion_temp['Cantidad Nov23'] - explosion_temp['INV_NOV']
        explosion_temp['Fal Nov23'][(explosion_temp['Fal Nov23']<0)] = 0
        for i in range(len(explosion_temp['SKU'])):
            if explosion_temp.loc[i, 'MOQ'] != 0:
                explosion_temp.loc[i, 'divnov'] = math.ceil(explosion_temp.loc[i,'Fal Nov23'] / explosion_temp.loc[i,'MOQ'])
            else:
                explosion_temp.loc[i, 'divnov'] = 0        
            explosion_temp.loc[i,'OC tempnov'] = (explosion_temp.loc[i,'divnov'])*(explosion_temp.loc[i,'MOQ'])-(explosion_temp.loc[i,'Rec Nov23'])
            if (explosion_temp.loc[i,'Fal Nov23']>0) & (explosion_temp.loc[i,'OC tempnov']>0):
                explosion_temp.loc[i,'OC NUEVANOV'] = explosion_temp.loc[i,'OC tempnov']
            else:
                explosion_temp.loc[i, 'OC NUEVANOV'] = 0
        explosion_temp['TOTAL OC_NOV'] = explosion_temp['Rec Nov23'] + explosion_temp['OC NUEVANOV']
        explosion_temp['INV_DIC'] = (explosion_temp['Cantidad Nov23'] - explosion_temp['INV_NOV']) - explosion_temp['TOTAL OC_NOV']
        explosion_temp['INV_DIC'][(explosion_temp['INV_DIC'] >0)] = 0
        explosion_temp['INV_DIC'][(explosion_temp['INV_DIC'] <0)] = (-1)*explosion_temp['INV_DIC']
        ##################################################################################################################################

        #################################MES DIC################################################################################
        explosion_temp['Fal Dic23'] = explosion_temp['Cantidad Dic23'] - explosion_temp['INV_DIC']
        explosion_temp['Fal Dic23'][(explosion_temp['Fal Dic23']<0)] = 0
        for i in range(len(explosion_temp['SKU'])):
            if explosion_temp.loc[i, 'MOQ'] != 0:
                explosion_temp.loc[i, 'divdic'] = math.ceil(explosion_temp.loc[i,'Fal Dic23'] / explosion_temp.loc[i,'MOQ'])
            else:
                explosion_temp.loc[i, 'divdic'] = 0        
            explosion_temp.loc[i,'OC tempdic'] = (explosion_temp.loc[i,'divdic'])*(explosion_temp.loc[i,'MOQ'])-(explosion_temp.loc[i,'Rec Dic23'])
            if (explosion_temp.loc[i,'Fal Dic23']>0) & (explosion_temp.loc[i,'OC tempdic']>0):
                explosion_temp.loc[i,'OC NUEVADIC'] = explosion_temp.loc[i,'OC tempdic']
            else:
                explosion_temp.loc[i, 'OC NUEVADIC'] = 0
        explosion_temp['TOTAL OC_DIC'] = explosion_temp['Rec Dic23'] + explosion_temp['OC NUEVADIC']
        explosion_temp['INV_ENE'] = (explosion_temp['Cantidad Dic23'] - explosion_temp['INV_DIC']) - explosion_temp['TOTAL OC_DIC']
        explosion_temp['INV_ENE'][(explosion_temp['INV_ENE'] >0)] = 0
        explosion_temp['INV_ENE'][(explosion_temp['INV_ENE'] <0)] = (-1)*explosion_temp['INV_ENE']
        ##################################################################################################################################

        #################################MES ENE################################################################################
        explosion_temp['Fal Ene24'] = explosion_temp['Cantidad Ene24'] - explosion_temp['INV_ENE']
        explosion_temp['Fal Ene24'][(explosion_temp['Fal Ene24']<0)] = 0
        for i in range(len(explosion_temp['SKU'])):
            if explosion_temp.loc[i, 'MOQ'] != 0:
                explosion_temp.loc[i, 'divene'] = math.ceil(explosion_temp.loc[i,'Fal Ene24'] / explosion_temp.loc[i,'MOQ'])
            else:
                explosion_temp.loc[i, 'divene'] = 0        
            explosion_temp.loc[i,'OC tempene'] = (explosion_temp.loc[i,'divene'])*(explosion_temp.loc[i,'MOQ'])-(explosion_temp.loc[i,'Rec Ene24'])
            if (explosion_temp.loc[i,'Fal Ene24']>0) & (explosion_temp.loc[i,'OC tempene']>0):
                explosion_temp.loc[i,'OC NUEVAENE'] = explosion_temp.loc[i,'OC tempene']
            else:
                explosion_temp.loc[i, 'OC NUEVAENE'] = 0
        explosion_temp['TOTAL OC_ENE'] = explosion_temp['Rec Ene24'] + explosion_temp['OC NUEVAENE']
        explosion_temp['INV_FEB'] = (explosion_temp['Cantidad Ene24'] - explosion_temp['INV_ENE']) - explosion_temp['TOTAL OC_ENE']
        explosion_temp['INV_FEB'][(explosion_temp['INV_FEB'] >0)] = 0
        explosion_temp['INV_FEB'][(explosion_temp['INV_FEB'] <0)] = (-1)*explosion_temp['INV_FEB']
        ##################################################################################################################################

        #################################MES FEB################################################################################
        explosion_temp['Fal Feb24'] = explosion_temp['Cantidad Feb24'] - explosion_temp['INV_FEB']
        explosion_temp['Fal Feb24'][(explosion_temp['Fal Feb24']<0)] = 0
        for i in range(len(explosion_temp['SKU'])):
            if explosion_temp.loc[i, 'MOQ'] != 0:
                explosion_temp.loc[i, 'divfeb'] = math.ceil(explosion_temp.loc[i,'Fal Feb24'] / explosion_temp.loc[i,'MOQ'])
            else:
                explosion_temp.loc[i, 'divfeb'] = 0        
            explosion_temp.loc[i,'OC tempfeb'] = (explosion_temp.loc[i,'divfeb'])*(explosion_temp.loc[i,'MOQ'])-(explosion_temp.loc[i,'Rec Feb24'])
            if (explosion_temp.loc[i,'Fal Feb24']>0) & (explosion_temp.loc[i,'OC tempfeb']>0):
                explosion_temp.loc[i,'OC NUEVAFEB'] = explosion_temp.loc[i,'OC tempfeb']
            else:
                explosion_temp.loc[i, 'OC NUEVAFEB'] = 0
        explosion_temp['TOTAL OC_FEB'] = explosion_temp['Rec Feb24'] + explosion_temp['OC NUEVAFEB']
        explosion_temp['INV_FEB'] = (explosion_temp['Cantidad Ene24'] - explosion_temp['INV_ENE']) - explosion_temp['TOTAL OC_ENE']
        explosion_temp['INV_FEB'][(explosion_temp['INV_FEB'] >0)] = 0
        explosion_temp['INV_FEB'][(explosion_temp['INV_FEB'] <0)] = (-1)*explosion_temp['INV_FEB']
        ##################################################################################################################################
        
        explosion_temp = explosion_temp[['SKU', 'MP_x', 'PROVEEDOR', 'DÍAS CRED', 'MP/ME', 'MOQ', 'Moneda', 'Costo', 'Existencia',
                                         'Cantidad', 'Faltante mp', 'Rec Sep23', 'OC NUEVA', 'TOTAL OC', 'Ingreso', 
                                         'INV_OCT', 'Cantidad Oct23', 'Fal Oct23', 'Rec Oct23', 'OC NUEVAOCT', 'TOTAL OC_OCT', 
                                         'INV_NOV', 'Cantidad Nov23', 'Fal Nov23', 'Rec Nov23', 'OC NUEVANOV', 'TOTAL OC_NOV',
                                         'INV_DIC', 'Cantidad Dic23', 'Fal Dic23', 'Rec Dic23', 'OC NUEVADIC', 'TOTAL OC_DIC',
                                         'INV_ENE', 'Cantidad Ene24', 'Fal Ene24', 'Rec Ene24', 'OC NUEVAENE', 'TOTAL OC_ENE',
                                         'INV_FEB', 'Cantidad Feb24', 'Fal Feb24', 'Rec Feb24', 'OC NUEVAFEB', 'TOTAL OC_FEB']]
        explosion_temp.columns = ['SKU', 'MP', 'PROVEEDOR', 'DIAS CRED', 'MP/ME', 'MOQ', 'Moneda', 'Costo', 'Existencia',
                                  'REQ_SEP', 'B.O. SEP', 'OC TRANSIT SEP', 'OC NUEVA SEP', 'TOTAL OC SEP', 'INGRESO A1',
                                  'INV_OCT', 'REQ_OCT', 'B.O. OCT', 'OC TRANSIT OCT', 'OC NUEVAOCT', 'TOTAL OC_OCT',
                                  'INV_NOV', 'REQ_NOV', 'B.O. NOV', 'OC TRANSIT NOV', 'OC NUEVANOV', 'TOTAL OC_NOV',
                                  'INV_DIC', 'REQ_DIC', 'B.O. DIC', 'OC TRANSIT DIC', 'OC NUEVADIC', 'TOTAL OC_DIC',
                                  'INV_ENE', 'REQ_ENE', 'B.O. ENE', 'OC TRANSIT ENE', 'OC NUEVAENE', 'TOTAL OC_ENE',
                                  'INV_FEB', 'REQ_FEB', 'B.O. FEB', 'OC TRANSIT FEB', 'OC NUEVAFEB', 'TOTAL OC_FEB' ]
            
        st.write(explosion_temp)
        st.download_button(label="Descargar", data=explosion_temp.to_csv(), mime="text/csv")
        st.info(frase, icon='💵')

    
        
    #st.balloons()
    
    #st.write(requi2)

if __name__ == '__main__':
    main()
