import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import altair as alt
from datetime import datetime
import re
st.set_page_config(layout="wide")

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

    #Quitamos espacios a los nombres de las columnas
    df_formulas.columns = df_formulas.columns.str.strip()
    df_productos.columns = df_productos.columns.str.strip()

    #Filtramos solo las columnas que necesitamos de cada base
    df_formulas = df_formulas[['Cve_copr', 'Cve_prod', 'Can_copr', 'Tip_copr', 'New_med', 'New_copr', 'Partida', 'Undfor', 
                                'Desc_prod', 'Cve_mon', 'Cve_tial', 'Tipcam', 'Tip_cam', 'Ren_copr', 'Cto_ent', 'Uncfor']]
    df_productos = df_productos[['Cve_prod', 'Desc_prod', 'Uni_med', 'Cto_ent', 'Cve_tial']]

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

     # convertimos la cantidad de KG a GR multiplicandola por 1000
    @st.cache_resource
    def gramos():
        gramos = df_formulas[['Can_copr','Undfor','Cto_ent']] # filto por cantidad y unidad de componente
        for i in range(len(df_formulas['Can_copr'])): # creo un for que recorra una columna entera, en este  caso la de cantidad 
            if gramos['Undfor'][i] == "KG": # if donde evalua, en la iteracion actual, si en la columna unidad_componente hay un KG
                 gramos['Can_copr'][i] = (gramos['Can_copr'][i])*1000 # Si lo anterior se cumple, se multiplica por 1000 la columna Cantidad en la iteracion actual
                 gramos['Undfor'][i]="GR" # Se reemplaza lo que hay en la columna Unidad_componente por el string GR
                 gramos['Cto_ent'][i]=  ( gramos['Cto_ent'][i])/1000
            else:
                gramos['Can_copr'][i] = gramos['Can_copr'][i]  # si no se cumple se deja tal cual
                gramos['Undfor'][i]=gramos['Undfor'][i]
                gramos['Cto_ent'][i]= gramos['Cto_ent'][i]
        return gramos
        #fin for
    df_formulas[['Can_copr','Undfor','Cto_ent']] = gramos() # una vez termindo el proceso se reemplazan los nuevos datos en df_formulas_n

    @st.cache_resource
    def gramos2():
        gramform = df_productos[['Uni_med', 'Cto_ent']] # Filtro las columnas correspondientes a cantidad y Unidad componente
        for i in range (len(df_productos['Uni_med'])): # recorro la una columna entera 
            if  gramform['Uni_med'][i] == "KG": # si en el recorrido encuentra un KG
                gramform['Uni_med'][i] = "GR" # lo reemplaza por "GR"
                gramform['Cto_ent'][i]=(gramform['Cto_ent'][i])/1000 # divido entre 1000
            else:
                gramform['Uni_med'][i]=gramform['Uni_med'][i] # en caso que no coinsida queda talcual
                gramform['Cto_ent'][i] = gramform['Cto_ent'][i]
        return gramform
        #fin for   
    df_productos[['Uni_med', 'Cto_ent']] = gramos2()


    st.title('Costos Farmiral')

    #Seleccionar si se va a consultar costos desglosados o costear
    if st.checkbox("Costos desglosados"):
    #Hacemos merge con los nombres de las formulas para facilitar la busqueda del producto a costear
        df_formulas_n = df_formulas.merge(df_productos.rename({'Desc_prod':'Formula'},axis=1), left_on='Cve_copr', 
            right_on='Cve_prod', how='left')
        df_formulas_n.columns = ['SKU', 'Componente', 'Cantidad', 'Tipo', 'Atributo', 'Version pt', 'Partida', 'Unidad_componente'
                                    , 'Nombre', 'Cve_mon', 'Tipo_x', 'Tipcam','Tip_cam', 'Rendimiento','Costo', 'Unidad'
                                    , 'Cve_prod_y', 'Formula', 'Unidad pt', 'Cto_ent_y', 'Tipo_prod']

    
        #Eliminamos las versiones V1, V2, V3 y V4
        df_formulas_n = df_formulas_n.loc[(df_formulas_n['Version pt']!='V1') & (df_formulas_n['Version pt']!='V2') & (df_formulas_n['Version pt']!='V3') & (df_formulas_n['Version pt']!='V4')]
        
        #Creamos el filtro para seleccionar la formula a análizar
        df_formulas_prueba = df_formulas_n[df_formulas_n.SKU.str.startswith('51')].reset_index()
        formula = st.selectbox('Formula', df_formulas_prueba['Formula'].sort_values().unique())        
        #Esta tabla nos da todo lo que contiene la formula "51"
        pt = df_formulas_n[df_formulas_n.Formula == formula]
        pt = pt[pt.SKU.str.startswith('51')].reset_index()
        #Nos quedamos solo con las columnas necesarias de la base
        pt = pt[['SKU','Componente','Nombre','Cantidad','Costo','Unidad_componente','Rendimiento','Unidad pt']]
        #Calculamos cantidades y costos unitarios
        pt['Cantidad'] = pt['Cantidad']/pt['Rendimiento']
        pt['Costo total'] = pt['Cantidad'] * pt['Costo']
        #Filtramos la tabla pt para obtener todos los materiales que se utilizan en el semiterminado
        semt = pt[pt.Componente.str.startswith('41')]['Nombre'].reset_index()
        #Obtenemos del filtro un simple valor para usar en la extracción de componentes
        semt = semt.iloc[0]['Nombre']
        semit = df_formulas_n[df_formulas_n.Formula == semt]
        semit = semit[semit.SKU.str.startswith('41')].reset_index()
        semit = semit[['SKU','Componente','Nombre','Cantidad','Costo','Unidad_componente','Rendimiento','Unidad pt']]
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
            st.altair_chart(pie_st, use_container_width=True)

        st.subheader('Materiales Producto Terminado por unidad')
        st.write(pt)
        st.subheader('Materiales Semiterminado por unidad')
        st.write(semit)
        #st.write(semt)

    if st.checkbox('Formulador'):
        #st.warning('Formulador en construcción')
        nombre_producto = st.text_input('Nombre del producto a formular')
        materias_lista = st.multiselect('Materia Prima ALPHA', df_productos['Desc_prod'].sort_values().unique())
        df_filtered = df_productos[df_productos['Desc_prod'].isin(materias_lista)].reset_index()
        df_formulador = df_filtered[['Cve_prod', 'Desc_prod', 'Uni_med', 'Cto_ent']]
        df_formulador.columns = ['SKU','Materia prima','Unidad','Costo']
        duplist = df_productos[df_productos.duplicated('Desc_prod')]
        cantidades_lista = st.text_input('Ingresa las cantidades necesarias por unidad en orden separados por una coma (,)')
        c_lista = re.split(",",cantidades_lista)

        mm = pd.Series(materias_lista)
        

        ###
        temp_lista=[]
        if len(cantidades_lista) != 0:
           for i in range(len(materias_lista)):
               n = float(c_lista[i])
               temp_lista.append(n)

        if len(temp_lista) !=0:
            cc = pd.Series(temp_lista)
            datamc = {'Materia prima': mm, 'Cantidad':cc}
            inter = pd.DataFrame(datamc)
            cantidad_total = inter['Cantidad'].sum()
            inter['Porcentaje (%)'] = round(((inter['Cantidad'])/cantidad_total)*100,2)
            inter_temp = inter.merge(df_formulador, on='Materia prima', how='left')
            inter_temp = inter_temp[['Materia prima', 'Cantidad', 'Porcentaje (%)', 'Unidad', 'Costo']]
            st.write(inter_temp)

            ###
            df_formulador = inter.merge(df_formulador, on='Materia prima', how='left')
            
        sku=[]
        m_lista=[]
        u_lista=[]
        c2_lista=[]
        c3_lista=[]
        if st.checkbox('Ingresar materias primas nuevas'):     
            materias_nuevas = st.text_input('(MPN) Ingresa los nombres de las materias primas nuevas separados por una coma (,)')
            unidad_nueva = st.text_input('(MPN) Ingresa las unidades por orden separados por una coma (,)')
            costo_nuevo = st.text_input('(MPN) Ingresa el costo por orden separado por una coma (,)')
            cantidad_nueva = st.text_input('(MPN) Ingresa las cantidades de las nuevas materias en orden separados po una coma (,)')
            
            

            if len(materias_nuevas) != 0:
                materias_nuevas = re.split(",",materias_nuevas)
                for i in range(len(materias_nuevas)):
                    m = materias_nuevas[i]
                    m_lista.append(m)
                    sku = list(range(len(m_lista)))
            if len(unidad_nueva) != 0:
                unidad_nueva = re.split(",",unidad_nueva)
                for i in range(len(unidad_nueva)):
                    u = unidad_nueva[i]
                    u_lista.append(u)
            if len(costo_nuevo) != 0:
                costo_nuevo = re.split(",",costo_nuevo)
                for i in range(len(costo_nuevo)):
                    c3 = float(costo_nuevo[i])
                    c3_lista.append(c3)
            if len(cantidad_nueva) != 0:
                cantidad_nueva = re.split(",",cantidad_nueva)
                for i in range(len(cantidad_nueva)):
                    c = float(cantidad_nueva[i])
                    c2_lista.append(c)

            mmn = pd.Series(m_lista)
            uun = pd.Series(u_lista)
            ccn = pd.Series(c3_lista)
            c2n = pd.Series(c2_lista)
            datanc = {'Materia prima nueva': mmn, 'Unidad':uun, 'Costo':ccn, 'Cantidad':c2n}
            inter2 = pd.DataFrame(datanc)
            st.write(inter2)

        skus = pd.Series(sku) 
        mm_lista = pd.Series(m_lista)
        uu_lista = pd.Series(u_lista)
        c3c_lista = pd.Series(c3_lista)
        c2c_lista = pd.Series(c2_lista)
        d = {'SKU':skus, 'Materia prima':mm_lista, 'Unidad':uu_lista, 'Costo':c3c_lista, 'Cantidad':c2c_lista}
        df = pd.DataFrame(data=d)
        unidad_base = st.text_input('Ingresa la unidad base del producto a formular')
        unidad_caja = st.text_input('Cuantas unidades contiene la presentación')
        if len(unidad_caja) != 0: 
            unidad_caja = float(unidad_caja)
        unidad_lote = st.text_input('Cuantas unidades contiene el lote de producción')
        if len(unidad_lote) != 0:
            unidad_lote = float(unidad_lote)
        #margen = st.text_input('Cual será el margen de costo para el precio')
        margen = st.select_slider('Selecciona margen de costo',
                    options=[25,50,75,90,100])
        #if len(margen) != 0:
        #    margen = float(margen)
        n_lista=[]
        if len(cantidades_lista) != 0:
           for i in range(len(materias_lista)):
               n = float(c_lista[i])
               n_lista.append(n)
            
        if len(n_lista) !=0:    
            df_formulador['Cantidad'] = n_lista
            df_formulador = pd.concat([df_formulador,df]).reset_index(drop=True)
            df_formulador['Costo unitario'] = df_formulador['Costo'] * df_formulador['Cantidad']
            df_formulador['Porcentaje (%)'] = round(((df_formulador['Costo unitario'])/(df_formulador['Costo unitario'].sum()))*100,2)
            if unidad_caja != 0:
                df_formulador['Costo caja'] = [i * unidad_caja for i in df_formulador['Costo unitario']]
            else:
                df_formulador['Costo caja'] = [0] * len(df_formulador['Materia prima'])
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

            col1, col2 = st.columns([15,15])
            with col1:
                st.write('Rendimiento: ' ,unidad_lote)
                st.write('Unidad Base: ' ,unidad_base)
                st.write('Precio sugerido: $', (df_formulador['Costo unitario'].sum())*(1+(margen/100))) 
            with col2:
                costo_unitario = df_formulador['Costo unitario'].sum()
                precio = costo_unitario*(1+margen) 
                st.write('Costo unitario: $' ,round(costo_unitario ,2))
                if unidad_caja != 0:
                    costo_caja = df_formulador['Costo caja'].sum()
                    st.write('Costo por caja: $' , round(costo_caja,2))
                if unidad_lote != 0:
                    costo_lote = df_formulador['Costo lote'].sum()
                    st.write('Costo por lote: $' , round(costo_lote,2))
            df_formulador = df_formulador[['Materia prima', 'Cantidad', 'SKU', 'Unidad', 'Costo', 'Costo unitario', 'Porcentaje (%)'
                                        ,'Costo caja', 'Costo lote']]
            
            st.write(df_formulador)
            # converir primeros tres encabezados en dataframe para poder descargarlos 
            diccionario = [unidad_lote, unidad_base,prsuge] #en la variable diccionario mando a llamr a los datos Rendimiento, aunidad base y precio sugerido 
            convert= pd.DataFrame(data=diccionario)# convierto los tados a un data frame
            convert.columns=['Data'] # renombramos la columna
            titu= pd.DataFrame(['Rendimiento: ','Unidad Base: ', 'Precio sugerido: $']) # creamos otro dataframe que va a servir de encavezados
            titu.columns=[' '] # renombro en blanco para que no enumere la columna 
            #convertir los ultimos 3 ecabezados en dataframe 
            diccionario2=[csto,cstoca,cstolo] # en la variable diccionario2 mando a llamar los datos de costo unitario, costo por caja y costo por lote
            convert2=pd.DataFrame(data=diccionario2) # Converto a dataframe
            convert2.columns=[' Data'] # renombro la columna
            titu2 = pd.DataFrame(['Costo unitario: $', 'Costo por caja: $', 'Costo por lote: $'])#creamos dataframe con los encabezados
            titu2.columns=['   '] # espacio en blanco

            espacio= pd.DataFrame([' ']) # este dataframe es para separar una columna entera y que quede en blanco
            espacio.columns=['  '] # dejamos en blanco la columna para que no muestre ningun numero

            nuevo=pd.concat([df_formulador,espacio,titu,convert,titu2,convert2], axis=1,) # concatenamos todos los dataframe en uno solo 
          
            st.download_button(label="Descargar", data=nuevo.to_csv(), mime="text/csv") # creamos el boton para descargar el nuevo dataframe con los datos
            st.altair_chart(pie_formulador, use_container_width=True)  




if __name__ == '__main__':
    main()
  



