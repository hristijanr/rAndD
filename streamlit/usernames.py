# usernames.py
import pandas as pd
import plotly.express as px

# Function to extract metadata from parsed query
def extract_metadata(parsed_query, field):
    return parsed_query.get('metadata', {}).get(field)

# Function to create bar chart
def create_bar_chart(data, x_label, y_label, title):
    chart = px.bar(x=data.index, y=data.values, labels={'x': x_label, 'y': y_label}, title=title)
    return chart

# Function to process usernames and create chart
def process_usernames(parsed_queries):
    usernames = [extract_metadata(parsed_query, 'USER_NAME') for parsed_query in parsed_queries.values()]
    username_counts = pd.Series(usernames).value_counts()
    username_chart = create_bar_chart(username_counts, 'Username', 'Occurrences', 'Occurrences of Usernames')
    return username_chart
