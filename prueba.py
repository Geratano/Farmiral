import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

#Cambiamos el directorio en terminal para darle 
#la ruta de imagen
img = Image.open('logo_farmiral.jpg')

#Separamos en 3 columnas la linea donde imprimira
#la imagen para centrarla
col1, col2, col3 = st.columns([5,10,1])
with col1:
	st.write("")

with col2:
	st.image(img,width=250)
with col3:
	st.write("")


col1, col2, col3 = st.columns([3,10,1])
with col1:
	st.write("")

with col2:
	st.title("Tablero de control")
with col3:
	st.write("")


#Leeremos la base de datos desde Github con pandas
#Usamos el encoding latin-1 porque si no arroja error
#ya que puede haber "ñ's" o acentos
df = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/base.csv',encoding='latin-1')
#Quitamos espacios a los nombres de columnas
df.columns = df.columns.str.strip()
#Filtramos la base para obtener solo las columnas
#importantes
df_ventas = df[['No_fac','Falta_fac','Subt_fac','Cve_factu','Cse_prod','Cant_surt','Lugar','Costo','Utilidad_mov','Margen',
'Categoria','Canal_prod','Canal_cliente','KAM','Subdirec','N_cred','Anio','Mes','Dia','Nom_cliente','Producto']]

#imprimimos como prueba los primeros cinco datos de la tabla
if st.checkbox("Raw data"):
	st.write(df_ventas.head(5))

#Separamos en dos frames de lado izquiero los filtros
#De lado derecho imprimiremos la tabla filtrada
st.sidebar.title("Filtros")	
emp_list =	st.sidebar.multiselect("Empresa", df_ventas['Cve_factu'].unique())
alm_list =  st.sidebar.multiselect("Almacén", df_ventas['Lugar'].unique())
ano_list =  st.sidebar.multiselect("Año", sorted(df_ventas['Anio'].unique()))
mes_list =  st.sidebar.multiselect("Mes", sorted(df_ventas['Mes'].unique()))
cte_list =  st.sidebar.multiselect("Cliente", sorted(df_ventas['Nom_cliente'].unique()))

	# if st.checkbox("Aplicar Filtros"):
if not emp_list:
	emp_list =	df_ventas['Cve_factu'].unique()
if not alm_list:
	alm_list = df_ventas['Lugar'].unique()
if not ano_list:
	ano_list = df_ventas['Anio'].unique()
if not mes_list:
	mes_list = df_ventas['Mes'].unique()
if not cte_list:
	cte_list = df_ventas['Nom_cliente'].unique()	
 
df_filtered = df_ventas[(df_ventas['Cve_factu'].isin(emp_list)) & (df_ventas['Lugar'].isin(alm_list)) & (df_ventas['Anio'].isin(ano_list)) & 
(df_ventas['Mes'].isin(mes_list)) & (df_ventas['Nom_cliente'].isin(cte_list))]


st.write(df_filtered.head(5))

