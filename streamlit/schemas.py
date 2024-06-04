# schemas.py
import pandas as pd
import plotly.express as px

# Function to extract metadata from parsed query
def extract_metadata(parsed_query, field):
    return parsed_query.get('metadata', {}).get(field)

# Function to create bar chart
def create_bar_chart(data, x_label, y_label, title):
    chart = px.bar(x=data.index, y=data.values, labels={'x': x_label, 'y': y_label}, title=title)
    return chart

# Function to process schemas and create chart
def process_schemas(parsed_queries):
    schemas = [extract_metadata(parsed_query, 'SCHEMA_NAME') for parsed_query in parsed_queries.values()]
    schema_counts = pd.Series(schemas).value_counts()
    schema_chart = create_bar_chart(schema_counts, 'Schema', 'Occurrences', 'Occurrences of Schemas')
    return schema_chart
