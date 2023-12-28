import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import altair as alt
from datetime import datetime, timedelta, date
#import streamlit_card as st_card
import millify
from millify import millify
from millify import prettify
#from zoneinfo import ZoneInfo
import pytz

st.set_page_config(layout="wide")


def main():	
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


	col1, col2, col3 = st.columns([5,10,1])
	with col1:
		st.write("")

	with col2:
		st.title("KPI'S")
	with col3:
		st.write("")


	@st.cache_resource
	def Canalcte():
		canal = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/canalcliente.csv',encoding='latin-1')
		return canal
	canal = Canalcte()
	@st.cache_resource
	def Factura():
		facturas = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/factura.csv',encoding='latin-1')
		return facturas
	facturas = Factura()
	@st.cache_resource
	def descuentos():
		desc = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/descuentos.csv',encoding='latin-1')
		return  desc
	descuento = descuentos()
	@st.cache_resource
	def tipocred():
		tipo = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/tipocred.csv',encoding='latin-1')
		return  tipo
	tipo = tipocred()
	@st.cache_resource
	def devoluciones():
		dev = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/devoluciones.csv',encoding='latin-1')
		return  dev
	devolucion = devoluciones()
	@st.cache_resource
	def Productos():
		prod = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/productos.csv',encoding='latin-1')
		return prod
	productos = Productos()


	mes_diccioanrio = { 1:'ene', 2:'feb', 3:'mar', 4:'abr', 5:'may',6:'jun',
		    			7:'jul',8:'ago',9:'sep',10:'oct',11:'nov',12:'dic'}
	#Tratamiento base canal
	canal.columns = canal.columns.str.strip()
	canal['CLIENTE'] = canal['CLIENTE'].str.strip()
	canal['Canal'] = canal['Canal'].str.strip()
	canal = canal[['Cve_cte', 'CLIENTE', 'Canal']]
	canal.columns = ['Cve_cte', 'Cliente_c', 'Canal']
	canal = canal.fillna(0)
	
	#Tratamiento base facturas
	facturas.columns = facturas.columns.str.strip()
	facturas['Cve_factu'] = facturas['Cve_factu'].str.strip()
	facturas['Cve_prod'] = facturas['Cve_prod'].str.strip()
	facturas['Nom_fac'] = facturas['Nom_fac'].str.strip()
	facturas['Desc_prod'] = facturas['Desc_prod'].str.strip()
	facturas = facturas[['No_fac', 'Falta_fac', 'Subt_fac', 'Total_fac', 'Cve_factu', 'Cve_prod', 'Valor_prod', 'Cant_surt', 'Cve_cte', 'Nom_fac', 
						 'Desc_prod', 'Cost_prom']]
	facturas.columns = ['No_fac', 'Fecha', 'Venta ($)', 'Total_fac', 'Cve_factu', 'SKU', 'Precio', 'Venta (PZA)', 'Cve_cte', 'Cliente', 'Producto', 'Cost_prom']
	facturas['Fecha'] = pd.to_datetime(facturas['Fecha'], format='%d/%m/%Y')
	facturas['Año'] = facturas['Fecha'].dt.year
	facturas['Mes'] = facturas['Fecha'].dt.month
	facturas['Mes2'] = pd.to_datetime(facturas['Fecha'], format='%d/%m/%Y').dt.strftime('%Y-%m')
	facturas = facturas.fillna(0)
	ventas = facturas.merge(canal, on='Cve_cte', how='left')
	ventas['Cliente_c'] = ventas['Cliente_c'].fillna('OTROS DISTRIBUIDORES')
	ventas['Canal'] = ventas['Canal'].fillna('OTROS DISTRIBUIDORES')
	
	#Tratamiento base tipo
	tipo.columns = tipo.columns.str.strip()
	tipo['Cve_ncre'] = tipo['Cve_ncre'].str.strip()
	tipo['Nom_ncre'] = tipo['Nom_ncre'].str.strip()
	tipo['INCLUYE'] = tipo['INCLUYE'].str.strip()
	tipo = tipo.fillna(0)

	#Tratamiento base descuento
	descuento.columns = descuento.columns.str.strip()
	descuento['No_nota'] = descuento['No_nota'].str.strip()
	descuento['Nom_cte'] = descuento['Nom_cte'].str.strip()
	descuento['Cve_ncre'] = descuento['Cve_ncre'].str.strip()
	descuento = descuento[['No_nota', 'Fecha', 'Cve_factu', 'Tot_nota', 'Nom_cte', 'No_cliente', 'Subtotal', 'Cve_ncre']]
	descuento.columns = ['No_nota', 'Fecha_desc', 'Cve_factu', 'Descuento', 'Cliente', 'Cve_cte', 'Subtotal', 'Cve_ncre']
	descuento['Fecha_desc'] = pd.to_datetime(descuento['Fecha_desc'], format='%d/%m/%Y')
	descuento['Año'] = descuento['Fecha_desc'].dt.year
	descuento['Mes'] = descuento['Fecha_desc'].dt.month
	descuento = descuento.fillna(0)
	descuento = descuento.groupby(['Año', 'Mes', 'Cve_cte', 'Cliente', 'Cve_ncre']).agg({'Descuento':'sum',
															             	 'Subtotal':'sum'}).reset_index()
	descuento = descuento.merge(tipo, on='Cve_ncre', how='left')
	
	#Tratamiento base devolucion
	devolucion.columns = devolucion.columns.str.strip()
	devolucion['No_nota'] = devolucion['No_nota'].str.strip()
	devolucion['Nom_cte'] = devolucion['Nom_cte'].str.strip()
	devolucion['Desc_prod'] = devolucion['Desc_prod'].str.strip()
	devolucion['Cve_prod'] = devolucion['Cve_prod'].str.strip()
	devolucion = devolucion[['No_nota', 'Fecha', 'Cve_factu', 'No_fac', 'Tot_nota', 'Nom_cte', 'No_cliente', 'Subtotal', 'Cve_prod',
	                         'Desc_prod', 'Cantidad', 'Valor_prod', 'Costo_prom']]
	devolucion.columns = ['No_nota', 'Fecha_dev', 'Cve_factu', 'No_fac', 'Devolucion', 'Cliente', 'Cve_cte', 'Subtotal', 'SKU',
						  'Producto', 'Cantidad', 'Precio', 'Costo_prom']
	devolucion['Fecha_dev'] = pd.to_datetime(devolucion['Fecha_dev'], format='%d/%m/%Y')
	devolucion['Año'] = devolucion['Fecha_dev'].dt.year
	devolucion['Mes'] = devolucion['Fecha_dev'].dt.month
	devolucion = devolucion.fillna(0)
	devolucion = devolucion.groupby(['Año', 'Mes', 'Cve_cte', 'Cliente', 'Producto']).agg({'Devolucion':'sum',
																			               'Subtotal':'sum'}).reset_index()					  

	#Tratamiento base productos
	productos.columns = productos.columns.str.strip()
	productos['Cve_prod'] = productos['Cve_prod'].str.strip()
	productos['Desc_prod'] = productos['Desc_prod'].str.strip()
	productos = productos[['Cve_prod', 'Desc_prod', 'Uni_med', 'Cto_ent']]
	productos.columns = ['SKU', 'Producto', 'Unidad', 'Costo']
	productos = productos.fillna(0)

	st.header('Propuesta 1')
	anio = st.selectbox('Año', ventas.sort_values(by=['Año'])['Año'].unique())
	ventas = ventas[ventas['Año']==anio].reset_index()
	
	
	kpi_ventaspes = pd.pivot_table(ventas, index=['Canal', 'Cliente', 'SKU'], values=['Venta ($)'], columns='Mes2', aggfunc='sum', margins=True).reset_index().fillna(0)
	kpi_ventaspza = pd.pivot_table(ventas, index=['Canal', 'Cliente', 'SKU'], values=['Venta (PZA)'], columns='Mes2', aggfunc='sum', margins=True).reset_index().fillna(0)
	
	st.subheader('Venta ($)')
	st.write(kpi_ventaspes)
	
	st.subheader('Venta (PZA)')
	st.write(kpi_ventaspza)
	


	st.header('Propuesta 2')
	ventas2 = ventas.sort_values(by=['Mes'])
	
	ventas2 = ventas2.groupby(['Mes', 'Canal', 'Cliente', 'SKU']).agg({'Venta ($)':'sum',
																	   'Venta (PZA)':'sum',
																	   'Cost_prom':'sum'}).reset_index()
	ventas2['Utilidad ($)'] = ventas2['Venta ($)'] - ventas2['Cost_prom']
	ventas2['Margen (%)'] = ventas2['Utilidad ($)'] / ventas2['Venta ($)']
	st.write(ventas2)




if __name__ == '__main__':
	main()