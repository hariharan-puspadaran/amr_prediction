import streamlit as st
import pickle
import sklearn
import pandas as pd
from datetime import date

st.title ("AMR Prediction using Genotypic Data")
st.header("Klebsiella pneumoniae")

if st.session_state['data'].empty:
    st.markdown("Please upload a dataset from the main page")
else:
     
    x_final = st.session_state['data']
    x_val = st.session_state['data'].replace(['-'],'0').replace(['+'],'1')
    x_val = x_val.iloc[:,1:10].values
    x_test = x_val.astype('int')


    #IMIPENEM
    loaded_model = pickle.load(open('IMIPENEM.sav', 'rb'))
    result_imi = loaded_model.predict(x_test).astype('int')
    x_final['IMIPENEM'] = result_imi.tolist()

    #MEROPENEM
    loaded_model = pickle.load(open('MEROPENEM.sav', 'rb'))
    result_mero = loaded_model.predict(x_test)
    x_final['MEROPENEM'] = result_mero.tolist()

    #DORIPENEM
    loaded_model = pickle.load(open('DORIPENEM.sav', 'rb'))
    result_dori = loaded_model.predict(x_test)
    x_final['DORIPENEM'] = result_dori.tolist()

    #CEFIDEROCOL
    loaded_model = pickle.load(open('CEFIDEROCOL.sav', 'rb'))
    result_cefi= loaded_model.predict(x_test)
    x_final['CEFIDEROCOL'] = result_cefi.tolist()

    x_final = x_final.replace([0],'S').replace([1],'I').replace([2],'R')
    # st.dataframe(x_final)
    st.dataframe(x_final)
    result_csv = x_final.to_csv(index=False).encode('utf-8')

    with st.container():
        st.download_button(
        label = "📥 Download result as .csv",
        data = result_csv,
        file_name = 'CRKP - Result '+date.today().strftime("%d.%m.%Y")+'.csv',
        mime='text/csv',
    )
