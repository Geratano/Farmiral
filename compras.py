import pandas as pd 
import streamlit as st 
from PIL import Image
import altair as alt
import numpy as np
from datetime import datetime
import re 

def main():
    img = Image.open('logo_farmiral.jpg')
    col1, col2, col3 = st.columns([5,10,1])
    with col1:
        st.write("")
	
    with col2:
        st.image(img,width=250)
    with col3:
        st.write("")

    st.write("Esto solo es una prueba de stramlit")
if __name__ == '__main__':
    main()
