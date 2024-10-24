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
		st.title("Plantilla de pagos")
	with col3:
		st.write("")


	@st.cache_resource
	def provcuentas():
		prov = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/proveedores_cuentas.csv', dtype={'Numero':str}, encoding='latin-1')
		return prov
	prov = provcuentas()

	#colu={
	#	'columna1':['none']* len(prov),
	#	'clumna2':['none']* len(prov),
	#	'columna3':['none']* len(prov)
	#}
	#prov=prov.assign(**colu)

	for i in range(len(prov['Alias'])):
		prov.loc[i,'Numero'] = str(prov.loc[i,'Numero'])

	cantidad_pagos = st.number_input('Cantidad de pagos a capturar', min_value=1, key=f'cantidad_pagos_{i}', step=1)
	cantidades_pagar = {}
	pagos_selec = {}
	provedores_selec = {}
	referencia = {}
	plantilla_pagos = {}
	tabla_fin = {}
	tabla_usu = {}
	df_temp = {}
	#tabla_dos = {}
    #base_me = {}
    #base_st = {}
    #bases_formulas = {}
    #explosion_part = {}
    
	for i in range(cantidad_pagos):
		provedores_select = f'provedores_select_{i}'
		cantidades_pagar2 = f'cantidades_pagar2_{i}'
		plantilla_pagos = f'plantilla_pagos2_{i}'
		referenciap = f'referenciap_{i}'

		provedores_selec[provedores_select] = st.selectbox('Elije al proveedor', prov['Alias'].sort_values().unique(), key=f'provedores_selec_{i}')
		cantidades_pagar[cantidades_pagar2] = st.number_input('Cantidad a pagar en MXN', key=f'cantidades_pagar2_{i}', step=1)
		referencia[referenciap] = st.text_input('Escribe el concepto de pago', key=f'referenciap_{i}')
		

	for i in range(cantidad_pagos):
		provedores_select = f'provedores_select_{i}'
		cantidades_pagar2 = f'cantidades_pagar2_{i}'
		plantilla_pagos = f'plantilla_pagos2_{i}'
		referenciap = f'referenciap_{i}'
		tabla_fin[plantilla_pagos] = prov[prov['Alias'] == provedores_selec.get(provedores_select)]
		tabla_usu[cantidades_pagar2] = [provedores_selec.get(provedores_select), cantidades_pagar.get(cantidades_pagar2), referencia.get(referenciap) ]
	
	
	ref_num = st.text_input('Escribe la referencia numerica')
	ref_str = st.text_input('Escribe la referencia de pagos')
	df_temp= pd.concat(tabla_fin.values(), ignore_index=True)
	df_temp = df_temp.rename(columns={'Alias':'Proveedor'})
	df_usu = pd.DataFrame(tabla_usu.values(), columns = ['Proveedor', 'Cantidad', 'Descripcion'])
	#st.write(df_usu)
	df_base = df_temp.merge(df_usu, on='Proveedor', how='left')
	col_names_banregio = ['Secuencia', 'Tipo', 'Cuenta_Destino', 'Importe', 'IVA', 'Descripcion', 'Ref_Numerica', 'Referencia']
	n = len(df_base['Proveedor'])
	sec = list(range(n))
	tipo = ["s" for i in range(n)]
	iva = [None]*n
	ref = [ref_num for i in range(n)]
	referencia = [ref_str for i in range(n)]
	#df_validacion = df_validacion.groupby(['Proveedor'])
	if st.checkbox('Plantilla Banregio'):
		df_banregio = pd.DataFrame(list(zip(sec, tipo, df_base['Numero'], df_base['Cantidad'], iva, df_base['Descripcion'], ref, referencia)), columns=col_names_banregio)
		st.write(df_banregio)
		df_validacion = pd.DataFrame(list(zip(df_base['Proveedor'], df_base['Cantidad'])), columns=['Proveedor', 'Cantidad'])
		df_validacion = df_validacion.groupby(['Proveedor']).agg({'Cantidad':'sum'}).reset_index()
		if st.checkbox('Validacion'):
			st.write(df_validacion)
			monto_pago = df_validacion['Cantidad'].sum()
			frase_val = 'Monto total de solicitud de pagos $ ' + str(round(monto_pago))
			st.info(frase_val, icon='💵')
			#st.write(frase_val)
			#st.write(cant_usu)
	#st.write(des_usu)
	
		#col_names = ['Secuencia', 'Tipo', 'Cuenta_Destino', 'Importe', 'IVA','Descripcion', 'Ref_Numerica','Referencia']
		# Secuencia= i
		# Tipo= 's'
		# Cuenta_destino= Numero
		# Importe= Cantidad a pagar en MXN
		#Iva=0
		#Descripcion= Escribe el concepto de pago
		#Ref_Numerica=(crear un recuadro donde ingresen la fecha)
		#Referencia=Alias
  
	#col_names = ['Proveedor', 'Correo', 'Clabe', 'RFC', 'Banco', 'Tipo']
	#df_temp = pd.DataFrame(tabla_fin, columns = col_names)
	#st.write(df_temp)

    #globals()[f'form_filter2_{i}'] = form_filter[form_filter['Producto'] == formulas_selec.get(nombres_formulas)]
    ####################PEDIR#####################################################
    # #st.write(bases_formulas.get('form_filter2_1')[bases_formulas.get('form_filter2_1')['Cve_prod'].str.startswith('M')].reset_index(drop=True))
    #     base_pt[formula_pt] = bases_formulas.get(f'form_filter2_{i}').copy()
    #     base_pt[formula_pt] = bases_formulas.get(f'form_filter2_{i}').dropna()
    #     #formula_pt[formula_pt] = bases_formulas.get(f'form_filter2_{i}').dropna()
    # #st.write(base_pt.get('formula_pt_0'))
    #     base_me[formula_me] = bases_formulas.get(f'form_filter2_{i}')[bases_formulas.get(f'form_filter2_{i}')['Cve_prod'].str.startswith('M')].reset_index(drop=True)
    #     #formula_me = formula_pt[formula_pt['Cve_prod'].str.startswith('M')].reset_index(drop=True)
    #     base_st[formula_st] = bases_formulas.get(f'form_filter2_{i}')[bases_formulas.get(f'form_filter2_{i}')['Cve_prod'].str.startswith('41')].reset_index(drop=True)
    #     #formula_st = formula_pt[formula_pt['Cve_prod'].str.startswith('41')].reset_index(drop=True)
    #     col_names = ['index', 'SKU pt', 'SKU', 'Cantidad rendimiento', 'New_med', 'New_copr', 'Unidad mp', 'MP','Rendimiento', 'Unidad', 'Cantidad', 'Producto']
    #     #merge_st = base_st.get(f'formula_st_{i}').merge(formulas, on='SKU', how='left')
    #     base_st.get(f'formula_st_{i}').columns = col_names
    #     base_st[formula_st] = base_st.get(f'formula_st_{i}').merge(formulas, on='SKU', how='left') 
    #     #formula_stt_i = formula_stt_i.merge(formulas, on='SKU', how='left')
    # #st.write(base_st.get('formula_st_0').columns)
    #     base_st[formula_st] = base_st.get(f'formula_st_{i}')[['SKU pt', 'SKU', 'MP_x', 'Rendimiento_x', 'Cve_prod', 'Cantidad rendimiento_y', 'Unidad mp_y', 'MP_y']]
    #     col_names2 = ['PT', 'SKU', 'ST', 'Rendimiento', 'Cve_prod', 'Cantidad rendimiento', 'Unidad', 'Producto']
    #     base_st.get(f'formula_st_{i}').columns = col_names2 
    #     base_st.get(f'formula_st_{i}')['Cantidad unitaria'] = base_st.get(f'formula_st_{i}')['Cantidad rendimiento'] / base_st.get(f'formula_st_{i}')['Rendimiento']
    # #st.write(base_st)
    #     col_names3 = ['SKU', 'ST', 'Producto', 'Rendimiento', 'Cve_prod', 'Cantidad rendimiento', 'Unidad', 'MP', 'Cantidad unitaria']
    #     base_st.get(f'formula_st_{i}').columns = col_names3 
    #     base_me[formula_me] = base_me.get(f'formula_me_{i}')[['SKU', 'Producto', 'Rendimiento', 'Cve_prod', 'Cantidad rendimiento', 'Unidad', 'MP', 'Cantidad']]
    #     col_names4 = ['SKU', 'Producto', 'Rendimiento', 'Cve_prod', 'Cantidad rendimiento', 'Unidad', 'MP', 'Cantidad unitaria']
    #     base_me.get(f'formula_me_{i}').columns = col_names4 
    # #st.write(base_me)
    #     #formulas_filter = pd.concat([formula_st, formula_me])
    #     formulas_filtro[formulas_filter] = pd.concat([base_st.get(f'formula_st_{i}'), base_me.get(f'formula_me_{i}')])
    
    #     formulas_filtro[formulas_filter] = formulas_filtro.get(f'formulas_filter_{i}').fillna(0)
    #     formulas_filtro[formulas_filter] = formulas_filtro.get(f'formulas_filter_{i}')[['SKU', 'Producto', 'Rendimiento', 'Cve_prod', 'Cantidad rendimiento', 'MP', 'Cantidad unitaria']]
    #     explosion_part[explosion_materiales] = formulas_filtro.get(f'formulas_filter_{i}').copy()
    #     explosion_part.get(f'explosion_materiales_{i}')['Cantidad total necesaria'] = explosion_part.get(f'explosion_materiales_{i}')['Cantidad unitaria'] * cantidades_selec.get(f'cantidades_select_{i}')
    #     explosion_part[explosion_materiales] = pd.DataFrame(explosion_part.get(f'explosion_materiales_{i}'))        
    # concat_exp = pd.concat(explosion_part.values(), axis=0, ignore_index=True)
    # concat_exp.rename(columns = {'SKU':'SKU PT', 'Cve_prod':'SKU'}, inplace = True)
    # concat_exp = concat_exp.merge(existeN_comp, on='SKU', how='left')
    # st.write(concat_exp)
    # st.download_button(label="Descargar", data=concat_exp.to_csv(), mime="text/csv")



if __name__ == '__main__':
	main()