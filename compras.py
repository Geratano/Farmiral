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
    existencias['Cve_prod'] = existencias['Cve_prod'].str.strip()
    existencias['Desc_prod'] = existencias['Desc_prod'].str.strip()
    #st.write(existencias)
    df_formulas.columns = df_formulas.columns.str.strip()
    df_formulas['Cve_copr'] = df_formulas['Cve_copr'].str.strip()
    df_formulas['Cve_prod'] = df_formulas['Cve_prod'].str.strip()
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
    fcst_victor.columns = ['Codigo', 'Producto', 'Unidad', 'Lote', 'dic23', 'ene24', 'feb24', 'mar24', 'abr24', 'may24', 'Almacen']
    fcst_victor = fcst_victor.fillna(0)
    fcst_victor2 = fcst_victor.copy()
    fcst_victor2['Forecast anual'] = (fcst_victor2['dic23'] + fcst_victor2['ene24'] + fcst_victor2['feb24'] + fcst_victor2['mar24'] + fcst_victor2['abr24'] + fcst_victor2['may24'])
    
    #fcst_victor2 = fcst_victor2.groupby(['Codigo','Producto']).agg({'Forecast anual':'sum'}).reset_index()
    #st.write(fcst_victor2)
    ##########
    df_existencias = existencias[['Cve_prod', 'Lote', 'Lugar', 'Cto_ent', 'Existencia', 'Fech_venc', 'Desc_prod', 'Uni_med']]
    df_existencias.columns = ['SKU', 'Lote', 'Lugar', 'Costo', 'Existencia', 'Vencimiento', 'Producto', 'Unidad']
    df_existencias_ot = existencias[['Cve_prod', 'Lote', 'Lugar', 'Cto_ent', 'Existencia', 'Fech_venc', 'Desc_prod', 'Uni_med']]
    df_existencias_ot.columns = ['SKU', 'Lote', 'Lugar', 'Costo', 'Existencia', 'Vencimiento', 'Producto', 'Unidad']

    #df_existencias['Lugar'] = df_existencias['Lugar'].str.strip()
    ###############ALMACENES DIFERENCIADOS##########################################################################################
    df_existencias = df_existencias[(df_existencias['Lugar']=='5') | (df_existencias['Lugar']=='4')]
    #st.write(df_existencias) 
    df_existencias2 = df_existencias_ot[(df_existencias_ot['Lugar']=='A1') | (df_existencias_ot['Lugar']=='A2') | (df_existencias_ot['Lugar']=='A3')]
    #st.write(df_existencias2)
    df_existenciasaspen = df_existencias_ot[(df_existencias_ot['Lugar']=='ASPEN')]
    df_existenciasgrisi = df_existencias_ot[(df_existencias_ot['Lugar']=='G1')|(df_existencias_ot['Lugar']=='G2')]
    df_existenciassimi = df_existencias_ot[(df_existencias_ot['Lugar']=='SIMILARES')]
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
    #st.write(existe)
    existemp = df_existencias2.groupby(['Producto', 'SKU']).agg({'Existencia':'sum'}).reset_index()
    #forecast = forecast.fillna(0)
    #forecast = forecast[forecast['Cve_prod'] != 0]
    existe['SKU'] = existe['SKU'].str.strip()
    #forecast['SKU'] = forecast['Cve_prod'].str.strip()
    #forecast = forecast[['SKU', 'Producto', 'Forecast']]
    fcst_victor2['SKU'] = fcst_victor2['Codigo'].str.strip()
    fcst_victor2 = fcst_victor2[['SKU', 'Producto', 'dic23', 'ene24', 'feb24', 'mar24', 'abr24', 'may24', 'Forecast anual', 'Almacen']]
    fcst_comp = fcst_victor2.copy()
    #st.write(fcst_comp)
    ################################FORECAST GENERAL########################################################################
    forecast = fcst_comp[['SKU', 'Producto', 'dic23', 'ene24', 'feb24', 'mar24', 'abr24', 'may24', 'Forecast anual', 'Almacen']]
    forecast.columns = ['SKU', 'Producto', 'dic23', 'ene24', 'feb24', 'mar24', 'abr24', 'may24', 'Forecast anual', 'Almacen']
    forecast['SKU'] = forecast['SKU'].str.strip()
    #st.write(forecast)
    ####################################################################################################################

    ###Pegamos la existencia del producto terminado para obtener los faltantes generales de PT
    t_existe = existe.fillna(0)
    t_existemp = existemp.fillna(0)

    t_existe = t_existe[['SKU', 'Producto', 'Existencia']]
    #st.write(t_existe)
    t_existemp = t_existemp[['SKU', 'Producto', 'Existencia']]
    #st.write(forecast)
    t_existe['SKU'] = t_existe['SKU'].str.strip()
    forecast['SKU'] = forecast['SKU'].str.strip()
    t_forecast = forecast.merge(t_existe, on='SKU', how='left').fillna(0)
    #st.write(t_forecast)
    t_forecast['Producto'] = t_forecast['Producto_x']


    for i in range(len(t_forecast['Producto'])):
        if t_forecast.loc[i,'Producto_x']==0:
            t_forecast.loc[i,'Producto'] = t_forecast.loc[i,'Producto_y']
            #t_forecast.loc[i,'Forecast'] = str(t_forecast.loc[i,'Forecast']).strip().replace('-','0')

    t_forecast = t_forecast[['SKU', 'Producto','dic23', 'ene24', 'feb24', 'mar24', 'abr24', 'may24', 'Forecast anual', 'Existencia', 'Almacen']]
    ###CAMBIO POR MES#######
    t_forecast['Faltantes'] = t_forecast['dic23'] - t_forecast['Existencia']
    #t_forecast['Faltantes'] = t_forecast['ene24'] - t_forecast['Existencia']
    #t_forecast['Faltantes'] = t_forecast['feb24'] - t_forecast['Existencia']
    ####SE CAMBIO ESTA LINEA TAMBIEN PARA INTEGRAR TODO EL FORECAST#########
    #t_forecast = t_forecast[t_forecast['Faltantes'] != 0]
    #st.write(t_forecast)
    #Forecast faltantes Completo
    fcst_faltantes = t_forecast[['SKU', 'Producto','dic23', 'ene24', 'feb24', 'mar24', 'abr24', 'may24', 'Forecast anual', 'Faltantes', 'Existencia', 'Almacen']]
    #####SE CAMBIO ESTA LINEA PARA INTEGRAR TODO EL FORECAST AUNQUE SE TENGA EXISTENCIA###########3
    #st.write(len(fcst_faltantes['Faltantes']))
    fcst_faltantes['Faltantes'][fcst_faltantes['Faltantes'] <= 0] = 0
    #for i in range(len(fcst_faltantes['Faltantes'])):
    #    if fcst_faltantes.loc[i,'Faltantes'] <= 0:
    #        fcst_faltantes.loc[i,'Faltantes'] ==0

    #fcst_faltantes[[fcst_faltantes['Faltantes']] <= 0 ] = 0 
    #fcst_faltantes = fcst_faltantes[fcst_faltantes['Faltantes']>0]
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
    
    #####MODIFICAR POR MES#######################
    pedir_fcstme['Faltantes me'] = pedir_fcstme['Faltantes'] * pedir_fcstme['Cantidad']
    #pedir_fcstme['Faltantes me'] = 0 * pedir_fcstme['Cantidad']    
    #pedir_fcstme['Faltantes me ene24'] = pedir_fcstme['Faltantes'] * pedir_fcstme['Cantidad']
    #pedir_fcstme['Faltantes me feb24'] = pedir_fcstme['feb24'] * pedir_fcstme['Cantidad']
    pedir_fcstme['Faltantes me ene24'] = pedir_fcstme['ene24'] * pedir_fcstme['Cantidad']
    pedir_fcstme['Faltantes me feb24'] = pedir_fcstme['feb24'] * pedir_fcstme['Cantidad']
    pedir_fcstme['Faltantes me mar24'] = pedir_fcstme['mar24'] * pedir_fcstme['Cantidad']
    pedir_fcstme['Faltantes me abr24'] = pedir_fcstme['abr24'] * pedir_fcstme['Cantidad']
    pedir_fcstme['Faltantes me may24'] = pedir_fcstme['may24'] * pedir_fcstme['Cantidad']
    #st.write(pedir_fcstme)
    pedir_fcstst = pedir_fcst[pedir_fcst['Cve_prod'].str.startswith('41')].reset_index(drop=True)
    pedir_fcstst.rename(columns = {'SKU':'SKU_f', 'Cve_prod':'SKU'}, inplace=True)
    pedir_fcstst['SKU'] = pedir_fcstst['SKU'].str.strip()
    pedir_fcstst = pedir_fcstst.merge(formulas, on='SKU', how='left')
    #st.write(pedir_fcstst)
    #Cantidad por pieza
    pedir_fcstst['Cantidad_y'] = pedir_fcstst['Cantidad rendimiento_y'] / pedir_fcstst['Rendimiento_x']
    ##########CAMBIO MES ################################################
    pedir_fcstst['Cantidad mp'] = pedir_fcstst['Cantidad_y'] * pedir_fcstst['Faltantes']
    #pedir_fcstst['Cantidad mp'] = pedir_fcstst['Cantidad_y'] * 0
    #st.write(pedir_fcstst)
    #pedir_fcstst['Cantidad mp ene24'] = pedir_fcstst['Cantidad_y'] * pedir_fcstst['Faltantes']
    #pedir_fcstst['Cantidad mp feb24'] = pedir_fcstst['Cantidad_y'] * pedir_fcstst['feb24']
    pedir_fcstst['Cantidad mp ene24'] = pedir_fcstst['Cantidad_y'] * pedir_fcstst['ene24']
    pedir_fcstst['Cantidad mp feb24'] = pedir_fcstst['Cantidad_y'] * pedir_fcstst['feb24']
    pedir_fcstst['Cantidad mp mar24'] = pedir_fcstst['Cantidad_y'] * pedir_fcstst['mar24']
    pedir_fcstst['Cantidad mp abr24'] = pedir_fcstst['Cantidad_y'] * pedir_fcstst['abr24']
    pedir_fcstst['Cantidad mp may24'] = pedir_fcstst['Cantidad_y'] * pedir_fcstst['may24']
    #st.write(pedir_fcstst)
    pedir_fcstst = pedir_fcstst[['Producto_x', 'Faltantes', 'MP_y', 'Cantidad mp', 'dic23', 'Cantidad mp ene24', 'Cantidad mp feb24', 'Cantidad mp mar24', 'Cantidad mp abr24', 'Cantidad mp may24', 'Forecast anual']]
    pedir_fcstst.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'dic23', 'Cantidad ene24', 'Cantidad feb24', 'Cantidad mar24', 'Cantidad abr24', 'Cantidad may24', 'Forecast anual']
    #st.write(pedir_fcstst)
    pedir_fcstme = pedir_fcstme[['Producto_x', 'Faltantes', 'MP', 'Faltantes me', 'dic23', 'Faltantes me ene24', 'Faltantes me feb24', 'Faltantes me mar24', 'Faltantes me abr24', 'Faltantes me may24', 'Forecast anual']]
    pedir_fcstme.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'dic23', 'Cantidad ene24', 'Cantidad feb24', 'Cantidad mar24', 'Cantidad abr24', 'Cantidad may24', 'Forecast anual']
    #st.write(pedir_fcstme)
    pedir2 = pd.concat([pedir_fcstst, pedir_fcstme])
    #st.write(pedir2)
    pedir2['MP'] = pedir2['MP'].str.strip()
    prods = productos[['Cve_prod', 'Desc_prod']]
    prods.columns = ['SKU', 'MP']
    pedir2 = pedir2.merge(prods, on='MP', how='left')
    #st.write(pedir2)
    #Columnas a pegar en la explosión
    pedir2t = pedir2.groupby(['SKU']).agg({'Cantidad ene24':'sum',
                                  'Cantidad feb24':'sum',
                                  'Cantidad mar24':'sum',
                                  'Cantidad abr24':'sum',
                                  'Cantidad may24':'sum'}).reset_index()
    #st.write(pedir2t)
    ######################################################################################################
    ####################PEDIR A1-A3#####################################################
    pedir_fcsta = fcst_faltantesa.merge(formulas, on='SKU', how='left')
    #st.write(pedir_fcst)
    pedir_fcsta = pedir_fcsta.dropna()
    #st.write(pedir_fcst)
    pedir_fcstmea = pedir_fcsta[pedir_fcsta['Cve_prod'].str.startswith('M')].reset_index(drop=True)
    ##############CAMBIO MES################################################
    pedir_fcstmea['Faltantes me'] = pedir_fcstmea['Faltantes'] * pedir_fcstmea['Cantidad']
    #pedir_fcstmea['Faltantes me'] = 0 * pedir_fcstmea['Cantidad']
    #pedir_fcstmea['Faltantes me ene24'] = pedir_fcstmea['Faltantes'] * pedir_fcstmea['Cantidad']
    #pedir_fcstmea['Faltantes me feb24'] = pedir_fcstmea['feb24'] * pedir_fcstmea['Cantidad']
    pedir_fcstmea['Faltantes me ene24'] = pedir_fcstmea['ene24'] * pedir_fcstmea['Cantidad']
    pedir_fcstmea['Faltantes me feb24'] = pedir_fcstmea['feb24'] * pedir_fcstmea['Cantidad']
    pedir_fcstmea['Faltantes me mar24'] = pedir_fcstmea['mar24'] * pedir_fcstmea['Cantidad']
    pedir_fcstmea['Faltantes me abr24'] = pedir_fcstmea['abr24'] * pedir_fcstmea['Cantidad']
    pedir_fcstmea['Faltantes me may24'] = pedir_fcstmea['may24'] * pedir_fcstmea['Cantidad']
    #st.write(pedir_fcstmea)
    pedir_fcststa = pedir_fcsta[pedir_fcsta['Cve_prod'].str.startswith('41')].reset_index(drop=True)
    pedir_fcststa.rename(columns = {'SKU':'SKU_f', 'Cve_prod':'SKU'}, inplace=True)
    pedir_fcststa['SKU'] = pedir_fcststa['SKU'].str.strip()
    pedir_fcststa = pedir_fcststa.merge(formulas, on='SKU', how='left')
    pedir_fcststa['Cantidad_y'] = pedir_fcststa['Cantidad rendimiento_y'] / pedir_fcststa['Rendimiento_x']
    
    ###############CAMBIO MES###################################
    pedir_fcststa['Cantidad mp'] = pedir_fcststa['Cantidad_y'] * pedir_fcststa['Faltantes']
    #pedir_fcststa['Cantidad mp'] = pedir_fcststa['Cantidad_y'] * 0
    #pedir_fcststa['Cantidad mp ene24'] = pedir_fcststa['Cantidad_y'] * pedir_fcststa['Faltantes']
    #pedir_fcststa['Cantidad mp feb24'] = pedir_fcststa['Cantidad_y'] * pedir_fcststa['feb24']
    pedir_fcststa['Cantidad mp ene24'] = pedir_fcststa['Cantidad_y'] * pedir_fcststa['ene24']
    pedir_fcststa['Cantidad mp feb24'] = pedir_fcststa['Cantidad_y'] * pedir_fcststa['feb24']
    pedir_fcststa['Cantidad mp mar24'] = pedir_fcststa['Cantidad_y'] * pedir_fcststa['mar24']
    pedir_fcststa['Cantidad mp abr24'] = pedir_fcststa['Cantidad_y'] * pedir_fcststa['abr24']
    pedir_fcststa['Cantidad mp may24'] = pedir_fcststa['Cantidad_y'] * pedir_fcststa['may24']
    pedir_fcststa = pedir_fcststa[['Producto_x', 'Faltantes', 'MP_y', 'Cantidad mp', 'dic23', 'Cantidad mp ene24', 'Cantidad mp feb24', 'Cantidad mp mar24', 'Cantidad mp abr24', 'Cantidad mp may24', 'Forecast anual']]
    pedir_fcststa.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'dic23', 'Cantidad ene24', 'Cantidad feb24', 'Cantidad mar24', 'Cantidad abr24', 'Cantidad may24', 'Forecast anual']
    #st.write(pedir_fcstst)
    pedir_fcstmea = pedir_fcstmea[['Producto_x', 'Faltantes', 'MP', 'Faltantes me', 'dic23', 'Faltantes me ene24', 'Faltantes me feb24', 'Faltantes me mar24', 'Faltantes me abr24', 'Faltantes me may24', 'Forecast anual']]
    pedir_fcstmea.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'dic23', 'Cantidad ene24', 'Cantidad feb24', 'Cantidad mar24', 'Cantidad abr24', 'Cantidad may24', 'Forecast anual']
    #st.write(pedir_fcstme)
    pedir2a = pd.concat([pedir_fcststa, pedir_fcstmea])
    #st.write(pedir2a)
    pedir2a['MP'] = pedir2a['MP'].str.strip()
    prods = productos[['Cve_prod', 'Desc_prod']]
    prods.columns = ['SKU', 'MP']
    pedir2a = pedir2a.merge(prods, on='MP', how='left')
    #Columnas a pegar en la explosión
    pedir2ta = pedir2a.groupby(['SKU']).agg({'Cantidad ene24':'sum',
                                  'Cantidad feb24':'sum',
                                  'Cantidad mar24':'sum',
                                  'Cantidad abr24':'sum',
                                  'Cantidad may24':'sum'}).reset_index()
    #st.write(pedir2a)
    ######################################################################################################
    ####################PEDIR ASPEN#####################################################
    pedir_fcstaspen = fcst_faltantesaspen.merge(formulas, on='SKU', how='left')
    #st.write(pedir_fcst)
    pedir_fcstaspen = pedir_fcstaspen.dropna()
    #st.write(pedir_fcst)
    pedir_fcstmeaspen = pedir_fcstaspen[pedir_fcstaspen['Cve_prod'].str.startswith('M')].reset_index(drop=True)
    
    #####################CAMBIO MES##################################
    pedir_fcstmeaspen['Faltantes me'] = pedir_fcstmeaspen['Faltantes'] * pedir_fcstmeaspen['Cantidad']
    #pedir_fcstmeaspen['Faltantes me'] = 0 * pedir_fcstmeaspen['Cantidad']
    #pedir_fcstmeaspen['Faltantes me ene24'] = pedir_fcstmeaspen['Faltantes'] * pedir_fcstmeaspen['Cantidad']
    #pedir_fcstmeaspen['Faltantes me feb24'] = pedir_fcstmeaspen['feb24'] * pedir_fcstmeaspen['Cantidad']
    pedir_fcstmeaspen['Faltantes me ene24'] = pedir_fcstmeaspen['ene24'] * pedir_fcstmeaspen['Cantidad']
    pedir_fcstmeaspen['Faltantes me feb24'] = pedir_fcstmeaspen['feb24'] * pedir_fcstmeaspen['Cantidad']
    pedir_fcstmeaspen['Faltantes me mar24'] = pedir_fcstmeaspen['mar24'] * pedir_fcstmeaspen['Cantidad']
    pedir_fcstmeaspen['Faltantes me abr24'] = pedir_fcstmeaspen['abr24'] * pedir_fcstmeaspen['Cantidad']
    pedir_fcstmeaspen['Faltantes me may24'] = pedir_fcstmeaspen['may24'] * pedir_fcstmeaspen['Cantidad']
    #st.write(pedir_fcstmea)
    pedir_fcststaspen = pedir_fcstaspen[pedir_fcstaspen['Cve_prod'].str.startswith('41')].reset_index(drop=True)
    pedir_fcststaspen.rename(columns = {'SKU':'SKU_f', 'Cve_prod':'SKU'}, inplace=True)
    pedir_fcststaspen['SKU'] = pedir_fcststaspen['SKU'].str.strip()
    pedir_fcststaspen = pedir_fcststaspen.merge(formulas, on='SKU', how='left')
    pedir_fcststaspen['Cantidad_y'] = pedir_fcststaspen['Cantidad rendimiento_y'] / pedir_fcststaspen['Rendimiento_x']
    
    ####################CAMBIO MES##################################################
    pedir_fcststaspen['Cantidad mp'] = pedir_fcststaspen['Cantidad_y'] * pedir_fcststaspen['Faltantes']
    #pedir_fcststaspen['Cantidad mp'] = pedir_fcststaspen['Cantidad_y'] * 0
    #pedir_fcststaspen['Cantidad mp ene24'] = pedir_fcststaspen['Cantidad_y'] * pedir_fcststaspen['Faltantes']
    #pedir_fcststaspen['Cantidad mp feb24'] = pedir_fcststaspen['Cantidad_y'] * pedir_fcststaspen['feb24']
    pedir_fcststaspen['Cantidad mp ene24'] = pedir_fcststaspen['Cantidad_y'] * pedir_fcststaspen['ene24']
    pedir_fcststaspen['Cantidad mp feb24'] = pedir_fcststaspen['Cantidad_y'] * pedir_fcststaspen['feb24']
    pedir_fcststaspen['Cantidad mp mar24'] = pedir_fcststaspen['Cantidad_y'] * pedir_fcststaspen['mar24']
    pedir_fcststaspen['Cantidad mp abr24'] = pedir_fcststaspen['Cantidad_y'] * pedir_fcststaspen['abr24']
    pedir_fcststaspen['Cantidad mp may24'] = pedir_fcststaspen['Cantidad_y'] * pedir_fcststaspen['may24']
    pedir_fcststaspen = pedir_fcststaspen[['Producto_x', 'Faltantes', 'MP_y', 'Cantidad mp', 'dic23', 'Cantidad mp ene24', 'Cantidad mp feb24', 'Cantidad mp mar24', 'Cantidad mp abr24', 'Cantidad mp may24', 'Forecast anual']]
    pedir_fcststaspen.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'dic23', 'Cantidad ene24', 'Cantidad feb24', 'Cantidad mar24', 'Cantidad abr24', 'Cantidad may24', 'Forecast anual']
    #st.write(pedir_fcstst)
    pedir_fcstmeaspen = pedir_fcstmeaspen[['Producto_x', 'Faltantes', 'MP', 'Faltantes me', 'dic23', 'Faltantes me ene24', 'Faltantes me feb24', 'Faltantes me mar24', 'Faltantes me abr24', 'Faltantes me may24', 'Forecast anual']]
    pedir_fcstmeaspen.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'dic23', 'Cantidad ene24', 'Cantidad feb24', 'Cantidad mar24', 'Cantidad abr24', 'Cantidad may24', 'Forecast anual']
    #st.write(pedir_fcstme)
    pedir2aspen = pd.concat([pedir_fcststaspen, pedir_fcstmeaspen])
    #st.write(pedir2a)
    pedir2aspen['MP'] = pedir2aspen['MP'].str.strip()
    prods = productos[['Cve_prod', 'Desc_prod']]
    prods.columns = ['SKU', 'MP']
    pedir2aspen = pedir2aspen.merge(prods, on='MP', how='left')
    #Columnas a pegar en la explosión
    pedir2taspen = pedir2aspen.groupby(['SKU']).agg({'Cantidad ene24':'sum',
                                  'Cantidad feb24':'sum',
                                  'Cantidad mar24':'sum',
                                  'Cantidad abr24':'sum',
                                  'Cantidad may24':'sum'}).reset_index()
    ######################################################################################################
    ####################PEDIR SIMILARES#####################################################
    pedir_fcstsimi = fcst_faltantessimi.merge(formulas, on='SKU', how='left')
    #st.write(pedir_fcst)
    pedir_fcstsimi = pedir_fcstsimi.dropna()
    #st.write(pedir_fcst)
    pedir_fcstmesimi = pedir_fcstsimi[pedir_fcstsimi['Cve_prod'].str.startswith('M')].reset_index(drop=True)

    ##################CAMBIO MES################################################
    pedir_fcstmesimi['Faltantes me'] = pedir_fcstmesimi['Faltantes'] * pedir_fcstmesimi['Cantidad']
    #pedir_fcstmesimi['Faltantes me'] = 0 * pedir_fcstmesimi['Cantidad']
    #pedir_fcstmesimi['Faltantes me ene24'] = pedir_fcstmesimi['Faltantes'] * pedir_fcstmesimi['Cantidad']
    #pedir_fcstmesimi['Faltantes me feb24'] = pedir_fcstmesimi['feb24'] * pedir_fcstmesimi['Cantidad']
    pedir_fcstmesimi['Faltantes me ene24'] = pedir_fcstmesimi['ene24'] * pedir_fcstmesimi['Cantidad']
    pedir_fcstmesimi['Faltantes me feb24'] = pedir_fcstmesimi['feb24'] * pedir_fcstmesimi['Cantidad']
    pedir_fcstmesimi['Faltantes me mar24'] = pedir_fcstmesimi['mar24'] * pedir_fcstmesimi['Cantidad']
    pedir_fcstmesimi['Faltantes me abr24'] = pedir_fcstmesimi['abr24'] * pedir_fcstmesimi['Cantidad']
    pedir_fcstmesimi['Faltantes me may24'] = pedir_fcstmesimi['may24'] * pedir_fcstmesimi['Cantidad']
    #st.write(pedir_fcstmea)
    pedir_fcststsimi = pedir_fcstsimi[pedir_fcstsimi['Cve_prod'].str.startswith('41')].reset_index(drop=True)
    pedir_fcststsimi.rename(columns = {'SKU':'SKU_f', 'Cve_prod':'SKU'}, inplace=True)
    pedir_fcststsimi['SKU'] = pedir_fcststsimi['SKU'].str.strip()
    pedir_fcststsimi = pedir_fcststsimi.merge(formulas, on='SKU', how='left')
    pedir_fcststsimi['Cantidad_y'] = pedir_fcststsimi['Cantidad rendimiento_y'] / pedir_fcststsimi['Rendimiento_x']
    
    ###################CAMBIO MES#################################################
    pedir_fcststsimi['Cantidad mp'] = pedir_fcststsimi['Cantidad_y'] * pedir_fcststsimi['Faltantes']
    #pedir_fcststsimi['Cantidad mp'] = pedir_fcststsimi['Cantidad_y'] * 0
    #pedir_fcststsimi['Cantidad mp ene24'] = pedir_fcststsimi['Cantidad_y'] * pedir_fcststsimi['Faltantes']
    #pedir_fcststsimi['Cantidad mp feb24'] = pedir_fcststsimi['Cantidad_y'] * pedir_fcststsimi['feb24']
    pedir_fcststsimi['Cantidad mp ene24'] = pedir_fcststsimi['Cantidad_y'] * pedir_fcststsimi['ene24']
    pedir_fcststsimi['Cantidad mp feb24'] = pedir_fcststsimi['Cantidad_y'] * pedir_fcststsimi['feb24']
    pedir_fcststsimi['Cantidad mp mar24'] = pedir_fcststsimi['Cantidad_y'] * pedir_fcststsimi['mar24']
    pedir_fcststsimi['Cantidad mp abr24'] = pedir_fcststsimi['Cantidad_y'] * pedir_fcststsimi['abr24']
    pedir_fcststsimi['Cantidad mp may24'] = pedir_fcststsimi['Cantidad_y'] * pedir_fcststsimi['may24']
    #st.write(pedir_fcststsimi)
    pedir_fcststsimi = pedir_fcststsimi[['Producto_x', 'Faltantes', 'MP_y', 'Cantidad mp', 'dic23', 'Cantidad mp ene24', 'Cantidad mp feb24', 'Cantidad mp mar24', 'Cantidad mp abr24', 'Cantidad mp may24', 'Forecast anual']]
    pedir_fcststsimi.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'dic23', 'Cantidad ene24', 'Cantidad feb24', 'Cantidad mar24', 'Cantidad abr24', 'Cantidad may24', 'Forecast anual']
    #st.write(pedir_fcstst)
    pedir_fcstmesimi = pedir_fcstmesimi[['Producto_x', 'Faltantes', 'MP', 'Faltantes me', 'dic23', 'Faltantes me ene24', 'Faltantes me feb24', 'Faltantes me mar24', 'Faltantes me abr24', 'Faltantes me may24', 'Forecast anual']]
    pedir_fcstmesimi.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'dic23', 'Cantidad ene24', 'Cantidad feb24', 'Cantidad mar24', 'Cantidad abr24', 'Cantidad may24', 'Forecast anual']
    #st.write(pedir_fcstme)
    pedir2simi = pd.concat([pedir_fcststsimi, pedir_fcstmesimi])
    #st.write(pedir2a)
    pedir2simi['MP'] = pedir2simi['MP'].str.strip()
    prods = productos[['Cve_prod', 'Desc_prod']]
    prods.columns = ['SKU', 'MP']
    pedir2simi = pedir2simi.merge(prods, on='MP', how='left')
    #Columnas a pegar en la explosión
    pedir2tsimi = pedir2simi.groupby(['SKU']).agg({'Cantidad ene24':'sum',
                                  'Cantidad feb24':'sum',
                                  'Cantidad mar24':'sum',
                                  'Cantidad abr24':'sum',
                                  'Cantidad may24':'sum'}).reset_index()
    ######################################################################################################
    ####################PEDIR GRISI#####################################################
    pedir_fcstgrisi = fcst_faltantesgrisi.merge(formulas, on='SKU', how='left')
    #st.write(pedir_fcstgrisi)
    pedir_fcstgrisi = pedir_fcstgrisi.dropna()
    #st.write(pedir_fcst)
    pedir_fcstmegrisi = pedir_fcstgrisi[pedir_fcstgrisi['Cve_prod'].str.startswith('M')].reset_index(drop=True)
    
    ####################CAMBIO MES###########################################
    pedir_fcstmegrisi['Faltantes me'] = pedir_fcstmegrisi['Faltantes'] * pedir_fcstmegrisi['Cantidad']
    #pedir_fcstmegrisi['Faltantes me'] = 0 * pedir_fcstmegrisi['Cantidad']
    #pedir_fcstmegrisi['Faltantes me ene24'] = pedir_fcstmegrisi['Faltantes'] * pedir_fcstmegrisi['Cantidad']
    #pedir_fcstmegrisi['Faltantes me feb24'] = pedir_fcstmegrisi['feb24'] * pedir_fcstmegrisi['Cantidad']
    pedir_fcstmegrisi['Faltantes me ene24'] = pedir_fcstmegrisi['ene24'] * pedir_fcstmegrisi['Cantidad']
    pedir_fcstmegrisi['Faltantes me feb24'] = pedir_fcstmegrisi['feb24'] * pedir_fcstmegrisi['Cantidad']
    pedir_fcstmegrisi['Faltantes me mar24'] = pedir_fcstmegrisi['mar24'] * pedir_fcstmegrisi['Cantidad']
    pedir_fcstmegrisi['Faltantes me abr24'] = pedir_fcstmegrisi['abr24'] * pedir_fcstmegrisi['Cantidad']
    pedir_fcstmegrisi['Faltantes me may24'] = pedir_fcstmegrisi['may24'] * pedir_fcstmegrisi['Cantidad']
    #st.write(pedir_fcstmea)
    pedir_fcststgrisi = pedir_fcstgrisi[pedir_fcstgrisi['Cve_prod'].str.startswith('41')].reset_index(drop=True)
    pedir_fcststgrisi.rename(columns = {'SKU':'SKU_f', 'Cve_prod':'SKU'}, inplace=True)
    pedir_fcststgrisi['SKU'] = pedir_fcststgrisi['SKU'].str.strip()
    pedir_fcststgrisi = pedir_fcststgrisi.merge(formulas, on='SKU', how='left')
    pedir_fcststgrisi['Cantidad_y'] = pedir_fcststgrisi['Cantidad rendimiento_y'] / pedir_fcststgrisi['Rendimiento_x']
    
    #################CAMBIO MES########################################
    pedir_fcststgrisi['Cantidad mp'] = pedir_fcststgrisi['Cantidad_y'] * pedir_fcststgrisi['Faltantes']
    #pedir_fcststgrisi['Cantidad mp'] = pedir_fcststgrisi['Cantidad_y'] * 0
    #pedir_fcststgrisi['Cantidad mp ene24'] = pedir_fcststgrisi['Cantidad_y'] * pedir_fcststgrisi['Faltantes']
    #pedir_fcststgrisi['Cantidad mp feb24'] = pedir_fcststgrisi['Cantidad_y'] * pedir_fcststgrisi['feb24']
    pedir_fcststgrisi['Cantidad mp ene24'] = pedir_fcststgrisi['Cantidad_y'] * pedir_fcststgrisi['ene24']
    pedir_fcststgrisi['Cantidad mp feb24'] = pedir_fcststgrisi['Cantidad_y'] * pedir_fcststgrisi['feb24']
    pedir_fcststgrisi['Cantidad mp mar24'] = pedir_fcststgrisi['Cantidad_y'] * pedir_fcststgrisi['mar24']
    pedir_fcststgrisi['Cantidad mp abr24'] = pedir_fcststgrisi['Cantidad_y'] * pedir_fcststgrisi['abr24']
    pedir_fcststgrisi['Cantidad mp may24'] = pedir_fcststgrisi['Cantidad_y'] * pedir_fcststgrisi['may24']
    pedir_fcststgrisi = pedir_fcststgrisi[['Producto_x', 'Faltantes', 'MP_y', 'Cantidad mp', 'dic23', 'Cantidad mp ene24', 'Cantidad mp feb24', 'Cantidad mp mar24', 'Cantidad mp abr24', 'Cantidad mp may24', 'Forecast anual']]
    pedir_fcststgrisi.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'dic23', 'Cantidad ene24', 'Cantidad feb24', 'Cantidad mar24', 'Cantidad abr24', 'Cantidad may24', 'Forecast anual']
    #st.write(pedir_fcstst)
    pedir_fcstmegrisi = pedir_fcstmegrisi[['Producto_x', 'Faltantes', 'MP', 'Faltantes me', 'dic23', 'Faltantes me ene24', 'Faltantes me feb24', 'Faltantes me mar24', 'Faltantes me abr24', 'Faltantes me may24', 'Forecast anual']]
    pedir_fcstmegrisi.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'dic23', 'Cantidad ene24', 'Cantidad feb24', 'Cantidad mar24', 'Cantidad abr24', 'Cantidad may24', 'Forecast anual']
    #st.write(pedir_fcstme)
    pedir2grisi = pd.concat([pedir_fcststgrisi, pedir_fcstmegrisi])
    #st.write(pedir2a)
    pedir2grisi['MP'] = pedir2grisi['MP'].str.strip()
    prods = productos[['Cve_prod', 'Desc_prod']]
    prods.columns = ['SKU', 'MP']
    pedir2grisi = pedir2grisi.merge(prods, on='MP', how='left')
    #Columnas a pegar en la explosión
    pedir2tgrisi = pedir2grisi.groupby(['SKU']).agg({'Cantidad ene24':'sum',
                                  'Cantidad feb24':'sum',
                                  'Cantidad mar24':'sum',
                                  'Cantidad abr24':'sum',
                                  'Cantidad may24':'sum'}).reset_index()
    ######################################################################################################
    #############REQUI GENERAL##########################################################################
    pedir2 = pedir2.merge(existeN_comp, on='SKU', how='left')
    pedir2 = pedir2.fillna(0)
    #st.write(pedir2)
    ##############CAMBIO MES###########################
    pedir2['Faltante mp'] = pedir2['Cantidad'] - pedir2['Existencia']
    #pedir2['Faltante mp'] = pedir2['Cantidad ene24'] - pedir2['Existencia']
    #pedir2['Faltante mp'] = pedir2['Cantidad feb24'] - pedir2['Existencia']
    #st.write(pedir2)
    ###COSTO FOR
    costo_for = df_formulas[['Desc_prod', 'Cto_rep']]
    costo_for.columns = ['MP', 'Costo']
    costo_for =costo_for.groupby(['MP']).agg({'Costo':'mean'}).reset_index()
    costo_for['MP'] = costo_for['MP'].str.strip()
    ###
    pedir2['Faltante mp'][(pedir2['Faltante mp'] < 0)] = 0
    #st.write(pedir2)
    requi2 = pedir2.groupby(['MP']).agg({'Cantidad':'sum', 'Existencia':'max', 'Faltante mp':'sum'}).reset_index()
    #st.write(requi2)
    requi2 = requi2.merge(costo_for, on='MP', how='left')
    requi2['Costo total'] = requi2['Faltante mp'] * requi2['Costo']
    total_requi2 = requi2['Costo total'].sum()
    #st.write(total_requi2)
    ######################################################################################################
    #############REQUI A1-A3##########################################################################
    pedira = pedir2a.merge(existeN_a, on='SKU', how='left')
    pedira = pedira.fillna(0)
    #st.write(pedira)
    ###################CAMBIO MES#######################################
    pedira['Faltante mp'] = pedira['Cantidad'] - pedira['Existencia']
    #pedira['Faltante mp'] = pedira['Cantidad ene24'] - pedira['Existencia']
    #pedira['Faltante mp'] = pedira['Cantidad feb24'] - pedira['Existencia']
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
    #################CAMBIO MES###############################
    pediraspen['Faltante mp'] = pediraspen['Cantidad'] - pediraspen['Existencia']
    #pediraspen['Faltante mp'] = pediraspen['Cantidad ene24'] - pediraspen['Existencia']
    #pediraspen['Faltante mp'] = pediraspen['Cantidad feb24'] - pediraspen['Existencia']
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
    #################################CAMBIO MES#######################################
    pedirsimi['Faltante mp'] = pedirsimi['Cantidad'] - pedirsimi['Existencia']
    #pedirsimi['Faltante mp'] = pedirsimi['Cantidad ene24'] - pedirsimi['Existencia']
    #pedirsimi['Faltante mp'] = pedirsimi['Cantidad feb24'] - pedirsimi['Existencia']
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
    ##################################CAMBIO MES#############################################
    pedirgrisi['Faltante mp'] = pedirgrisi['Cantidad'] - pedirgrisi['Existencia']
    #pedirgrisi['Faltante mp'] = pedirgrisi['Cantidad ene24'] - pedirgrisi['Existencia']
    #pedirgrisi['Faltante mp'] = pedirgrisi['Cantidad feb24'] - pedirgrisi['Existencia']
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
    if st.checkbox('Explosion PT'):
        form_filter = formulas[formulas.SKU.str.startswith('51')].reset_index()
        cantidad_explosiones = st.number_input('Numero de formulas a explosionar', min_value=1, key=f'cantidad_explosion_{i}', step=1)
        formulas_selec = {}
        cantidades_selec = {}
        formulas_filtro = {}
        base_pt = {}
        base_me = {}
        base_st = {}
        bases_formulas = {}
        explosion_part = {}
        for i in range(cantidad_explosiones):
            nombres_formulas = f'formula_selec_{i}'
            cantidades_select = f'cantidades_select_{i}'
            form_filter2 = f'form_filter2_{i}'
            formula_pt = f'formula_pt_{i}'
            formula_me = f'formula_me_{i}'
            formula_st = f'formula_st_{i}'
            formulas_filter = f'formulas_filter_{i}'
            explosion_materiales = f'explosion_materiales_{i}'
            formulas_selec[nombres_formulas] = st.selectbox('Formula a explosionar', form_filter['Producto'].sort_values().unique(), key=f'formula_selec_{i}')
            cantidades_selec[cantidades_select] = st.number_input('Cantidad a explosionar', key=f'cantidades_select_{i}', step=1)
        for i in range(cantidad_explosiones):
            nombres_formulas = f'formula_selec_{i}'
            cantidades_select = f'cantidades_select_{i}'
            form_filter2 = f'form_filter2_{i}'
            formula_pt = f'formula_pt_{i}'
            formula_me = f'formula_me_{i}'
            formula_st = f'formula_st_{i}'
            formulas_filter = f'formulas_filter_{i}'
            explosion_materiales = f'explosion_materiales_{i}'
            bases_formulas[form_filter2] = form_filter[form_filter['Producto'] == formulas_selec.get(nombres_formulas)]
            #globals()[f'form_filter2_{i}'] = form_filter[form_filter['Producto'] == formulas_selec.get(nombres_formulas)]
        ####################PEDIR#####################################################
        #st.write(bases_formulas.get('form_filter2_1')[bases_formulas.get('form_filter2_1')['Cve_prod'].str.startswith('M')].reset_index(drop=True))
            base_pt[formula_pt] = bases_formulas.get(f'form_filter2_{i}').copy()
            base_pt[formula_pt] = bases_formulas.get(f'form_filter2_{i}').dropna()
            #formula_pt[formula_pt] = bases_formulas.get(f'form_filter2_{i}').dropna()
        #st.write(base_pt.get('formula_pt_0'))
            base_me[formula_me] = bases_formulas.get(f'form_filter2_{i}')[bases_formulas.get(f'form_filter2_{i}')['Cve_prod'].str.startswith('M')].reset_index(drop=True)
            #formula_me = formula_pt[formula_pt['Cve_prod'].str.startswith('M')].reset_index(drop=True)
            base_st[formula_st] = bases_formulas.get(f'form_filter2_{i}')[bases_formulas.get(f'form_filter2_{i}')['Cve_prod'].str.startswith('41')].reset_index(drop=True)
            #formula_st = formula_pt[formula_pt['Cve_prod'].str.startswith('41')].reset_index(drop=True)
            col_names = ['index', 'SKU pt', 'SKU', 'Cantidad rendimiento', 'New_med', 'New_copr', 'Unidad mp', 'MP','Rendimiento', 'Unidad', 'Cantidad', 'Producto']
            #merge_st = base_st.get(f'formula_st_{i}').merge(formulas, on='SKU', how='left')
            base_st.get(f'formula_st_{i}').columns = col_names
            base_st[formula_st] = base_st.get(f'formula_st_{i}').merge(formulas, on='SKU', how='left') 
            #formula_stt_i = formula_stt_i.merge(formulas, on='SKU', how='left')
        #st.write(base_st.get('formula_st_0').columns)
            base_st[formula_st] = base_st.get(f'formula_st_{i}')[['SKU pt', 'SKU', 'MP_x', 'Rendimiento_x', 'Cve_prod', 'Cantidad rendimiento_y', 'Unidad mp_y', 'MP_y']]
            col_names2 = ['PT', 'SKU', 'ST', 'Rendimiento', 'Cve_prod', 'Cantidad rendimiento', 'Unidad', 'Producto']
            base_st.get(f'formula_st_{i}').columns = col_names2 
            base_st.get(f'formula_st_{i}')['Cantidad unitaria'] = base_st.get(f'formula_st_{i}')['Cantidad rendimiento'] / base_st.get(f'formula_st_{i}')['Rendimiento']
        #st.write(base_st)
            col_names3 = ['SKU', 'ST', 'Producto', 'Rendimiento', 'Cve_prod', 'Cantidad rendimiento', 'Unidad', 'MP', 'Cantidad unitaria']
            base_st.get(f'formula_st_{i}').columns = col_names3 
            base_me[formula_me] = base_me.get(f'formula_me_{i}')[['SKU', 'Producto', 'Rendimiento', 'Cve_prod', 'Cantidad rendimiento', 'Unidad', 'MP', 'Cantidad']]
            col_names4 = ['SKU', 'Producto', 'Rendimiento', 'Cve_prod', 'Cantidad rendimiento', 'Unidad', 'MP', 'Cantidad unitaria']
            base_me.get(f'formula_me_{i}').columns = col_names4 
        #st.write(base_me)
            #formulas_filter = pd.concat([formula_st, formula_me])
            formulas_filtro[formulas_filter] = pd.concat([base_st.get(f'formula_st_{i}'), base_me.get(f'formula_me_{i}')])
        
            formulas_filtro[formulas_filter] = formulas_filtro.get(f'formulas_filter_{i}').fillna(0)
            formulas_filtro[formulas_filter] = formulas_filtro.get(f'formulas_filter_{i}')[['SKU', 'Producto', 'Rendimiento', 'Cve_prod', 'Cantidad rendimiento', 'MP', 'Cantidad unitaria']]
            explosion_part[explosion_materiales] = formulas_filtro.get(f'formulas_filter_{i}').copy()
            explosion_part.get(f'explosion_materiales_{i}')['Cantidad total necesaria'] = explosion_part.get(f'explosion_materiales_{i}')['Cantidad unitaria'] * cantidades_selec.get(f'cantidades_select_{i}')
            explosion_part[explosion_materiales] = pd.DataFrame(explosion_part.get(f'explosion_materiales_{i}'))        
        concat_exp = pd.concat(explosion_part.values(), axis=0, ignore_index=True)
        concat_exp.rename(columns = {'SKU':'SKU PT', 'Cve_prod':'SKU'}, inplace = True)
        concat_exp = concat_exp.merge(existeN_comp, on='SKU', how='left')
        st.write(concat_exp)
        st.download_button(label="Descargar", data=concat_exp.to_csv(), mime="text/csv")
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
        st.download_button(label="Descargar", data=df_compras.to_csv(), mime="text/csv")

    recepcion = df_compras.copy()
    recepcion.columns = recepcion.columns.str.strip()
    recepcion['Status'] = recepcion['Status'].str.strip()
    recepcion['Status_aut'] = recepcion['Status_aut'].str.strip()
    recepcion = recepcion[(recepcion['Status'] !='Surtido') & (recepcion['Status_aut'] == 'Aceptada')] 
    ###CAMBIO MES#############
    recepcion['Rec dic23'] = recepcion['X_Entregar'][(recepcion['Mes'] == '12')]
    recepcion['Rec ene24'] = recepcion['X_Entregar'][(recepcion['Mes'] == '1') & (recepcion['Anio']) == '2024']
    recepcion['Rec feb24'] = recepcion['X_Entregar'][(recepcion['Mes'] == '2') & (recepcion['Anio']) == '2024']
    recepcion['Rec mar24'] = recepcion['X_Entregar'][(recepcion['Mes'] == '3') & (recepcion['Anio']) == '2024']
    recepcion['Rec abr24'] = recepcion['X_Entregar'][(recepcion['Mes'] == '4') & (recepcion['Anio']) == '2024']
    recepcion['Rec may24'] = recepcion['X_Entregar'][(recepcion['Mes'] == '5') & (recepcion['Anio']) == '2024']
    recepcion = recepcion.fillna(0)
    #st.write(recepcion)
    recepcion = recepcion.groupby(['Cve_prod']).agg({'X_Entregar':'sum',
                                                     'Rec dic23':'sum',
                                                     'Rec ene24':'sum',
                                                     'Rec feb24':'sum',
                                                     'Rec mar24':'sum',
                                                     'Rec abr24':'sum',
                                                     'Rec may24':'sum'}).reset_index()
    recepcion.columns = ['SKU', 'X_Entregar', 'Rec dic23', 'Rec ene24', 'Rec feb24', 'Rec mar24', 'Rec abr24', 'Rec may24']
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
    #############################CAMBIO MES###############################################################
    explosion['Inv inicial'] = (explosion['Cantidad'] - explosion['Existencia']) - explosion['Rec dic23']
    explosion['Inv inicial'][(explosion['Inv inicial'] >0)] = 0
    explosion['Inv inicial'][(explosion['Inv inicial'] <0)] = (-1)*explosion['Inv inicial']

    #explosion['Inv inicial'] = explosion['Existencia']
    
    #Faltantes Enero
    #explosion['Fal ene24'] = explosion['Cantidad ene24'] - explosion['Inv inicial']
    #explosion['Fal ene24'][(explosion['Fal ene24'] <0)] = 0
    #explosion['Costo ene24'] = explosion['Fal ene24'] * explosion['Costo']
    
    #Inventario inicial Enero
    #explosion['Inv inicial ene24'] = (explosion['Cantidad'] - explosion['Inv inicial']) - explosion['Rec dic23']
    #explosion['Inv inicial ene24'][(explosion['Inv inicial ene24'] >0)] = 0
    #explosion['Inv inicial ene24'][(explosion['Inv inicial ene24'] <0)] = (-1)*explosion['Inv inicial ene24']
    #Faltantes Enero
    explosion['Fal ene24'] = explosion['Cantidad ene24'] - explosion['Inv inicial']
    #explosion['Fal feb24'] = explosion['Cantidad feb24'] - explosion['Inv inicial']
    explosion['Fal ene24'][(explosion['Fal ene24'] <0)] = 0
    explosion['Costo ene24'] = explosion['Fal ene24'] * explosion['Costo']

    #Inventario inicial Febrero
    explosion['Inv inicial feb24'] = (explosion['Cantidad ene24'] - explosion['Inv inicial']) - explosion['Rec ene24']
    explosion['Inv inicial feb24'][(explosion['Inv inicial feb24'] >0)] = 0
    explosion['Inv inicial feb24'][(explosion['Inv inicial feb24'] <0)] = (-1)*explosion['Inv inicial feb24']
    #Faltantes Febrero
    explosion['Fal feb24'] = explosion['Cantidad feb24'] - explosion['Inv inicial feb24']
    #explosion['Fal feb24'] = explosion['Cantidad feb24'] - explosion['Inv inicial']
    explosion['Fal feb24'][(explosion['Fal feb24'] <0)] = 0
    explosion['Costo feb24'] = explosion['Fal feb24'] * explosion['Costo']
    
    #Inventario inicial Marzo
    explosion['Inv inicial mar24'] = (explosion['Cantidad feb24'] - explosion['Inv inicial feb24']) - explosion['Rec feb24']
    explosion['Inv inicial mar24'][(explosion['Inv inicial mar24'] >0)] = 0
    explosion['Inv inicial mar24'][(explosion['Inv inicial mar24'] <0)] = (-1)*explosion['Inv inicial mar24']
    #Faltantes Marzo
    explosion['Fal mar24'] = explosion['Cantidad mar24'] - explosion['Inv inicial mar24']
    explosion['Fal mar24'][(explosion['Fal mar24'] <0)] = 0
    explosion['Costo mar24'] = explosion['Fal mar24'] * explosion['Costo']
    
    #Inventario inicial Abril
    explosion['Inv inicial abr24'] = (explosion['Cantidad mar24'] - explosion['Inv inicial mar24']) - explosion['Rec mar24']
    explosion['Inv inicial abr24'][(explosion['Inv inicial abr24'] >0)] = 0
    explosion['Inv inicial abr24'][(explosion['Inv inicial abr24'] <0)] = (-1)*explosion['Inv inicial abr24']
    #Faltantes Abril
    explosion['Fal abr24'] = explosion['Cantidad abr24'] - explosion['Inv inicial abr24']
    explosion['Fal abr24'][(explosion['Fal abr24'] <0)] = 0
    explosion['Costo abr24'] = explosion['Fal abr24'] * explosion['Costo']
    
    #Inventario inicial Mayo
    explosion['Inv inicial may24'] = (explosion['Cantidad abr24'] - explosion['Inv inicial abr24']) - explosion['Rec abr24']
    explosion['Inv inicial may24'][(explosion['Inv inicial may24'] >0)] = 0
    explosion['Inv inicial may24'][(explosion['Inv inicial may24'] <0)] = (-1)*explosion['Inv inicial may24']
    #Faltantes Mayo
    explosion['Fal may24'] = explosion['Cantidad may24'] - explosion['Inv inicial may24']
    explosion['Fal may24'][(explosion['Fal may24'] <0)] = 0
    explosion['Costo may24'] = explosion['Fal may24'] * explosion['Costo']
    
    #for i in range(len(explosion['SKU'])):
    #    if explosion.loc[i,'Inv inicial']>0:
    #        explosion.loc[i,'Inv inicial'] = 0
    #    else:
    #        explosion.loc[i,'Inv inicial'] = (-1)*explosion.loc[i,'Inv inicial']
    explosion = explosion[['SKU', 'MP', 'Moneda', 'Costo', 'Existencia', 'Cantidad', 'Faltante mp', 'Costo total', 'Rec dic23', 
               'Inv inicial', 'Cantidad ene24', 'Fal ene24', 'Costo ene24', 'Rec ene24', 
               'Inv inicial feb24', 'Cantidad feb24', 'Fal feb24', 'Costo feb24' , 'Rec feb24',
               'Inv inicial mar24', 'Cantidad mar24', 'Fal mar24', 'Costo mar24', 'Rec mar24',
               'Inv inicial abr24', 'Cantidad abr24', 'Fal abr24', 'Costo abr24', 'Rec abr24',
               'Inv inicial may24', 'Cantidad may24', 'Fal may24', 'Costo may24', 'Rec may24']]
    
    #st.write(explosion)
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
    ############################CAMBIO MES########################################
    explosiona['Inv inicial'] = (explosiona['Cantidad'] - explosiona['Existencia']) - explosiona['Rec dic23']
    explosiona['Inv inicial'][(explosiona['Inv inicial'] >0)] = 0
    explosiona['Inv inicial'][(explosiona['Inv inicial'] <0)] = (-1)*explosiona['Inv inicial']
    
    #explosiona['Inv inicial'] = explosiona['Existencia']
    #Inventario inicial Enero
    explosiona['Inv inicial ene24'] = (explosiona['Cantidad'] - explosiona['Inv inicial']) - explosiona['Rec dic23']
    explosiona['Inv inicial ene24'][(explosiona['Inv inicial ene24'] >0)] = 0
    explosiona['Inv inicial ene24'][(explosiona['Inv inicial ene24'] <0)] = (-1)*explosiona['Inv inicial ene24']
    #Faltantes Enero
    explosiona['Fal ene24'] = explosiona['Cantidad ene24'] - explosiona['Inv inicial ene24']
    explosiona['Fal ene24'][(explosiona['Fal ene24'] <0)] = 0
    explosiona['Costo ene24'] = explosiona['Fal ene24'] * explosiona['Costo']
    #Inventario inicial FEBiembre
    explosiona['Inv inicial feb24'] = (explosiona['Cantidad ene24'] - explosiona['Inv inicial ene24']) - explosiona['Rec ene24']
    explosiona['Inv inicial feb24'][(explosiona['Inv inicial feb24'] >0)] = 0
    explosiona['Inv inicial feb24'][(explosiona['Inv inicial feb24'] <0)] = (-1)*explosiona['Inv inicial feb24']
    #Faltantes FEBiembre
    explosiona['Fal feb24'] = explosiona['Cantidad feb24'] - explosiona['Inv inicial feb24']
    explosiona['Fal feb24'][(explosiona['Fal feb24'] <0)] = 0
    explosiona['Costo feb24'] = explosiona['Fal feb24'] * explosiona['Costo']
    #Inventario inicial diciembre
    explosiona['Inv inicial mar24'] = (explosiona['Cantidad feb24'] - explosiona['Inv inicial feb24']) - explosiona['Rec feb24']
    explosiona['Inv inicial mar24'][(explosiona['Inv inicial mar24'] >0)] = 0
    explosiona['Inv inicial mar24'][(explosiona['Inv inicial mar24'] <0)] = (-1)*explosiona['Inv inicial mar24']
    #Faltantes diciembre
    explosiona['Fal mar24'] = explosiona['Cantidad mar24'] - explosiona['Inv inicial mar24']
    explosiona['Fal mar24'][(explosiona['Fal mar24'] <0)] = 0
    explosiona['Costo mar24'] = explosiona['Fal mar24'] * explosiona['Costo']
    #Inventario inicial Enero
    explosiona['Inv inicial abr24'] = (explosiona['Cantidad mar24'] - explosiona['Inv inicial mar24']) - explosiona['Rec mar24']
    explosiona['Inv inicial abr24'][(explosiona['Inv inicial abr24'] >0)] = 0
    explosiona['Inv inicial abr24'][(explosiona['Inv inicial abr24'] <0)] = (-1)*explosiona['Inv inicial abr24']
    #Faltantes Enero
    explosiona['Fal abr24'] = explosiona['Cantidad abr24'] - explosiona['Inv inicial abr24']
    explosiona['Fal abr24'][(explosiona['Fal abr24'] <0)] = 0
    explosiona['Costo abr24'] = explosiona['Fal abr24'] * explosiona['Costo']
    #Inventario inicial Febrero
    explosiona['Inv inicial may24'] = (explosiona['Cantidad abr24'] - explosiona['Inv inicial abr24']) - explosiona['Rec abr24']
    explosiona['Inv inicial may24'][(explosiona['Inv inicial may24'] >0)] = 0
    explosiona['Inv inicial may24'][(explosiona['Inv inicial may24'] <0)] = (-1)*explosiona['Inv inicial may24']
    #Faltantes Febrero
    explosiona['Fal may24'] = explosiona['Cantidad may24'] - explosiona['Inv inicial may24']
    explosiona['Fal may24'][(explosiona['Fal may24'] <0)] = 0
    explosiona['Costo may24'] = explosiona['Fal may24'] * explosiona['Costo']
    explosiona = explosiona[['SKU', 'MP', 'Moneda', 'Costo', 'Existencia', 'Cantidad', 'Faltante mp', 'Costo total', 'Rec dic23', 
               'Inv inicial', 'Cantidad ene24', 'Fal ene24', 'Costo ene24', 
               'Inv inicial feb24', 'Cantidad feb24', 'Fal feb24', 'Costo feb24',
               'Inv inicial mar24', 'Cantidad mar24', 'Fal mar24', 'Costo mar24',
               'Inv inicial abr24', 'Cantidad abr24', 'Fal abr24', 'Costo abr24',
               'Inv inicial may24', 'Cantidad may24', 'Fal may24', 'Costo may24']]

    #######################################################################################################
    
    inversionmesa = explosiona['Costo feb24'].sum()
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
    
    ########################CAMBIO MES#######################################################################
    #explosionaspen['Inv inicial'] = (explosionaspen['Cantidad'] - explosionaspen['Existencia']) - explosionaspen['Rec dic23']
    #explosionaspen['Inv inicial'][(explosionaspen['Inv inicial'] >0)] = 0
    #explosionaspen['Inv inicial'][(explosionaspen['Inv inicial'] <0)] = (-1)*explosionaspen['Inv inicial']
    
    explosionaspen['Inv inicial'] = explosionaspen['Existencia']
    #st.write(explosionaspen)
    #Faltantes ENEubre
    explosionaspen['Fal ene24'] = explosionaspen['Cantidad ene24'] - explosionaspen['Inv inicial']
    explosionaspen['Fal ene24'][(explosionaspen['Fal ene24'] <0)] = 0
    explosionaspen['Costo ene24'] = explosionaspen['Fal ene24'] * explosionaspen['Costo']
    #Inventario inicial FEBiembre
    explosionaspen['Inv inicial feb24'] = (explosionaspen['Cantidad ene24'] - explosionaspen['Inv inicial']) - explosionaspen['Rec ene24']
    explosionaspen['Inv inicial feb24'][(explosionaspen['Inv inicial feb24'] >0)] = 0
    explosionaspen['Inv inicial feb24'][(explosionaspen['Inv inicial feb24'] <0)] = (-1)*explosionaspen['Inv inicial feb24']
    #Faltantes FEBiembre
    explosionaspen['Fal feb24'] = explosionaspen['Cantidad feb24'] - explosionaspen['Inv inicial feb24']
    explosionaspen['Fal feb24'][(explosionaspen['Fal feb24'] <0)] = 0
    explosionaspen['Costo feb24'] = explosionaspen['Fal feb24'] * explosionaspen['Costo']
    #Inventario inicial diciembre
    explosionaspen['Inv inicial mar24'] = (explosionaspen['Cantidad feb24'] - explosionaspen['Inv inicial feb24']) - explosionaspen['Rec feb24']
    explosionaspen['Inv inicial mar24'][(explosionaspen['Inv inicial mar24'] >0)] = 0
    explosionaspen['Inv inicial mar24'][(explosionaspen['Inv inicial mar24'] <0)] = (-1)*explosionaspen['Inv inicial mar24']
    #Faltantes diciembre
    explosionaspen['Fal mar24'] = explosionaspen['Cantidad mar24'] - explosionaspen['Inv inicial mar24']
    explosionaspen['Fal mar24'][(explosionaspen['Fal mar24'] <0)] = 0
    explosionaspen['Costo mar24'] = explosionaspen['Fal mar24'] * explosionaspen['Costo']
    #Inventario inicial Enero
    explosionaspen['Inv inicial abr24'] = (explosionaspen['Cantidad mar24'] - explosionaspen['Inv inicial mar24']) - explosionaspen['Rec mar24']
    explosionaspen['Inv inicial abr24'][(explosionaspen['Inv inicial abr24'] >0)] = 0
    explosionaspen['Inv inicial abr24'][(explosionaspen['Inv inicial abr24'] <0)] = (-1)*explosionaspen['Inv inicial abr24']
    #Faltantes Enero
    explosionaspen['Fal abr24'] = explosionaspen['Cantidad abr24'] - explosionaspen['Inv inicial abr24']
    explosionaspen['Fal abr24'][(explosionaspen['Fal abr24'] <0)] = 0
    explosionaspen['Costo abr24'] = explosionaspen['Fal abr24'] * explosionaspen['Costo']
    #Inventario inicial Febrero
    explosionaspen['Inv inicial may24'] = (explosionaspen['Cantidad abr24'] - explosionaspen['Inv inicial abr24']) - explosionaspen['Rec abr24']
    explosionaspen['Inv inicial may24'][(explosionaspen['Inv inicial may24'] >0)] = 0
    explosionaspen['Inv inicial may24'][(explosionaspen['Inv inicial may24'] <0)] = (-1)*explosionaspen['Inv inicial may24']
    #Faltantes Febrero
    explosionaspen['Fal may24'] = explosionaspen['Cantidad may24'] - explosionaspen['Inv inicial may24']
    explosionaspen['Fal may24'][(explosionaspen['Fal may24'] <0)] = 0
    explosionaspen['Costo may24'] = explosionaspen['Fal may24'] * explosionaspen['Costo']
    explosionaspen = explosionaspen[['SKU', 'MP', 'Moneda', 'Costo', 'Existencia', 'Cantidad', 'Faltante mp', 'Costo total', 'Rec dic23', 
               'Inv inicial', 'Cantidad ene24', 'Fal ene24', 'Costo ene24', 
               'Inv inicial feb24', 'Cantidad feb24', 'Fal feb24', 'Costo feb24',
               'Inv inicial mar24', 'Cantidad mar24', 'Fal mar24', 'Costo mar24',
               'Inv inicial abr24', 'Cantidad abr24', 'Fal abr24', 'Costo abr24',
               'Inv inicial may24', 'Cantidad may24', 'Fal may24', 'Costo may24']]
    ########################################################################################################
    
    inversionmesaspen = explosionaspen['Costo feb24'].sum()
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
    #####################################CAMBIO MES##########################################################
    #explosionsimi['Inv inicial'] = (explosionsimi['Cantidad'] - explosionsimi['Existencia']) - explosionsimi['Rec dic23']
    #explosionsimi['Inv inicial'][(explosionsimi['Inv inicial'] >0)] = 0
    #explosionsimi['Inv inicial'][(explosionsimi['Inv inicial'] <0)] = (-1)*explosionsimi['Inv inicial']
    
    explosionsimi['Inv inicial'] = explosionsimi['Existencia']

    #Faltantes ENEubre
    explosionsimi['Fal ene24'] = explosionsimi['Cantidad ene24'] - explosionsimi['Inv inicial']
    explosionsimi['Fal ene24'][(explosionsimi['Fal ene24'] <0)] = 0
    explosionsimi['Costo ene24'] = explosionsimi['Fal ene24'] * explosionsimi['Costo']
    #Inventario inicial FEBiembre
    explosionsimi['Inv inicial feb24'] = (explosionsimi['Cantidad ene24'] - explosionsimi['Inv inicial']) - explosionsimi['Rec ene24']
    explosionsimi['Inv inicial feb24'][(explosionsimi['Inv inicial feb24'] >0)] = 0
    explosionsimi['Inv inicial feb24'][(explosionsimi['Inv inicial feb24'] <0)] = (-1)*explosionsimi['Inv inicial feb24']
    #Faltantes FEBiembre
    explosionsimi['Fal feb24'] = explosionsimi['Cantidad feb24'] - explosionsimi['Inv inicial feb24']
    explosionsimi['Fal feb24'][(explosionsimi['Fal feb24'] <0)] = 0
    explosionsimi['Costo feb24'] = explosionsimi['Fal feb24'] * explosionsimi['Costo']
    #Inventario inicial diciembre
    explosionsimi['Inv inicial mar24'] = (explosionsimi['Cantidad feb24'] - explosionsimi['Inv inicial feb24']) - explosionsimi['Rec feb24']
    explosionsimi['Inv inicial mar24'][(explosionsimi['Inv inicial mar24'] >0)] = 0
    explosionsimi['Inv inicial mar24'][(explosionsimi['Inv inicial mar24'] <0)] = (-1)*explosionsimi['Inv inicial mar24']
    #Faltantes diciembre
    explosionsimi['Fal mar24'] = explosionsimi['Cantidad mar24'] - explosionsimi['Inv inicial mar24']
    explosionsimi['Fal mar24'][(explosionsimi['Fal mar24'] <0)] = 0
    explosionsimi['Costo mar24'] = explosionsimi['Fal mar24'] * explosionsimi['Costo']
    #Inventario inicial Enero
    explosionsimi['Inv inicial abr24'] = (explosionsimi['Cantidad mar24'] - explosionsimi['Inv inicial mar24']) - explosionsimi['Rec mar24']
    explosionsimi['Inv inicial abr24'][(explosionsimi['Inv inicial abr24'] >0)] = 0
    explosionsimi['Inv inicial abr24'][(explosionsimi['Inv inicial abr24'] <0)] = (-1)*explosionsimi['Inv inicial abr24']
    #Faltantes Enero
    explosionsimi['Fal abr24'] = explosionsimi['Cantidad abr24'] - explosionsimi['Inv inicial abr24']
    explosionsimi['Fal abr24'][(explosionsimi['Fal abr24'] <0)] = 0
    explosionsimi['Costo abr24'] = explosionsimi['Fal abr24'] * explosionsimi['Costo']
    #Inventario inicial Febrero
    explosionsimi['Inv inicial may24'] = (explosionsimi['Cantidad abr24'] - explosionsimi['Inv inicial abr24']) - explosionsimi['Rec abr24']
    explosionsimi['Inv inicial may24'][(explosionsimi['Inv inicial may24'] >0)] = 0
    explosionsimi['Inv inicial may24'][(explosionsimi['Inv inicial may24'] <0)] = (-1)*explosionsimi['Inv inicial may24']
    #Faltantes Febrero
    explosionsimi['Fal may24'] = explosionsimi['Cantidad may24'] - explosionsimi['Inv inicial may24']
    explosionsimi['Fal may24'][(explosionsimi['Fal may24'] <0)] = 0
    explosionsimi['Costo may24'] = explosionsimi['Fal may24'] * explosionsimi['Costo']
    #for i in range(len(explosion['SKU'])):
    #    if explosion.loc[i,'Inv inicial']>0:
    #        explosion.loc[i,'Inv inicial'] = 0
    #    else:
    #        explosion.loc[i,'Inv inicial'] = (-1)*explosion.loc[i,'Inv inicial']
    explosionsimi = explosionsimi[['SKU', 'MP', 'Moneda', 'Costo', 'Existencia', 'Cantidad', 'Faltante mp', 'Costo total', 'Rec dic23', 
               'Inv inicial', 'Cantidad ene24', 'Fal ene24', 'Costo ene24', 
               'Inv inicial feb24', 'Cantidad feb24', 'Fal feb24', 'Costo feb24',
               'Inv inicial mar24', 'Cantidad mar24', 'Fal mar24', 'Costo mar24',
               'Inv inicial abr24', 'Cantidad abr24', 'Fal abr24', 'Costo abr24',
               'Inv inicial may24', 'Cantidad may24', 'Fal may24', 'Costo may24']]
    
    ########################################################################################################

    
    inversionmessimi = explosionsimi['Costo feb24'].sum()
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

    ###########################CAMBIO MES##############################################
    #explosiongrisi['Inv inicial'] = (explosiongrisi['Cantidad'] - explosiongrisi['Existencia']) - explosiongrisi['Rec dic23']
    #explosiongrisi['Inv inicial'][(explosiongrisi['Inv inicial'] >0)] = 0
    #explosiongrisi['Inv inicial'][(explosiongrisi['Inv inicial'] <0)] = (-1)*explosiongrisi['Inv inicial']
    
    explosiongrisi['Inv inicial'] = explosiongrisi['Existencia']

    #Faltantes ENEubre
    explosiongrisi['Fal ene24'] = explosiongrisi['Cantidad ene24'] - explosiongrisi['Inv inicial']
    explosiongrisi['Fal ene24'][(explosiongrisi['Fal ene24'] <0)] = 0
    explosiongrisi['Costo ene24'] = explosiongrisi['Fal ene24'] * explosiongrisi['Costo']
    #Inventario inicial FEBiembre
    explosiongrisi['Inv inicial feb24'] = (explosiongrisi['Cantidad ene24'] - explosiongrisi['Inv inicial']) - explosiongrisi['Rec ene24']
    explosiongrisi['Inv inicial feb24'][(explosiongrisi['Inv inicial feb24'] >0)] = 0
    explosiongrisi['Inv inicial feb24'][(explosiongrisi['Inv inicial feb24'] <0)] = (-1)*explosiongrisi['Inv inicial feb24']
    #Faltantes FEBiembre
    explosiongrisi['Fal feb24'] = explosiongrisi['Cantidad feb24'] - explosiongrisi['Inv inicial feb24']
    explosiongrisi['Fal feb24'][(explosiongrisi['Fal feb24'] <0)] = 0
    explosiongrisi['Costo feb24'] = explosiongrisi['Fal feb24'] * explosiongrisi['Costo']
    #Inventario inicial diciembre
    explosiongrisi['Inv inicial mar24'] = (explosiongrisi['Cantidad feb24'] - explosiongrisi['Inv inicial feb24']) - explosiongrisi['Rec feb24']
    explosiongrisi['Inv inicial mar24'][(explosiongrisi['Inv inicial mar24'] >0)] = 0
    explosiongrisi['Inv inicial mar24'][(explosiongrisi['Inv inicial mar24'] <0)] = (-1)*explosiongrisi['Inv inicial mar24']
    #Faltantes diciembre
    explosiongrisi['Fal mar24'] = explosiongrisi['Cantidad mar24'] - explosiongrisi['Inv inicial mar24']
    explosiongrisi['Fal mar24'][(explosiongrisi['Fal mar24'] <0)] = 0
    explosiongrisi['Costo mar24'] = explosiongrisi['Fal mar24'] * explosiongrisi['Costo']
    #Inventario inicial Enero
    explosiongrisi['Inv inicial abr24'] = (explosiongrisi['Cantidad mar24'] - explosiongrisi['Inv inicial mar24']) - explosiongrisi['Rec mar24']
    explosiongrisi['Inv inicial abr24'][(explosiongrisi['Inv inicial abr24'] >0)] = 0
    explosiongrisi['Inv inicial abr24'][(explosiongrisi['Inv inicial abr24'] <0)] = (-1)*explosiongrisi['Inv inicial abr24']
    #Faltantes Enero
    explosiongrisi['Fal abr24'] = explosiongrisi['Cantidad abr24'] - explosiongrisi['Inv inicial abr24']
    explosiongrisi['Fal abr24'][(explosiongrisi['Fal abr24'] <0)] = 0
    explosiongrisi['Costo abr24'] = explosiongrisi['Fal abr24'] * explosiongrisi['Costo']
    #Inventario inicial Febrero
    explosiongrisi['Inv inicial may24'] = (explosiongrisi['Cantidad abr24'] - explosiongrisi['Inv inicial abr24']) - explosiongrisi['Rec abr24']
    explosiongrisi['Inv inicial may24'][(explosiongrisi['Inv inicial may24'] >0)] = 0
    explosiongrisi['Inv inicial may24'][(explosiongrisi['Inv inicial may24'] <0)] = (-1)*explosiongrisi['Inv inicial may24']
    #Faltantes Febrero
    explosiongrisi['Fal may24'] = explosiongrisi['Cantidad may24'] - explosiongrisi['Inv inicial may24']
    explosiongrisi['Fal may24'][(explosiongrisi['Fal may24'] <0)] = 0
    explosiongrisi['Costo may24'] = explosiongrisi['Fal may24'] * explosiongrisi['Costo']
    #for i in range(len(explosion['SKU'])):
    #    if explosion.loc[i,'Inv inicial']>0:
    #        explosion.loc[i,'Inv inicial'] = 0
    #    else:
    #        explosion.loc[i,'Inv inicial'] = (-1)*explosion.loc[i,'Inv inicial']
    explosiongrisi = explosiongrisi[['SKU', 'MP', 'Moneda', 'Costo', 'Existencia', 'Cantidad', 'Faltante mp', 'Costo total', 'Rec dic23', 
               'Inv inicial', 'Cantidad ene24', 'Fal ene24', 'Costo ene24', 
               'Inv inicial feb24', 'Cantidad feb24', 'Fal feb24', 'Costo feb24',
               'Inv inicial mar24', 'Cantidad mar24', 'Fal mar24', 'Costo mar24',
               'Inv inicial abr24', 'Cantidad abr24', 'Fal abr24', 'Costo abr24',
               'Inv inicial may24', 'Cantidad may24', 'Fal may24', 'Costo may24']]
    
    ################################################################################################################
    
    inversionmesgrisi = explosiongrisi['Costo feb24'].sum()
    frasegrisi = 'Inversión total del mes $' + str(round(inversionmesgrisi,2))
    ####################################################################################
    #if st.checkbox('Requerimientos por almacen'):
    #    uno, dos = st.columns([1, 1])
    #    with uno:
    #        st.title('Almacén A1-A3')
    #        st.write(explosiona)
    #        st.download_button(label="Descargar", data=explosiona.to_csv(), mime="text/csv")
    #        st.info(frasea, icon='💵')
    #        st.title('Almacén ASPEN')
    #        st.write(explosionaspen)
    #        st.download_button(label="Descargar", data=explosionaspen.to_csv(), mime="text/csv")
    #        st.info(fraseaspen, icon='💵')
    #    with dos:
    #        st.title('Almacén SIMILARES')
    #        st.write(explosionsimi)
    #        st.download_button(label="Descargar", data=explosionsimi.to_csv(), mime="text/csv")
    #        st.info(frasesimi, icon='💵')
    #        st.title('Almacén GRISI')
    #        st.write(explosiongrisi)
    #        st.download_button(label="Descargar", data=explosiongrisi.to_csv(), mime="text/csv")
    #        st.info(frasegrisi, icon='💵')

    if st.checkbox('Requerimientos general'):
        explosion_temp = explosion.merge(moq, on='SKU', how='left')
        explosion_temp = explosion_temp.fillna(0)
        #st.write(explosion_temp)
        explosion_temp['OC NUEVA'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC NUEVAENE'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC NUEVAFEB'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC NUEVAMAR'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC NUEVAABR'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC NUEVAMAY'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['div'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['divene'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['divfeb'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['divmar'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['divabr'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['divmay'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC temp'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC tempene'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC tempfeb'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC tempmar'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC tempabr'] = pd.Series(0, index=range(len(explosion['SKU'])))
        explosion_temp['OC tempmay'] = pd.Series(0, index=range(len(explosion['SKU'])))
        #hola = math.ceil(explosion_temp.loc[22,'Faltante mp'] / explosion_temp.loc[22, 'MOQ'])
        #hola = (math.ceil(explosion_temp.loc[22,'Faltante mp'] / explosion_temp.loc[22,'MOQ']))*(explosion_temp.loc[22,'MOQ'])-(explosion_temp.loc[22,'Rec dic23'])
        #st.write(hola)
        ########################################3333CAMBIO MES##########################################################################
        for i in range(len(explosion_temp['SKU'])):
            explosion_temp.loc[i, 'MOQ'] = float(explosion_temp.loc[i, 'MOQ'])
            explosion_temp = explosion_temp.fillna(0)
            if explosion_temp.loc[i,'MOQ'] != 0:
                explosion_temp.loc[i, 'div'] = math.ceil(explosion_temp.loc[i,'Faltante mp'] / explosion_temp.loc[i,'MOQ'])
            else:
                explosion_temp.loc[i, 'div'] = 0

            explosion_temp.loc[i,'OC temp'] = (explosion_temp.loc[i,'div'])*(explosion_temp.loc[i,'MOQ'])-(explosion_temp.loc[i,'Rec dic23'])
        
            if (explosion_temp.loc[i,'Faltante mp']>0) & (explosion_temp.loc[i,'OC temp']>0):
                explosion_temp.loc[i,'OC NUEVA'] = explosion_temp.loc[i,'OC temp']
            else:
                explosion_temp.loc[i, 'OC NUEVA'] = 0  
        

        explosion_temp['TOTAL OC'] = explosion_temp['Rec dic23'] + explosion_temp['OC NUEVA']
        explosion_temp = explosion_temp.merge(a1, on='SKU', how='left')
        explosion_temp = explosion_temp.fillna(0)
        ######################################CAMBIO MES###########################################################################
        explosion_temp['INV_ENE'] = (explosion_temp['Cantidad'] - explosion_temp['Existencia']) - explosion_temp['TOTAL OC']
        #explosion_temp['INV_ENE'] = explosion_temp['Existencia']
        #explosion_temp['INV_FEB'] = explosion_temp['Existencia'] 
        explosion_temp['INV_ENE'][(explosion_temp['INV_ENE'] >0)] = 0
        explosion_temp['INV_ENE'][(explosion_temp['INV_ENE'] <0)] = (-1)*explosion_temp['INV_ENE']
        
        #################################MES ENE################################################################################
        explosion_temp['Fal ene24'] = explosion_temp['Cantidad ene24'] - explosion_temp['INV_ENE']
        explosion_temp['Fal ene24'][(explosion_temp['Fal ene24']<0)] = 0
        for i in range(len(explosion_temp['SKU'])):
            if explosion_temp.loc[i, 'MOQ'] != 0:
                explosion_temp.loc[i, 'divene'] = math.ceil(explosion_temp.loc[i,'Fal ene24'] / explosion_temp.loc[i,'MOQ'])
            else:
                explosion_temp.loc[i, 'divene'] = 0        
            explosion_temp.loc[i,'OC tempene'] = (explosion_temp.loc[i,'divene'])*(explosion_temp.loc[i,'MOQ'])-(explosion_temp.loc[i,'Rec ene24'])
            if (explosion_temp.loc[i,'Fal ene24']>0) & (explosion_temp.loc[i,'OC tempene']>0):
                explosion_temp.loc[i,'OC NUEVAENE'] = explosion_temp.loc[i,'OC tempene']
            else:
                explosion_temp.loc[i, 'OC NUEVAENE'] = 0
        explosion_temp['TOTAL OC_ENE'] = explosion_temp['Rec ene24'] + explosion_temp['OC NUEVAENE']
        explosion_temp['INV_FEB'] = (explosion_temp['Cantidad ene24'] - explosion_temp['INV_ENE']) - explosion_temp['TOTAL OC_ENE']
        explosion_temp['INV_FEB'][(explosion_temp['INV_FEB'] >0)] = 0
        explosion_temp['INV_FEB'][(explosion_temp['INV_FEB'] <0)] = (-1)*explosion_temp['INV_FEB']
        ###################################################################################################################################

        #################################MES FEB################################################################################
        explosion_temp['Fal feb24'] = explosion_temp['Cantidad feb24'] - explosion_temp['INV_FEB']
        explosion_temp['Fal feb24'][(explosion_temp['Fal feb24']<0)] = 0
        for i in range(len(explosion_temp['SKU'])):
            if explosion_temp.loc[i, 'MOQ'] != 0:
                explosion_temp.loc[i, 'divfeb'] = math.ceil(explosion_temp.loc[i,'Fal feb24'] / explosion_temp.loc[i,'MOQ'])
            else:
                explosion_temp.loc[i, 'divfeb'] = 0        
            explosion_temp.loc[i,'OC tempfeb'] = (explosion_temp.loc[i,'divfeb'])*(explosion_temp.loc[i,'MOQ'])-(explosion_temp.loc[i,'Rec feb24'])
            if (explosion_temp.loc[i,'Fal feb24']>0) & (explosion_temp.loc[i,'OC tempfeb']>0):
                explosion_temp.loc[i,'OC NUEVAFEB'] = explosion_temp.loc[i,'OC tempfeb']
            else:
                explosion_temp.loc[i, 'OC NUEVAFEB'] = 0
        explosion_temp['TOTAL OC_FEB'] = explosion_temp['Rec feb24'] + explosion_temp['OC NUEVAFEB']
        explosion_temp['INV_MAR'] = (explosion_temp['Cantidad feb24'] - explosion_temp['INV_FEB']) - explosion_temp['TOTAL OC_FEB']
        explosion_temp['INV_MAR'][(explosion_temp['INV_MAR'] >0)] = 0
        explosion_temp['INV_MAR'][(explosion_temp['INV_MAR'] <0)] = (-1)*explosion_temp['INV_MAR']
        ##################################################################################################################################

        #################################MES MAR################################################################################
        explosion_temp['Fal mar24'] = explosion_temp['Cantidad mar24'] - explosion_temp['INV_MAR']
        explosion_temp['Fal mar24'][(explosion_temp['Fal mar24']<0)] = 0
        for i in range(len(explosion_temp['SKU'])):
            if explosion_temp.loc[i, 'MOQ'] != 0:
                explosion_temp.loc[i, 'divmar'] = math.ceil(explosion_temp.loc[i,'Fal mar24'] / explosion_temp.loc[i,'MOQ'])
            else:
                explosion_temp.loc[i, 'divmar'] = 0        
            explosion_temp.loc[i,'OC tempmar'] = (explosion_temp.loc[i,'divmar'])*(explosion_temp.loc[i,'MOQ'])-(explosion_temp.loc[i,'Rec mar24'])
            if (explosion_temp.loc[i,'Fal mar24']>0) & (explosion_temp.loc[i,'OC tempmar']>0):
                explosion_temp.loc[i,'OC NUEVAMAR'] = explosion_temp.loc[i,'OC tempmar']
            else:
                explosion_temp.loc[i, 'OC NUEVAMAR'] = 0
        explosion_temp['TOTAL OC_MAR'] = explosion_temp['Rec mar24'] + explosion_temp['OC NUEVAMAR']
        explosion_temp['INV_ABR'] = (explosion_temp['Cantidad mar24'] - explosion_temp['INV_MAR']) - explosion_temp['TOTAL OC_MAR']
        explosion_temp['INV_ABR'][(explosion_temp['INV_ABR'] >0)] = 0
        explosion_temp['INV_ABR'][(explosion_temp['INV_ABR'] <0)] = (-1)*explosion_temp['INV_ABR']
        ##################################################################################################################################

        #################################MES ABR################################################################################
        explosion_temp['Fal abr24'] = explosion_temp['Cantidad abr24'] - explosion_temp['INV_ABR']
        explosion_temp['Fal abr24'][(explosion_temp['Fal abr24']<0)] = 0
        for i in range(len(explosion_temp['SKU'])):
            if explosion_temp.loc[i, 'MOQ'] != 0:
                explosion_temp.loc[i, 'divabr'] = math.ceil(explosion_temp.loc[i,'Fal abr24'] / explosion_temp.loc[i,'MOQ'])
            else:
                explosion_temp.loc[i, 'divabr'] = 0        
            explosion_temp.loc[i,'OC tempabr'] = (explosion_temp.loc[i,'divabr'])*(explosion_temp.loc[i,'MOQ'])-(explosion_temp.loc[i,'Rec abr24'])
            if (explosion_temp.loc[i,'Fal abr24']>0) & (explosion_temp.loc[i,'OC tempabr']>0):
                explosion_temp.loc[i,'OC NUEVAABR'] = explosion_temp.loc[i,'OC tempabr']
            else:
                explosion_temp.loc[i, 'OC NUEVAABR'] = 0
        explosion_temp['TOTAL OC_ABR'] = explosion_temp['Rec abr24'] + explosion_temp['OC NUEVAABR']
        explosion_temp['INV_MAY'] = (explosion_temp['Cantidad abr24'] - explosion_temp['INV_ABR']) - explosion_temp['TOTAL OC_ABR']
        explosion_temp['INV_MAY'][(explosion_temp['INV_MAY'] >0)] = 0
        explosion_temp['INV_MAY'][(explosion_temp['INV_MAY'] <0)] = (-1)*explosion_temp['INV_MAY']
        ##################################################################################################################################

        #################################MES MAY################################################################################
        explosion_temp['Fal may24'] = explosion_temp['Cantidad may24'] - explosion_temp['INV_MAY']
        explosion_temp['Fal may24'][(explosion_temp['Fal may24']<0)] = 0
        for i in range(len(explosion_temp['SKU'])):
            if explosion_temp.loc[i, 'MOQ'] != 0:
                explosion_temp.loc[i, 'divmay'] = math.ceil(explosion_temp.loc[i,'Fal may24'] / explosion_temp.loc[i,'MOQ'])
            else:
                explosion_temp.loc[i, 'divmay'] = 0        
            explosion_temp.loc[i,'OC tempmay'] = (explosion_temp.loc[i,'divmay'])*(explosion_temp.loc[i,'MOQ'])-(explosion_temp.loc[i,'Rec may24'])
            if (explosion_temp.loc[i,'Fal may24']>0) & (explosion_temp.loc[i,'OC tempmay']>0):
                explosion_temp.loc[i,'OC NUEVAMAY'] = explosion_temp.loc[i,'OC tempmay']
            else:
                explosion_temp.loc[i, 'OC NUEVAMAY'] = 0
        explosion_temp['TOTAL OC_MAY'] = explosion_temp['Rec may24'] + explosion_temp['OC NUEVAMAY']
        explosion_temp['INV_MAY'] = (explosion_temp['Cantidad abr24'] - explosion_temp['INV_ABR']) - explosion_temp['TOTAL OC_ABR']
        explosion_temp['INV_MAY'][(explosion_temp['INV_MAY'] >0)] = 0
        explosion_temp['INV_MAY'][(explosion_temp['INV_MAY'] <0)] = (-1)*explosion_temp['INV_MAY']
        ##################################################################################################################################
        ############################CAMBIO MES ELIMINAMOS SEPTIEMBRE##########################################################
        #explosion_temp = explosion_temp[['SKU', 'MP_x', 'PROVEEDOR', 'DÍAS CRED', 'MP/ME', 'MOQ', 'Moneda', 'Costo', 'Existencia',
        #                                 'Cantidad', 'Faltante mp', 'Rec dic23', 'OC NUEVA', 'TOTAL OC', 'Ingreso', 
        #                                 'INV_ENE', 'Cantidad ene24', 'Fal ene24', 'Rec ene24', 'OC NUEVAENE', 'TOTAL OC_ENE', 
        #                                 'INV_FEB', 'Cantidad feb24', 'Fal feb24', 'Rec feb24', 'OC NUEVAFEB', 'TOTAL OC_FEB',
        #                                 'INV_DIC', 'Cantidad mar24', 'Fal mar24', 'Rec mar24', 'OC NUEVADIC', 'TOTAL OC_DIC',
        #                                 'INV_ENE', 'Cantidad abr24', 'Fal abr24', 'Rec abr24', 'OC NUEVAENE', 'TOTAL OC_ENE',
        #                                 'INV_FEB', 'Cantidad may24', 'Fal may24', 'Rec may24', 'OC NUEVAFEB', 'TOTAL OC_FEB']]
        #explosion_temp.columns = ['SKU', 'MP', 'PROVEEDOR', 'DIAS CRED', 'MP/ME', 'MOQ', 'Moneda', 'Costo', 'Existencia',
        #                          'REQ_SEP', 'B.O. SEP', 'OC TRANSIT SEP', 'OC NUEVA SEP', 'TOTAL OC SEP', 'INGRESO A1',
        #                          'INV_ENE', 'REQ_ENE', 'B.O. ENE', 'OC TRANSIT ENE', 'OC NUEVAENE', 'TOTAL OC_ENE',
        #                          'INV_FEB', 'REQ_FEB', 'B.O. FEB', 'OC TRANSIT FEB', 'OC NUEVAFEB', 'TOTAL OC_FEB',
        #                          'INV_DIC', 'REQ_DIC', 'B.O. DIC', 'OC TRANSIT DIC', 'OC NUEVADIC', 'TOTAL OC_DIC',
        #                          'INV_ENE', 'REQ_ENE', 'B.O. ENE', 'OC TRANSIT ENE', 'OC NUEVAENE', 'TOTAL OC_ENE',
        #                          'INV_FEB', 'REQ_FEB', 'B.O. FEB', 'OC TRANSIT FEB', 'OC NUEVAFEB', 'TOTAL OC_FEB' ]
        #ELIMINAMOS ENEUBRE
        #explosion_temp = explosion_temp[['SKU', 'MP_x', 'PROVEEDOR', 'DÍAS CRED', 'MP/ME', 'MOQ', 'Moneda', 'Costo', 'Existencia', 
        #                                 'INV_ENE', 'Cantidad ene24', 'Fal ene24', 'Rec ene24', 'OC NUEVAENE', 'TOTAL OC_ENE', 'Ingreso',
        #                                 'INV_FEB', 'Cantidad feb24', 'Fal feb24', 'Rec feb24', 'OC NUEVAFEB', 'TOTAL OC_FEB',
        #                                 'INV_DIC', 'Cantidad mar24', 'Fal mar24', 'Rec mar24', 'OC NUEVADIC', 'TOTAL OC_DIC',
        #                                 'INV_ENE', 'Cantidad abr24', 'Fal abr24', 'Rec abr24', 'OC NUEVAENE', 'TOTAL OC_ENE',
        #                                 'INV_FEB', 'Cantidad may24', 'Fal may24', 'Rec may24', 'OC NUEVAFEB', 'TOTAL OC_FEB']]
        #explosion_temp.columns = ['SKU', 'MP', 'PROVEEDOR', 'DIAS CRED', 'MP/ME', 'MOQ', 'Moneda', 'Costo', 'Existencia',
        #                          'INV_ENE', 'REQ_ENE', 'B.O. ENE', 'OC TRANSIT ENE', 'OC NUEVAENE', 'TOTAL OC_ENE', 'INGRESO A1',
        #                          'INV_FEB', 'REQ_FEB', 'B.O. FEB', 'OC TRANSIT FEB', 'OC NUEVAFEB', 'TOTAL OC_FEB',
        #                          'INV_DIC', 'REQ_DIC', 'B.O. DIC', 'OC TRANSIT DIC', 'OC NUEVADIC', 'TOTAL OC_DIC',
        #                          'INV_ENE', 'REQ_ENE', 'B.O. ENE', 'OC TRANSIT ENE', 'OC NUEVAENE', 'TOTAL OC_ENE',
        #                          'INV_FEB', 'REQ_FEB', 'B.O. FEB', 'OC TRANSIT FEB', 'OC NUEVAFEB', 'TOTAL OC_FEB' ]
        explosion_temp = explosion_temp[['SKU', 'MP_x', 'PROVEEDOR', 'DÍAS CRED', 'MP/ME', 'MOQ', 'Moneda', 'Costo', 'Existencia', 
                                         'Cantidad', 'Faltante mp', 'Rec dic23', 'OC NUEVA', 'TOTAL OC', 'Ingreso',
                                         'INV_ENE', 'Cantidad ene24', 'Fal ene24', 'Rec ene24', 'OC NUEVAENE', 'TOTAL OC_ENE',
                                         'INV_FEB', 'Cantidad feb24', 'Fal feb24', 'Rec feb24', 'OC NUEVAFEB', 'TOTAL OC_FEB',
                                         'INV_MAR', 'Cantidad mar24', 'Fal mar24', 'Rec mar24', 'OC NUEVAMAR', 'TOTAL OC_MAR',
                                         'INV_ABR', 'Cantidad abr24', 'Fal abr24', 'Rec abr24', 'OC NUEVAABR', 'TOTAL OC_ABR',
                                         'INV_MAY', 'Cantidad may24', 'Fal may24', 'Rec may24', 'OC NUEVAMAY', 'TOTAL OC_MAY']]
        explosion_temp.columns = ['SKU', 'MP', 'PROVEEDOR', 'DIAS CRED', 'MP/ME', 'MOQ', 'Moneda', 'Costo', 'Existencia',
                                  'REQ_DIC', 'B.O. DIC', 'OC TRANSIT DIC', 'OC NUEVADIC', 'TOTAL OC_DIC', 'ingresosa1',
                                  'INV_ENE', 'REQ_ENE', 'B.O. ENE', 'OC TRANSIT ENE', 'OC NUEVAENE', 'TOTAL OC_ENE',
                                  'INV_FEB', 'REQ_FEB', 'B.O. FEB', 'OC TRANSIT FEB', 'OC NUEVAFEB', 'TOTAL OC_FEB',
                                  'INV_MAR', 'REQ_MAR', 'B.O. MAR', 'OC TRANSIT MAR', 'OC NUEVAMAR', 'TOTAL OC_MAR',
                                  'INV_ABR', 'REQ_ABR', 'B.O. ABR', 'OC TRANSIT ABR', 'OC NUEVAABR', 'TOTAL OC_ABR',
                                  'INV_MAY', 'REQ_MAY', 'B.O. MAY', 'OC TRANSIT MAY', 'OC NUEVAMAY', 'TOTAL OC_MAY', ]
            
        st.write(explosion_temp)
        st.download_button(label="Descargar", data=explosion_temp.to_csv(), mime="text/csv")
        st.info(frase, icon='💵')

    
        
    #st.balloons()
    
    #st.write(requi2)

if __name__ == '__main__':
    main()
