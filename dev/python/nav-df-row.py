import streamlit as st
import pandas as pd  
# initialize list of lists
data = {'col1': [1, 2, 3, 4], 'col2': [300, 400, 500, 600]}  
# Create the pandas DataFrame
df = pd.DataFrame(data) 
# print dataframe.
st.dataframe(df)

# Using Session State for pagination
# from example - https://github.com/streamlit/release-demos/blob/0.84/0.84/demos/pagination.py
if "record_index" not in st.session_state:
    st.session_state.record_index = 0

def next_record():
    st.session_state.record_index += 1

def prev_record():
    st.session_state.record_index -= 1

c_prev, c_next = st.columns(2)

with c_prev:
    if st.session_state.record_index > 0:
        st.button("< Prev", on_click=prev_record)
    else:
        st.write("") 

with c_next:
    if st.session_state.record_index < len(df.index)-1:
        st.button("Next >", on_click=next_record)
    else:
        st.write("") 

df_selected = df.iloc[st.session_state.record_index]
st.write(df_selected)