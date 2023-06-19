import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import altair as alt
from datetime import datetime
import re


def main():
    img = Image.open('logo_farmiral.jpg')
    col1, col2, col3 = st.columns([5,10,1])
    with col1:
        st.write("")
	
    with col2:
        st.image(img,width=250)
    with col3:
        st.write("")
	#Cargamos las bases que vamos a utilizar desde aqui    
    df_formulas = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/formulas.csv',encoding='latin-1')
    df_productos = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/productos.csv',encoding='latin-1')

    #Quitamos espacios a los nombres de las columnas
    df_formulas.columns = df_formulas.columns.str.strip()
    df_productos.columns = df_productos.columns.str.strip()

    #Filtramos solo las columnas que necesitamos de cada base
    df_formulas = df_formulas[['Cve_copr', 'Cve_prod', 'Can_copr', 'Tip_copr', 'New_med', 'New_copr', 'Partida', 'Undfor', 
                                'Desc_prod', 'Cve_mon', 'Cve_tial', 'Tipcam', 'Tip_cam', 'Ren_copr', 'Cto_ent', 'Uncfor']]
    df_productos = df_productos[['Cve_prod', 'Desc_prod', 'Uni_med', 'Cto_ent', 'Cve_tial']]

    #Quitamos los posibles espacios sobrantes de cada columna
    df_formulas['Cve_prod'] = df_formulas['Cve_prod'].str.strip()    
    df_formulas['Cve_copr'] = df_formulas['Cve_copr'].str.strip()
    df_formulas['New_med'] = df_formulas['New_med'].str.strip()
    df_formulas['New_copr'] = df_formulas['New_copr'].str.strip()
    df_formulas['Undfor'] = df_formulas['Undfor'].str.strip()
    df_formulas['Desc_prod'] = df_formulas['Desc_prod'].str.strip()
    df_formulas['Uncfor'] = df_formulas['Uncfor'].str.strip()
    df_productos['Cve_prod'] = df_productos['Cve_prod'].str.strip()
    df_productos['Desc_prod'] = df_productos['Desc_prod'].str.strip()
    df_productos['Uni_med'] = df_productos['Uni_med'].str.strip()

    #Titulo del documento
    st.title('Costos Farmiral')

    #Seleccionar si se va a consultar costos desglosados o costear
    if st.checkbox("Costos desglosados"):
    #Hacemos merge con los nombres de las formulas para facilitar la busqueda del producto a costear
        df_formulas_n = df_formulas.merge(df_productos.rename({'Desc_prod':'Formula'},axis=1), left_on='Cve_copr', 
            right_on='Cve_prod', how='left')
        df_formulas_n.columns = ['SKU', 'Componente', 'Cantidad', 'Tipo', 'Atributo', 'Version pt', 'Partida', 'Unidad componente'
                                    , 'Nombre', 'Cve_mon', 'Tipo_x', 'Tipcam','Tip_cam', 'Rendimiento','Costo', 'Unidad'
                                    , 'Cve_prod_y', 'Formula', 'Unidad pt', 'Cto_ent_y', 'Tipo_prod']
        #Eliminamos las versiones V1, V2, V3 y V4
        df_formulas_n = df_formulas_n.loc[(df_formulas_n['Version pt']!='V1') & (df_formulas_n['Version pt']!='V2') 
            & (df_formulas_n['Version pt']!='V3') & (df_formulas_n['Version pt']!='V4')]
        #Creamos el filtro para seleccionar la formula a análizar
        df_formulas_prueba = df_formulas_n[df_formulas_n.SKU.str.startswith('51')].reset_index()
        formula = st.selectbox('Formula', df_formulas_prueba['Formula'].sort_values().unique())        
        #Esta tabla nos da todo lo que contiene la formula "51"
        pt = df_formulas_n[df_formulas_n.Formula == formula]
        pt = pt[pt.SKU.str.startswith('51')].reset_index()
        #Nos quedamos solo con las columnas necesarias de la base
        pt = pt[['SKU','Componente','Nombre','Cantidad','Costo','Unidad componente','Rendimiento','Unidad pt']]
        #Calculamos cantidades y costos unitarios
        pt['Cantidad'] = pt['Cantidad']/pt['Rendimiento']
        pt['Costo total'] = pt['Cantidad'] * pt['Costo']
        #Filtramos la tabla pt para obtener todos los materiales que se utilizan en el semiterminado
        semt = pt[pt.Componente.str.startswith('41')]['Nombre'].reset_index()
        #Obtenemos del filtro un simple valor para usar en la extracción de componentes
        semt = semt.iloc[0]['Nombre']
        semit = df_formulas_n[df_formulas_n.Formula == semt]
        semit = semit[semit.SKU.str.startswith('41')].reset_index()
        semit = semit[['SKU','Componente','Nombre','Cantidad','Costo','Unidad componente','Rendimiento','Unidad pt']]
        semit['Cantidad'] = semit['Cantidad']/semit['Rendimiento']
        semit['Costo total'] = semit['Cantidad'] * semit['Costo']
        st.subheader('Costos')
        col1, col2 = st.columns([15,15])
        with col1:
            st.write('Rendimiento: ' ,pt.iloc[0]['Rendimiento'])
            st.write('Unidad Base: ' ,pt.iloc[0]['Unidad pt'])    
        with col2:
            costo_n1 = semit.groupby(['SKU']).agg({'Costo total':'sum'}).iloc[0]['Costo total']
            cantidad_n1 = pt[pt.Componente.str.startswith('41')]['Cantidad'].reset_index().iloc[0]['Cantidad']
            costo_total_n1 = costo_n1 * cantidad_n1
            costo_total_pt = pt.groupby(['SKU']).agg({'Costo total':'sum'}).iloc[0]['Costo total']
            st.write('Costo nivel 1: $' ,round(costo_total_n1 ,2))
            st.write('Costo ME: $' , round(costo_total_pt - costo_total_n1,2))
            st.write('Costo total: $' , round(costo_total_pt,2))
        left, right = st.columns([20,20])
        with left:
            #Con esta instrucción permitimos a altair mostrar la gráfica aunque tenga mas de 5000 renglones
            alt.data_transformers.enable('default', max_rows=None)
            chart_pt = pt.groupby(['Componente','Nombre']).agg({'Costo total':'sum'}).reset_index()
            pie_pt = alt.Chart(chart_pt, title='Costos pt').mark_arc().encode(
                                theta=alt.Theta(field='Costo total', type="quantitative"),
                                color=alt.Color(field='Nombre', type="nominal"),
                                tooltip = ['Nombre','Costo total']
                                )
            #Mostramos el objeto en streamlit
            st.altair_chart(pie_pt, use_container_width=True)
        with right:
            #Con esta instrucción permitimos a altair mostrar la gráfica aunque tenga mas de 5000 renglones
            alt.data_transformers.enable('default', max_rows=None)
            chart_st = semit.groupby(['Componente','Nombre']).agg({'Costo total':'sum'}).reset_index()
            pie_st = alt.Chart(chart_st, title='Costos st').mark_arc().encode(
                                theta=alt.Theta(field='Costo total', type="quantitative"),
                                color=alt.Color(field='Nombre', type="nominal"),
                                tooltip = ['Nombre','Costo total']
                                )
            #Mostramos el objeto en streamlit
            st.altair_chart(pie_st, use_container_width=True)

        st.subheader('Materiales Producto Terminado por unidad')
        st.write(pt)
        st.subheader('Materiales Semiterminado por unidad')
        st.write(semit)
        #st.write(semt)

    if st.checkbox('Formulador'):
        #st.warning('Formulador en construcción')
        nombre_producto = st.text_input('Nombre del producto a formular')
        materias_lista = st.multiselect('Materia Prima', df_productos['Desc_prod'].sort_values().unique())
        df_filtered = df_productos[df_productos['Desc_prod'].isin(materias_lista)]
        df_formulador = df_filtered[['Cve_prod', 'Desc_prod', 'Uni_med', 'Cto_ent']]
        df_formulador.columns = ['SKU','Materia prima','Unidad','Costo']
        duplist = df_productos[df_productos.duplicated('Desc_prod')]
        cantidades_lista = st.text_input('Ingresa las cantidades necesarias por unidad en orden separados por una coma (,)')
        c_lista = re.split(",",cantidades_lista)
        unidad_caja = st.text_input('Cuantas unidades contiene la presentación')
        if len(unidad_caja) != 0: 
            unidad_caja = float(unidad_caja)
        unidad_lote = st.text_input('Cuantas unidades contiene el lote de producción')
        if len(unidad_lote) != 0:
            unidad_lote = float(unidad_lote)
        margen = st.text_input('Cual será el margen de costo para el precio')
        if len(margen) != 0:
            margen = float(margen)
        n_lista=[]
        #Tiene un +1 en lo que se resuelve lo de los duplicados
        if len(cantidades_lista) != 0:
           for i in range(len(materias_lista)+1):
               n = float(c_lista[i])
               n_lista.append(n)
        df_formulador['Cantidad'] = n_lista
        df_formulador['Costo unitario'] = df_formulador['Costo'] * df_formulador['Cantidad']
        df_formulador['Costo caja'] = [i * unidad_caja for i in df_formulador['Costo unitario']]
        df_formulador['Costo lote'] = [i * unidad_lote for i in df_formulador['Costo unitario']]

        #Con esta instrucción permitimos a altair mostrar la gráfica aunque tenga mas de 5000 renglones
        alt.data_transformers.enable('default', max_rows=None)
        chart_formulador = df_formulador.groupby(['SKU','Materia prima']).agg({'Costo unitario':'sum'}).reset_index()
        pie_formulador = alt.Chart(chart_formulador, title=nombre_producto).mark_arc().encode(
                                theta=alt.Theta(field='Costo unitario', type="quantitative"),
                                color=alt.Color(field='Materia prima', type="nominal"),
                                tooltip = ['Materia prima','Costo unitario']
                                )

        st.write(df_formulador)
        st.altair_chart(pie_formulador, use_container_width=True) 



if __name__ == '__main__':
    main()
  



