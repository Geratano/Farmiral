import streamlit as st
import pandas as pd
from PIL import Image

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

    # Create or retrieve DataFrame from session_state
    if 'data' not in st.session_state:
        st.session_state.data = create_initial_dataframe()

    #st.write('Current DataFrame:', st.session_state.data)
    
    # Collect user input for new row
    provedores_selec = st.selectbox('Elije al proveedor', prov['Proveedor'].sort_values().unique())
    cantidades_pagar = st.number_input('Cantidad a pagar', step=1)
    tc = st.number_input('Tipo de cambio', value=1.00, step=0.01)
    cantidades_pagar = cantidades_pagar*tc
    fact = st.text_input('Escribe el concepto de pago')
    
    #col_names_banregio = ['Secuencia', 'Tipo', 'Cuenta_Destino', 'Importe', 'IVA', 'Descripcion', 'Ref_Numerica', 'Referencia']
    if st.button('Append Row'):
        # Construct a row from user input
        new_row = {'Proveedor': provedores_selec, 'Monto': cantidades_pagar, 'Facturas': fact }
        
        # Append the new row to the DataFrame
        st.session_state.data = append_row(st.session_state.data, new_row)
        
        st.success('Row appended successfully!')

    st.write('Validacion:', st.session_state.data)
    monto_pago = st.session_state.data['Monto'].sum()
    frase_val = 'Monto total de solicitud de pagos $ ' + str(round(monto_pago))
    st.info(frase_val, icon='💵')
    #st.write(st.session_state.data['Proveedor'])
    df_temp = st.session_state.data.merge(prov, on='Proveedor', how='left')
    ref_num = st.text_input('Escribe la referencia numerica')
    ref_str = st.text_input('Escribe la referencia de pagos')
    
    if st.checkbox('Plantilla Banregio'):
        col_names_banregio = ['Secuencia', 'Tipo', 'Cuenta_Destino', 'Importe', 'IVA', 'Descripcion', 'Ref_Numerica', 'Referencia']
        n=len(st.session_state.data['Proveedor'])
        sec = list(range(n))
        tipo = ["s" for i in range(n)]
        iva = [0]*n
        ref = [ref_num for i in range(n)]
        referencia = [ref_str for i in range(n)]
        col_names_banregio = ['Secuencia', 'Tipo', 'Cuenta_Destino', 'Importe', 'IVA', 'Descripcion', 'Ref_Numerica', 'Referencia']
        data = list(zip(sec, tipo, df_temp['Clabe'], df_temp['Monto'], iva, df_temp['Facturas'], ref, referencia))
        df_banregio = pd.DataFrame(data, columns=col_names_banregio)
        st.write(df_banregio)     

if __name__ == '__main__':
    main()
