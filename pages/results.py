import streamlit as st
import pickle
import sklearn
import pandas as pd
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


st.title ("AMR Prediction using Genotypic Data")
if st.session_state['model_type']=="":
    st.markdown("Please select a microbe type from the main page")
else:
    st.header(st.session_state['model_type'])
    st.markdown("Prediction results")

if st.session_state['data'].empty:
    st.markdown("Please upload a dataset from the main page")
else:
    
    option = st.session_state['model_type']
    if (option == 'Klebsiella pneumoniae'):
        x_final = st.session_state['data']
        x_val = st.session_state['data'].replace(['-'],'0').replace(['+'],'1')
        x_val = x_val.iloc[:,1:10].values
        x_test = x_val.astype('int')
        columns = ['IMIPENEM','MEROPENEM','DORIPENEM','CEFIDEROCOL']

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

    
    elif (option == 'Acinetobacter baumannii'):
        x_final = st.session_state['data']
        x_val = st.session_state['data'].replace(['-'],'0').replace(['+'],'1')
        x_val = x_val.iloc[:,1:16].values
        x_test = x_val.astype('int')
        columns = ['IMIPENEM','MEROPENEM','DORIPENEM']

        #IMIPENEM
        loaded_model = pickle.load(open('CRO_IMIPENEM.sav', 'rb'))
        result_imi = loaded_model.predict(x_test).astype('int')
        x_final['IMIPENEM'] = result_imi.tolist()

        #MEROPENEM
        loaded_model = pickle.load(open('CRO_MEROPENEM.sav', 'rb'))
        result_mero = loaded_model.predict(x_test)
        x_final['MEROPENEM'] = result_mero.tolist()

        #DORIPENEM
        loaded_model = pickle.load(open('CRO_DORIPENEM.sav', 'rb'))
        result_dori = loaded_model.predict(x_test)
        x_final['DORIPENEM'] = result_dori.tolist()

        x_final = x_final.replace([0],'S').replace([1],'I').replace([2],'R')

    else:
        x_final = st.session_state['data']
        x_val = st.session_state['data'].replace(['-'],'0').replace(['+'],'1')
        x_val = x_val.iloc[:,1:4].values
        x_test = x_val.astype('int')
        columns = ['IMIPENEM','MEROPENEM','DORIPENEM']

        #IMIPENEM
        loaded_model = pickle.load(open('CRPA_IMIPENEM.sav', 'rb'))
        result_imi = loaded_model.predict(x_test).astype('int')
        x_final['IMIPENEM'] = result_imi.tolist()

        #MEROPENEM
        loaded_model = pickle.load(open('CRPA_MEROPENEM.sav', 'rb'))
        result_mero = loaded_model.predict(x_test)
        x_final['MEROPENEM'] = result_mero.tolist()

        #DORIPENEM
        loaded_model = pickle.load(open('CRPA_DORIPENEM.sav', 'rb'))
        result_dori = loaded_model.predict(x_test)
        x_final['DORIPENEM'] = result_dori.tolist()

        x_final = x_final.replace([0],'S').replace([1],'I').replace([2],'R')
     

    tab1, tab2 = st.tabs(["Table", "Graph"])
    with tab1: 
        tab1.subheader("Tabulated Output")
        tab1.dataframe(x_final)
        
    with tab2:
        tab2.subheader("Bar Chart of Output")
        visual_output = pd.DataFrame (columns, columns = ['Antimicrobial'])
        
        out_results = np.arange(len(columns) * 3).reshape(3, len(columns))
        for i in range (len(columns)):
            for j in range (3):
                try:
                    current = x_final[columns[i]].value_counts()[j].astype(int)
                except IndexError:
                    current = 0     
                out_results[j][i] = current
                
        visual_output['Susceptible'] = out_results[0].astype(int)
        visual_output['Intermediate'] = out_results[1].astype(int)
        visual_output['Resistant'] = out_results[2].astype(int)
        
        
        fig = px.bar(visual_output, x = 'Antimicrobial', y=['Susceptible','Intermediate','Resistant'])
        tab2.plotly_chart(fig, theme="streamlit", use_conatiner_width=True)

    result_csv = x_final.to_csv(index=False).encode('utf-8')   

    with st.container():
        st.download_button(
        label = "📥 Download result as .csv",
        data = result_csv,
        file_name = 'CRKP - Result '+date.today().strftime("%d.%m.%Y")+'.csv',
        mime='text/csv',
    )
