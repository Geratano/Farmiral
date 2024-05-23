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
    prov.columns = ['Proveedor', 'Correo', 'Clabe', 'RFC', 'Banco', 'Tipo']
    for i in range(len(prov['Proveedor'])):
        prov.loc[i,'Clabe'] = str(prov.loc[i,'Clabe'])
    prov['Clabe'] = prov['Clabe'].astype(str)
    # Create or retrieve DataFrame from session_state
    if 'data' not in st.session_state:
        st.session_state.data = create_initial_dataframe()

    #st.write('Current DataFrame:', st.session_state.data)
    
    # Collect user input for new row
    provedores_selec = st.selectbox('Elije al proveedor', prov['Proveedor'].sort_values().unique())
    cantidades_pagar = st.number_input('Cantidad a pagar', step=1)
    tc = st.number_input('Tipo de cambio', value=1.0000, step=0.0001)
    cantidades_pagar = cantidades_pagar*tc
    fact = st.text_input('Escribe el concepto de pago')
    #col_names_banregio = ['Secuencia', 'Tipo', 'Cuenta_Destino', 'Importe', 'IVA', 'Descripcion', 'Ref_Numerica', 'Referencia']
    if st.button('Append Row'):
        # Construct a row from user input
        new_row = {'Proveedor': provedores_selec, 'Monto': cantidades_pagar, 'Facturas': fact, 'tc': tc, 'USD': cantidades_pagar/tc }
        
        # Append the new row to the DataFrame
        st.session_state.data = append_row(st.session_state.data, new_row)
        
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
            st.warning('Carga una base')
    ref_num = st.text_input('Escribe la referencia numerica')
    ref_str = st.text_input('Escribe la referencia de pagos')

    if st.checkbox('Plantilla Banregio'):
        col_names_banregio = ['Secuencia', 'Tipo', 'Cuenta_Destino', 'Importe', 'IVA', 'Descripcion', 'Ref_Numerica', 'Referencia']
        #n=len(st.session_state.data['Proveedor'])
        n=len(df_temp['Proveedor'])
        sec = list(range(n))
        tipo = ["s" for i in range(n)]
        iva = [0]*n
        ref = [ref_num for i in range(n)]
        referencia = [ref_str for i in range(n)]
        col_names_banregio = ['Secuencia', 'Tipo', 'Cuenta_Destino', 'Importe', 'IVA', 'Descripcion', 'Ref_Numerica', 'Referencia']
        data = list(zip(sec, tipo, df_temp['Clabe'], df_temp['Monto'], iva, df_temp['Facturas'], ref, referencia))
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
        #def download_link(object_to_download, download_filename, download_link_text):
        #    if isinstance(object_to_download, pd.DataFrame):
        #        object_to_download = object_to_download.to_csv(index=False, quoting=csv.QUOTE_NONNUMERIC)
        #    
        #    b64 = base64.b64encode(object_to_download.encode()).decode()
        #    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

        # Crear un enlace de descarga en Streamlit
        #st.markdown(download_link(df_banregio, 'p_banregio.csv', 'Descargar Plantilla Banregio'), unsafe_allow_html=True)
if __name__ == '__main__':
    main()
