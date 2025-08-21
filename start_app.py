import streamlit as st

st.title('스티림릿 안녕하세요')
st.write('Hello, streamlit!')
name = st.text_input('이름:')
if name : 
    st.write(f'안녕하세요... {name}님')
    
st.divider()

import pandas as pd
df = pd.read_csv('./data/ABNB_stock.csv')
df