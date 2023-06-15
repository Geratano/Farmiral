import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import altair as alt
from datetime import datetime
from colorama import init,Fore,Back,Style

def main():
    img = Image.open('logo_farmiral.jpg')
    col1, col2, col3 = st.columns([5,10,1])
    with col1:
        st.write("")
	
    with col2:
        st.image(img,width=250)
    with col3:
        st.write("")
    df = pd.read_excel('')
	    
if __name__ == '__main__':
    main()
  



