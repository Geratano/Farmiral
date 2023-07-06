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
	df.columns = df.columns.str.strip()
	remisiones.columns = remisiones.columns.str.strip()
	pedidos.columns = pedidos.columns.str.strip()
	canal.columns = canal.columns.str.strip()
	#Filtramos la base para obtener solo las columnas
	#importantes
	df_ventas = df[['No_fac','Falta_fac','Subt_fac','Cve_factu','Cse_prod','Cant_surt','Lugar','Costo','Utilidad_mov','Margen',
	'Categoria','Canal_prod','Canal_cliente','KAM','Subdirec','N_cred','Anio','Mes','Dia','Nom_cliente','Producto']]
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
	df_pedidos = pedidos[['No_ped', 'F_alta_ped', 'Cve_cte', 'Nom_cte', 'Status', 'Cve_prod', 'Fecha_ent_a', 'Cant_prod', 
						  'Cant_surtp', 'Liquidado', 'Saldo', 'Valor_prod', 'Uni_med', 'Desc_prod']]
	df_pedidos.columns = ['No_ped', 'Fecha_alta', 'Cve_cte', 'Cliente', 'Estatus', 'SKU', 'Fecha_entrega', 'Cantidad_pedida',
						  'Cantidad_surtida', 'Liquidado', 'Saldo', 'Precio', 'Unidad', 'Producto']
	pedidos = df_pedidos.merge(canal, on='Cve_cte', how='left')
	for i in range(len(pedidos.loc[:,'Saldo'])):
		if pedidos.loc[i,'Saldo'] < 0:
			pedidos.loc[i,'Saldo'] = 0
	pedidos['importe'] = pedidos['Saldo'] * pedidos['Precio']

	#imprimimos como prueba los primeros cinco datos de la tabla
	if st.checkbox("Raw data"):
		st.write(df_ventas.head(5))

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
	###Computaremos el back order anterior (ant) si la fecha de entrega es antes del mes actual posterior (pos) si es despues del mes actual
	###y el mes si es el corriente
	pedidos['Mes_alta'] = pedidos['Fecha_alta']
	pedidos['Mes_ent'] = pedidos['Fecha_entrega']
	pedidos['Back_month'] = pedidos['Mes_alta']
	for i in range(len(pedidos.loc[:,'Fecha_alta'])):
		try:
			pedidos.loc[i,'Fecha_alta'] = pd.to_datetime(pedidos.loc[i,'Fecha_alta'], format='%d/%m/%Y')
			pedidos.loc[i,'Mes_alta'] = pedidos.loc[i,'Fecha_alta'].month
			pedidos.loc[i,'Fecha_entrega'] = pd.to_datetime(pedidos.loc[i,'Fecha_entrega'], format='%d/%m/%Y')
			pedidos.loc[i,'Mes_ent'] = pedidos.loc[i, 'Fecha_entrega'].month
		except ValueError:
			pedidos.loc[i, 'Mes_ent'] = pedidos.loc[i, 'Mes_alta']
		if pedidos.loc[i,'Mes_alta'] == m:
			pedidos.loc[i,'Back_month'] = m
		elif  pedidos.loc[i, 'Mes_ent'] > m:
			pedidos.loc[i, 'Back_month'] = 'POS'
		else: 
			pedidos.loc[i, 'Back_month'] = 'ANT'
	#st.write(pedidos.columns)
	#st.write(remisiones.head(5))
	#st.write(pedidos[pedidos['Back_month'] == 'ANT']['Back_month'])
	
	back_ant = pedidos[pedidos['Back_month'] == 'ANT']
	back_ant = back_ant.groupby(['Canal']).agg({'importe':'sum'})
	back_ant.columns = ['Back anterior']
	back_pos = pedidos[pedidos['Back_month'] == 'POS']
	back_pos = back_pos.groupby(['Canal']).agg({'importe':'sum'})
	back_pos.columns = ['Back posterior']
	back_act = pedidos[pedidos['Back_month'] == m]
	back_act = back_act.groupby(['Canal']).agg({'importe':'sum'})
	back_act.columns = ['Back Mes']
	#st.write(pedidos.head(5))
	#st.write(pedidos.head(5))
	avance = avance.merge(remisiones, on='Canal', how='left')
	avance = avance.merge(back_ant, on='Canal', how='left')
	avance = avance.merge(back_pos, on='Canal', how='left')
	avance = avance.merge(back_act, on='Canal', how='left')
	uno, dos = st.columns([1,1])
	with uno:
		st.metric('Ventas al dia ($)', millify(v_dia), delta=millify(avance_objetivo))
		#st_card('Ventas al dia ($)', v_dia, show_progress=True)
	with dos:
		prefixes = ['%']
		st.metric('Avance en tiempo (%)', millify(por_tiempo), delta = millify(dif_avance_por))
	#st.write('$ ', d_act.iloc[:,2].sum(axis=0))

	st.write(avance)
	#st.write(avance_mes) # se muestra la tabla filtrando por mes actual

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
 
	df_filtered = df_ventas[
			 (df_ventas['Cve_factu'].isin(emp_list)) & 
			 (df_ventas['Lugar'].isin(alm_list)) & 
			 (df_ventas['Anio'].isin(ano_list)) & 
			 (df_ventas['Mes'].isin(mes_list)) &
			 (df_ventas['Nom_cliente'].isin(cte_list))]

	df_filtered = df_filtered[['Nom_cliente','Producto','Cant_surt', 'Subt_fac', 'Utilidad_mov','Margen']]
	
	st.subheader('Tabla beneficio por producto')
	df_group = df_filtered.groupby(['Producto']).agg({'Cant_surt':'sum',
													  'Subt_fac':'sum',
						   							  'Utilidad_mov':'sum', 
													  'Margen':'mean'})
	df_group = df_group.sort_values(by=['Utilidad_mov'],ascending=False)
	df_group.columns = ['Venta (PZA)', 'Venta ($)', 'Utilidad', 'Margen']
	st.write(df_group)

	#top, bottom=st.columns([10,10])
	top, bottom=st.columns(2)
	with top:
		#GRAFICA TOP 5
		#Con esta instrucción permitimos a altair mostrar la gráfica aunque tenga mas de 5000 renglones
		alt.data_transformers.enable('default', max_rows=None)
		#Agrupamos los datos, ordenamos de mayor a menor por la utilidad y extraemos 5 datos
		top_5 = df_filtered.groupby(['Producto'], as_index = False).agg({'Cant_surt':'sum', 
								   										'Utilidad_mov':'sum', 
																		'Margen':'mean'})
		top_5 = df_group.sort_values(by=['Utilidad'],ascending=False).head(5).reset_index()
		#top_6 = top_6.rename_axis(index=['Producto','Cant_surt','Utilidad_mov','Margen'])
		#top_5 = df_filtered[['Producto','Utilidad_mov']]
		#Construimos el gráfico con altair 
		pie_top = alt.Chart(top_5, title='Top 5 Utilidad').mark_arc().encode(
	    theta=alt.Theta(field='Utilidad', type="quantitative"),
	   	color=alt.Color(field='Producto', type="nominal"),
	   	tooltip = ['Producto','Utilidad']
	   	)
	    #Mostramos el objeto en streamlit
		st.altair_chart(pie_top, use_container_width=True)
	with bottom:
		#GRAFICA BOTTOM 5
		#Con esta instrucción permitimos a altair mostrar la gráfica aunque tenga mas de 5000 renglones
		alt.data_transformers.enable('default', max_rows=None)
		#Agrupamos los datos, ordenamos de mayor a menor por la utilidad y extraemos 5 datos
		bottom_5 = df_filtered.groupby(['Producto'], as_index = False).agg({'Cant_surt':'sum', 
								      										'Utilidad_mov':'sum',
																			'Margen':'mean'})
		bottom_5 = df_group.sort_values(by=['Utilidad'],ascending=True).head(5).reset_index()
		#top_6 = top_6.rename_axis(index=['Producto','Cant_surt','Utilidad_mov','Margen'])
		#top_5 = df_filtered[['Producto','Utilidad_mov']]
		#Construimos el gráfico con altair 
		pie_bottom = alt.Chart(bottom_5, title='Bottom 5 Utilidad').mark_arc().encode(
	    theta=alt.Theta(field='Utilidad', type="quantitative"),
	   	color=alt.Color(field='Producto', type="nominal"),
	   	tooltip = ['Producto','Utilidad']
	   	)
	    #Mostramos el objeto en streamlit
		st.altair_chart(pie_bottom, use_container_width=True)
		#GRAFICA BOTTOM 5
		# bottom_5 = df_filtered.groupby(['Producto'], as_index = False).agg({'Cant_surt':'sum', 'Utilidad_mov':'sum', 'Margen':'mean'})
		# bottom_5 = df_group.sort_values(by=['Utilidad_mov'],ascending=True).head(5).reset_index()	
		# pie_bottom = alt.Chart(bottom_5, title='Bottom 5 Utilidad').mark_arc().encode(
      	# theta=alt.Theta(field='Utilidad_mov', type="quantitative"),
      	# color=alt.Color(field='Producto', type="nominal"),
      	# tooltip = ['Producto','Utilidad_mov'])
      	# st.altair_chart(pie_bottom, use_container_width=True)

		
		#st.altair_chart(alt.Chart(top_5, title='Top 5 Utilidad').transform_aggregate(
		# 	Utilidad_mov = 'sum(Utilidad_mov)',
		# 	groupby = ['Producto'],
		# 	).mark_arc().encode(
	 	# 	theta=alt.Theta(field="Utilidad_mov", type="quantitative"),
     	# 	color=alt.Color(field="Producto",type="nominal"),
	 	# tooltip = ['Producto', 'Utilidad_mov']))
		#tooltip=alt.Tooltip("Producto","Utilidad_mov"))
		
		#top_5.plot(kind='pie',y='Utilidad_mov',title='Top 5 Utilidad')
	#Siguiente sección con datos de ventas historicos
	st.subheader('Tabla históricos por año')
	#Agrupamos primero nuestro dataframe por factura para poder descontar las notas de crédito
	sub_fac =df_ventas.groupby(['No_fac']).agg({'Subt_fac':'sum',
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
	sub_fac.columns = ['Anio','Mes','Venta ($)','Venta (Pza)','Costo total','Utilidad','Margen (%)']
	st.write(sub_fac[sub_fac['Anio']== anio].drop(columns=['Anio']))

	
if __name__ == '__main__':
	main()
