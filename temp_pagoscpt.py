import streamlit as st
import pandas as pd
from PIL import Image
#from io import StringIO
#from openpyxl import Workbook
from io import BytesIO
import csv
import base64

# Function to append row to DataFrame
def append_row(df, row):
    #return df.append(row, ignore_index=True)
    row = pd.DataFrame([row])
    return pd.concat([df, row], ignore_index=True)

# Function to create initial DataFrame
def create_initial_dataframe():
    return pd.DataFrame(columns=['Proveedor', 'Monto', 'Facturas'])  # Update column names as needed
def initial_dataframe():
    return pd.DataFrame(columns=['Proveedor', 'Correo', 'Clave', 'RFC', 'Banco', 'Tipo','Persona_tipo','Id_banco'])

st.set_page_config(layout="wide")

# Main function
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
      # agregamos la columna id_banco la cual contiene los primeros 3 digitos de la cuenta + 0 al principio
    try:
        prov['Id_banco'] = '0'+ prov['Numero'].str[:3]
    except KeyError: # si se recarga la página, las columnas del dataframe cambian, si eso sucede se ejecuta la siguiente linea con el nombre de la columna correspondiente a la nueva info
        prov['Id_banco'] = '0'+ prov['Clave'].str[:3]

    prov.columns = ['Proveedor', 'Correo', 'Clave', 'RFC', 'Banco', 'Tipo','Persona_tipo','Id_banco']
    for i in range(len(prov['Proveedor'])):
        prov.loc[i,'Clave'] = str(prov.loc[i,'Clave'])
    prov['Clave'] = prov['Clave'].astype(str)
    prov['RFC'] = prov['RFC'].astype(str)
    
  
   

    # Create or retrieve DataFrame from session_state
    if 'data' not in st.session_state:
        st.session_state.data = create_initial_dataframe()

    if 'filtered_data' not in st.session_state:
        st.session_state.filtered_data = initial_dataframe()

    #st.write('Current DataFrame:', st.session_state.data)
    
    # Collect user input for new row
    provedores_selec = st.selectbox('Elije al proveedor', prov['Proveedor'].sort_values().unique())
    cantidades_pagar = st.number_input('Cantidad a pagar', value=1.00, step=1e-4, format="%.4f")
    tc = st.number_input('Tipo de cambio', value=1.00, step=1e-4, format="%.4f")
    cantidades_pagar = cantidades_pagar*tc
    fact = st.text_input('Escribe el concepto de pago')
    #col_names_banregio = ['Secuencia', 'Tipo', 'Cuenta_Destino', 'Importe', 'IVA', 'Descripcion', 'Ref_Numerica', 'Referencia']
    if st.button('Append Row'):
        # Construct a row from user input
        new_row = {'Proveedor': provedores_selec, 'Monto': cantidades_pagar, 'Facturas': fact, 'tc': tc, 'USD': cantidades_pagar/tc }

        # Append the new row to the DataFrame
        st.session_state.data = append_row(st.session_state.data, new_row)
        # filtro los datos por selección    
        filtered_prov = prov[prov['Proveedor'] == provedores_selec]
        # Convertir la fila filtrada en un DataFrame
        if not filtered_prov.empty:
            st.session_state.filtered_data = append_row(st.session_state.filtered_data, filtered_prov.iloc[0])

        
        st.success('Row appended successfully!')
        

    st.write('Validacion:', st.session_state.data)
    monto_pago = st.session_state.data['Monto'].sum()
    frase_val = 'Monto total de solicitud de pagos $ ' + str(round(monto_pago))
    st.info(frase_val, icon='💵')
    #st.write(st.session_state.data['Proveedor'])
    df_temp = st.session_state.data.merge(prov, on='Proveedor', how='left')
    
     
    if st.checkbox('Cargar base prellenada'):
        try:
            df_temp = st.file_uploader('Selecciona la base prellenada', type='csv')
            df_temp = pd.read_csv(df_temp, dtype={'Numero':str}, encoding='latin-1')
            df_temp = pd.DataFrame(df_temp)
            st.write('Validacion:', df_temp)
            monto_pago = df_temp['Monto'].sum()
            frase_val = 'Monto total de solicitud de pagos $ ' + str(round(monto_pago))
            st.info(frase_val, icon='💵')
            #st.write(df_temp)
            df_temp = df_temp.merge(prov, on='Proveedor', how='left')
            #st.write(df_temp)
        except ValueError:
            st.warning('Carga una base ')
        except KeyError:
            st.error('⚠️BASE NO COMPATIBLE, CARGA UNA BASE CORRECTA.⚠️')

    ref_num = st.text_input('Escribe la referencia numerica')
    ref_str = st.text_input('Escribe la referencia de pagos')

    if st.checkbox('Plantilla Banregio'):
        try:
            col_names_banregio = ['Secuencia', 'Tipo', 'Cuenta_Destino', 'Importe', 'IVA', 'Descripcion', 'Ref_Numerica', 'Referencia']
            #n=len(st.session_state.data['Proveedor'])  
            n=len(df_temp['Proveedor'])
            sec = list(range(n))
            tipo = ["s" for i in range(n)]
            iva = [0]*n
            ref = [ref_num for i in range(n)]
            referencia = [ref_str for i in range(n)]
            col_names_banregio = ['Secuencia', 'Tipo', 'Cuenta_Destino', 'Importe', 'IVA', 'Descripcion', 'Ref_Numerica', 'Referencia']
            data = list(zip(sec, tipo, df_temp['Clave'], df_temp['Monto'], iva, df_temp['Facturas'], ref, referencia))
            df_banregio = pd.DataFrame(data, columns=col_names_banregio)
            df_banregio['Cuenta_Destino'] = df_banregio['Cuenta_Destino'].astype(str)
            st.write(df_banregio)


            def to_excel(df):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Sheet1')
                processed_data = output.getvalue()
                return processed_data
            def get_download_link(data, filename, text):
                b64 = base64.b64encode(data).decode()
                return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{text}</a>'
            excel_data = to_excel(df_banregio)
            st.markdown(get_download_link(excel_data, 'p_banregio.xlsx', 'Descargar plantilla Banregio'), unsafe_allow_html=True)
        except TypeError:
            st.warning("Cargando base...")
        except KeyError:
            st.error("⚠️LA BASE CARGADA NO ES COMPATIBLE.⚠️")
    
    if st.checkbox('Plantilla Banco Base'):
        try:
            
           
            if len(df_temp) > 0:

                cadena_lista = []
                for index, row in df_temp.iterrows():
                    cadena_lista.append("SP|"+ row['Proveedor'].replace(" ", "")+"|"+row['Clave'].replace(" ", "")+"|MXN|"+row['Id_banco'].replace(" ", "")+"|"+ row['Persona_tipo'].replace(" ", "")+"|||"+row['Proveedor'].replace(" ", "")+"|"+row['RFC'].replace(" ", "")+"||"+row['Correo'].replace(" ", "")+"||")
                st.write(cadena_lista)

                cadena_str2 = "\n".join(cadena_lista)
                def get_text_download_link(text, filename, text_link):
                    b64 = base64.b64encode(text.encode()).decode()
                    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">{text_link}</a>'
                st.markdown(get_text_download_link(cadena_str2, 'Banco_Base.txt', 'Descargar Plantilla'), unsafe_allow_html=True)

            else:
                cadena = []
                for index, row in st.session_state.filtered_data.iterrows():
                    cadena.append("SP|"+ row['Proveedor'].replace(" ", "")+"|"+row['Clave'].replace(" ", "")+"|MXN|"+row['Id_banco'].replace(" ", "")+"|"+ row['Persona_tipo'].replace(" ", "")+"|||"+row['Proveedor'].replace(" ", "")+"|"+row['RFC'].replace(" ", "")+"||"+row['Correo'].replace(" ", "")+"||")
                st.write(cadena)

                cadena_str = "\n".join(cadena)
                def get_text_download_link(text, filename, text_link):
                    b64 = base64.b64encode(text.encode()).decode()
                    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">{text_link}</a>'
                st.markdown(get_text_download_link(cadena_str, 'Banco_Base.txt', 'Descargar Plantilla'), unsafe_allow_html=True)
        except KeyError:
            st.error("⚠️LA BASE CARGADA NO ES COMPATIBLE.⚠️ ")
        except TypeError:
            st.warning("Cargando base...")
            

if __name__ == '__main__':
    main()
