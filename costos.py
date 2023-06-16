import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import altair as alt
from datetime import datetime
from colorama import init,Fore,Back,Style


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
        st.write()
        #Eliminamos las versiones V1, V2, V3 y V4
        df_formulas_n = df_formulas_n.loc[(df_formulas_n['Version pt']!='V1') & (df_formulas_n['Version pt']!='V2') 
            & (df_formulas_n['Version pt']!='V3') & (df_formulas_n['Version pt']!='V4')]
        #Creamos el filtro para seleccionar la formula a análizar
        formula = st.selectbox('Formula', df_formulas_n['Formula'].unique())
        #Esta tabla nos da todo lo que contiene la formula "51"
        pt = df_formulas_n[df_formulas_n.Formula == formula]
        pt = pt[pt.SKU.str.startswith('51')]
        #Nos quedamos solo con las columnas necesarias de la base
        pt = pt[['SKU','Componente','Cantidad','Unidad componente','Nombre','Rendimiento','Costo','Unidad pt']]
        #Filtramos la tabla pt para obtener todos los materiales que se utilizan en el semiterminado
        semt = pt[pt.Componente.str.startswith('41')]['Nombre']
        #Obtenemos del filtro un simple valor para usar en la extracción de componentes
        semt = semt.iloc[0]
        semit = df_formulas_n[df_formulas_n.Formula == semt]
        semit = semit[semit.SKU.str.startswith('41')]
        st.subheader('Costos Producto terminado')
        st.write(pt)
        st.subheader('Costos Semiterminado')
        st.write(semit)


    if st.checkbox('Formulador'):
        st.write(df_productos.head(5))

#    col1, col2 = st.columns([15,15])
#    with col1:
#        st.write(df_formulas.head(5))
#    with col2:
#        st.write(df_productos.head(5))
if __name__ == '__main__':
    main()
  



