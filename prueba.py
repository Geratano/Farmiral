import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import altair as alt
from datetime import datetime

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

	st.header("Avance diario")

	#st.write(fac_act.iloc[:,2].sum(axis=0))
	#st.write(a_act.head(5))
	# Creacion del grupo canal_prod
	#fac_act = df_ventas.groupby(['Anio','Mes','Canal_prod']).agg({'Cant_surt':'sum',
	#											'Subt_fac':'sum',
	#											'Utilidad_mov':'sum',
	#											'Margen':'mean'}).reset_index()
	fac_act = df_ventas.groupby(['Anio','Mes','Canal_cliente']).agg({'Cant_surt':'sum',
												'Subt_fac':'sum',
												'Utilidad_mov':'sum',
												'Margen':'mean'}).reset_index()
	fac_act = fac_act.sort_values(by=['Utilidad_mov'],ascending=False)
	
	# se creó un diccionario el cual contiene los meses del año 
	mes_diccioanrio = { 1:'ene', 2:'feb', 3:'mar', 4:'abr', 5:'may',6:'jun',
		    			7:'jul',8:'ago',9:'sep',10:'oct',11:'nov',12:'dic'}
	now = datetime.now() # se guarda la fecha actual
	act = now.year # de la fecha actual se guarda solo el año en curso
	m = now.month # de la fecha actual se guarda el mes en curso(esto solo devolverá un numero) 
	mes = mes_diccioanrio[m]  # el numero que se guardó en la variable 'm' corresponde al mes en curso, de esta forma se manda a llamar el nombre del mes, que ya esta identificado en el diccionario 
	a_act = fac_act[fac_act['Anio']== act].drop(columns=['Anio']) # se aplica el filto por año, el cual se almacenará e la variable a_act
	#st.write(a_act.iloc[:,4].sum(axis=0))
	d_act = a_act[a_act['Mes'] == mes].drop(columns=['Mes'])
	st.write('$ ', d_act.iloc[:,2].sum(axis=0))
	st.write(a_act[a_act['Mes']== mes].drop(columns=['Mes'])) # se muestra la tabla filtrando por mes actual

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

	df_filtered = df_filtered[['Nom_cliente','Producto','Cant_surt','Utilidad_mov','Margen']]
	
	st.subheader('Tabla beneficio por producto')
	df_group = df_filtered.groupby(['Producto']).agg({'Cant_surt':'sum', 
						   							  'Utilidad_mov':'sum', 
													  'Margen':'mean'})
	df_group = df_group.sort_values(by=['Utilidad_mov'],ascending=False)
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
		top_5 = df_group.sort_values(by=['Utilidad_mov'],ascending=False).head(5).reset_index()
		#top_6 = top_6.rename_axis(index=['Producto','Cant_surt','Utilidad_mov','Margen'])
		#top_5 = df_filtered[['Producto','Utilidad_mov']]
		#Construimos el gráfico con altair 
		pie_top = alt.Chart(top_5, title='Top 5 Utilidad').mark_arc().encode(
	    theta=alt.Theta(field='Utilidad_mov', type="quantitative"),
	   	color=alt.Color(field='Producto', type="nominal"),
	   	tooltip = ['Producto','Utilidad_mov']
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
		bottom_5 = df_group.sort_values(by=['Utilidad_mov'],ascending=True).head(5).reset_index()
		#top_6 = top_6.rename_axis(index=['Producto','Cant_surt','Utilidad_mov','Margen'])
		#top_5 = df_filtered[['Producto','Utilidad_mov']]
		#Construimos el gráfico con altair 
		pie_bottom = alt.Chart(bottom_5, title='Bottom 5 Utilidad').mark_arc().encode(
	    theta=alt.Theta(field='Utilidad_mov', type="quantitative"),
	   	color=alt.Color(field='Producto', type="nominal"),
	   	tooltip = ['Producto','Utilidad_mov']
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
