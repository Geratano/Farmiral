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
	#@st.cache_resource
	#def cargar1():
	#	base1 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/base.csv',encoding='latin-1')
	#	return  base1
	#df = cargar1()
	#Objetivos del mes
	@st.cache_resource
	def cargar2():
		base2 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/objetivos.csv',encoding='latin-1')
		return base2
	objetivos = cargar2()
	@st.cache_resource
	def cargar3():
		base3 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/remisiones.csv',encoding='latin-1')
		return  base3
	remisiones = cargar3()
	@st.cache_resource
	def cargar4():
		base4 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/pedidos.csv',encoding='latin-1')
		return  base4
	pedidos = cargar4()
	@st.cache_resource
	def cargar5():
		base5 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/canalcliente.csv',encoding='latin-1')
		return base5
	canal = cargar5()
	@st.cache_resource
	def cargar6():
		base6 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/existencias.csv',encoding='latin-1')
		return base6
	existencias = cargar6()
	@st.cache_resource
	def cargar7():
		base7 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/controlproduccion.csv',encoding='latin-1')
		return base7
	alfred = cargar7()
	@st.cache_resource
	def cargar8():
		base8 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/Plan2023.csv',encoding='latin-1')
		return base8
	forecast = cargar8()
	@st.cache_resource
	def cargar9():
		base9 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/formulas.csv',encoding='latin-1')
		return base9
	df_formulas = cargar9()
	@st.cache_resource
	def cargar10():
		base10 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/productos.csv',encoding='latin-1')
		return base10
	productos = cargar10()
	@st.cache_resource
	def cargar11():
		base11 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/sellout.csv',encoding='latin-1')
		return base11
	sellout = cargar11()
	@st.cache_resource
	def cargar12():
		base12 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/factura.csv',encoding='latin-1')
		return base12
	facturas = cargar12()
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
	def clases():
		clases = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/clases.csv',encoding='latin-1')
		return  clases
	clases = clases()

	


	#df.columns = df.columns.str.strip()
	remisiones.columns = remisiones.columns.str.strip()
	pedidos.columns = pedidos.columns.str.strip()
	canal.columns = canal.columns.str.strip()
	existencias.columns = existencias.columns.str.strip()
	df_formulas.columns = df_formulas.columns.str.strip()
	alfred.columns = alfred.columns.str.strip()
	productos.columns = productos.columns.str.strip()
	sellout.columns = sellout.columns.str.strip()
	facturas.columns = facturas.columns.str.strip()
	facturas['Cse_prod'] = facturas['Cse_prod'].str.strip()
	for i in range(len(facturas['No_fac'])):
		facturas.loc[i,'No_fac'] = str(facturas.loc[i,'No_fac'])
	
	facturas['No_fac'] = facturas['No_fac'].str.strip()
	descuento.columns = descuento.columns.str.strip()
	descuento['No_fac'] = descuento['No_fac'].str.strip()
	for i in range(len(descuento['No_fac'])):
		descuento.loc[i,'No_fac'] = str(descuento.loc[i,'No_fac'])	
	devolucion.columns = devolucion.columns.str.strip()
	devolucion['No_fac'] = devolucion['No_fac'].str.strip()
	for i in range(len(devolucion['No_fac'])):
		devolucion.loc[i,'No_fac'] = str(devolucion.loc[i,'No_fac'])
	clases.columns = clases.columns.str.strip()
	clases['Categoria'] = clases['Categoria'].str.strip()
	clases['Des_prod'] = clases['Desc_prod'].str.strip()
	productos['Cve_prod'] = productos['Cve_prod'].str.strip()
	productos['Desc_prod'] = productos['Desc_prod'].str.strip()
	productos['Cse_prod'] = productos['Cse_prod'].str.strip()
	df_productos = productos[['Cve_prod', 'Desc_prod']]
	df_productos.columns = ['SKU', 'Producto']
	forecast.columns = forecast.columns.str.strip()
	forecast.columns = ['Cve_prod', 'Producto', 'Tamano lotes', 'Presentacion', 'Cliente', 'Stock', 'Plan Julio', 'Forecast', 'Lotes origin', 'Lotes', 'Nota','NO']
	forecast = forecast[['Cve_prod', 'Producto', 'Plan Julio', 'Forecast', 'Lotes origin']]

	
	#Filtramos la base para obtener solo las columnas
	#importantes
	###CONSTRUCCION BASE DE CLASES PARA CATEGORIZAR LOS PRODUCTOS###
	clases = clases[['SKU', 'Categoria', 'Des_prod']]

	###CONSTRUCCION DESCUENTOS Y DEVOLUCIONES LUIS###
	#filtro las columnas
	df_descuento = descuento[['No_nota','Tip_not','Fecha','Cve_factu','No_fac','Tot_nota','Saldo','Nom_cte','No_cliente','Iva','Subtotal','Tip_cam','Nom_age','Cve_ncre']]
	df_descuento['Cve_ncre'] = df_descuento['Cve_ncre'].str.strip() # quito espacios a Cve_ncre

	#quito los espacios de las columnas en la base tipocred
	tipo.columns=tipo.columns.str.strip()
	tipo['Cve_ncre']= tipo['Cve_ncre'].str.strip()
	df_descuentos = df_descuento.merge(tipo, on='Cve_ncre', how='left') # hago merge con las tablas descuenos y tipocred
	df_descuentos['No_fac'] = df_descuentos['No_fac'].str.strip()
	#df_descuentos['No_fac'] = pd.to_numeric(df_descuentos['No_fac'])
	#st.write(df_descuentos[df_descuentos['No_fac'] == 4811])
	#quito los espacios de las columnas de la base devoliucion
	devolucion.columns= devolucion.columns.str.strip()
	#filtro las columnas
	df_devolucion = devolucion[['No_nota','Tip_not','Fecha','Cve_factu','No_fac','Tot_nota','Saldo','Nom_cte','No_cliente',
								'Iva','Subtotal','Tip_cam','Nom_age','Cve_ncre']]
	m_devolucion = df_devolucion.merge(tipo, on='Cve_ncre', how='left') # hago merge de la tabla devolucion con la tabla tipo
	m_devolucion['INCLUYE']= 'SI' # en la columna INCLUYE  lleno todo con un si 
	m_devolucion=m_devolucion.fillna(0) # Donde haya un none se reemplaza con un 0
	notasc = pd.concat([df_descuentos,m_devolucion]) # concateno las bases descuentos con devolcion
	notasc = notasc.fillna(0).reset_index()
	#for i in range(len(notasc['No_fac'])):
	#	notasc.loc[i,'No_fac'] = str(notasc.loc[i,'No_fac'])
	#st.write(notasc)
	#st.write(comp)
	#################################################
	#CONSTRUCCION FACTURAS#
	#canal['Cve_cte'] = canal['Cve_cte'].str.strip()
	#facturas['Cve_cte'] = facturas['Cve_cte'].str.strip()
	df_facturas = facturas.merge(canal, on='Cve_cte', how='left')
	df_facturas['Costo'] = df_facturas['Cost_prom']/df_facturas['Cant_surt']
	df_facturas['Precio'] = df_facturas['Subt_fac']/df_facturas['Cant_surt']
	df_facturas['Utilidad'] = df_facturas['Precio'] - df_facturas['Costo']
	df_facturas['Utilidad_mov'] = df_facturas['Utilidad'] * df_facturas['Cant_surt']
	df_facturas['Margen'] = round((df_facturas['Utilidad']/df_facturas['Precio']),3)*100
	df_facturas['Falta_fac'] = pd.to_datetime(df_facturas['Falta_fac'], format = '%d/%m/%Y' )
	df_facturas['Anio'] = df_facturas['Falta_fac'].dt.year
	df_facturas['Mes'] = df_facturas['Falta_fac'].dt.month
	df_facturas['Dia'] = df_facturas['Falta_fac'].dt.day
	df_facturas['Nom_cliente'] = df_facturas['Nom_fac'].str.strip()
	#df_facturas = df_facturas.astype({'Nom_cliente':'string'})
	df_facturas['Producto'] = df_facturas['Desc_prod'].str.strip()
	for i in range(len(df_facturas['No_fac'])):
		df_facturas.loc[i,'No_fac'] = str(df_facturas.loc[i,'No_fac'])
	df_facturas['No_fac'] = df_facturas['No_fac'].str.strip()
	#st.write(df_facturas)
	################################################################################
	#luisar = df_facturas.merge(clases, on='Cse_prod', how='left')

	nc_tabla = notasc[['No_fac', 'Subtotal']]
	for i in range(len(nc_tabla['No_fac'])):
		nc_tabla.loc[i,'No_fac'] = str(nc_tabla.loc[i,'No_fac'])
	

	nc_tabla = nc_tabla.groupby(['No_fac']).agg({'Subtotal':'sum'}).reset_index()
	#for i in range(len(nc_tabla['No_fac'])):
	#	nc_tabla.loc[i,'No_fac'] = str(nc_tabla.loc[i,'No_fac'])
	#dftemp = df_facturas.merge(nc_tabla, on='No_fac', how='left')
	#st.write(nc_tabla)
	dftemp = df_facturas.merge(nc_tabla, on='No_fac', how='left').fillna(0).reset_index()
	
	dftemp['N_cred'] = dftemp['Subtotal']
	#st.write(dftemp)
	#st.write(dftemp.columns)
	#st.write(dftemp.columns)
	#st.write(dftemp)
	df = dftemp[['No_fac', 'Falta_fac', 'Status_fac', 'Descuento', 'Subt_fac', 'Total_fac', 'Iva', 'Saldo_fac', 'Cve_factu',
				 'Cve_cte', 'Cse_prod', 'Cve_prod', 'New_med', 'Valor_prod', 'Cant_surt', 'Cve_mon', 'Tip_cam', 'Unidad', 'No_ped',
				 'No_rem', 'Cve_suc', 'Lote', 'Dcto1', 'Dcto2', 'Cve_age', 'Nom_fac', 'Desc_prod', 'Cost_prom', 'Lugar',
				 'Hora_fac', 'Cve_age2', 'Lista_med', 'F_pago', 'Saldo_fac', 'Costo', 'Precio', 'Utilidad', 'Utilidad_mov',
				 'Margen', 'Canal', 'Kam', 'Subdirector', 'N_cred', 'Anio', 'Mes', 'Dia', 'Nom_cliente', 'Producto']]
	#st.write(df)
	df['Canal_cliente'] = df['Canal'].str.strip()

	#st.write(df_facturas['Margen'])
	#st.write(df)
	#######################
	#df_ventas = df[['No_fac','Falta_fac','Subt_fac','Cve_factu','Cse_prod','Cant_surt','Lugar','Costo','Utilidad_mov','Margen'
	#,'Canal_cliente','Kam','Subdirector','N_cred','Anio','Mes','Dia','Nom_cliente','Producto']]
	df_ventas = df[['No_fac','Falta_fac','Subt_fac','Cve_factu','Cse_prod','Cant_surt','Lugar','Costo','Utilidad_mov','Margen'
	,'Canal_cliente','Kam','Subdirector','N_cred','Anio','Mes','Dia','Nom_fac','Producto']]
	df_ventas.columns = ['No_fac','Falta_fac','Subt_fac','Cve_factu','Cse_prod','Cant_surt','Lugar','Costo','Utilidad_mov','Margen'
	,'Canal_cliente','Kam','Subdirector','N_cred','Anio','Mes','Dia','Nom_cliente','Producto']
	df_ventas = df_ventas.fillna(0)
	#st.write(df_ventas)
	#st.write(df_ventas)
	###TRATAMIENTO BASE EXISTENCIAS###
	df_existencias = existencias[['Cve_prod', 'Lote', 'Lugar', 'Cto_ent', 'Existencia', 'Fech_venc', 'Desc_prod', 'Uni_med']]
	df_existencias.columns = ['SKU', 'Lote', 'Lugar', 'Costo', 'Existencia', 'Vencimiento', 'Producto', 'Unidad']
	#df_existencias['Lugar'] = df_existencias['Lugar'].str.strip()
	df_existencias = df_existencias[(df_existencias['Lugar']=='5') | (df_existencias['Lugar']=='4')]
	df_existencias_4 = df_existencias[(df_existencias['Lugar']=='4')]
	df_existencias_5 = df_existencias[(df_existencias['Lugar']=='5')]
	df_existencias_4 = df_existencias_4.groupby(['Producto']).agg({'Costo':'mean', 'Existencia':'sum'}).reset_index()
	df_existencias_4.columns = ['Producto', 'Costo', 'Existencia proceso']
	df_existencias_5 = df_existencias_5.groupby(['Producto']).agg({'Costo':'mean', 'Existencia':'sum'}).reset_index()
	df_existencias_5.columns = ['Producto', 'Costo', 'Existencia pt']
	#st.write(existencias[(existencias['Lugar']=='5')])
	###TRATAMIENTO BASE REMISIONES###
	df_remisiones = remisiones[['No_rem', 'Cve_cte', 'Nom_cte', 'Cve_prod', 'Cant_surt', 'Desc_prod', 'Valor_prod']]
	df_remisiones.columns = ['No_rem', 'Cve_cte', 'Cliente', 'SKU', 'Cantidad', 'Producto', 'Precio']
	canal.columns = ['Cve_cte', 'Cliente', 'Canal', 'Kam', 'Subdirector']
	canal['Canal'] = canal['Canal'].str.strip()

	remisiones = df_remisiones.merge(canal, on='Cve_cte', how='left')
	remisiones['importe'] = remisiones['Cantidad'] * remisiones['Precio']
	remisiones.columns = ['No_rem', 'Cve_cte', 'Cliente', 'SKU', 'Cantidad', 'Producto', 'Precio', 'CTE', 'Canal', 'Kam', 'Subdirector', 'importe']
	remisiones = remisiones.groupby(['Canal']).agg({'Cantidad':'sum',
													'importe':'sum'})
	remisiones.columns = ['Remision (PZA)', 'Remision ($)']
	###TRATAMIENTO BASE PEDIDOS###
	###TRATAMIENTO BASE FORMULAS####Quitamos los posibles espacios sobrantes de cada columna
	formulas = df_formulas[['Cve_copr', 'Cve_prod', 'Can_copr', 'New_med', 'Undfor', 'Desc_prod', 'Ren_copr', 'Uncfor']]
	formulas.columns = ['SKU', 'Cve_prod', 'Cantidad rendimiento', 'New_med', 'Unidad mp', 'MP', 'Rendimiento', 'Unidad']
	formulas['Cantidad'] = formulas['Cantidad rendimiento']/formulas['Rendimiento']
	formulas['SKU'] = formulas['SKU'].str.strip()
	formulas = formulas.merge(df_productos, on='SKU', how='left')
	#st.write(formulas)
	###MESES REPETIDO VERIFICAR DESPUES###
	# se creó un diccionario el cual contiene los meses del año 
	mes_diccioanrio = { 1:'ene', 2:'feb', 3:'mar', 4:'abr', 5:'may',6:'jun',
		    			7:'jul',8:'ago',9:'sep',10:'oct',11:'nov',12:'dic'}
	now = datetime.now(pytz.timezone("America/Mexico_City")) # se guarda la fecha actual
	dia = now.day
	if dia == 1:
	#	st.write('Si es')
		yesterday = now.replace(month=now.month, day=now.day)
	else:
		yesterday = now.replace(month = now.month, day = now.day - 1)

	act = now.year # de la fecha actual se guarda solo el año en curso
	m = now.month # de la fecha actual se guarda el mes en curso(esto solo devolverá un numero) 
	################################################################
	df_pedidos = pedidos[['No_ped', 'F_alta_ped', 'Cve_cte', 'Nom_cte', 'Status', 'Cve_prod', 'Fecha_ent_a', 'Cant_prod', 
						  'Cant_surtp', 'Liquidado', 'Saldo', 'Valor_prod', 'Uni_med', 'Desc_prod']]
	df_pedidos.columns = ['No_ped', 'Fecha_alta', 'Cve_cte', 'Cliente', 'Estatus', 'SKU', 'Fecha_entrega', 'Cantidad_pedida',
						  'Cantidad_surtida', 'Liquidado', 'Saldo', 'Precio', 'Unidad', 'Producto']
	###Computaremos el back order anterior (ant) si la fecha de entrega es antes del mes actual posterior (pos) si es despues del mes actual
	###y el mes si es el corriente
	df_pedidos['Mes_alta'] = df_pedidos['Fecha_alta']
	df_pedidos['Mes_ent'] = df_pedidos['Fecha_entrega']
	df_pedidos['Back_month'] = df_pedidos['Mes_alta']

	for i in range(len(df_pedidos.loc[:,'Fecha_alta'])):
		try:
			df_pedidos.loc[i,'Fecha_alta'] = pd.to_datetime(df_pedidos.loc[i,'Fecha_alta'], format='%d/%m/%Y')
			df_pedidos.loc[i,'Mes_alta'] = df_pedidos.loc[i,'Fecha_alta'].month
			df_pedidos.loc[i,'Fecha_entrega'] = pd.to_datetime(df_pedidos.loc[i,'Fecha_entrega'], format='%d/%m/%Y')
			df_pedidos.loc[i,'Mes_ent'] = df_pedidos.loc[i, 'Fecha_entrega'].month
		except ValueError:
			df_pedidos.loc[i, 'Mes_ent'] = df_pedidos.loc[i, 'Mes_alta']
	
		if (df_pedidos.loc[i,'Mes_alta'] == m) & (df_pedidos.loc[i,'Mes_ent'] == m):
			df_pedidos.loc[i,'Back_month'] = m
		elif  df_pedidos.loc[i, 'Mes_ent'] > m:
			df_pedidos.loc[i, 'Back_month'] = 'POS'
		else: 
			df_pedidos.loc[i, 'Back_month'] = 'ANT'
	#st.write(df_pedidos)
	###st.write(pedidos.columns)
	#st.write(remisiones.head(5))
	#st.write(pedidos[pedidos['Back_month'] == 'ANT']['Back_month'])

	pedidos = df_pedidos.merge(canal, on='Cve_cte', how='left')

	for i in range(len(pedidos.loc[:,'Saldo'])):
		if pedidos.loc[i,'Saldo'] < 0:
			pedidos.loc[i,'Saldo'] = 0
	pedidos['importe'] = pedidos['Saldo'] * pedidos['Precio']
	#st.write(pedidos)
	#st.write(pedidos)
	#imprimimos como prueba los primeros cinco datos de la tabla
	#if st.checkbox("Raw data"):
	#	st.write(df_ventas.head(5))
	alfred = alfred.fillna(0)
	#st.write(alfred)
	alfred = alfred[alfred['SKU'] != 0]
	n_capt = alfred[(alfred['RESULTADO 41'] == 0) | (alfred['ORDEN 51'] == 0) | (alfred['RESULTADO 51'] == 0)]
	alfred.columns = ['SKU', 'Producto', 'Lote', 'Caducidad', 'Cantidad', 'Tamano lote', 'Fecha', 'Contenedor', 
	'Observacion', 'Resultado 41', 'Orden 51', 'Resultado 51']
	#st.write(alfred)
	for i in range(len(alfred['Cantidad'])):
		#alfred.loc[i,'Cantidad'] = alfred.loc[i,'Cantidad'].replace('.',';').replace(',','.').replace(';','')
		alfred.loc[i,'Cantidad'] = float(alfred.loc[i,'Cantidad'])
	#alfred['Cantidad'].replace('.',',')
	#alfred['Cantidad'] = float(alfred['Cantidad'])
	alfred = alfred.groupby(['Producto','SKU']).agg({'Cantidad':'sum'}).reset_index()
	existe = df_existencias.groupby(['Producto','SKU']).agg({'Existencia':'sum'
													   }).reset_index()
	forecast = forecast.fillna(0)
	forecast = forecast[forecast['Cve_prod'] != 0]
	existe['SKU'] = existe['SKU'].str.strip()
	forecast['SKU'] = forecast['Cve_prod'].str.strip()
	forecast = forecast[['SKU', 'Producto', 'Forecast']]

	t_existe = existe.merge(alfred, on='SKU', how='outer')
	t_existe = t_existe.fillna(0)
	t_existe['Producto'] = t_existe['Producto_x']
	for i in range(len(t_existe['Producto'])):
		if t_existe.loc[i,'Producto_x'] == 0:
			t_existe.loc[i,'Producto'] = t_existe.loc[i,'Producto_y']

	t_existe['Existencia'] = t_existe['Existencia'] + t_existe['Cantidad']

	t_existe = t_existe[['SKU', 'Producto', 'Existencia']]

	t_forecast = forecast.merge(t_existe, on='SKU', how='outer').fillna(0)

	t_forecast['Producto'] = t_forecast['Producto_x']



	for i in range(len(t_forecast['Producto'])):
		if t_forecast.loc[i,'Producto_x']==0:
			t_forecast.loc[i,'Producto'] = t_forecast.loc[i,'Producto_y']
			#t_forecast.loc[i,'Forecast'] = str(t_forecast.loc[i,'Forecast']).strip().replace('-','0')

	t_forecast = t_forecast[['SKU', 'Producto', 'Forecast', 'Existencia']]
	t_forecast['Faltantes'] = t_forecast['Forecast'] - t_forecast['Existencia']
	t_forecast = t_forecast[t_forecast['Faltantes'] != 0]

	if st.button('Actualizar data'):
		st.cache_resource.clear()

	#st.write(alfred)
	#st.write(t_forecast)
	#st.write(df_ventas)
	st.header("Avance diario de ventas")

	#Agrupamos primero nuestro dataframe por factura para poder descontar las notas de crédito
	sub_fac1 =df_ventas.groupby(['No_fac', 'Canal_cliente']).agg({'Subt_fac':'sum',
					     						'Cant_surt':'sum',
												'N_cred':'mean',
												'Costo':'sum',
												'Utilidad_mov':'sum',
												'Margen':'mean',
												'Anio':'max',
												'Mes':'max',
												'Dia':'max'}).reset_index()
	
	sub_fac2 = df_ventas.groupby(['No_fac', 'Canal_cliente']).agg({'Subt_fac':'sum',
					     						'Cant_surt':'sum',
												'N_cred':'mean',
												'Costo':'sum',
												'Utilidad_mov':'sum',
												'Margen':'mean',
												'Anio':'max',
												'Mes':'max',
												'Dia':'max',
												'Producto':'max',
												'Nom_cliente':'max'}).reset_index()	
	
	#Para poder restar las notas de crédito eliminamos los NAS
	sub_fac1['N_cred'] = sub_fac1['N_cred'].fillna(0)
	sub_fac1['Subt_fac'] = sub_fac1['Subt_fac'] - sub_fac1['N_cred']
	sub_fac2['N_cred'] = sub_fac2['N_cred'].fillna(0)
	sub_fac2['Subt_fac'] = sub_fac2['Subt_fac'] - sub_fac2['N_cred']
	
	#st.write(sub_fac1)

	#st.write(sub_fac1)
	#st.write(fac_act.iloc[:,2].sum(axis=0))
	#st.write(a_act.head(5))
	# Creacion del grupo canal_prod
	#fac_act = df_ventas.groupby(['Anio','Mes','Canal_prod']).agg({'Cant_surt':'sum',
	#											'Subt_fac':'sum',
	#											'Utilidad_mov':'sum',
	#											'Margen':'mean'}).reset_index()




	fac_act = sub_fac1.groupby(['Anio','Mes','Canal_cliente']).agg({'Cant_surt':'sum',
												'Subt_fac':'sum',
												'Utilidad_mov':'sum',
												'Margen':'mean'}).reset_index()
	fac_act = fac_act.sort_values(by=['Utilidad_mov'],ascending=False)
	#st.write(fac_act)
	#Función para obtener el ultimo dia del mes
	def last_day_of_month(date):
		if date.month == 12:
			return date.replace(day=31)
		return date.replace(month=date.month+1, day=1) - timedelta(days=1)

	# se creó un diccionario el cual contiene los meses del año 
	mes_diccioanrio = { 1:'ene', 2:'feb', 3:'mar', 4:'abr', 5:'may',6:'jun',
		    			7:'jul',8:'ago',9:'sep',10:'oct',11:'nov',12:'dic'}
	now = datetime.now(pytz.timezone("America/Mexico_City")) # se guarda la fecha actual
	#st.write(now.day)
	dia = now.day
	if dia == 1:
		yesterday = now.replace(month = now.month, day = now.day)
	else:
		yesterday = now.replace(month = now.month, day = now.day - 1)
	
	act = now.year # de la fecha actual se guarda solo el año en curso
	m = now.month # de la fecha actual se guarda el mes en curso(esto solo devolverá un numero) 
	mes = mes_diccioanrio[m]  # el numero que se guardó en la variable 'm' corresponde al mes en curso, de esta forma se manda a llamar el nombre del mes, que ya esta identificado en el diccionario 
	fac_act['Anio'] = pd.to_numeric(fac_act['Anio'])
	a_act = fac_act[fac_act['Anio']== act].drop(columns=['Anio']) # se aplica el filto por año, el cual se almacenará e la variable a_act
	#st.write(fac_act['Anio'])
	#st.write(a_act)
	#st.write(a_act)
	last_day = last_day_of_month(now)
	#st.write(a_act.iloc[:,4].sum(axis=0))
	#a_act['Mes'] = a_act['Mes'].str.strip()
	#a_act['Mes'] = pd.to_numeric(a_act['Mes'])
	#st.write(a_act[a_act['Mes']==mes])
	#st.write(mes)
	a_act = a_act.replace({'Mes': mes_diccioanrio})
	#st.write(a_act)
	d_act = a_act[a_act['Mes'] == mes].drop(columns=['Mes'])
	#st.write(d_act)
	obj_canal = objetivos.groupby(['Cliente','Desc_prod','Canal']).agg({'Objetivos pesos':'sum',
																	'Objetivo piezas':'sum'})
	
	v_dia = d_act.iloc[:,2].sum(axis=0)
	#Calculamos el avance porcentual en tiempo
	por_tiempo = (now.day/last_day.day)*100
	obj_canal = obj_canal.groupby(['Canal']).agg({'Objetivos pesos':'sum',
													'Objetivo piezas':'sum'})
	avance_mes = a_act[a_act['Mes']== mes].drop(columns=['Mes'])
	avance = pd.merge(obj_canal, avance_mes, how='left', right_on=['Canal_cliente'], left_index=True).reset_index()
	avance = avance[['Canal_cliente', 'Cant_surt', 'Subt_fac', 'Utilidad_mov', 'Margen', 'Objetivos pesos', 'Objetivo piezas']]
	avance.columns = ['Canal', 'Venta(PZA)', 'Venta($)', 'Utilidad', 'Margen', 'Objetivo($)', 'Objetivo(PZA)']
	avance = avance.sort_values(by=['Objetivo($)'],ascending=False)
	v_objetivo = avance.iloc[:,5].sum(axis=0)
	avance_objetivo = v_dia - v_objetivo
	avance_objetivo_por = (v_dia/v_objetivo)*100
	dif_avance_por = avance_objetivo_por - por_tiempo
	
	
	back_ant = pedidos[pedidos['Back_month'] == 'ANT']
	back_ant = back_ant.groupby(['Canal']).agg({'importe':'sum'})
	back_ant.columns = ['Back anterior']
	back_pos = pedidos[pedidos['Back_month'] == 'POS']
	back_pos = back_pos.groupby(['Canal']).agg({'importe':'sum'})
	back_pos.columns = ['Back posterior']
	back_act = pedidos[(pedidos['Back_month'] == m)]
	back_act = back_act.groupby(['Canal']).agg({'importe':'sum'})
	back_act.columns = ['Back Mes']
	#st.write(pedidos)
	#st.write(back_ant.sum())
	#st.write(pedidos.head(5))
	avance = avance.merge(remisiones, on='Canal', how='left')
	avance = avance.merge(back_ant, on='Canal', how='left')
	avance = avance.merge(back_pos, on='Canal', how='left')
	avance = avance.merge(back_act, on='Canal', how='left')
	avance = avance.fillna(0)
	#p_pedidos = pedidos.groupby(['Producto']).agg({''})
	#st.write(df_existencias.head(5))
	p_pedidos = pedidos.groupby(['Producto', 'SKU', 'Back_month']).agg({'Cantidad_pedida':'sum',
																			'Cantidad_surtida':'sum',
																			'Liquidado':'sum',
																			'Saldo':'sum',
																			'Precio':'mean',
																			'importe':'sum'}).reset_index()
	p_pedidos = p_pedidos.merge(df_existencias_4, on='Producto', how='outer')
	p_pedidos = p_pedidos.merge(df_existencias_5, on='Producto', how='outer')

	back_ant = p_pedidos[(p_pedidos['Back_month'] == 'ANT')][['Producto','Saldo','Precio','importe']]
	back_pos = p_pedidos[(p_pedidos['Back_month'] == 'POS')][['Producto','Saldo','Precio','importe']]
	back_act = p_pedidos[(p_pedidos['Back_month'] == m)][['Producto','Saldo','Precio','importe']]	
	produccion = back_ant.merge(back_pos, on='Producto', how='outer')
	produccion = produccion.merge(back_act, on='Producto', how='outer')
	produccion = produccion.merge(df_existencias_4, on='Producto', how='left')
	produccion = produccion.merge(df_existencias_5, on='Producto', how='left')
	produccion.columns = ['Producto', 'Back Ant (PZA)', 'Precio BA', 'Importe BA', 'Back Pos (PZA)', 'Precio BP', 'Importe BP',
						  'Back Act (PZA)', 'Precio B_ACT', 'Importe B_ACT', 'Costo proc', 'Existencia proceso', 'Costo Pt', 
						  'Existencia PT']
	produccion = produccion.fillna(0)
	#Añadimos las columnas que serviran de metrica para el avance de producción
	produccion['Existencia total'] = produccion['Existencia proceso'] + produccion['Existencia PT']
	produccion['Back del mes ($)'] = produccion['Importe B_ACT'] + produccion['Importe BA']
	produccion['Back del mes (PZA)'] = produccion['Back Act (PZA)'] + produccion['Back Ant (PZA)']
	produccion['Avance proceso'] = produccion['Existencia proceso']/produccion['Back del mes (PZA)']
	produccion['Avance terminado'] = produccion['Existencia PT']/produccion['Back del mes (PZA)']
	produccion['Avance produccion'] = produccion['Avance proceso'] + produccion['Avance terminado']
	#st.write(df_existencias_5.head(5))
	#st.write(back_ant.head(5))
	#produccion.replace(None, 0)
	#produccion = produccion.fillna(0)
	#produccion['Back Ant ($)'] = produccion['Back Ant (PZA)'] * produccion['Precio BA']
	#produccion['Back Pos ($)'] = produccion['Back Pos (PZA)'] * produccion['Precio BP']
	#produccion['Back Act ($)'] = produccion['Back Act (PZA)'] * produccion['Precio B_ACT']
	#produccion['Back total (PZA)'] = produccion['Back Ant (PZA)'] + produccion['Back Pos (PZA)'] + produccion['Back Act (PZA)']
	#produccion['Back total ($)'] = produccion['Back Ant ($)'] + produccion['Back Pos ($)'] + produccion['Back Act ($)']
	produccion['Existencia total'] = produccion['Existencia proceso'] + produccion['Existencia PT']
	#pp1 = produccion['Importe BA'].sum()
	#pp2 = produccion['Importe B_ACT'].sum()
	#pp3 = produccion['Importe BP'].sum()
	
	
	#st.write(pp3)
	#mes_corriente = mes_diccioanrio[m]
	#descuentos = sub_fac1[(sub_fac1['Mes'] == mes_corriente)]
	#descuentos = descuentos.groupby(['No_fac']).agg({'N_cred':'mean'}).reset_index()
	#descuentos = descuentos[descuentos['N_cred']<0]
	#st.write(descuentos)

	uno, dos = st.columns([1,1])
	with uno:
		st.metric('Ventas al dia ($)', millify(v_dia, precision=1), delta=millify(avance_objetivo, precision=1))
		#st_card('Ventas al dia ($)', v_dia, show_progress=True)
	with dos:
		prefixes = ['%']
		st.metric('Avance en tiempo (%)', millify(por_tiempo, precision=2), delta = millify(dif_avance_por, precision=2))
	#st.write('$ ', d_act.iloc[:,2].sum(axis=0))

	st.write(avance)
	
	######CONSTRUCCIÓN PARA REPORTE DE ABRAHAMA########
	if st.checkbox('Reporte Abraham'):
		#anio, mes = st.columns([1,1])
		#Mes_si = st.selectbox('Selecciona el mes para el reporte Abraham Torres', sub_fac2['Mes'].unique())
		Mes_si = st.multiselect('Selecciona los meses para el reporte Abraham Torres', sub_fac2['Mes'].unique())
		anio_si = st.selectbox('Selecciona el año para el reporte Abraham Torres', sub_fac2['Anio'].unique())
	####################AÑO###########################
		clas = clases.copy()
		clas.columns = ['SKU','Categoria','Producto']
		sub_fac2.columns = ['No_fac', 'Canal_cliente', 'sub_fac', 'Cant_surt', 'N_cred', 'Costo', 'Utilidad_mov', 'Margen', 'Anio', 'Mes',
							'Dia', 'Producto', 'Cliente']
		sub_fac2 = sub_fac2[sub_fac2['Anio']==anio_si]
		objetivo_temp = objetivos.copy()
		clas['Cve_prod'] = clas['SKU'].str.strip()
		objetivo_temp['Cve_prod'] = objetivo_temp['Cve_prod'].str.strip()
		objetivo_temp = pd.merge(objetivo_temp, clas, on='Cve_prod', how='left').reset_index()
		#st.write(objetivo_temp)
		objetivo = objetivo_temp.groupby(['Cve_cte', 'Cliente', 'Categoria']).agg({'Objetivos pesos':'sum',
															      'Objetivo piezas':'sum'}).reset_index()
		#st.write(objetivo)
		fac_repo = pd.merge(sub_fac2, clas, on='Producto', how='left').reset_index(drop=True)
		fac_cte = df[['No_fac', 'Cve_cte']] 
		fac_cte = fac_cte.groupby(['No_fac']).agg({'Cve_cte':'max'}).reset_index()
		#st.write(fac_cte)
		#fac_cte = pd.merge(fac_cte, objetivo, on='Cve_cte', how='left')
		#st.write(fac_cte)
		fac_repo = pd.merge(fac_repo, fac_cte, on='No_fac', how='left').reset_index(drop=True)
		#st.write(fac_repo)
		#st.write(fac_repo)
		fac_repo['Cliente'] = fac_repo['Cliente'].str.strip()
		fac_repo['Categoria'] = fac_repo['Categoria'].fillna('OTRA')
		fac_repo = fac_repo.fillna(0)
		#st.write(fac_repo)
		final = fac_repo.groupby(['Categoria', 'Cliente']).agg({'sub_fac':'sum',
																'Cant_surt':'sum',
																'Cve_cte':'max'})
		final = pd.merge(final, objetivo, on=['Cve_cte', 'Categoria'], how='left').reset_index(drop=True)
		final = final[['Categoria', 'Cliente', 'sub_fac', 'Cant_surt', 'Objetivos pesos', 'Objetivo piezas', 'Cve_cte']]
		final.columns = ['Categoria', 'Cliente', 'Venta $', 'Venta PZA', 'Objetivo $', 'Objetivo PZA', 'Cve_cte']
		final = final.fillna(0)
		#st.write(final)
		##################AÑO############################################################

		####################MES###########################
		clas2 = clases.copy()
		clas2.columns = ['SKU','Categoria','Producto']
		sub_fac2.columns = ['No_fac', 'Canal_cliente', 'sub_fac', 'Cant_surt', 'N_cred', 'Costo', 'Utilidad_mov', 'Margen', 'Anio', 'Mes',
							'Dia', 'Producto', 'Cliente']					
		#sub_fac3 = sub_fac2[sub_fac2['Mes']==Mes_si]
		sub_fac3 = sub_fac2[sub_fac2['Mes'].isin(Mes_si)]
		objetivo_temp = objetivos.copy()
		clas2['Cve_prod'] = clas2['SKU'].str.strip()
		objetivo_temp['Cve_prod'] = objetivo_temp['Cve_prod'].str.strip()
		objetivo_temp = pd.merge(objetivo_temp, clas2, on='Cve_prod', how='left').reset_index()
		#st.write(objetivo_temp)
		objetivo = objetivo_temp.groupby(['Cve_cte', 'Cliente', 'Categoria']).agg({'Objetivos pesos':'sum',
															      'Objetivo piezas':'sum'}).reset_index()
		#st.write(objetivo)
		fac_repo2 = pd.merge(sub_fac3, clas2, on='Producto', how='left').reset_index(drop=True)
		fac_cte2 = df[['No_fac', 'Cve_cte']] 
		fac_cte2 = fac_cte2.groupby(['No_fac']).agg({'Cve_cte':'max'}).reset_index()
		#st.write(fac_cte)
		#fac_cte = pd.merge(fac_cte, objetivo, on='Cve_cte', how='left')
		#st.write(fac_cte)
		fac_repo2 = pd.merge(fac_repo2, fac_cte2, on='No_fac', how='left').reset_index(drop=True)
		#st.write(fac_repo)
		#st.write(fac_repo)
		fac_repo2['Cliente'] = fac_repo2['Cliente'].str.strip()
		fac_repo2['Categoria'] = fac_repo2['Categoria'].fillna('OTRA')
		fac_repo2 = fac_repo2.fillna(0)
		#st.write(fac_repo)
		final2 = fac_repo2.groupby(['Categoria', 'Cliente']).agg({'sub_fac':'sum',
																'Cant_surt':'sum',
																'Cve_cte':'max'})
		final2 = pd.merge(final2, objetivo, on=['Cve_cte', 'Categoria'], how='left').reset_index(drop=True)
		final2 = final2[['Categoria', 'Cliente', 'sub_fac', 'Cant_surt', 'Objetivos pesos', 'Objetivo piezas', 'Cve_cte']]
		final2.columns = ['Categoria', 'Cliente', 'Venta $', 'Venta PZA', 'Objetivo $', 'Objetivo PZA', 'Cve_cte']
		final2 = final2.fillna(0)
		##################MES############################################################

		################################################################################



		#st.write(final)

		client_list = [372, 373, 281, 4, 435, 364, 423]
		final = final[(final['Cve_cte'].isin(client_list))]
		final2 = final2[(final2['Cve_cte'].isin(client_list))]
		so_cte = sellout.copy()
		#st.write(clases)
		clas3 = clases.copy()
		clas3.columns=['Cve_prod', 'Categoria', 'Desc_prod']
		clas3['Cve_prod'] = clas3['Cve_prod'].str.strip()
		so_cte = pd.merge(so_cte, clas3, on='Cve_prod', how='left')
		so_cte = so_cte[so_cte['Anio'] == act]
		so_cte = so_cte.fillna(0)
		#st.write(so_cte)
		so_pesos = so_cte[['Categoria', 'Cliente', 'Venta ($)', 'Mes', 'Cve_cte']]
		so_pesos = so_pesos[so_pesos['Cve_cte'].isin(client_list)]
		so_pesos['Categoria'] = so_pesos['Categoria'].replace(0,'OTRA')
		so_pesos = so_pesos.groupby(['Mes', 'Categoria', 'Cliente']).agg({'Venta ($)':'sum'}).reset_index()
		#st.write(so_pesos)
		
		#so_cte = so_cte.groupby(['Categoria', 'Cliente']).agg({'Venta ($)':'sum',
		#													   'Venta (pza)':'sum'})
		#st.write(mes_diccioanrio[m])
		#if (final['Cliente'] == 0):
		#	final['Cliente'] == 'PHARMA PLUS'
		#st.write(final)
		#st.write(sellout)

		#with anio:
		#	st.write(final)
		#	if st.checkbox('Sellout'):
		#		st.write(so_pesos)
		#with mes:
		#Mes_si = st.selectbox('Selecciona el mes', final2['Mes'].unique())
		st.write(final2)
	
	st.header('Avance Producción')
	
	produccion = produccion.fillna(0)
	produccion = produccion.replace([np.inf,-np.inf],0)
	
	

	chart_data = produccion[['Producto','Back del mes (PZA)', 'Existencia proceso', 'Existencia PT', 'Existencia total']]
	chart_data = chart_data[chart_data['Back del mes (PZA)'] > 0]
	chart_data['Avance terminado'] = chart_data['Existencia PT']/chart_data['Back del mes (PZA)']
	chart_data['Avance proceso'] = chart_data['Existencia proceso']/chart_data['Back del mes (PZA)']
	chart_data['Avance produccion'] = chart_data['Avance terminado'] + chart_data['Avance proceso']
	chart_data = chart_data.sort_values(by=['Back del mes (PZA)'],ascending=False)
	#avancept = chart_data['Avance terminado'].mean()*100
	#avancepro = chart_data['Avance proceso'].mean()*100
	#avancetot = chart_data['Avance produccion'].mean()*100
	#st.write(chart_data)


	uno, dos = st.columns([1,1])
	with uno:
		st.metric('Pedidos del mes ($)', millify(produccion['Importe B_ACT'].sum(), precision=1))
		st.metric('Pedidos Acumulados sin entregar ($)', millify(produccion['Importe BA'].sum(), precision=1))
		st.metric('Pedidos a entregar después ($)', millify(produccion['Importe BP'].sum(), precision=1))
	with dos:
		st.metric('Pedidos del mes (PZA)', prettify(round(produccion['Back Act (PZA)'].sum())))
		st.metric('Pedidos Acumulados sin entregar (PZA)', prettify(round(produccion['Back Ant (PZA)'].sum())))
		st.metric('Pedidos a entregar después (PZA)', prettify(round(produccion['Back Pos (PZA)'].sum())))
	#with tres:
	#	st.metric('Avance promedio PT (%)', avancept)
	#	st.metric('Avance promedio Proceso (%)', avancepro)
	#	st.metric('Avance promedio total (%)', avancetot)

	if st.checkbox('Ver tabla completa de avance producción, pedidos y existencia por producto'):
		st.write(chart_data)
	bar_data = chart_data[['Producto', 'Back del mes (PZA)', 'Existencia total']]

	base = alt.Chart(bar_data).transform_calculate(
		BackOrder = "'BackOrder'",
		Existencia = "'Existencia'",
	)
	scale = alt.Scale(domain=['BackOrder', 'Existencia'], range=['salmon', 'DarkCyan'])

	barr = base.mark_bar(color='salmon').encode(
		x=alt.X('Producto', title='Producto'),
		y=alt.Y('Back del mes (PZA)', axis=alt.Axis(title='Back Order')),
		color=alt.Color('BackOrder:N', scale=scale, title=''),
	)
	barr2 = base.mark_bar(color='DarkCyan').encode(
		x=alt.X('Producto', title='Producto'),
		y=alt.Y('Existencia total', axis=alt.Axis(title='Existencia')),
		color=alt.Color('Existencia:N', scale=scale, title=''),
	)
	stack = alt.layer(
		barr + barr2)
	st.altair_chart(stack)
	faltantes = chart_data.copy()
	faltantes['Faltantes'] = faltantes['Back del mes (PZA)'] - faltantes['Existencia total']
	faltantes = faltantes[['Producto','Back del mes (PZA)', 'Existencia total', 'Faltantes']]
	faltantes = faltantes[faltantes['Faltantes']>0].reset_index(drop=True)
	#faltantes['Faltantes'] = faltantes['Faltantes']*(-1)
	faltantes = faltantes[['Producto', 'Back del mes (PZA)', 'Faltantes', 'Existencia total']]
	faltantes = faltantes.sort_values(by=['Faltantes'], ascending=False)
	faltantes['Producto'] = faltantes['Producto'].str.strip()
	faltantes_nom = faltantes.merge(df_productos, on='Producto', how='left')
	#st.write(faltantes_nom)
	fcst_faltantes = t_forecast[['SKU', 'Producto', 'Forecast', 'Faltantes', 'Existencia']]
	fcst_faltantes = fcst_faltantes[fcst_faltantes['Faltantes']>0]
	
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
						  (existeN['Lugar'] == 'G2')]
	existeN_comp.columns = ['SKU', 'Lugar', 'MP', 'Existencia']
	existeN_comp = existeN_comp.groupby(['MP']).agg({'Existencia':'sum'}).reset_index()
	#st.write(existeN_comp)
    ####################################
    ### EXPLOSION DE MATERIALES BACK ORDER ###
	pedir_back = faltantes_nom.merge(formulas, on='SKU', how='left')
	
	pedir_back = pedir_back.fillna(0)

	#st.write(pedir_back)
	pedir_back.columns = ['Formula', 'Back del mes (PZA)', 'Faltantes', 'Existencia total', 'SKU', 'Componente', 'Cantidad rendimiento',
						  'Version', 'Unidad mp', 'MP', 'Rendimiento', 'Unidad', 'Cantidad', 'Formulab']
	#st.write(pedir_back)
	pedir_back['Componente'] = pedir_back['Componente'].replace(0,'N')
	#st.write(pedir_back)
	pedir_backme = pedir_back[pedir_back['Componente'].str.startswith('M')].reset_index(drop=True)
	#st.write(pedir_backme)
	pedir_backme['Faltantes me'] = pedir_backme['Cantidad'] * pedir_backme['Faltantes']
	pedir_backst = pedir_back[pedir_back['Componente'].str.startswith('41')].reset_index(drop=True)
	pedir_backst.rename(columns = {'SKU':'SKU_f', 'Componente':'SKU'}, inplace=True)
	pedir_backst['SKU'] = pedir_backst['SKU'].str.strip()
	#formulas.columns = ['']
	pedir_backst = pedir_backst.merge(formulas, on='SKU', how='left')
	pedir_backst['Cantidad mp'] = pedir_backst['Cantidad_y'] * pedir_backst['Faltantes']
	#faltantes_tot = faltantes_nom.merge(t_forecast, on='SKU', how='outer')
	pedir_backst = pedir_backst[['Formula', 'Faltantes', 'MP_y', 'Cantidad mp', 'Back del mes (PZA)']]
	pedir_backst.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'Back del mes (PZA)']
	pedir_backme = pedir_backme[['Formula', 'Faltantes', 'MP', 'Cantidad', 'Back del mes (PZA)']]
	pedir = pd.concat([pedir_backst, pedir_backme])
	pedir['MP'] = pedir['MP'].str.strip()
	pedir = pedir.merge(existeN_comp, on='MP', how='left')
	pedir = pedir.fillna(0)
	pedir['Faltante mp'] = pedir['Cantidad'] - pedir['Existencia']
	pedir['Faltante mp'][(pedir['Faltante mp'] < 0)] = 0
	requi = pedir.groupby(['MP']).agg({'Cantidad':'sum', 'Existencia':'sum', 'Faltante mp':'sum'}).reset_index()
	costo_for = df_formulas[['Desc_prod', 'Cto_rep']]
	costo_for.columns = ['MP', 'Costo']
	costo_for =costo_for.groupby(['MP']).agg({'Costo':'mean'}).reset_index()
	costo_for['MP'] = costo_for['MP'].str.strip()
	#st.write(costo_for)
	requi = requi.merge(costo_for, on='MP', how='left')
	requi['Costo total'] = requi['Faltante mp'] * requi['Costo']
	total_requi = requi['Costo total'].sum()
	frase1 = 'Inversión total $' + str(round(total_requi,2))
	##########################################
	### EXPLOSION DE MATERIALES FORECAST ###
	pedir_fcst = fcst_faltantes.merge(formulas, on='SKU', how='left')
	pedir_fcst = pedir_fcst.dropna()
	#st.write(pedir_fcst)
	pedir_fcstme = pedir_fcst[pedir_fcst['Cve_prod'].str.startswith('M')].reset_index(drop=True)
	pedir_fcstme['Faltantes me'] = pedir_fcstme['Faltantes'] * pedir_fcstme['Cantidad']
	pedir_fcstst = pedir_fcst[pedir_fcst['Cve_prod'].str.startswith('41')].reset_index(drop=True)
	pedir_fcstst.rename(columns = {'SKU':'SKU_f', 'Cve_prod':'SKU'}, inplace=True)
	pedir_fcstst['SKU'] = pedir_fcstst['SKU'].str.strip()
	pedir_fcstst = pedir_fcstst.merge(formulas, on='SKU', how='left')
	pedir_fcstst['Cantidad mp'] = pedir_fcstst['Cantidad_y'] * pedir_fcstst['Faltantes']
	pedir_fcstst = pedir_fcstst[['Producto_x', 'Faltantes', 'MP_y', 'Cantidad mp', 'Forecast']]
	pedir_fcstst.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'Forecast']
	pedir_fcstme = pedir_fcstme[['Producto_x', 'Faltantes', 'MP', 'Faltantes me', 'Forecast']]
	pedir_fcstme.columns = ['Formula', 'Faltantes', 'MP', 'Cantidad', 'Forecast']
	pedir2 = pd.concat([pedir_fcstst, pedir_fcstme])
	pedir2['MP'] = pedir2['MP'].str.strip()
	pedir2 = pedir2.merge(existeN_comp, on='MP', how='left')
	pedir2 = pedir2.fillna(0)
	pedir2['Faltante mp'] = pedir2['Cantidad'] - pedir2['Existencia']
	pedir2['Faltante mp'][(pedir2['Faltante mp'] < 0)] = 0
	requi2 = pedir2.groupby(['MP']).agg({'Cantidad':'sum', 'Existencia':'sum', 'Faltante mp':'sum'}).reset_index()
	requi2 = requi2.merge(costo_for, on='MP', how='left')
	requi2['Costo total'] = requi2['Faltante mp'] * requi2['Costo']
	total_requi2 = requi2['Costo total'].sum()
	frase2 = 'Inversión total $' + str(round(total_requi2,2))
	##########################################	
	#st.write(pedir_fcstme)
	#st.write(formulas)
	if st.checkbox('Piezas faltantes Back Order'):
		tabla, grafico = st.columns([1,1])
		with tabla:
			st.write(faltantes)
		with grafico:
			g_falt = alt.Chart(faltantes).mark_bar(color='salmon').encode(
				x=alt.X('Faltantes', title='Faltantes'),
				y=alt.Y('Producto', title='Producto')
				)
			st.altair_chart(g_falt)
		if st.checkbox('Materiales faltantes Back'):
			tabla, requisicion = st.columns([1,1])
			with tabla:
				st.write('Materiales por formula', pedir)
				#st.download_button(label="Descargar", data=pedir.to_csv(), mime="text/csv")
			with requisicion:
				st.write('Requisición', requi)
				#st.download_button(label="Descargar", data=requi.to_csv(), mime="text/csv")
				st.info(frase1)
	if st.checkbox('Piezas faltantes Forecast'):
		tabla, grafico = st.columns([1,1])
		with tabla:
			st.write(fcst_faltantes)
		with grafico:
			f_falt = alt.Chart(fcst_faltantes).mark_bar(color='DarkCyan').encode(
			x=alt.X('Faltantes', title='Faltantes'),
			y=alt.Y('Producto', title='Producto')
			)
			st.altair_chart(f_falt)
		if st.checkbox('Materiales faltantes Forecast'):
			tabla, requisicion = st.columns([1,1])
			with tabla:
				st.write('Materiales por formula', pedir2)
				#st.download_button(label="Descargar", data=pedir2.to_csv(), mime="text/csv")
			with requisicion:
				st.write('Requisición', requi2)
				#st.download_button(label="Descargar", data=requi2.to_csv(), mime="text/csv")
				st.info(frase2)
	#if st.checkbox('Piezas faltantes Forecast'):

	#barr = alt.Chart(bar_data).mark_bar(color='salmon').encode(
	#	x=alt.X('Producto', title='Producto'),
	#	y=alt.Y('Back del mes (PZA)', axis=alt.Axis(title='Back Order')),	
	#)
	#barr_2 = alt.Chart(bar_data).mark_tick(
	#	color='red',
	#	thickness=3,
	#	size=40 * 0.9,
	#	).encode(
	#	x='Producto',
	#	y='Existencia total'
	#	)
	#barr_3 = alt.Chart(bar_data).mark_bar(color='DarkCyan').encode(
	#	x=alt.X('Producto', title='Producto'),
	#	y=alt.Y('Existencia total', axis=alt.Axis(title='Existencia')),
	#)

	#st.altair_chart(barr + barr_3)


	#st.write(avance_mes) # se muestra la tabla filtrando por mes actual

	#Separamos en dos frames de lado izquiero los filtros
	for i in range(len(df_ventas['Nom_cliente'])):
		df_ventas.loc[i,'Nom_cliente'] = str(df_ventas.loc[i,'Nom_cliente'])
	#De lado derecho imprimiremos la tabla filtrada


	st.sidebar.title("Filtros")	
	emp_list =	st.sidebar.multiselect("Empresa", df_ventas['Cve_factu'].unique())
	ano_list =  st.sidebar.multiselect("Año", sorted(df_ventas['Anio'].unique()))
	mes_list =  st.sidebar.multiselect("Mes", sorted(df_ventas['Mes'].unique()))
	cte_list =  st.sidebar.multiselect("Cliente", sorted(df_ventas['Nom_cliente'].unique()))

		# if st.checkbox("Aplicar Filtros"):
	if not emp_list:
		emp_list =	df_ventas['Cve_factu'].unique()
	if not ano_list:
		ano_list = df_ventas['Anio'].unique()
	if not mes_list:
		mes_list = df_ventas['Mes'].unique()
	if not cte_list:
		cte_list = df_ventas['Nom_cliente'].unique()	
 	
	df_filtered = df_ventas[
			 (df_ventas['Cve_factu'].isin(emp_list)) & 
			 (df_ventas['Anio'].isin(ano_list)) & 
			 (df_ventas['Mes'].isin(mes_list)) &
			 (df_ventas['Nom_cliente'].isin(cte_list))]
	#Mes por letra 3 digitos
	#st.write(mes_diccioanrio[10])
	mes_letra = []
	for i in range(len(mes_list)):
		mes_letra.append(mes_diccioanrio[mes_list[i]])

	df_sellout = sellout[
			(sellout['Mes'].isin(mes_letra)) &
			(sellout['Anio'].isin(ano_list)) &
			(sellout['Cliente'].isin(cte_list))]

	df_filtered = df_filtered[['Nom_cliente','Producto','Cant_surt', 'Subt_fac', 'Utilidad_mov','Margen']]
	df_sellout = df_sellout.fillna(0)
	#Agregamos la columna porcentaje que será la venta ($) entre el total de ventas
	
	tot_vta = df_filtered.iloc[:,3].sum(axis=0)

	df_filtered['Porcentaje'] = (df_filtered['Subt_fac']/tot_vta)*100 
	###BENEFICIO POR PRODUCTO###
	st.subheader('Tabla beneficio por producto')
	df_filtered['Producto'] = df_filtered['Producto'].str.strip()
	df_group = df_filtered.groupby(['Producto']).agg({'Cant_surt':'sum',
													  'Subt_fac':'sum',
						   							  'Utilidad_mov':'sum', 
													  'Margen':'mean',
													  'Porcentaje':'sum'})
	df_group = df_group.sort_values(by=['Utilidad_mov'],ascending=False)
	df_group = df_group[['Cant_surt', 'Subt_fac', 'Utilidad_mov', 'Porcentaje']]
	df_group.columns = ['Venta (PZA)', 'Venta ($)', 'Utilidad', 'Porcentaje']
	st.write(df_group)
	#st.download_button(label="Descargar", data=df_group.to_csv(), mime="text/csv")
	###SELLOUTXPRODUCTO###
	df_groups = df_sellout.groupby(['Producto']).agg({'Venta (pza)':'sum',
													  'Venta ($)':'sum'}).sort_values(by=['Venta (pza)'],ascending=False)
	df_groups = df_groups[(df_groups['Venta (pza)'] > 0)]
	if st.checkbox('Sellout por producto'):
		st.write(df_groups)
		#st.download_button(label="Descargar", data=df_groups.to_csv(), mime="text/csv")

	#top, bottom=st.columns([10,10])
	top, bottom=st.columns(2)
	with top:
		#GRAFICA TOP 5
		#Con esta instrucción permitimos a altair mostrar la gráfica aunque tenga mas de 5000 renglones
		alt.data_transformers.enable('default', max_rows=None)
		#Agrupamos los datos, ordenamos de mayor a menor por la utilidad y extraemos 5 datos
		top_5 = df_filtered.groupby(['Producto'], as_index = False).agg({'Cant_surt':'sum', 
								   										'Subt_fac':'sum', 
																		'Margen':'mean'})
		top_5 = df_group.sort_values(by=['Venta ($)'],ascending=False).head(5).reset_index()
		#top_6 = top_6.rename_axis(index=['Producto','Cant_surt','Utilidad_mov','Margen'])
		#top_5 = df_filtered[['Producto','Utilidad_mov']]
		#Construimos el gráfico con altair 
		pie_top = alt.Chart(top_5, title='Top 5 Ventas por Producto').mark_arc().encode(
	    theta=alt.Theta(field='Venta ($)', type="quantitative"),
	   	color=alt.Color(field='Producto', type="nominal"),
	   	tooltip = ['Producto','Venta ($)', 'Porcentaje']
	   	)
	    #Mostramos el objeto en streamlit
		st.altair_chart(pie_top, use_container_width=True)
	with bottom:
		#GRAFICA BOTTOM 5
		#Con esta instrucción permitimos a altair mostrar la gráfica aunque tenga mas de 5000 renglones
		alt.data_transformers.enable('default', max_rows=None)
		#Agrupamos los datos, ordenamos de mayor a menor por la utilidad y extraemos 5 datos
		bottom_5 = df_filtered.groupby(['Producto'], as_index = False).agg({'Cant_surt':'sum', 
								      										'Subt_fac':'sum',
																			'Margen':'mean'})
		bottom_5 = df_group.sort_values(by=['Venta ($)'],ascending=True).head(5).reset_index()
		#top_6 = top_6.rename_axis(index=['Producto','Cant_surt','Utilidad_mov','Margen'])
		#top_5 = df_filtered[['Producto','Utilidad_mov']]
		#Construimos el gráfico con altair 
		pie_bottom = alt.Chart(bottom_5, title='Bottom 5 Ventas por Producto').mark_arc().encode(
	    theta=alt.Theta(field='Venta ($)', type="quantitative"),
	   	color=alt.Color(field='Producto', type="nominal", scale=alt.Scale(scheme='tableau10')),
	   	tooltip = ['Producto','Venta ($)', 'Porcentaje']
	   	)
	    #Mostramos el objeto en streamlit
		st.altair_chart(pie_bottom, use_container_width=True)
	############################
	###BENEFICIO POR CLIENTE###
	st.subheader('Tabla beneficio por cliente')
	df_filtered['Nom_cliente'] = df_filtered['Nom_cliente'].str.strip()
	df_group = df_filtered.groupby(['Nom_cliente']).agg({'Cant_surt':'sum',
													  'Subt_fac':'sum',
						   							  'Utilidad_mov':'sum', 
													  'Margen':'mean',
													  'Porcentaje':'sum'})
	df_group = df_group.sort_values(by=['Subt_fac'],ascending=False)
	df_group = df_group[['Cant_surt', 'Subt_fac', 'Utilidad_mov', 'Porcentaje']]
	df_group.columns = ['Venta (PZA)', 'Venta ($)', 'Utilidad', 'Porcentaje']
	st.write(df_group)
	#st.download_button(label="Descargar", data=df_group.to_csv(), mime="text/csv")
	###SELLOUT POR CLIENTE###
	df_groupsc = df_sellout.groupby(['Cliente']).agg({'Venta (pza)':'sum',
													 'Venta ($)':'sum'}).sort_values(by=['Venta (pza)'],ascending=False)
	df_groupsc = df_groupsc[(df_groupsc['Venta (pza)']>0)]
	if st.checkbox('Sellout por cliente'):
		st.write(df_groupsc)
		#st.download_button(label="Descargar", data=df_groupsc.to_csv(), mime="text/csv")
	#top, bottom=st.columns([10,10])
	top, bottom=st.columns(2)
	with top:
		#GRAFICA TOP 5
		#Con esta instrucción permitimos a altair mostrar la gráfica aunque tenga mas de 5000 renglones
		alt.data_transformers.enable('default', max_rows=None)
		#Agrupamos los datos, ordenamos de mayor a menor por la utilidad y extraemos 5 datos
		top_5 = df_filtered.groupby(['Nom_cliente'], as_index = False).agg({'Cant_surt':'sum', 
								   										'Subt_fac':'sum', 
																		'Margen':'mean'})
		top_5 = df_group.sort_values(by=['Venta ($)'],ascending=False).head(5).reset_index()
		#top_6 = top_6.rename_axis(index=['Producto','Cant_surt','Utilidad_mov','Margen'])
		#top_5 = df_filtered[['Producto','Utilidad_mov']]
		#Construimos el gráfico con altair 
		pie_top = alt.Chart(top_5, title='Top 5 Ventas por Cliente').mark_arc().encode(
	    theta=alt.Theta(field='Venta ($)', type="quantitative"),
	   	color=alt.Color(field='Nom_cliente', type="nominal"),
	   	tooltip = ['Nom_cliente','Venta ($)', 'Porcentaje']
	   	)
	    #Mostramos el objeto en streamlit
		st.altair_chart(pie_top, use_container_width=True)
	with bottom:
		#GRAFICA BOTTOM 5
		#Con esta instrucción permitimos a altair mostrar la gráfica aunque tenga mas de 5000 renglones
		alt.data_transformers.enable('default', max_rows=None)
		#Agrupamos los datos, ordenamos de mayor a menor por la utilidad y extraemos 5 datos
		bottom_5 = df_filtered.groupby(['Nom_cliente'], as_index = False).agg({'Cant_surt':'sum', 
								      										'Subt_fac':'sum',
																			'Margen':'mean'})
		bottom_5 = df_group.sort_values(by=['Venta ($)'],ascending=True).head(5).reset_index()
		#top_6 = top_6.rename_axis(index=['Producto','Cant_surt','Utilidad_mov','Margen'])
		#top_5 = df_filtered[['Producto','Utilidad_mov']]
		#Construimos el gráfico con altair 
		pie_bottom = alt.Chart(bottom_5, title='Bottom 5 Ventas por Cliente').mark_arc().encode(
	    theta=alt.Theta(field='Venta ($)', type="quantitative"),
	   	color=alt.Color(field='Nom_cliente', type="nominal", scale=alt.Scale(scheme='tableau10')),
	   	tooltip = ['Nom_cliente','Venta ($)', 'Porcentaje']
	   	)
	    #Mostramos el objeto en streamlit
		st.altair_chart(pie_bottom, use_container_width=True)
	############################


	#Siguiente sección con datos de ventas historicos
	st.subheader('Tabla históricos por año')
	#Agrupamos primero nuestro dataframe por factura para poder descontar las notas de crédito
	df_filtered_2 = df_ventas[
			 (df_ventas['Cve_factu'].isin(emp_list)) & 
			 (df_ventas['Nom_cliente'].isin(cte_list))]
	clas3 = clases.copy()
	clas3.columns = ['SKU','Categoria','Producto']
	df_filtered_2 = pd.merge(df_filtered_2, clas3, on='Producto', how='left')
	df_filtered_2['Categoria'] = df_filtered_2['Categoria'].fillna('OTRA')
	#st.write(df_filtered_2)
	#st.write(notasc)
	#ncred = notasc.copy()
	#ncred = ncred[['No_fac', 'Subtotal']]
	facprod = df_filtered_2[['No_fac', 'Producto', 'Categoria', 'Subt_fac', 'Cant_surt']]
	#st.write(df_filtered_2)
	facprod.columns = facprod.columns.str.strip()
	sub_fac =df_filtered_2.groupby(['No_fac']).agg({'Subt_fac':'sum',
					     						'Cant_surt':'sum',
												'N_cred':'mean',
												'Costo':'sum',
												'Utilidad_mov':'sum',
												'Margen':'mean',
												'Anio':'max',
												'Mes':'max'}).reset_index()
	#st.write(sub_fac)
	#sub_fac = pd.merge(df_filtered_2, ncred, on=['No_fac'], how='left')
	#Para poder restar las notas de crédito eliminamos los NAS
	sub_fac['N_cred'] = sub_fac['N_cred'].fillna(0)
	sub_fac['Subt_fac'] = sub_fac['Subt_fac'] - sub_fac['N_cred']
	
	sub_fac4 = pd.merge(sub_fac, facprod, on='No_fac', how='left')
	#st.write(sub_fac4)
	
	sub_fac4 = sub_fac4.groupby(['Anio','Mes','Categoria']).agg({'Subt_fac_x':'sum',
													'Cant_surt_x':'sum',
													'Costo':'sum',
													'Utilidad_mov':'sum',
													'Margen':'mean',
													'Subt_fac_y':'sum',
													'Cant_surt_y':'sum'}).reset_index()
	#st.write(sub_fac4)
	anio = st.selectbox('Año',sub_fac4['Anio'].unique())

	#sub_fac = sub_fac[(sub_fac['Nom_cliente'].isin(cte_list))]
	sub_fac4.columns = ['Anio','Mes', 'Categoria', 'Venta ($)','Venta (Pza)','Costo total','Utilidad','Margen (%)', 'Venta sin desc', 'Cantidad']
	sub_final4 = sub_fac4[sub_fac4['Anio']== anio].drop(columns=['Anio'])
	sub_final4 = sub_final4.fillna(0)
	st.write(sub_final4)
	#st.download_button(label="Descargar", data=sub_final4.to_csv(), mime="text/csv")

	
if __name__ == '__main__':
	main()
