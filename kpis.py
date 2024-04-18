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
	def Clientes():
		clientes = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/clientes.csv',encoding='latin-1')
		return clientes
	clientes = Clientes()
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
	@st.cache_resource
	def cobranza():
		cxc = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/cobranza.csv',encoding='latin-1')
		return cxc
	cobranza = cobranza()
	@st.cache_resource
	def porpagar():
		cxp = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/porpagar.csv',encoding='latin-1')
		return cxp
	porpagar = porpagar()
	@st.cache_resource
	def pagos_sem():
		pagos = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/pagos_sem.csv',encoding='latin-1')
		return pagos
	pagos = pagos_sem()


	mes_diccioanrio = { 1:'ene', 2:'feb', 3:'mar', 4:'abr', 5:'may',6:'jun',
		    			7:'jul',8:'ago',9:'sep',10:'oct',11:'nov',12:'dic'}
	#Tratamiento base canal
	canal.columns = canal.columns.str.strip()
	canal['CLIENTE'] = canal['CLIENTE'].str.strip()
	canal['Canal'] = canal['Canal'].str.strip()
	canal = canal[['Cve_cte', 'CLIENTE', 'Canal']]
	canal.columns = ['Cve_cte', 'Cliente_c', 'Canal']
	canal = canal.fillna(0)

	#Tratamiento base cliente
	clientes.columns = clientes.columns.str.strip()
	clientes['Nom_cte'] = clientes['Nom_cte'].str.strip()
	
	#Tratamiento base facturas
	facturas.columns = facturas.columns.str.strip()
	facturas['Cve_factu'] = facturas['Cve_factu'].str.strip()
	facturas['Cve_prod'] = facturas['Cve_prod'].str.strip()
	facturas['Nom_fac'] = facturas['Nom_fac'].str.strip()
	facturas['Desc_prod'] = facturas['Desc_prod'].str.strip()

	#Trabajo con base alterna para rescatar descuentos aplicados directamente a la factura
	facturas_temp = facturas.copy()
	facturas_temp = facturas_temp[['No_fac', 'Falta_fac', 'Descuento', 'Subt_fac', 'Total_fac', 'Cve_factu', 'Cve_prod', 'Valor_prod', 'Cant_surt', 'Cve_cte', 'Nom_fac', 
						 'Desc_prod', 'Cost_prom']]
	facturas_temp.columns = ['No_fac', 'Fecha', 'Descuento_dir', 'Venta ($)', 'Total_fac', 'Cve_factu', 'SKU', 'Precio', 'Venta (PZA)', 'Cve_cte', 'Cliente', 'Producto', 'Cost_prom']
	facturas_temp['Fecha'] = pd.to_datetime(facturas_temp['Fecha'], format='%d/%m/%Y')
	facturas_temp['Año'] = facturas_temp['Fecha'].dt.year
	facturas_temp['Mes'] = facturas_temp['Fecha'].dt.month
	facturas_temp['Mes2'] = pd.to_datetime(facturas_temp['Fecha'], format='%d/%m/%Y').dt.strftime('%Y-%m')
	facturas_temp = facturas_temp.fillna(0)
	ventas_temp = facturas_temp.merge(canal, on='Cve_cte', how='left')
	ventas_temp['Cliente_c'] = ventas_temp['Cliente_c'].fillna('OTROS DISTRIBUIDORES')
	ventas_temp['Canal'] = ventas_temp['Canal'].fillna('OTROS DISTRIBUIDORES')
	###########################################################################################

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

	#Tratamiento base cobranza
	cobranza.columns = cobranza.columns.str.strip()
	cobranza['Cve_factu'] = cobranza['Cve_factu'].str.strip()
	cobranza['Nom_cte'] = cobranza['Nom_cte'].str.strip()
	cobranza = cobranza[['Cve_factu', 'No_fac', 'Falta_fac', 'Cve_cte', 'Saldo_fac', 'Lim_cre', 'Dia_cre',
						 'Fech_venci', 'Total_fac']]
	cobranza.columns = ['Cve_factu', 'No_fac', 'Fecha', 'Cve_cte', 'Saldo cxc', 'Limite credito', 'Dias', 'Vencimiento', 'Total facturado']
	cobranza = cobranza.merge(clientes, on='Cve_cte', how='left')
	cobranza['Fecha'] = pd.to_datetime(cobranza['Fecha'], format='%d/%m/%Y')
	cobranza['Añof'] = cobranza['Fecha'].dt.year
	cobranza['Mesf'] = cobranza['Fecha'].dt.month
	cobranza['Mes2f'] = pd.to_datetime(cobranza['Fecha'], format='%d/%m/%Y').dt.strftime('%Y-%b')
	cobranza = cobranza.fillna(0)
	cobranza['Vencimiento'] = pd.to_datetime(cobranza['Vencimiento'], format='%d/%m/%Y')
	cobranza['Año'] = cobranza['Vencimiento'].dt.year
	cobranza['Mes'] = cobranza['Vencimiento'].dt.month
	cobranza['Mesn'] = pd.to_datetime(cobranza['Vencimiento'], format='%d/%m/%Y').dt.strftime('%b')
	cobranza['Semana'] = cobranza['Vencimiento'].dt.isocalendar().week.astype('int')
	cobranza['Sem2'] = pd.to_datetime(cobranza['Vencimiento'], format='%d/%m/%Y').dt.strftime('%Y-%b-%V')

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
	descuento = descuento[['No_nota', 'Fecha', 'Cve_factu', 'No_fac', 'Tot_nota', 'Nom_cte', 'No_cliente', 'Subtotal', 'Cve_ncre']]
	descuento.columns = ['No_nota', 'Fecha_desc', 'Cve_factu', 'No_fac', 'Descuento', 'Cliente', 'Cve_cte', 'Subtotal', 'Cve_ncre']
	descuento['Fecha_desc'] = pd.to_datetime(descuento['Fecha_desc'], format='%d/%m/%Y')
	descuento['Año'] = descuento['Fecha_desc'].dt.year
	descuento['Mes'] = descuento['Fecha_desc'].dt.month
	descuento['Mes2'] = pd.to_datetime(descuento['Fecha_desc'], format='%d/%m/%Y').dt.strftime('%Y-%m')
	descuento = descuento.fillna(0)
	descuento = descuento.groupby(['Año', 'Mes', 'Mes2', 'Cve_cte', 'Cliente', 'No_fac', 'Cve_ncre']).agg({'Descuento':'sum',
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
	devolucion['Mes2'] = pd.to_datetime(devolucion['Fecha_dev'], format='%d/%m/%Y').dt.strftime('%Y-%m')
	devolucion = devolucion.fillna(0)
	devolucion = devolucion.groupby(['Año', 'Mes', 'Mes2', 'Cve_cte', 'Cliente', 'No_fac', 'SKU', 'Producto']).agg({'Devolucion':'sum',
																			               'Subtotal':'sum'}).reset_index()
	#st.write(devolucion)
	#Tratamiento base productos
	productos.columns = productos.columns.str.strip()
	productos['Cve_prod'] = productos['Cve_prod'].str.strip()
	productos['Desc_prod'] = productos['Desc_prod'].str.strip()
	productos = productos[['Cve_prod', 'Desc_prod', 'Uni_med', 'Cto_ent']]
	productos.columns = ['SKU', 'Producto', 'Unidad', 'Costo']
	productos = productos.fillna(0)

	#Tratamiento base por pagar
	porpagar.columns = porpagar.columns.str.strip()
	porpagar['Nom_prov'] = porpagar['Nom_prov'].str.strip()
	porpagar = porpagar[['No_facc', 'Falta_fac', 'Cve_prov', 'Nom_prov', 'Saldo_fac', 'Dia_cre', 'Cve_mon', 'U_tip_cam', 'Fech_venci', 'Total_fac', 'Cve_iva']]
	porpagar.columns = ['No_facc', 'Falta_fac', 'Cve_prov', 'Proveedor', 'Saldo_CXP', 'Dias_credito', 'Moneda', 'TC', 'Vencimiento', 'Total_facturado', 'Tipo_proveedor']
	porpagar['Vencimiento'] = pd.to_datetime(porpagar['Vencimiento'], format='%d/%m/%Y').fillna(0)
	porpagar['Año'] = porpagar['Vencimiento'].dt.year
	porpagar['Mes'] = porpagar['Vencimiento'].dt.month
	porpagar['Mesn'] = pd.to_datetime(porpagar['Vencimiento'], format='%d/%m/%Y').dt.strftime('%b')
	porpagar['Semana'] = porpagar['Vencimiento'].dt.isocalendar().week.astype('int')
	porpagar['Sem2'] = pd.to_datetime(porpagar['Vencimiento'], format='%d/%m/%Y').dt.strftime('%Y-%b-%V')
	
	#Tratamiento base pagos
	pagos.columns = pagos.columns.str.strip()
	pagos['Nom_cte'] = pagos['Nom_cte'].str.strip()
	#########FILTROS############
	st.sidebar.title('Filtros')
	canal_list   = st.sidebar.multiselect('Canal', ventas['Canal'].unique())
	cliente_list = st.sidebar.multiselect('Cliente', ventas['Cliente'].unique())
	sku_list     = st.sidebar.multiselect('SKU', ventas['Producto'].unique())
	
	
	if not canal_list:
		canal_list = ventas['Canal'].unique()
	if not cliente_list:
		cliente_list = ventas['Cliente'].unique()
	if not sku_list:
		sku_list = ventas['Producto'].unique()

	ventas = ventas[(ventas['Canal'].isin(canal_list)) 
				   &(ventas['Cliente'].isin(cliente_list))
				   &(ventas['Producto'].isin(sku_list))]
	ventas_temp = ventas_temp[(ventas_temp['Canal'].isin(canal_list))
							 &(ventas_temp['Cliente'].isin(cliente_list))
							 &(ventas_temp['Producto'].isin(sku_list))] 
	
	if st.checkbox('Resumen anual'):
		kpi_ventas_an_pes = pd.pivot_table(ventas, index=['Canal', 'Cliente', 'SKU'], values=['Venta ($)'], columns='Año', aggfunc='sum', margins=True).reset_index().fillna(0)
		st.write(kpi_ventas_an_pes)
	anio = st.selectbox('Año', ventas.sort_values(by=['Año'])['Año'].unique())
	ventas = ventas[ventas['Año']==anio].reset_index()
	ventas_temp = ventas_temp[ventas_temp['Año'] == anio].reset_index()

	#descuento = descuento[descuento['Año']==anio].reset_index(drop=True)
	#devolucion = devolucion[devolucion['Año']==anio].reset_index(drop=True)
	descuento = descuento.merge(canal, on='Cve_cte', how='left').reset_index(drop=True).fillna(0)
	descuento = descuento.drop(columns=['Cliente'])
	descuento = descuento.rename(columns={'Cliente_c':'Cliente'})
	descuento = descuento[(descuento['Canal'].isin(canal_list))
						 &(descuento['Cliente'].isin(cliente_list))]
	#st.write(descuento)
	devolucion = devolucion.merge(canal, on='Cve_cte', how='left').reset_index(drop=True).fillna(0)
	devolucion = devolucion.drop(columns=['Cliente'])
	devolucion = devolucion.rename(columns={'Cliente_c':'Cliente'})
	devolucion = devolucion[(devolucion['Canal'].isin(canal_list))
						 &(devolucion['Cliente'].isin(cliente_list))]
	kpi_ventaspes = pd.pivot_table(ventas, index=['Canal', 'Cliente', 'SKU'], values=['Venta ($)'], columns='Mes2', aggfunc='sum', margins=True).reset_index().fillna(0)
	kpi_ventaspza = pd.pivot_table(ventas, index=['Canal', 'Cliente', 'SKU'], values=['Venta (PZA)'], columns='Mes2', aggfunc='sum', margins=True).reset_index().fillna(0)
	
	if st.checkbox('Propuesta 1'):
		st.header('Propuesta 1')
		st.subheader('Venta ($)')
		st.write(kpi_ventaspes)
		
		if st.checkbox('Resumen canal'):
			kpi_ventaspestemp = pd.pivot_table(ventas, index=['Canal'], values=['Venta ($)'], columns='Mes2', aggfunc='sum', margins=True).reset_index().fillna(0)
			st.write(kpi_ventaspestemp)
		#st.write(kpi_ventaspestemp)
		
		kpi_descuento = pd.pivot_table(descuento, index=['Canal', 'Cliente'], values=['Descuento'], columns='Mes2', aggfunc='sum', margins=True).reset_index().fillna(0)
		
		kpi_devolucion = pd.pivot_table(devolucion, index=['Canal', 'Cliente'], values=['Devolucion'], columns='Mes2', aggfunc='sum', margins=True).reset_index().fillna(0)
		st.subheader('Descuentos ($)')
		st.write(kpi_descuento)
		st.subheader('Devoluciones ($)')
		st.write(kpi_devolucion)


		st.subheader('Venta (PZA)')
		st.write(kpi_ventaspza)
	
	
	
	
	st.header('Ventas')
	#####################SIN DESCUENTOS DIRECTOS"#############################################################
	ventas2 = ventas.sort_values(by=['Mes'])
	descuento2 = descuento.sort_values(by=['Mes'])
	devolucion2 = devolucion.sort_values(by=['Mes'])
	#st.write(ventas2)
	ventas2 = ventas2.groupby(['Mes', 'Canal', 'Cliente', 'SKU']).agg({'Venta ($)':'sum',
																	   'Venta (PZA)':'sum',
																	   'Cost_prom':'sum'}).reset_index()
	descuento3 = descuento2.groupby(['Mes', 'Canal', 'Cliente', 'No_fac']).agg({'Descuento':'sum'}).reset_index()
	#st.write(descuento3)
	devolucion3 = devolucion2.groupby(['Mes', 'Canal', 'Cliente', 'No_fac', 'SKU']).agg({'Devolucion':'sum'}).reset_index()
	descuento2 = descuento2.groupby(['Mes', 'Canal', 'Cliente']).agg({'Descuento':'sum'}).reset_index()
	devolucion2 = devolucion2.groupby(['Mes', 'Canal', 'Cliente']).agg({'Devolucion':'sum'}).reset_index()
	ventas2 = pd.merge(ventas2, descuento2, on=['Mes', 'Canal', 'Cliente'], how='left').reset_index(drop=True).fillna(0)
	ventas2 = pd.merge(ventas2, devolucion2, on=['Mes', 'Canal', 'Cliente'], how='left').reset_index(drop=True).fillna(0)
	ventas2['Utilidad ($)'] = ventas2['Venta ($)'] - ventas2['Cost_prom']
	ventas2['Margen (%)'] = ventas2['Utilidad ($)'] / ventas2['Venta ($)']
	###############################################################################################################
	#####################CON DESCUENTOS DIRECTOS"#############################################################
	productos_temp = productos[['SKU', 'Producto']]
	productos_temp['SKU'] = productos_temp['SKU'].str.strip()
	productos_temp['Producto'] = productos_temp['Producto'].str.strip()
	#productos_temp.columns = ['SKU', 'Producto']
	ventas2_temp = ventas_temp.sort_values(by=['Mes'])
	descuento2 = descuento.sort_values(by=['Mes'])
	devolucion2 = devolucion.sort_values(by=['Mes'])
	for i in range(len(ventas2_temp['Descuento_dir'])):
		ventas2_temp.loc[i,'Descuento_dir'] = float(ventas2_temp.loc[i,'Descuento_dir'])
	ventas3_temp = ventas2_temp.groupby(['Mes', 'Canal', 'Cliente', 'No_fac', 'SKU']).agg({'Venta ($)':'sum',
																						   'Descuento_dir':'sum',
																						   'Venta (PZA)':'sum',
	
																						   'Cost_prom':'sum'}).reset_index()
	descuento3 = descuento3.groupby(['Canal', 'Cliente', 'No_fac']).agg({'Descuento':'sum'}).reset_index()
	#st.write(descuento3)
	for i in range(len(ventas3_temp['No_fac'])):
		ventas3_temp.loc[i,'No_fac'] = str(ventas3_temp.loc[i,'No_fac'])
		ventas3_temp.loc[i,'No_fac'] = str(ventas3_temp.loc[i,'No_fac'])
	ventas3_temp = pd.merge(ventas3_temp, devolucion3, on=['Canal', 'Cliente', 'No_fac', 'SKU'], how='left').reset_index(drop=True).fillna(0)
	ventas3_temp = pd.merge(ventas3_temp, descuento3, on=['Canal', 'Cliente', 'No_fac'], how='left').reset_index(drop=True).fillna(0)
	
	
	ventas2_temp = ventas2_temp.groupby(['Mes', 'Canal', 'Cliente', 'SKU']).agg({'Venta ($)':'sum',
																	   'Descuento_dir':'sum',
																	   'Venta (PZA)':'sum',
																	   'Cost_prom':'sum'}).reset_index()
	descuento2 = descuento2.groupby(['Mes', 'Canal', 'Cliente']).agg({'Descuento':'sum'}).reset_index()
	devolucion2 = devolucion2.groupby(['Mes', 'Canal', 'Cliente']).agg({'Devolucion':'sum'}).reset_index()
	ventas2_temp = pd.merge(ventas2_temp, descuento2, on=['Mes', 'Canal', 'Cliente'], how='left').reset_index(drop=True).fillna(0)
	ventas2_temp = pd.merge(ventas2_temp, devolucion2, on=['Mes', 'Canal', 'Cliente'], how='left').reset_index(drop=True).fillna(0)
	ventas2_temp['Utilidad ($)'] = ventas2_temp['Venta ($)'] - ventas2_temp['Cost_prom']
	ventas2_temp['Margen (%)'] = ventas2_temp['Utilidad ($)'] / ventas2_temp['Venta ($)']
	ventas2_temp = pd.merge(ventas2_temp, productos_temp, on='SKU', how='left')
	###############################################################################################################
	#ventas3_temp = ventas3_temp.drop(columns=['Mes_y', 'Mes'])
	#ventas3_temp = ventas3_temp.rename(columns={'Mes_x':'Mes'})
	for i in range(len(ventas3_temp['No_fac'])):
		ventas3_temp.loc[i,'Descuento'] = (ventas3_temp.loc[i,'Descuento']/1.16)
		ventas3_temp.loc[i,'Devolucion'] = (ventas3_temp.loc[i,'Devolucion']/1.16)
	ventas3_temp = ventas3_temp.fillna(0) 
	descuento_total_por_factura = ventas3_temp.groupby('No_fac')['Descuento'].mean()
	total_factura = ventas3_temp.groupby('No_fac')['Venta ($)'].sum()
	#st.write(total_factura)
	#for i in range(len(descuento_total_por_factura)):
	#	descuento_total_por_factura.loc[i,'No_fac'] = str(descuento_total_por_factura.loc[i,'No_fac'])
	ventas3_temp['Proporcion_descuento'] = ventas3_temp.apply(lambda row: row['Venta ($)'] / total_factura[row['No_fac']], axis=1)
	ventas3_temp['Descuento_proporcional'] = ventas3_temp['Proporcion_descuento'] * ventas3_temp['Descuento']
	ventas3_temp['Venta_Neta'] = ventas3_temp['Venta ($)'] - ventas3_temp['Descuento_proporcional'] - ventas3_temp['Devolucion']
	ventas3_temp['Utilidad ($)'] = ventas3_temp['Venta_Neta'] - ventas3_temp['Cost_prom']
	ventas3_temp['Margen (%)'] = ventas3_temp['Utilidad ($)'] / ventas3_temp['Venta_Neta']
	ventas3_temp = pd.merge(ventas3_temp, productos_temp, on='SKU', how='left')
	st.write(ventas3_temp)
	#st.write(ventas2_temp)
	#st.download_button(label="Descargar", data=ventas2_temp.to_csv(), mime="text/csv")
	hoy = datetime.today()
	if st.checkbox('CXC'):
		st.header('CXC')
		cobranza['Estatus'] = cobranza['Cve_factu']
		for i in range(len(cobranza['No_fac'])):
			if cobranza.loc[i,'Vencimiento']<hoy:
				cobranza.loc[i,'Estatus'] = 'Vencido'
			else:
				cobranza.loc[i,'Estatus'] = 'Corriente'
		for i in range(len(cobranza['No_fac'])):
			if cobranza.loc[i,'Año'] == 2025:
				cobranza.loc[i,'Estatus'] = 'Futuro'
		for i in range(len(cobranza['Estatus'])):
			if cobranza.loc[i,'Estatus'] == 'Vencido':
				cobranza.loc[i,'Semana'] = 'Vencido'
			if cobranza.loc[i,'Estatus'] == 'Futuro':
				cobranza.loc[i,'Semana'] = 'Futuro'
		for i in range(len(cobranza['Estatus'])):
			if cobranza.loc[i,'Estatus'] == 'Vencido':
				cobranza.loc[i,'Mesn'] = 'Vencido'
			if cobranza.loc[i,'Estatus'] == 'Futuro':
				cobranza.loc[i,'Mesn'] = 'Futuro'
		cobranza_det = cobranza.copy()
		cobranza_det.columns = ['Cve_factu', 'No_fac', 'Fecha', 'Cve_cte', 'Saldo cxc', 'Limite credito', 'Dias', 'Vencimiento', 'Total facturado',
							'Cliente', 'Añof', 'Mesf', 'Mes2f', 'Año', 'Mes', 'Mesn', 'Semana', 'Sem2', 'Estatus']
		#st.write(cobranza_det)
	
		cobranza_det1 = cobranza_det.groupby(['Cve_cte', 'Cliente', 'Año', 'Sem2']).agg({'Saldo cxc':'sum'}).reset_index()
		#st.write(cobranza_det)
		kpi_cobranza = pd.pivot_table(cobranza_det, index=['Cliente'], values=['Saldo cxc'], columns=['Semana','Mesn'], aggfunc='sum', margins=True).reset_index().fillna(0)
	
		st.write(kpi_cobranza)
	
	if st.checkbox('CXP'):
		st.header('CXP')
		
		porpagar['Estatus'] = porpagar['No_facc']
		for i in range(len(porpagar['No_facc'])):
			if porpagar.loc[i,'Moneda'] == 2:
				porpagar.loc[i,'Saldo_CXP'] = porpagar.loc[i,'Saldo_CXP'] * porpagar.loc[i,'TC']
		for i in range(len(porpagar['No_facc'])):
			if porpagar.loc[i,'Vencimiento']<hoy:
				porpagar.loc[i,'Estatus'] = 'Vencido'
			else:
				porpagar.loc[i,'Estatus'] = 'Corriente'
		for i in range(len(porpagar['Estatus'])):
			if porpagar.loc[i,'Estatus'] == 'Vencido':
				porpagar.loc[i,'Semana']  = 'Vencido'
		for i in range(len(porpagar['Estatus'])):
			if porpagar.loc[i,'Estatus'] == 'Vencido':
				porpagar.loc[i,'Mesn'] = 'Vencido'
		porpagar = porpagar.fillna(0)

		kpi_porpagar = pd.pivot_table(porpagar, index=['Proveedor'], values=['Saldo_CXP'], columns=['Semana', 'Mesn'], aggfunc='sum', margins=True).reset_index().fillna(0)
		st.write(kpi_porpagar)


if __name__ == '__main__':
	main()