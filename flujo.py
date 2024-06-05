import streamlit as st
import pandas as pd
from PIL import Image
import re
import altair as alt
import numpy as np
from io import BytesIO
import csv
import base64

st.set_page_config(layout="wide")
def main():
    img = Image.open('logo_farmiral.jpg')

    colm1, colm2, colm3 = st.columns([5,10,1])
    with colm1:
        st.write("")
    with colm2:
        st.image(img,width=250)
    with colm3:
        st.write("")

    colmn1, colmn2, colmn3 = st.columns([5,10,1])
    with colmn1:
        st.write("")
    with colmn2:
        st.title("")
    with colmn3:
        st.write(" ")
  
    # imprtamos las bases
    ruta= 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTcbKssx2R_56l9NlUZm7uk2-dLWPYo8xooEI4fodTOQnNjKq8iQiX_9i2imJRRPQ/pub?gid=596894446&single=true&output=csv'
    ruta2= 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRgYuKpr_VZVrloxr41Pio2t2_jVFSw3RnQtxuSOGJuOcjgOqh7qizdzglNMvTOslmsdBSpYxvQyzcx/pub?output=csv'
    fl = pd.read_csv(ruta,encoding='latin-1')
    sl= pd.read_csv(ruta2,encoding='latin-1')
    #cambio de nombre a columnas
    fl.columns=['Concepto','Estimado','Real','Prioridad','Semana','Mes','Clasificacion','Subclasificacion','Tipo','Revision','Concepto en presupuesto']
    sl.columns=['Semana','Saldo inicial']


   
    
# funcion para convertir los datos str a float
    def limpiar(s):
        if isinstance(s,str): # si los datos son de tipo sting
            s = s.strip() # eliminar espacios al inicio y al final
            if s == "-": # si el dato solo es un signo menos
                return 0 # reemplazar por cero
            s = re.sub(r'\s+', '', s) # eliminar todos los espacios
            s= s.replace(',','') # eliminar comas
        return s 
    
    fl['Estimado']=fl['Estimado'].apply(limpiar) # limpiamos los datos llamando a la función
    fl['Estimado']= pd.to_numeric(fl['Estimado'], errors='coerce') # convertimos los datos a float
    fl['Real']= fl['Real'].apply(limpiar)
    fl['Real']=pd.to_numeric(fl['Real'],errors='coerce')
    fl =fl.fillna(0)

    #Creacion de la columna seguimiento
    fl['Seguimiento']= np.where( # np.where regresa 1 valor dependiendo
        (fl['Revision']=="si") &((fl['Estimado']-fl['Real'])>0), #condicion doble
         fl['Estimado']-fl['Real'],0 # valor que devuelve dependiendo si se cumplen las condiciones
                                ) 
    # filtro por semana
    colu1,colu2,colu3= st.columns([5,7,2])
    with colu1:
        sem = st.selectbox('Semana', fl['Semana'].sort_values().unique())   
        
    semana= fl[fl['Semana']==sem]
    df_semana = pd.DataFrame(semana) 
    slfiltro = sl[sl['Semana']==sem]
    fl_filtro_sem= fl[fl['Semana']==sem]

    # creacion de tabla pivote
    tabla= df_semana.pivot_table(
        index=["Prioridad","Concepto en presupuesto"],
        values=["Estimado","Real"],
        aggfunc="sum",
        fill_value=0
    )

    suma= df_semana.pivot_table(
        index="Tipo",
        values=["Estimado", "Real", "Seguimiento"],
        aggfunc="sum",
        fill_value=0
    )

    df_tabla=tabla.reset_index() # convertimos la tabla pivote en dataframe
    df_suma=suma.reset_index()
    #recumeramos el saldo inicial de la tabla saldo inicial filtrada 
    saldo_inicial=slfiltro['Saldo inicial'].values[0] if not slfiltro.empty else 0
    # creamos un dataframe utilizando un diccionatio en el cual rellenamos con el saldo inicial
    saldo_inicial_df =pd.DataFrame({'Tipo':['Saldo inicial'],'Estimado':[saldo_inicial],'Real':[saldo_inicial],'Seguimiento':[0]})
    #concatenamos la los dataframe de saldo inicial y la tabla suma
    df_suma=pd.concat([saldo_inicial_df,df_suma], ignore_index=True)
    
    # calculo en estimado tabla pivote 
    inicial_e= df_suma.loc[0,'Estimado'] # recuperamos el dato en la posicion 0 de la columna estimado
    egreso_e= df_suma.loc[1,'Estimado'] 
    ingreso_e= df_suma.loc[2,'Estimado']
    r_temp_e= inicial_e + ingreso_e - egreso_e # hacemos operaciones con los datos adquiridos
    resultado_e= round(r_temp_e,2) # guardamos el resultado con decimales no mayor a 2 

    # calculo de Rea tabla pivote
    inicial_r = df_suma.loc[0,'Real']
    egreso_r = df_suma.loc[1,'Real']
    ingreso_r = df_suma.loc[2,'Real']
    r_temp_r = inicial_r + ingreso_r - egreso_r
    resultado_r = round(r_temp_r,2)

    # colocamos el valor del resultado del real en la la coluna seguiiento
    df_suma.loc[0,'Seguimiento'] = resultado_r

    inicial_s = df_suma.loc[0,'Seguimiento']
    egreso_s = df_suma.loc[1,'Seguimiento']
    ingreso_s = df_suma.loc[2,'Seguimiento']
    r_temp_s = inicial_s + ingreso_s - egreso_s
    resultado_s = round(r_temp_s,2)
    # Creo un dataframe con los resultados 
    saldo_final = pd.DataFrame({'Tipo':'Saldo Final','Estimado':[resultado_e],'Real':[resultado_r],'Seguimiento':[resultado_s]})
    df_suma = pd.concat([df_suma,saldo_final], ignore_index=True) # concateno a la tabla pivote
    
    # función para cambiar de color los numeros negativos
    def color_negativo(val):
        if isinstance(val, (int, float)):  # Asegurarse de que el valor es numérico
            color = 'red' if val < 0 else '' # si el valor es menor a cero guardas rojo, de lo contrario no guardas nada
            return f'color: {color}' # regresa un estilo css con el color establecido
        return '' # en caso de que el valor sea str no regresa nada
    

    with colu2:
        st.write("Saldos",df_suma.style.applymap(color_negativo)) # imprimimos la tabla agregando el estilo de la funcion color_negativo
        
    with colu3:
        st.write("")
    
    col1, col2, col3= st.columns([10,10,10])
    with col1:
        st.subheader('Desglose Flujo')
        st.write(df_tabla)
    with col2:
        st.subheader('Detalle concepto')
        seleccion = st.selectbox('Filtro', fl_filtro_sem['Concepto en presupuesto'].sort_values().unique())   
        filtro= fl_filtro_sem[fl_filtro_sem['Concepto en presupuesto']==seleccion]
        #Eliminamos de la visualización algunas columnas
        filtro = filtro[['Concepto', 'Estimado', 'Real', 'Seguimiento', 'Mes']]
        total_est = filtro['Estimado'].sum()
        total_real = filtro['Real'].sum()
        frase_est = 'Estimado total $ ' + str(round(total_est))
        frase_real = 'Real total $ ' + str(round(total_real))
        st.write(filtro)
        st.info(frase_est, icon='💵')
        st.info(frase_real, icon='💵')
    with col3:
        st.subheader('Avance')
        chart_data = {'Tipo': ['Estimado', 'Real'],
                      'Monto': [total_est, total_real]}
        chart_df = pd.DataFrame(chart_data)
        total_monto = chart_df['Monto'].sum()
        chart_df['Porcentaje'] = (chart_df['Monto']/total_monto) * 100
        pie_bottom = alt.Chart(chart_df, title='Estimado vs Real').mark_arc().encode(
        theta=alt.Theta(field='Monto', type="quantitative"),
        color=alt.Color(field='Tipo', type="nominal", scale=alt.Scale(scheme='tableau10')), 
        tooltip = [alt.Tooltip(field="Monto", type="quantitative"), 
                   alt.Tooltip(field='Tipo', type='nominal'),
                   alt.Tooltip(field='Porcentaje', type='quantitative', format=".2f")],

        )
        #Mostramos el objeto en streamlit
        st.altair_chart(pie_bottom, use_container_width=True)
    
    #scale=alt.Scale(scheme='tableau10')



if __name__ == '__main__':
    main()