import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import altair as alt
from datetime import datetime, timedelta, date
#import streamlit_card as st_card
import millify
from millify import millify
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
	@st.cache_resource
	def cargar1():
		base1 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/base.csv',encoding='latin-1')
		return  base1
	df = cargar1()
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
	def cargar8():
		base8 = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/Plan2023.csv',encoding='latin-1')
		return base8
	forecast = cargar8()
	def cargar7():
		base7 = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTSWo4ymE0xBaN-Yx0a9PFAwkD5L5CHK8duCdevjwdgt-bFyXpGQZjuzq9FLnBLFg/pub?gid=1655033046&single=true&output=csv',encoding='latin-1')
		return base7
	alfred = cargar7()

	df.columns = df.columns.str.strip()
	remisiones.columns = remisiones.columns.str.strip()
	pedidos.columns = pedidos.columns.str.strip()
	canal.columns = canal.columns.str.strip()
	existencias.columns = existencias.columns.str.strip()
	alfred.columns = alfred.columns.str.strip()
	forecast.columns = forecast.columns.str.strip()
	forecast.columns = ['Cve_prod', 'Producto', 'Tamano lotes', 'Presentacion', 'Cliente', 'Stock', 'Plan Julio', 'Forecast', 'Lotes origin', 'Lotes', 'Nota','NO']
	forecast = forecast[['Cve_prod', 'Producto', 'Plan Julio', 'Forecast', 'Lotes origin']]

	#Filtramos la base para obtener solo las columnas
	#importantes
	df_ventas = df[['No_fac','Falta_fac','Subt_fac','Cve_factu','Cse_prod','Cant_surt','Lugar','Costo','Utilidad_mov','Margen',
	'Categoria','Canal_prod','Canal_cliente','KAM','Subdirec','N_cred','Anio','Mes','Dia','Nom_cliente','Producto']]
	###TRATAMIENTO BASE EXISTENCIAS###
	df_existencias = existencias[['Cve_prod', 'Lote', 'Lugar', 'Cto_ent', 'Existencia', 'Fech_venc', 'Desc_prod', 'Uni_med']]
	df_existencias.columns = ['SKU', 'Lote', 'Lugar', 'Costo', 'Existencia', 'Vencimiento', 'Producto', 'Unidad']
	df_existencias = df_existencias[(df_existencias['Lugar']==5) | (df_existencias['Lugar']==4)]
	df_existencias_4 = df_existencias[(df_existencias['Lugar']==4)]
	df_existencias_5 = df_existencias[(df_existencias['Lugar']==5)]
	df_existencias_4 = df_existencias_4.groupby(['Producto']).agg({'Costo':'mean', 'Existencia':'sum'}).reset_index()
	df_existencias_4.columns = ['Producto', 'Costo', 'Existencia proceso']
	df_existencias_5 = df_existencias_5.groupby(['Producto']).agg({'Costo':'mean', 'Existencia':'sum'}).reset_index()
	df_existencias_5.columns = ['Producto', 'Costo', 'Existencia pt']
	
	###TRATAMIENTO BASE REMISIONES###
	df_remisiones = remisiones[['No_rem', 'Cve_cte', 'Nom_cte', 'Cve_prod', 'Cant_surt', 'Desc_prod', 'Valor_prod']]
	df_remisiones.columns = ['No_rem', 'Cve_cte', 'Cliente', 'SKU', 'Cantidad', 'Producto', 'Precio']
	canal.columns = ['Cve_cte', 'Cliente', 'Canal', 'Kam', 'Subdirector']
	remisiones = df_remisiones.merge(canal, on='Cve_cte', how='left')
	remisiones['importe'] = remisiones['Cantidad'] * remisiones['Precio']
	remisiones.columns = ['No_rem', 'Cve_cte', 'Cliente', 'SKU', 'Cantidad', 'Producto', 'Precio', 'CTE', 'Canal', 'Kam', 'Subdirector', 'importe']
	remisiones = remisiones.groupby(['Canal']).agg({'Cantidad':'sum',
													'importe':'sum'})
	remisiones.columns = ['Remision (PZA)', 'Remision ($)']
	###TRATAMIENTO BASE PEDIDOS###
	###MESES REPETIDO VERIFICAR DESPUES###
	# se creó un diccionario el cual contiene los meses del año 
	mes_diccioanrio = { 1:'ene', 2:'feb', 3:'mar', 4:'abr', 5:'may',6:'jun',
		    			7:'jul',8:'ago',9:'sep',10:'oct',11:'nov',12:'dic'}
	now = datetime.now() # se guarda la fecha actual
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
	
		if df_pedidos.loc[i,'Mes_alta'] == m:
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
	#imprimimos como prueba los primeros cinco datos de la tabla
	#if st.checkbox("Raw data"):
	#	st.write(df_ventas.head(5))
	alfred = alfred.fillna(0)
	alfred = alfred[alfred['SKU'] != 0]
	n_capt = alfred[(alfred['RESULTADO 41'] == 0) | (alfred['ORDEN 51'] == 0) | (alfred['RESULTADO 51'] == 0)]
	alfred.columns = ['SKU', 'Producto', 'Lote', 'Caducidad', 'Cantidad', 'Tamano lote', 'Fecha', 'Contenedor',
	 'Observacion', 'Resultado 41', 'Orden 51', 'Resultado 51']
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
	st.header("Avance diario")

	#Agrupamos primero nuestro dataframe por factura para poder descontar las notas de crédito
	sub_fac1 =df_ventas.groupby(['No_fac','Canal_cliente']).agg({'Subt_fac':'sum',
					     						'Cant_surt':'sum',
												'N_cred':'mean',
												'Costo':'sum',
												'Utilidad_mov':'sum',
												'Margen':'mean',
												'Anio':'max',
												'Mes':'max',
												'Dia':'max'}).reset_index()
	
	#Para poder restar las notas de crédito eliminamos los NAS
	sub_fac1['N_cred'] = sub_fac1['N_cred'].fillna(0)
	sub_fac1['Subt_fac'] = sub_fac1['Subt_fac'] + sub_fac1['N_cred']

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
	#Función para obtener el ultimo dia del mes
	def last_day_of_month(date):
		if date.month == 12:
			return date.replace(day=31)
		return date.replace(month=date.month+1, day=1) - timedelta(days=1)

	# se creó un diccionario el cual contiene los meses del año 
	mes_diccioanrio = { 1:'ene', 2:'feb', 3:'mar', 4:'abr', 5:'may',6:'jun',
		    			7:'jul',8:'ago',9:'sep',10:'oct',11:'nov',12:'dic'}
	now = datetime.now() # se guarda la fecha actual
	yesterday = now.replace(month = now.month, day = now.day - 1)
	act = now.year # de la fecha actual se guarda solo el año en curso
	m = now.month # de la fecha actual se guarda el mes en curso(esto solo devolverá un numero) 
	mes = mes_diccioanrio[m]  # el numero que se guardó en la variable 'm' corresponde al mes en curso, de esta forma se manda a llamar el nombre del mes, que ya esta identificado en el diccionario 
	a_act = fac_act[fac_act['Anio']== act].drop(columns=['Anio']) # se aplica el filto por año, el cual se almacenará e la variable a_act
	last_day = last_day_of_month(now)
	#st.write(a_act.iloc[:,4].sum(axis=0))
	d_act = a_act[a_act['Mes'] == mes].drop(columns=['Mes'])
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
	back_act = pedidos[pedidos['Back_month'] == m]
	back_act = back_act.groupby(['Canal']).agg({'importe':'sum'})
	back_act.columns = ['Back Mes']

	#st.write(back_ant.sum())
	#st.write(pedidos.head(5))
	avance = avance.merge(remisiones, on='Canal', how='left')
	avance = avance.merge(back_ant, on='Canal', how='left')
	avance = avance.merge(back_pos, on='Canal', how='left')
	avance = avance.merge(back_act, on='Canal', how='left')
	#p_pedidos = pedidos.groupby(['Producto']).agg({''})
	#st.write(df_existencias.head(5))
	p_pedidos = pedidos.groupby(['Producto', 'Back_month']).agg({'Cantidad_pedida':'sum',
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
	uno, dos = st.columns([1,1])
	with uno:
		st.metric('Ventas al dia ($)', millify(v_dia), delta=millify(avance_objetivo))
		#st_card('Ventas al dia ($)', v_dia, show_progress=True)
	with dos:
		prefixes = ['%']
		st.metric('Avance en tiempo (%)', millify(por_tiempo), delta = millify(dif_avance_por))
	#st.write('$ ', d_act.iloc[:,2].sum(axis=0))

	st.write(avance)
	
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
		st.metric('Pedidos del mes ($)', millify(produccion['Importe B_ACT'].sum()))
		st.metric('Pedidos Acumulados sin entregar ($)', millify(produccion['Importe BA'].sum()))
		st.metric('Pedidos a entregar después ($)', millify(produccion['Importe BP'].sum()))
	with dos:
		st.metric('Pedidos del mes (PZA)', millify(produccion['Back Act (PZA)'].sum()))
		st.metric('Pedidos Acumulados sin entregar (PZA)', millify(produccion['Back Ant (PZA)'].sum()))
		st.metric('Pedidos a entregar después (PZA)', millify(produccion['Back Pos (PZA)'].sum()))
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
	fcst_faltantes = t_forecast[['Producto', 'Forecast', 'Faltantes', 'Existencia']]
	fcst_faltantes = fcst_faltantes[fcst_faltantes['Faltantes']>0]
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

	df_filtered = df_filtered[['Nom_cliente','Producto','Cant_surt', 'Subt_fac', 'Utilidad_mov','Margen']]

	#Agregamos la columna porcentaje que será la venta ($) entre el total de ventas
	
	tot_vta = df_filtered.iloc[:,3].sum(axis=0)

	df_filtered['Porcentaje'] = (df_filtered['Subt_fac']/tot_vta)*100 
	###BENEFICIO POR PRODUCTO###
	st.subheader('Tabla beneficio por producto')
	df_group = df_filtered.groupby(['Producto']).agg({'Cant_surt':'sum',
													  'Subt_fac':'sum',
						   							  'Utilidad_mov':'sum', 
													  'Margen':'mean',
													  'Porcentaje':'sum'})
	df_group = df_group.sort_values(by=['Utilidad_mov'],ascending=False)
	df_group = df_group[['Cant_surt', 'Subt_fac', 'Utilidad_mov', 'Porcentaje']]
	df_group.columns = ['Venta (PZA)', 'Venta ($)', 'Utilidad', 'Porcentaje']
	st.write(df_group)

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
	df_group = df_filtered.groupby(['Nom_cliente']).agg({'Cant_surt':'sum',
													  'Subt_fac':'sum',
						   							  'Utilidad_mov':'sum', 
													  'Margen':'mean',
													  'Porcentaje':'sum'})
	df_group = df_group.sort_values(by=['Subt_fac'],ascending=False)
	df_group = df_group[['Cant_surt', 'Subt_fac', 'Utilidad_mov', 'Porcentaje']]
	df_group.columns = ['Venta (PZA)', 'Venta ($)', 'Utilidad', 'Porcentaje']
	st.write(df_group)

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

	sub_fac =df_filtered_2.groupby(['No_fac']).agg({'Subt_fac':'sum',
					     						'Cant_surt':'sum',
												'N_cred':'mean',
												'Costo':'sum',
												'Utilidad_mov':'sum',
												'Margen':'mean',
												'Anio':'max',
												'Mes':'max'}).reset_index()
	
	#Para poder restar las notas de crédito eliminamos los NAS
	sub_fac['N_cred'] = sub_fac['N_cred'].fillna(0)
	sub_fac['Subt_fac'] = sub_fac['Subt_fac'] + sub_fac['N_cred']

	sub_fac = sub_fac.groupby(['Anio','Mes']).agg({'Subt_fac':'sum',
													'Cant_surt':'sum',
													'Costo':'sum',
													'Utilidad_mov':'sum',
													'Margen':'mean'}).reset_index()
	
	anio = st.selectbox('Año',sub_fac['Anio'].unique())

	#sub_fac = sub_fac[(sub_fac['Nom_cliente'].isin(cte_list))]
	sub_fac.columns = ['Anio','Mes','Venta ($)','Venta (Pza)','Costo total','Utilidad','Margen (%)']
	st.write(sub_fac[sub_fac['Anio']== anio].drop(columns=['Anio']))

	
if __name__ == '__main__':
	main()
