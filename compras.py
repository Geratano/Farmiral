import pandas as pd 
import streamlit as st 
from PIL import Image
import altair as alt
import numpy as np
from datetime import datetime,timedelta
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

    @st.cache_resource
    def load_compras():
        compras = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/compras.csv',encoding='latin-1')
        return compras
    compras = load_compras()

    compras.columns = compras.columns.str.strip()
    compras['Cve_prod'] = compras['Cve_prod'].str.strip()
    compras['Desc_prod'] = compras['Desc_prod'].str.strip()
    compras['Nom_prov'] = compras['Nom_prov'].str.strip()

    df_compras = compras[['Cve_prod','Desc_prod', 'Nom_prov', 'F_ent','Cant_prod','Cant_surtp','Valor_prod','Des_mon']]

    df_compras['F_ent'] = pd.to_datetime(df_compras['F_ent'], format='%d-%m-%Y')

    st.write(df_compras)

if __name__ == '__main__':
    main()
