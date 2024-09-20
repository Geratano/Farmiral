import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import altair as alt
from datetime import datetime
import re

st.set_page_config(layout="wide")
img = Image.open('logo_farmiral.jpg')

colm1, colm2, colm3 = st.columns([5,10,1])
with colm1:
    st.write("")
with colm2:
    st.image(img,width=250)
with colm3:
    st.write("")

Encabezados={'Unnamed: 0':'Fecha','Unnamed: 1':'Factura','Unnamed: 2':'Beneficiario','Unnamed: 3':'Concepto','Unnamed: 4':'Ingreso','Unnamed: 5':'Egreso','Unnamed: 6':'Saldo','Unnamed: 7':'Conc','Unnamed: 8':'Cuenta','Unnamed: ':'Banco'}
Seleccion_enc=['Fecha','Factura','Beneficiario','Concepto','Ingreso','Egreso','Saldo','Conc','Cuenta','Banco']

biacora_url = f'https://docs.google.com/spreadsheets/d/e/2PACX-1vRByl7w0s3x_vE3BvsOC-7fXv7025hX-WZsbN0PUjWXQBzwTpgotB87GOZixUZ94A/pub?gid=1234439197&single=true&output=csv'
df_bitacora_costos = pd.read_csv(biacora_url,encoding='utf-8')

@st.cache_resource
def baseconbranza():
    cobranza_url=f'https://raw.githubusercontent.com/Geratano/Farmiral/main/cobranza.csv'
    df_cobranza = pd.read_csv(cobranza_url,encoding='latin-1')
    return df_cobranza
df_cobranza = baseconbranza()

def base_drive():
    bancos_url= f'https://docs.google.com/spreadsheets/d/e/2PACX-1vRCsZMLswLp_uNDwYdoYYbEHeaG1pfN_MBTNZ-_mPI_g5LzbLocV2tR5-XpT6e_RA/pub?gid=574013258&single=true&output=csv' 
    temp= pd.read_csv(bancos_url) 
    temp.columns=temp.columns.str.strip() # quito espacios en blanco 
    temp.rename(columns=Encabezados,inplace=True) # renombro los encabezados 
    temp=temp[Seleccion_enc] # selecciono solo los encabezados que necesito
    return temp



def limpiar(s):
    if isinstance(s,str): # si los datos son de tipo sting
        s = s.strip() # eliminar espacios al inicio y al final
        if s == "-": # si el dato solo es un signo menos
            return 0 # reemplazar por cero
        s = re.sub(r'\s+', '', s) # eliminar todos los espacios
        s= s.replace('.','') # Eliminar los puntos 
        s= s.replace(',','.') # remplazar comas por puntos
        return s    
    
df_bancos = base_drive() #llamo la funcioin base drive

df_bancos['Ingreso']= df_bancos['Ingreso'].apply(limpiar) # aplico la funcion limpiar 
df_bancos['Ingreso']=pd.to_numeric(df_bancos['Ingreso']) # convierto a numero 

df_bancos['Egreso']= df_bancos['Egreso'].apply(limpiar)
df_bancos['Egreso']=pd.to_numeric(df_bancos['Egreso'])

df_bancos['Saldo']= df_bancos['Saldo'].apply(limpiar)
df_bancos['Saldo']=pd.to_numeric(df_bancos['Saldo'])

# funcion donde traigo el saldo actual capturado 
def saldo_banco(banco): # recibo como paramatro el nombre del banco 
    # utilizo la funcion loc para localiza la coincidencia en la columna banco, tomando en cuenta el nombre del banco, despues filtro solo por la columna saldo y me traigo el ultimo valor de la seleccion
    saldo = df_bancos.loc[df_bancos['Banco'] == banco]['Saldo'].tail(1).values[0]
    return saldo # retorno el resultado

# me creo un diccionario en el cual va a tener los bancos y los los saldos de cada banco haciendo uso de la funcion saldo_banco para cada caso
saldos={'Bancos':['Santander','Banorte','Banregio','Banco base','Mifel','Farmiral SA','Icm','STP Farmiral','Banregio Xanalab',
                  'Banco base Xanalab','Santander Xanalab','Mifel Xanalab','STP Xanalab','Banco base anterior','Banregio icm'], 

        'Saldos':[saldo_banco('santander_far'),saldo_banco('banorte_far'),saldo_banco('banregio_far'),saldo_banco('bbase_far'),
                  saldo_banco('mifel_far'),saldo_banco('sa_far'),saldo_banco('icm_far'),saldo_banco('stp_far'),saldo_banco('banregio_xana'),
                  saldo_banco('bbase_xana'), saldo_banco('santander_xana'), saldo_banco('mifel_xana'), saldo_banco('stp_xana')
                  , saldo_banco('bbase_ant'), saldo_banco('banregio_icm')]}

df_saldos = pd.DataFrame(saldos) # convierto el diccionario en un dataframe
total_saldos= round(df_saldos['Saldos'].sum(),2) # sumo la columna saldos del nuevo dataframe

df_bancos['Fecha']= pd.to_datetime(df_bancos['Fecha'], dayfirst=True) #convierto la fecha indicando que inician por el día
df_bancos['Semana']=df_bancos['Fecha'].dt.isocalendar().week # creo la columna semana y me traigo la semana del año
df_bancos['Mes']=df_bancos['Fecha'].dt.month # creo la columna mes y me traigo elmes del año 
df_bancos['Año']=df_bancos['Fecha'].dt.year.astype(int) # creo la columna año y me traigo el año

# quitar los espacios en los titulos de las columnas
df_cobranza.columns= df_cobranza.columns.str.strip() 
df_bitacora_costos.columns=df_bitacora_costos.columns.str.strip()
df_cobranza['Nom_cte']=df_cobranza['Nom_cte'].str.strip()

df_cobranza.rename(columns={'No_fac':'FACTURA'},inplace=True) # renombro la columna No_fac para hacer merge
df_cobranza['FACTURA']=df_cobranza['FACTURA'].astype(str) # convierto la columna factura a str
df_bitacora_costos['FACTURA'] = df_bitacora_costos['FACTURA'].fillna(0) # si hay vacio se pone un 0
df_bitacora_costos['FACTURA'] = df_bitacora_costos['FACTURA'].astype(int) # convierto en entero para quitar el .00 en los registros 
df_bitacora_costos['FACTURA'] = df_bitacora_costos['FACTURA'].astype(str) # convierto a str para hacer merge
todo = pd.merge( df_bitacora_costos,df_cobranza, how= 'inner', on= 'FACTURA') # junto las 2 bases con merge
todo['FECHA DE ENTREGA'] = pd.to_datetime(todo['FECHA DE ENTREGA']).dt.date # la fecha de entrega esta com str, la convierto a fecha 
todo['FECHA VENCIMIENTO']= todo['FECHA DE ENTREGA'] + pd.to_timedelta(todo['Dia_cre'], unit='D') # hago la suma de la fecha de entrega mas los días de credito
st.write(todo)
todo = todo[['Nom_cte','FACTURA','Saldo_fac','Falta_fac','FECHA DE ENTREGA','FECHA VENCIMIENTO']]
st.write("todo",todo)

col1,col2,col3 = st.columns([5,5,5])
with col1:
    st.write("")
with col2:
    st.write("Resumen",df_saldos)
    st.write("total",total_saldos)
with col3:
    st.write("")

if st.checkbox('Movimientos'):
    col1,col2 = st.columns([20,80])
    with col1:
        df_filtrado = df_bancos
        if st.checkbox('Año',value=True):
            year = df_filtrado['Año'].sort_values().unique() # ordenamos el año
            selec_year=st.selectbox('Año',year,index=len(year)-1) # creamos la seleccion mostrando el año mas reciente
            df_filtrado= df_filtrado.loc[df_filtrado['Año']==selec_year] # filtramos por coincidencia
        if st.checkbox('Mes',value=True):
            mes= df_filtrado['Mes'].sort_values().unique()
            selec_mes= st.selectbox('Mes',mes, index=len(mes)-1) # creamos la seleccion 
            df_filtrado = df_filtrado.loc[df_filtrado['Mes']==selec_mes] # filtramos por coinsidencias
        if st.checkbox('Semana',value=True):
            semana= df_filtrado['Semana'].sort_values().unique()
            selec_sem = st.selectbox('Semana',semana,index=len(semana)-1)
            df_filtrado= df_filtrado.loc[df_filtrado['Semana']==selec_sem]
        if st.checkbox('Concepto'):
            selec_concepto = st.multiselect('Concepto',df_filtrado['Concepto'].sort_values().unique())
            df_filtrado = df_filtrado[df_filtrado['Concepto'].isin(selec_concepto)]
    with col2:
        df_filtrado['Fecha']=df_filtrado['Fecha'].dt.date
        st.write("Filtrado",df_filtrado)

