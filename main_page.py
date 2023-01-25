
import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

st.title ("AMR Prediction using Genotypic Data")

if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame()
if 'model_type' not in st.session_state:
    st.session_state['model_type'] = ""
#Section for users to choose the type of microbe to evaluate
option =""
option = st.selectbox('Microbe Species: ',('Klebsiella pneumoniae', 'Acinetobacter baumannii', 'Pseudomonas aeruginosa')) 
st.header(option)
with st.container():
    st.markdown("Please use the csv file below as a baseline structure to tabulate your data. The columnns represent the list of genes to be tested in this species.")
    template_name = str(option)+" - Template.csv"
    df = pd.read_csv(template_name)
    template_csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
    label = "📥 Press to Download Template",
    data = template_csv,
    file_name = template_name,
    mime='text/csv',
    )

st.header("Upload the spreadsheet with data to be classified")

def check_csv(df, option):
    if (option == 'Klebsiella pneumoniae'):
        if {'NDM','VIM','OXA','KPC','IMP','TEM','SHV','AmpC','CTX-M-1'}.issubset(df.columns):
            return True
        else:
            return False
    elif(option == 'Acinetobacter baumannii'):
        if {'CTXM 1','CTXM 2','CTXM 9','GES','IMP','NDM','Oxa 23','Oxa 24','Oxa 51','Oxa 58','PER','SHV','SIM1','TEM','VEB','VIM'}.issubset(df.columns):
            return True
        else:
            return False
    else:
        if {'ampC','IMP','VIM'}.issubset(df.columns):
            return True
        else:
            return False
        
    
def geterrors(dfObj, value):
    col_list = []
    row_list = []
    results = dfObj.isin([value])
    check_list = results.any()
    col_names = list(check_list[check_list == True].index)
    
    for here in col_names:
        rows = list(results[here][results[here] == True].index)
        for row in rows:
            col_list.append(here)
            row_list.append(dfObj._get_value(row, 'Strain label'))
            
    return col_list, row_list

uploaded_file = st.file_uploader("Choose a CSV file",type=['csv'],)
if uploaded_file is not None:
    new_df = pd.read_csv(uploaded_file)
    checker = check_csv(new_df,option)
    if checker:
        val_holder = new_df.loc[:, new_df.columns != 'Strain label'].values
        temp = val_holder[val_holder != '+']
        answer = temp[temp != '-']
        if answer.any():
            unique_err = list(set(answer))
            checker = False
            for i in range(len(unique_err)):
                column, row = geterrors(new_df, unique_err[i])
                for j in range(len(row)):
                    output_warning = "Invalid value at Strain Label: " + str(row[j]) + " and Column: " + str(column[j])
                    st.markdown(output_warning)
        if checker:         
            prev_df = new_df.head(5)
            st.markdown("Preview of uploaded csv file")
            st.dataframe(prev_df)
            
        if checker:
            submit = st.button("Submit")
            if submit:
                st.session_state['data'] = new_df
                st.session_state['model_type'] = option
                switch_page("results")
    else:
        st.markdown("Invalid File. Please make sure the corect template file was used to record the data")

# if 'data' not in st.session_state:
#     st.session_state['data'] = pd.DataFrame()
# if checker:
#     submit = st.button("Submit")
#     if submit:
#         st.session_state['data'] = new_df
#         switch_page("results")

    
# st.caption("this is the caption")
# st.code("x=2021")
# st.latex(r''' a+a r^1+a r^2+a r^3 ''')

