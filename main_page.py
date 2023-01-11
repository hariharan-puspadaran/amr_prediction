
import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

st.title ("AMR Prediction using Genotypic Data")
st.header("Klebsiella pneumoniae")
with st.container():
    st.markdown("Below is a template of the data spreadsheet")
    df = pd.read_csv("CRKP - Template.csv")
    template_csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
    label = "📥 Press to Download Template",
    data = template_csv,
    file_name = 'CRKP - Template.csv',
    mime='text/csv',
    )

st.header("Upload the spreadsheet with data to be classified")

import streamlit as st
import os.path
import pathlib

uploaded_file = st.file_uploader("Choose a CSV file",type=['csv'],)
if uploaded_file is not None:
    new_df = pd.read_csv(uploaded_file)
    prev_df = new_df.head(5)
    st.markdown("Preview of uploaded csv file")
    st.dataframe(prev_df)

from streamlit_extras.switch_page_button import switch_page

if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame()
    
submit = st.button("Submit")
if submit:
    st.session_state['data'] = new_df
    switch_page("results")

# st.caption("this is the caption")
# st.code("x=2021")
# st.latex(r''' a+a r^1+a r^2+a r^3 ''')

