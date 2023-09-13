import pandas as pd 
import streamlit as st 
from PIL import Image
import altair as alt
import numpy as np
from datetime import datetime,timedelta
import re 

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

    fcst_faltantes = t_forecast[['SKU', 'Producto','Sep23', 'Oct23', 'Nov23', 'Dic23', 'Ene23', 'Feb24', 'Forecast anual', 'Faltantes', 'Existencia']]
    fcst_faltantes = fcst_faltantes[fcst_faltantes['Faltantes']>0]

    #st.write(fcst_faltantes)
    ###############fcst faltantes es el forecast con sus faltantes a nivel pt

    ### EXISTENCIAS MATERIAS PRIMAS ###
    existeN = existencias[['Cve_prod', 'Lugar', 'Desc_prod','Existencia']]
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
    existeN_aspen = existeN[(existeN['Lugar'] == 'ASPEN')]                        
    existeN_simi = existeN[(existeN['Lugar'] == 'SIMILARES')]  
    existeN_grisi = existeN[(existeN['Lugar'] == 'G2') |
                          (existeN['Lugar'] == 'G1')]
    #General
    existeN_comp.columns = ['SKU', 'Lugar', 'MP', 'Existencia']
    existeN_comp['SKU'] = existeN_comp['SKU'].str.strip()
    existeN_comp = existeN_comp.groupby(['SKU']).agg({'Existencia':'sum'}).reset_index()
    #Aspen
    existeN_aspen.columns = ['SKU', 'Lugar', 'MP', 'Existencia']
    existeN_aspen['SKU'] = existeN_aspen['SKU'].str.strip()
    existeN_aspen = existeN_aspen.groupby(['SKU']).agg({'Existencia':'sum'}).reset_index()
    #Simi
    existeN_simi.columns = ['SKU', 'Lugar', 'MP', 'Existencia']
    existeN_simi['SKU'] = existeN_comp['SKU'].str.strip()
    existeN_simi = existeN_simi.groupby(['SKU']).agg({'Existencia':'sum'}).reset_index()
    #grisi
    existeN_grisi.columns = ['SKU', 'Lugar', 'MP', 'Existencia']
    existeN_grisi['SKU'] = existeN_grisi['SKU'].str.strip()
    existeN_grisi = existeN_grisi.groupby(['SKU']).agg({'Existencia':'sum'}).reset_index()
    #st.write(existeN_comp)
    ###############
    #st.write(formulas)
    pedir_fcst = fcst_faltantes.merge(formulas, on='SKU', how='left')
    #st.write(pedir_fcst)
    pedir_fcst = pedir_fcst.dropna()
    #st.write(pedir_fcst)
    pedir_fcstme = pedir_fcst[pedir_fcst['Cve_prod'].str.startswith('M')].reset_index(drop=True)
    pedir_fcstme['Faltantes me'] = pedir_fcstme['Faltantes'] * pedir_fcstme['Cantidad']
    pedir_fcstst = pedir_fcst[pedir_fcst['Cve_prod'].str.startswith('41')].reset_index(drop=True)
    pedir_fcstst.rename(columns = {'SKU':'SKU_f', 'Cve_prod':'SKU'}, inplace=True)
    pedir_fcstst['SKU'] = pedir_fcstst['SKU'].str.strip()
    pedir_fcstst = pedir_fcstst.merge(formulas, on='SKU', how='left')
    pedir_fcstst['Cantidad_y'] = pedir_fcstst['Cantidad rendimiento_y'] / pedir_fcstst['Rendimiento_x']
    pedir_fcstst['Cantidad mp'] = pedir_fcstst['Cantidad_y'] * pedir_fcstst['Faltantes']
    pedir_fcstst = pedir_fcstst[['Producto_x', 'Faltantes', 'MP_y', 'Cantidad mp', 'Sep23', 'Oct23', 'Nov23', 'Dic23', 'Ene23', 'Feb24', 'Forecast anual']]
    pedir_fcstst.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'Sep23', 'Oct23', 'Nov23', 'Dic23', 'Ene23', 'Feb24', 'Forecast anual']
    pedir_fcstme = pedir_fcstme[['Producto_x', 'Faltantes', 'MP', 'Faltantes me', 'Sep23', 'Oct23', 'Nov23', 'Dic23', 'Ene23', 'Feb24', 'Forecast anual']]
    pedir_fcstme.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'Sep23', 'Oct23', 'Nov23', 'Dic23', 'Ene23', 'Feb24', 'Forecast anual']
    pedir2 = pd.concat([pedir_fcstst, pedir_fcstme])
    pedir2['MP'] = pedir2['MP'].str.strip()
    ######################################################################################################
    prods = productos[['Cve_prod', 'Desc_prod']]
    prods.columns = ['SKU', 'MP']
    pedir2 = pedir2.merge(prods, on='MP', how='left')
    #st.write(pedir2)
    ######################################################################################################
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
    

    #st.write(requi2)

#####################################################################################################################################
    # creo un dataframe vacio con una columna llamada mes
    mes= pd.DataFrame(columns=['Mes'])
    #Filtro las columnas que necesito
    df_compras = compras[['F_alta_ped','Cve_prod','Desc_prod', 'Nom_prov', 'F_ent','Cant_prod','Cant_surtp','Valor_prod',
                          'Des_mon', 'Status', 'Status_aut']]
    # hago un substring que me de solo los numeros del mes 
    mes['Mes'] = df_compras['F_ent'].str[3:5]
    # concateno el mes con mi dataframe df_compras
    df_compras = pd.concat([df_compras,mes], axis=1)

    # Cant_prod - Cant_surtp
    x_entregar = df_compras['Cant_prod'] - df_compras['Cant_surtp']
    df_compras = pd.concat([df_compras,x_entregar], axis=1)
    df_compras.columns=['F_alta_ped','Cve_prod','Desc_prod', 'Nom_prov', 'F_ent','Cant_prod','Cant_surtp','Valor_prod',
                        'Des_mon', 'Status', 'Status_aut', 'Mes','X_Entregar']
    
    df_compras = df_compras[['F_alta_ped', 'Cve_prod','Desc_prod', 'Nom_prov','X_Entregar','Cant_surtp','Cant_prod',
                             'Status', 'Status_aut', 'F_ent','Mes','Valor_prod','Des_mon']]
    for i in range(len(df_compras.loc[:,'F_ent'])):
        try:
            df_compras.loc[i,'F_ent'] = pd.to_datetime(df_compras.loc[i,'F_ent'], format='%d/%m/%Y')
        except ValueError:
            df_compras.loc[i, 'F_ent'] = pd.to_datetime(df_compras.loc[i, 'F_alta_ped'], format='%d/%m/%Y')
    
    df_compras = df_compras[['Cve_prod','Desc_prod', 'Nom_prov','X_Entregar','Cant_surtp','Cant_prod', 
                             'Status', 'Status_aut', 'F_ent','Mes','Valor_prod','Des_mon']]
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
        st.write(existeN_grisi)
    if st.checkbox('Almacenes Aspen'):
        st.write(existeN_aspen)
    if st.checkbox('Almacenes Similares'):
        st.write(existeN_simi)
    if st.checkbox('Ordenes de compra'):
        st.write(df_compras)

    explosion = requi2.copy()
    prods = productos[['Cve_prod', 'Desc_prod', 'Cve_monc']]
    prods.columns = ['SKU', 'MP', 'Moneda']
    explosion = explosion.merge(prods, on='MP', how='left')
    #st.write(requi2)
    explosion = explosion.fillna(0)
    explosion = explosion[['SKU', 'MP', 'Moneda', 'Costo', 'Existencia', 'Cantidad', 'Faltante mp']]
    explosion['Faltante mp'] = explosion['Cantidad'] - explosion['Existencia']
    explosion['Faltante mp'][(explosion['Faltante mp'] < 0)] = 0
    tc = st.text_input('Tipo de cambio', '17.00')
    tc = float(tc)
    for i in range(len(explosion['SKU'])):
        if explosion.loc[i,'Moneda'] == 2:
            explosion.loc[i,'Costo'] = tc * explosion.loc[i,'Costo']
    recepcion = df_compras.copy()
    recepcion = recepcion.groupby(['Cve_prod']).agg({'X_Entregar':'sum'}).reset_index()
    recepcion.columns = ['SKU', 'X_Entregar']
    explosion = explosion.merge(recepcion, on='SKU', how='left')
    explosion = explosion.fillna(0)
    explosion['Costo total'] = explosion['Faltante mp'] * explosion['Costo']
    #st.write(df_compras)
    st.write(explosion)
    inversionmes = explosion['Costo total'].sum()
    frase = 'Inversión total del mes $' + str(round(inversionmes,2))
    st.info(frase, icon='💵')

    #st.balloons()
    
    #st.write(requi2)

if __name__ == '__main__':
    main()
