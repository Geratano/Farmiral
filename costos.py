import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import altair as alt
from datetime import datetime
import re
st.set_page_config(layout="wide")

#funcion para agregar nueva fila
def agregar_fila(df, row):
    row = pd.DataFrame([row])
    return pd.concat([df, row], ignore_index=True)

# Funcion para crear un dataframe inical 
def inicializador():
    return pd.DataFrame(columns=['Materia prima', 'Cantidad','Unidad','Costo'])  
def eliminar_fila(df, index):
    return df.drop(index).reset_index(drop=True)
def main():
    img = Image.open('logo_farmiral.jpg')
    col1, col2, col3 = st.columns([5,10,1])
    with col1:
        st.write("")
	
    with col2:
        st.image(img,width=250)
    with col3:
        st.write("")

        #Cargamos las bases que vamos a utilizar desde aqui  
    @st.cache_resource
    def load_model():
        checkpoints = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/formulas.csv',encoding='latin-1')
        return checkpoints
    df_formulas = load_model()  
    @st.cache_resource
    def load_model2():
        checkpoints = pd.read_csv('https://raw.githubusercontent.com/Geratano/Farmiral/main/productos.csv',encoding='latin-1')
        return checkpoints
    df_productos = load_model2() 

    ruta= 'https://docs.google.com/spreadsheets/d/1-CchhP1_OYewPJz2wGf-4bArmED1H-M5/pub?gid=806142732&single=true&output=csv'
    df_drive = pd.read_csv(ruta,encoding='utf-8')
        # funcion para convertir los datos str a float
    def limpiar(s):
        if isinstance(s,str): # si los datos son de tipo sting
            s = s.strip() # eliminar espacios al inicio y al final
            if s == "-": # si el dato solo es un signo menos
                return 0 # reemplazar por cero
            s = re.sub(r'\s+', '', s) # eliminar todos los espacios
            s= s.replace(',','') # eliminar comas
            s= s.replace('$','') # eliminar sinos de pesos
        return s 
    df_drive.columns= ['CODIGO','DESCRIPCION','PROVEEDOR','TIPO','COSTO','MONEDA','MOQ','UMB','TIMPOS DE ENTREGA','COMENTARIOS','SIN NOMBRE'] # renombrar columnas para que no haya problemas si se cambia el nombre an la original
    df_drive['COSTO']=df_drive['COSTO'].apply(limpiar) # se aplica la funcion limpiar
    df_drive['COSTO']=pd.to_numeric(df_drive['COSTO'],errors='coerce') # se convierte a numeros
    df_drive['CODIGO']= df_drive['CODIGO'].str.strip()

    #Quitamos espacios a los nombres de las columnas
    df_formulas.columns = df_formulas.columns.str.strip()
    df_productos.columns = df_productos.columns.str.strip()
   

    #Filtramos solo las columnas que necesitamos de cada base
    df_formulas = df_formulas[['Cve_copr', 'Cve_prod', 'Can_copr', 'Tip_copr', 'New_med', 'New_copr', 'Partida', 'Undfor', 
                                'Desc_prod', 'Cve_mon', 'Cve_tial', 'Tipcam', 'Tip_cam', 'Ren_copr', 'Cto_ent', 'Uncfor']]
    df_productos = df_productos[['Cve_prod', 'Desc_prod', 'Uni_med', 'Cto_ent', 'Cve_tial','Fec_ent','Cve_monc','Prov_std']]
    
    #Quitamos los posibles espacios sobrantes de cada columna
    df_formulas['Cve_prod'] = df_formulas['Cve_prod'].str.strip()    
    df_formulas['Cve_copr'] = df_formulas['Cve_copr'].str.strip()
    df_formulas['New_med'] = df_formulas['New_med'].str.strip()
    df_formulas['New_copr'] = df_formulas['New_copr'].str.strip()
    df_formulas['Undfor'] = df_formulas['Undfor'].str.strip()
    df_formulas['Desc_prod'] = df_formulas['Desc_prod'].str.strip()
    df_formulas['Uncfor'] = df_formulas['Uncfor'].str.strip()
    df_productos['Cve_prod'] = df_productos['Cve_prod'].str.strip()
    df_productos['Desc_prod'] = df_productos['Desc_prod'].str.strip()
    df_productos['Uni_med'] = df_productos['Uni_med'].str.strip()
    df_productos['Fec_ent'] = df_productos['Fec_ent'].str.strip()
    
  
    # conversión de kilos a gramos 
    df_formulas['Can_copr']= np.where(df_formulas['Undfor']=='KG',df_formulas['Can_copr'] * 1000,df_formulas['Can_copr'])
    df_formulas['Cto_ent']= np.where(df_formulas['Undfor']=='KG',df_formulas['Cto_ent'] / 1000,df_formulas['Cto_ent'])
    df_formulas['Undfor']= np.where(df_formulas['Undfor']=='KG','GR',df_formulas['Undfor'])

    # Conversion de kilos a gramos en las columnas unid_med y cto_ent
    df_productos['Cto_ent'] = np.where(df_productos['Uni_med']== 'KG',(df_productos['Cto_ent']/1000),df_productos['Cto_ent'])
    df_productos['Uni_med'] = np.where(df_productos['Uni_med']== 'KG','GR',df_productos['Uni_med'])

    # reemplazo los valores en los códigos cuando los encuentre en la base del drive poniendo prioridad lo que se encuentre en el drive
    #se guarda en la columna elegida Prov_std = sleccionamos la columan a buscar la coincidencia Cve_prod, con el .map le decimos que el
    #  indice va ser CODIGO y seleccionamos la columna la cual vamos a traer el valor PROVEEDOR, cuando encuentre una coincidencia entre
    #  el indice CODIGO Y Cve_prod, traerá el dato PROVEEDOR y lo reemplazará en Prov_std
    df_productos['Prov_std'] = df_productos['Cve_prod'].map(df_drive.set_index('CODIGO')['PROVEEDOR']).fillna(df_productos['Prov_std'])
    df_productos['Cve_monc'] = df_productos['Cve_prod'].map(df_drive.set_index('CODIGO')['MONEDA']).fillna(df_productos['Cve_monc'])
    df_productos['Cto_ent'] = df_productos['Cve_prod'].map(df_drive.set_index('CODIGO')['COSTO']).fillna(df_productos['Cto_ent'])

   
    st.title('Costos Farmiral')
    #Seleccionar si se va a consultar costos desglosados o costear
    if st.checkbox("Costos desglosados"):
    #Hacemos merge con los nombres de las formulas para facilitar la busqueda del producto a costear
        df_formulas_n = df_formulas.merge(df_productos.rename({'Desc_prod':'Formula'},axis=1), left_on='Cve_copr', 
            right_on='Cve_prod', how='left')
        df_formulas_n.columns = ['SKU', 'Componente', 'Cantidad', 'Tipo', 'Atributo', 'Version pt', 'Partida', 'Unidad_componente', 'Nombre', 'Cve_mon', 'Tipo_x', 'Tipcam','Tip_cam', 'Rendimiento','Costo', 'Unidad', 'Cve_prod_y', 'Formula', 'Unidad pt', 'Cto_ent_y', 'Tipo_prod','Uni_med','Fec_ent','Prov_std']
    
        #Eliminamos las versiones V1, V2, V3 y V4
        df_formulas_n = df_formulas_n.loc[(df_formulas_n['Version pt']!='V1') & (df_formulas_n['Version pt']!='V2') & (df_formulas_n['Version pt']!='V3') & (df_formulas_n['Version pt']!='V4')]
        
        #Creamos el filtro para seleccionar la formula a análizar
        df_formulas_prueba = df_formulas_n[df_formulas_n.SKU.str.startswith('51')].reset_index()
        tipo_cambio1= st.number_input('Tipo de cambio',value=1.00, step=1e-4, format="%.4f")
        formula = st.selectbox('Formula', df_formulas_prueba['Formula'].sort_values().unique())        
        #Esta tabla nos da todo lo que contiene la formula "51"
        pt = df_formulas_n[df_formulas_n.Formula == formula]
        pt = pt[pt.SKU.str.startswith('51')].reset_index()
        #Nos quedamos solo con las columnas necesarias de la base
        pt = pt[['SKU','Componente','Nombre','Cantidad','Costo','Unidad_componente','Rendimiento','Unidad pt','Cve_mon']]
        pt['Costo']=np.where(pt['Cve_mon']==2,pt['Costo']*tipo_cambio1,pt['Costo'])
        #Calculamos cantidades y costos unitarios
        pt['Cantidad'] = pt['Cantidad']/pt['Rendimiento']
        pt['Costo total'] = pt['Cantidad'] * pt['Costo']
        #Filtramos la tabla pt para obtener todos los materiales que se utilizan en el semiterminado
        semt = pt[pt.Componente.str.startswith('41')]['Nombre'].reset_index()
        #Obtenemos del filtro un simple valor para usar en la extracción de componentes
        semt = semt.iloc[0]['Nombre']
        semit = df_formulas_n[df_formulas_n.Formula == semt]
        semit = semit[semit.SKU.str.startswith('41')].reset_index()
        semit = semit[['SKU','Componente','Nombre','Cantidad','Costo','Unidad_componente','Rendimiento','Unidad pt','Cve_mon']]
        semit['Costo']=np.where(semit['Cve_mon']==2,semit['Costo']*tipo_cambio1,semit['Costo'])
        semit['Cantidad'] = semit['Cantidad']/semit['Rendimiento']
        semit['Costo total'] = semit['Cantidad'] * semit['Costo']

        st.subheader('Costos')
        col1, col2 = st.columns([15,15])
        with col1:
            st.write('Rendimiento: ' ,pt.iloc[0]['Rendimiento'])
            st.write('Unidad Base: ' ,pt.iloc[0]['Unidad pt'])    
        with col2:
            unidad_st = pt[pt.Componente.str.startswith('41')]['Unidad_componente'].reset_index().iloc[0]['Unidad_componente']
            if unidad_st == "GR":
                costo_n1 = semit.groupby(['SKU']).agg({'Costo total':'sum'}).iloc[0]['Costo total']/1000
            else:
                costo_n1 = semit.groupby(['SKU']).agg({'Costo total':'sum'}).iloc[0]['Costo total']
            costo_st = pt[pt.Componente.str.startswith('41')]['Costo'].reset_index().iloc[0]['Costo']
            pt.Costo = pt.Costo.replace({costo_st:costo_n1})
            pt['Costo total'] = pt['Cantidad'] * pt['Costo']
            cantidad_n1 = pt[pt.Componente.str.startswith('41')]['Cantidad'].reset_index().iloc[0]['Cantidad']
            #st.write(costo_n1)
            costo_total_n1 = costo_n1 * cantidad_n1
            costo_total_pt = pt.groupby(['SKU']).agg({'Costo total':'sum'}).iloc[0]['Costo total']
            
            
            #pt[pt.Componente.str.startswith('41')]['Costo'].reset_index().iloc[0]['Costo'] = costo_n1
            #st.write(pt[pt.Componente.str.startswith('41')])
            st.write('Costo nivel 1: $' ,round(costo_total_n1 ,2))
            st.write('Costo ME: $' , round(costo_total_pt - costo_total_n1,2))
            st.write('Costo total: $' , round(costo_total_pt,2))
        left, right = st.columns([20,20])
        with left:
            #Con esta instrucción permitimos a altair mostrar la gráfica aunque tenga mas de 5000 renglones
            alt.data_transformers.enable('default', max_rows=None)
            chart_pt = pt.groupby(['Componente','Nombre']).agg({'Costo total':'sum'}).reset_index()
            pie_pt = alt.Chart(chart_pt, title='Costos pt').mark_arc().encode(
                                theta=alt.Theta(field='Costo total', type="quantitative"),
                                color=alt.Color(field='Nombre', type="nominal"),
                                tooltip = ['Nombre','Costo total']
                                )
            #Mostramos el objeto en streamlit
            st.altair_chart(pie_pt, use_container_width=True)
        with right:
            #Con esta instrucción permitimos a altair mostrar la gráfica aunque tenga mas de 5000 renglones
            alt.data_transformers.enable('default', max_rows=None)
            chart_st = semit.groupby(['Componente','Nombre']).agg({'Costo total':'sum'}).reset_index()
            pie_st = alt.Chart(chart_st, title='Costos st').mark_arc().encode(
                                theta=alt.Theta(field='Costo total', type="quantitative"),
                                color=alt.Color(field='Nombre', type="nominal"),
                                tooltip = ['Nombre','Costo total']
                                )
            #Mostramos el objeto en streamlit
            st.altair_chart(pie_st, use_container_width =True)

        st.subheader('Materiales Producto Terminado por unidad')
        st.write(pt)
        st.subheader('Materiales Semiterminado por unidad')
        st.write(semit)
        pprint = pd.concat([pt, semit])
        st.download_button(label="Descargar", data=pprint.to_csv(), mime="text/csv nuvo")
        #st.write(semt)
    
#------------------------------------------------------------- FORMULADOR ------------------------------------------------------------------------
#     
    if st.checkbox('Formulador'):
        tipo_cambio = st.number_input('Tipo de cambio',value=1.00, step=1e-4, format="%.4f")
        nombre_producto = st.text_input('Nombre del producto a formular')
        unidad_base = st.text_input('Ingresa la unidad base del producto a formular')
        # unidad_caja = st.text_input('Cuantas unidades contiene la presentación')
        # if len(unidad_caja) != 0: 
        #     unidad_caja = float(unidad_caja)
        st.subheader('DOSIS')
        unidad_lote = st.text_input('Cuantas piezas contiene el lote de producción')
        if len(unidad_lote) != 0:
            unidad_lote = float(unidad_lote)
        #margen = st.text_input('Cual será el margen de costo para el precio')
        # margen = st.select_slider('Selecciona margen de costo',
        #             options=[25,50,75,90,100])

        # Si no existe el dataframe se crea uno atemporal
        if 'data' not in st.session_state:
            st.session_state.data = inicializador()
        #st.warning('Formulador en construcción')
        
        materias_lista = st.selectbox('Materia Prima ALPHA', df_productos['Desc_prod'].sort_values().unique())
        Unidad = df_productos[ df_productos['Desc_prod']==materias_lista]
        
        cantidades_lista = st.number_input(f"Ingresa la cantidad para: **{materias_lista}** en {Unidad['Uni_med'].values[0]}",value=1.00, step=1e-10, format="%.10f")
       # cálculo costo por tipo cambio
        Unidad['Cto_ent']= np.where(Unidad['Cve_monc']== 2 ,Unidad['Cto_ent'] * tipo_cambio, Unidad['Cto_ent'])
        if st.button('Agregar fila'):

            # contador que acumula el todal de la columna cantidad
            contador= float(cantidades_lista)
            for elemento in st.session_state.data['Cantidad']:
                contador += float(elemento)
            # creacion de la fila nueva
            new_row = {'SKU': Unidad['Cve_prod'].values[0],'Materia prima': materias_lista, 'Cantidad': cantidades_lista, 'Porcentaje (%)': "", 'Unidad': Unidad['Uni_med'].values[0], 'Costo': Unidad['Cto_ent'].values[0], 'Fecha': Unidad['Fec_ent'].values[0],'Moneda': Unidad['Cve_monc'].values[0],'Proveedor': Unidad['Prov_std'].values[0]   }
           # se agrega la fila nueva al df usando la funcion agregar_fila 
            st.session_state.data = agregar_fila(st.session_state.data, new_row)
            # se calcua el porcentaje y de agrega a la columna porcentaje (%) 
            for cantidad in st.session_state.data['Cantidad']:
                st.session_state.data['Porcentaje (%)'] =  round(float((cantidad)/contador)*100,4)

    #------------------- Botón eliminar --------------------------------------------------            
        iz,der = st.columns([37,63])
        with iz:
            # seleccionas el indice a eliminar
            indice= st.session_state.data.index
            selec = st.selectbox('Selecciona el indice a eliminar', indice.sort_values().unique())
            #si se presiona e boton se ejecuta la funcion eliminar
            if st.button('Eliminar fila'):
                st.session_state.data = eliminar_fila(st.session_state.data,selec)
                st.success(f"Fila con índice {selec} eliminada.")
        with der:
            st.write(st.session_state.data)
        
        if 'nuevas' not in st.session_state:
            st.session_state.nuevas = inicializador()

#--------------------------------------------------------- INGRESAR NUEVAS MATERIAS  --------------------------------------------------------------------------------------------

        if st.checkbox('Ingresar materias primas nuevas'):     
            materias_nuevas = st.text_input('(MPN) Ingresa el nombre de la nueva materia prima')
            unidad_nueva = st.text_input('(MPN) Ingresa la unidad')
            costo_nuevo = st.number_input(f'(MPN) Ingresa el costo para: **{materias_nuevas}**',value=1.00, step=1e-4, format="%.4f")
            moneda = st.selectbox('Elige el tipo de moneda',( 'MXN','USD'))
            cantidad_nueva = st.number_input(f'(MPN) Ingresa la cantidad para: **{materias_nuevas}**',value=1.00, step=1e-10, format="%.10f")
            # si el tipo de moneda es mxicana dejar igual, en caso contrario multiplicar por tipo_cambio
            if moneda == 'MXN':
                moneda = 1
                conversion = costo_nuevo
            else:
                moneda = 2
                conversion = costo_nuevo * tipo_cambio
            cont = 0
            if st.button('Agregar Fila'):
                
                cont += int(cont) + 1
                fecha_hoy = datetime.today().date()
                nueva_fila = {'SKU': cont,'Materia prima': materias_nuevas, 'Cantidad': cantidad_nueva, 'Unidad': unidad_nueva, 'Costo': conversion,'Fecha': fecha_hoy.strftime('%d/%m/%Y'), 'Moneda': moneda }
                # se agrega la fila nueva al df usando la funcion agregar_fila 
                st.session_state.nuevas = agregar_fila(st.session_state.nuevas, nueva_fila)
           
            #------------------- Botón eliminar --------------------------------------------------            
            iz,der = st.columns([37,63])
            with iz:
                # seleccionas el indice a eliminar
                indice= st.session_state.nuevas.index
                selec2 = st.selectbox('Selecciona el indice a eliminar ', indice.sort_values().unique())
                #si se presiona e boton se ejecuta la funcion eliminar
                if st.button('Eliminar fila '):
                    st.session_state.nuevas = eliminar_fila(st.session_state.nuevas,selec2)
                    st.success(f"Fila con índice {selec2} eliminada.")
            with der:
                st.write(st.session_state.nuevas) 

#----------------------------------------------------------------- CONCATENAR BASES -------------------------------------------------------------------
        n_lista = st.session_state.data['Cantidad'].tolist()
        if len(n_lista) !=0:    
            st.session_state.data['Cantidad'] = n_lista
            df_formulador = pd.concat([st.session_state.data,st.session_state.nuevas]).reset_index(drop=True)
            df_formulador['Costo unitario'] = df_formulador['Costo'] * df_formulador['Cantidad']
            df_formulador['Porcentaje (%)'] = round(((df_formulador['Costo unitario'])/(df_formulador['Costo unitario'].sum()))*100,2)
            # if unidad_caja != 0:
            #     df_formulador['Costo caja'] = [i * unidad_caja for i in df_formulador['Costo unitario']]
            # else:
            #     df_formulador['Costo caja'] = [0] * len(df_formulador['Materia prima'])
            if unidad_lote != 0:    
                df_formulador['Costo lote'] = [i * unidad_lote for i in df_formulador['Costo unitario']]
            else:
                df_formulador['Costo lote'] = [0] * len(df_formulador['Materia prima'])
            #Agregamos las materias nuevas a los dataframes

            #Con esta instrucción permitimos a altair mostrar la gráfica aunque tenga mas de 5000 renglones
            alt.data_transformers.enable('default', max_rows=None)
            chart_formulador = df_formulador.groupby(['SKU','Materia prima']).agg({'Costo unitario':'sum', 'Porcentaje (%)':'sum'}).reset_index()
            pie_formulador = alt.Chart(chart_formulador, title=nombre_producto).mark_arc().encode(
                                theta=alt.Theta(field='Costo unitario', type="quantitative"),
                                color=alt.Color(field='Materia prima', type="nominal"),
                                tooltip = ['Materia prima','Costo unitario','Porcentaje (%)']
                                ).interactive()

            #col1, col2 = st.columns([15,15])
            #with col1:
            #    st.write('Rendimiento: ' ,unidad_lote)
            #    st.write('Unidad Base: ' ,unidad_base)
                #st.write('Precio sugerido: $', (df_formulador['Costo unitario'].sum())*(1+(margen/100))) 
            #with col2:
            costo_unitario = df_formulador['Costo unitario'].sum()
               ## precio = costo_unitario*(1+ margen) 
            precio = costo_unitario  
            #    st.write('Costo unitario: $' ,round(costo_unitario ,2))
            #    # if unidad_caja != 0:
            #    #     costo_caja = df_formulador['Costo caja'].sum()
            #    #     #st.write('Costo por caja: $' , round(costo_caja,2))
            if unidad_lote != 0:
                costo_lote = df_formulador['Costo lote'].sum()
            #        st.write('Costo por lote: $' , round(costo_lote,2))
            df_formulador = df_formulador[['Materia prima', 'Cantidad', 'SKU', 'Unidad', 'Costo', 'Costo unitario', 'Porcentaje (%)'
                                        , 'Costo lote','Fecha','Moneda','Proveedor']]
            
           
            #st.write(df_formulador)
            ######################################### Aqui ##################################
                        ##########PIEZAS######################3
        st.subheader('PIEZAS')
        dosis = st.number_input("Cuantas dosis contiene la presentación ",value=1.00, step=1e-10, format="%.10f")
        if 'pza' not in st.session_state:
            st.session_state.pza = inicializador()
        unidad_lote_pza = st.text_input('Cuantas piezas contiene el lote de pt')
        if len(unidad_lote_pza) != 0:
            unidad_lote_pza = float(unidad_lote_pza)
        
        #margen = st.text_input('Cual será el margen de costo para el precio')
        margen = st.select_slider('Selecciona margen de costo', options=[25,50,75,90,100])


        materias_lista_pza = st.selectbox('Materia Prima ALPHA pt', df_productos['Desc_prod'].sort_values().unique())
        Unidad_pza = df_productos[ df_productos['Desc_prod']==materias_lista_pza]
        cantidades_lista_pza = st.number_input(f"Ingresa la cantidad para pt: **{materias_lista_pza}** en {Unidad_pza['Uni_med'].values[0]}",value=1.00, step=1e-10, format="%.10f")
        # cálculo costo por tipo cambio
        Unidad_pza['Cto_ent']= np.where(Unidad_pza['Cve_monc']== 2 ,Unidad_pza['Cto_ent'] * tipo_cambio, Unidad_pza['Cto_ent'])
        if st.button('Agregar fila pt'):
        # contador que acumula el todal de la columna cantidad
            contador = float(cantidades_lista_pza)
            for elemento in st.session_state.pza['Cantidad']:
                contador += float(elemento)
            # creacion de la fila nueva
            # creacion de la fila nueva
            new_row_pza = {'SKU': Unidad_pza['Cve_prod'].values[0],'Materia prima': materias_lista_pza, 'Cantidad': cantidades_lista_pza, 'Porcentaje (%)': "", 'Unidad': Unidad_pza['Uni_med'].values[0], 'Costo': Unidad_pza['Cto_ent'].values[0], 'Fecha': Unidad_pza['Fec_ent'].values[0],'Moneda': Unidad_pza['Cve_monc'].values[0],'Proveedor': Unidad_pza['Prov_std'].values[0]   }
            #new_row_pza = {'SKU': Unidad_pza['Cve_prod'].values[0],'Materia prima': materias_lista_pza, 'Cantidad': cantidades_lista_pza, 'Porcentaje (%)': "", 'Unidad': Unidad_pza['Uni_med'].values[0], 'Costo': Unidad_pza['Cto_ent'].values[0], 'Fecha': Unidad_pza['Fec_ent'].values[0],'Moneda': Unidad_pza['Cve_monc'].values[0]   }
           # se agrega la fila nueva al df usando la funcion agregar_fila 
            st.session_state.pza = agregar_fila(st.session_state.pza, new_row_pza)
            # se calcua el porcentaje y de agrega a la columna porcentaje (%) 
            for cantidad in st.session_state.pza['Cantidad']:
                st.session_state.pza['Porcentaje (%)'] =  round(float((cantidad)/contador)*100,4)

    #------------------- Botón eliminar --------------------------------------------------            
        iz,der = st.columns([37,63])
        with iz:
            # seleccionas el indice a eliminar
            indice= st.session_state.pza.index
            selec = st.selectbox('Selecciona el indice a eliminar pt', indice.sort_values().unique())
            #si se presiona e boton se ejecuta la funcion eliminar
            if st.button('Eliminar fila pt'):
                st.session_state.pza = eliminar_fila(st.session_state.pza,selec)
                st.success(f"Fila con índice {selec} eliminada.")
        with der:
            st.write(st.session_state.pza)
        
        if 'pzanuevas' not in st.session_state:
            st.session_state.pzanuevas = inicializador()

#--------------------------------------------------------- INGRESAR NUEVAS MATERIAS  --------------------------------------------------------------------------------------------

        if st.checkbox('Ingresar materias primas nuevas pt'):     
            materias_nuevas_pza = st.text_input('(MPN) Ingresa el nombre de la nueva materia prima pt')
            unidad_nueva_pza = st.text_input('(MPN) Ingresa la unidad pt')
            costo_nuevo_pza = st.number_input(f'(MPN) Ingresa el costo para pt: **{materias_nuevas_pza}**',value=1.00, step=1e-4, format="%.4f")
            moneda_pza = st.selectbox('Elige el tipo de moneda pt',( 'MXN','USD'))
            cantidad_nueva_pza = st.number_input(f'(MPN) Ingresa la cantidad para pt: **{materias_nuevas_pza}**',value=1.00, step=1e-10, format="%.10f")
            # si el tipo de moneda es mxicana dejar igual, en caso contrario multiplicar por tipo_cambio
            if moneda == 'MXN':
                moneda = 1
                conversion = costo_nuevo
            else:
                moneda = 2
                conversion = costo_nuevo * tipo_cambio
            cont = 0
            if st.button('Agregar Fila pt'):
                
                cont += int(cont) + 1
                fecha_hoy = datetime.today().date()
                nueva_fila_pza = {'SKU': cont,'Materia prima': materias_nuevas_pza, 'Cantidad': cantidad_nueva_pza, 'Unidad': unidad_nueva_pza, 'Costo': conversion,'Fecha': fecha_hoy.strftime('%d/%m/%Y'), 'Moneda': moneda }
                # se agrega la fila nueva al df usando la funcion agregar_fila 
                st.session_state.pzanuevas = agregar_fila(st.session_state.pzanuevas, nueva_fila_pza)
           
            #------------------- Botón eliminar --------------------------------------------------            
            iz,der = st.columns([37,63])
            with iz:
                # seleccionas el indice a eliminar
                indice= st.session_state.pzanuevas.index
                selec2 = st.selectbox('Selecciona el indice a eliminar pt ', indice.sort_values().unique())
                #si se presiona e boton se ejecuta la funcion eliminar
                if st.button('Eliminar fila pt '):
                    st.session_state.pzanuevas = eliminar_fila(st.session_state.pzanuevas,selec2)
                    st.success(f"Fila con índice {selec2} eliminada.")
            with der:
                st.write(st.session_state.pzanuevas)

                ###################################################################
        try:
            df_st = df_formulador.copy()
            
            df_st = df_st.rename(columns={'Costo lote' : 'Costo lote st' })
            if dosis != 0:    
                    df_st['Cantidad'] = df_st['Cantidad'] * dosis
                    df_st['Costo unitario'] = df_st['Costo unitario'] * df_st['Cantidad']       
        
            #st.write(df_st)
            
            #######################CONCATENAR BASES PT#############################

            n_lista_pza = st.session_state.pza['Cantidad'].tolist()
            if len(n_lista) !=0:    
                st.session_state.pza['Cantidad'] = n_lista_pza
                df_formulador_pt = pd.concat([st.session_state.pza,st.session_state.pzanuevas]).reset_index(drop=True)
                df_formulador_pt['Costo unitario'] = df_formulador_pt['Costo'] * df_formulador_pt['Cantidad']
                df_formulador_pt['Porcentaje (%)'] = round(((df_formulador_pt['Costo unitario'])/(df_formulador_pt['Costo unitario'].sum()))*100,2)
                # if unidad_caja != 0:
                #     df_formulador['Costo caja'] = [i * unidad_caja for i in df_formulador['Costo unitario']]
                # else:
                #     df_formulador['Costo caja'] = [0] * len(df_formulador['Materia prima'])
                if unidad_lote_pza != 0:    
                    df_formulador_pt['Costo lote'] = [i * unidad_lote_pza for i in df_formulador_pt['Costo unitario']]
                else:
                    df_formulador_pt['Costo lote'] = [0] * len(df_formulador_pt['Materia prima'])
                #Agregamos las materias nuevas a los dataframes

                #Con esta instrucción permitimos a altair mostrar la gráfica aunque tenga mas de 5000 renglones
                alt.data_transformers.enable('default', max_rows=None)
                chart_formulador_pt = df_formulador_pt.groupby(['SKU','Materia prima']).agg({'Costo unitario':'sum', 'Porcentaje (%)':'sum'}).reset_index()
                pie_formulador_pt = alt.Chart(chart_formulador_pt, title=nombre_producto).mark_arc().encode(
                                    theta=alt.Theta(field='Costo unitario', type="quantitative"),
                                    color=alt.Color(field='Materia prima', type="nominal"),
                                    tooltip = ['Materia prima','Costo unitario','Porcentaje (%)']
                                    ).interactive()

                #col1, col2 = st.columns([15,15])
                #with col1:
                #    st.write('Rendimiento: ' ,unidad_lote)
                #    st.write('Unidad Base: ' ,unidad_base)
                    #st.write('Precio sugerido: $', (df_formulador['Costo unitario'].sum())*(1+(margen/100))) 
                #with col2:
                costo_unitario_pt = df_formulador_pt['Costo unitario'].sum()
                ## precio = costo_unitario*(1+ margen) 
                precio_pt = costo_unitario_pt  
                #    st.write('Costo unitario: $' ,round(costo_unitario ,2))
                #    # if unidad_caja != 0:
                #    #     costo_caja = df_formulador['Costo caja'].sum()
                #    #     #st.write('Costo por caja: $' , round(costo_caja,2))
                if unidad_lote_pza != 0:
                    costo_lote_pt = df_formulador_pt['Costo lote'].sum()
                #        st.write('Costo por lote: $' , round(costo_lote,2))
                df_formulador_pt = df_formulador_pt[['Materia prima', 'Cantidad', 'SKU', 'Unidad', 'Costo', 'Costo unitario', 'Porcentaje (%)'
                                            , 'Costo lote','Fecha','Moneda', 'Proveedor']]

                df_pt = df_formulador_pt.copy()
                df_pt = df_pt.rename(columns={'Costo lote' : 'Costo lote ME' })
                #st.write(df_pt)

            #######################################################################

            ###########################CONCATENAR BASES PT Y ST#####################################################

            df_final = pd.concat([df_st,df_pt]).reset_index(drop=True)
            st.write(df_final)

            #Con esta instrucción permitimos a altair mostrar la gráfica aunque tenga mas de 5000 renglones
            alt.data_transformers.enable('default', max_rows=None)
            chart_formulador_final = df_final.groupby(['SKU','Materia prima']).agg({'Costo unitario':'sum', 'Porcentaje (%)':'sum'}).reset_index()
            pie_formulador_final = alt.Chart(chart_formulador_final, title=nombre_producto).mark_arc().encode(
                                theta=alt.Theta(field='Costo unitario', type="quantitative"),
                                color=alt.Color(field='Materia prima', type="nominal"),
                                tooltip = ['Materia prima','Costo unitario','Porcentaje (%)']
                                ).interactive()

            col1, col2 = st.columns([15,15])
            with col1:
                st.write('Rendimiento: ' ,unidad_lote_pza)
                st.write('Unidad Base: ' ,unidad_base)
                st.write('Precio sugerido: $', (df_final['Costo unitario'].sum())*(1+(margen/100))) 
            with col2:
                costo_unitario_final = df_final['Costo unitario'].sum()
            ## precio = costo_unitario*(1+ margen) 
                precio_final = costo_unitario_final  
                st.write('Costo unitario: $' ,round(costo_unitario_final ,2))
                #    # if unidad_caja != 0:
                #    #     costo_caja = df_formulador['Costo caja'].sum()
                #    #     #st.write('Costo por caja: $' , round(costo_caja,2))
                if unidad_lote_pza != 0:
                    costo_lote_st = df_st['Costo lote st'].sum()
                if unidad_lote_pza != 0:
                    costo_lote_pt = df_pt['Costo lote ME'].sum()
                costo_lote_final = costo_lote_st + costo_lote_pt

                st.write('Costo por lote pt: $', round(costo_lote_final, 2))                
                #        st.write('Costo por lote: $' , round(costo_lote,2))
            ########################################################################################################



            # converir primeros tres encabezados en dataframe para poder descargarlos 
            diccionario = [unidad_lote, unidad_base,precio] #en la variable diccionario mando a llamr a los datos Rendimiento, aunidad base y precio sugerido 
            convert= pd.DataFrame(data=diccionario)# convierto los tados a un data frame
            convert.columns=['Data'] # renombramos la columna
            titu= pd.DataFrame(['Rendimiento: ','Unidad Base: ', 'Precio sugerido: $']) # creamos otro dataframe que va a servir de encavezados
            titu.columns=[' '] # renombro en blanco para que no enumere la columna 
            #convertir los ultimos 3 ecabezados en dataframe 
            #diccionario2=[costo_unitario,costo_caja,costo_lote] # en la variable diccionario2 mando a llamar los datos de costo unitario, costo por caja y costo por lote
            diccionario2=[costo_unitario,costo_lote] # en la variable diccionario2 mando a llamar los datos de costo unitario, costo por caja y costo por lote
            convert2=pd.DataFrame(data=diccionario2) # Converto a dataframe
            convert2.columns=[' Data'] # renombro la columna
            titu2 = pd.DataFrame(['Costo unitario: $', 'Costo por caja: $', 'Costo por lote: $'])#creamos dataframe con los encabezados
            titu2.columns=['   '] # espacio en blanco

            espacio= pd.DataFrame([' ']) # este dataframe es para separar una columna entera y que quede en blanco
            espacio.columns=['  '] # dejamos en blanco la columna para que no muestre ningun numero

            nuevo=pd.concat([df_final,espacio,titu,convert,titu2,convert2], axis=1,) # concatenamos todos los dataframe en uno solo 
            
            st.download_button(label="Descargar ", data=nuevo.to_csv(), mime="text/csv") # creamos el boton para descargar el nuevo dataframe con los datos
            st.altair_chart(pie_formulador_final, use_container_width=True)
        except UnboundLocalError:
            st.write("")
        except KeyError:
            st.write("")
      
if __name__ == '__main__':
    main()
  



