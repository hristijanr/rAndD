import os
import json
import streamlit as st
from schemas import process_schemas
from usernames import process_usernames
from tables import process_tables
from warehouses import process_warehouses

# fun for loading parsed queries from JSON files
def load_parsed_queries(directory):
    parsed_queries = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                parsed_query = json.load(file)
                parsed_queries[filename] = parsed_query
    return parsed_queries

# Directory with te parsed queries
parsed_queries_directory = '/Users/hristijanrahmanov/Downloads/parsed_queries'

# Loading parsed queries
parsed_queries = load_parsed_queries(parsed_queries_directory)

# max items to be displayed
max_bars = st.sidebar.slider('Max number of items to display:', min_value=10, max_value=50, value=20)

# Creating charts
schema_chart = process_schemas(parsed_queries)
username_chart = process_usernames(parsed_queries)
table_chart = process_tables(parsed_queries, max_bars=max_bars)
warehouse_chart = process_warehouses(parsed_queries, max_bars=max_bars)

# Creating navigation bar
st.sidebar.title('Navigation')
selected_chart = st.sidebar.radio('Go to:', ['Schemas', 'Usernames', 'Tables', 'Warehouses'])

# Display charts
if selected_chart == 'Schemas':
    st.title('Occurrences of Schemas')
    st.plotly_chart(schema_chart)
elif selected_chart == 'Usernames':
    st.title('Occurrences of Usernames')
    st.plotly_chart(username_chart)
elif selected_chart == 'Tables':
    st.title('Occurrences of Tables')
    st.plotly_chart(table_chart)
elif selected_chart == 'Warehouses':
    st.title('Occurrences of Warehouses')
    st.plotly_chart(warehouse_chart)


# Copyright footer
footer_text = "\u00A9 BlueCloud"

# Display footer
st.markdown(f'<p style="text-align:center; color:gray;">{footer_text}</p>', unsafe_allow_html=True)
