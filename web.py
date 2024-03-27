import streamlit as st
# in terminal run command: "streamlit run web.py" to run the web app

import functions

all_todos_list = functions.get_todos()

# The components below will be shown by order on the webpage
st.title("To-Do App")
st.subheader("This is a simple To-Do app")
st.write("This app is to increase your productivity.")

for todo in all_todos_list:
    st.checkbox(todo)

st.text_input(label="", placeholder="Enter a new to-do item...")
