import streamlit as st

# Imagenes
from PIL import Image
img = Image.open('logo_farmiral.jpg')
st.image(img)

#Titulos
st.title('Farmiral streamlit tutorial')

#Encabezados 
st.header('Biomiral Prueba encabezado')
st.subheader('Prueba sub encabezado')

#Texto
st.text('Esta es la primera linea a escribir de texto normal')

#Markdown, los hashtag son para aumentar fuente y negrita
st.markdown('### Probar markdown')

#Ventanas de exito, error
st.success('Exito')

st.info('Información')

st.warning('Esto es una alerta')

st.error('Esto es un error, peligro')

st.exception(NameError('name three not defined'))

#Obtener ayuda acerca de funciones
st.help(range)

#Escribir texto libre
st.write('Texto libre con st.write')

st.write(6+2)

##Video
#video_file = open("example.mp4","rb").read()
#st.video(video_file)

##Audio
#audio_file = open("example.mp3","rb").read()
#st.audio(audio_file,format='audio/mp3')

#Widget
#Checkbox
if st.checkbox("Show/Hide"):
	st.text("Showing or Hiding widget")

#Radio
status = st.radio("What is your status", ("Active", "Inactive", "Holo"))

if status == 'Active':
	st.success('You are Active')

if status == 'Inactive':
	st.warning('Be careful')

# Selectbox
ocuppation = st.selectbox("Your Ocuppation", ["Programmer", "Datascientist", "Doctor", "Bussinessman"])
st.write("Your selected this option ", ocuppation)


#Multiselect
location = st.multiselect("Where do you work?", ("London", "New York", "Accra"))
st.write("You selected",len(location),"locations")

#Slider
level = st.slider("What is your level", 1,10)

# Buttons
st.button("simple Button")

if st.button("Presioname"):
	st.text("Streamlit is cool")

#text input
firstname = st.text_input("Enter your firstname", "Type Here...")
if st.button("Guardar"):
	result = firstname.title()
	st.success(result)

#text area
message = st.text_area("Enter your firstname", "Type Here...")
if st.button("Guardar mensaje"):
	result = message.title()
	st.success(result)

#Date input
import datetime
today = st.date_input("Today is", datetime.datetime.now())

#Time
the_time = st.time_input("The time is ",datetime.time())

#Displaying JSON
st.text("Display JSON")
st.json({'name': "Jesse", 'gender': "male"})

#Display Raw Code
st.text("Display Raw Code")
st.code("import numpy as np")

#Display Raw Code
with st.echo():
	#This will also show as a comment
	import pandas as pd
	df = pd.DataFrame()

#Progress Bar

import time
my_bar = st.progress(0)
for p in range(10):
	my_bar.progress(p+1)


#Spinner
with st.spinner("Waiting .."):
	time.sleep(5)
st.success("Finished!")

#Balloons
#st.balloons()

#Sidebars
st.sidebar.header("about")
st.sidebar.text("This is Streamlit tutorial")

#Functions
@st.cache
def run_fxn():
	return range(100)

st.write(run_fxn())

#Plots
#st.pyplot()

#Dataframe
#st.dataframe(df)
#Tables
#st.table(df)
