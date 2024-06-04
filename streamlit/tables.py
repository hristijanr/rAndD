import re
import pandas as pd
import plotly.express as px


# Function to extract metadata from parsed query
def extract_metadata(parsed_query, field):
    return parsed_query.get('metadata', {}).get(field)


# Function to create bar chart
def create_bar_chart(data, x_label, y_label, title, max_bars=20):
    data = data.sort_values().tail(max_bars)  # Get the top N tables
    chart = px.bar(data, x=data.index, y=data.values,
                   labels={'x': x_label, 'y': y_label}, title=title)
    chart.update_layout(xaxis=dict(title=y_label, tickmode='linear', tickfont=dict(size=10)),
                        yaxis=dict(title=x_label),
                        width=800, height=600, margin=dict(b=200))
    return chart



# Function to extract table names from SQL queries
def extract_table_names(queries):
    table_names = []
    for query in queries:
        # Match table names after FROM keyword
        matches = re.findall(r'FROM\s+([a-zA-Z0-9_\.]+)', query, re.IGNORECASE)
        table_names.extend(matches)

        # Match table names after JOIN keyword
        join_matches = re.findall(r'JOIN\s+([a-zA-Z0-9_\.]+)', query, re.IGNORECASE)
        table_names.extend(join_matches)

    return table_names


# Function to process tables and create chart
def process_tables(parsed_queries, max_bars=20):
    queries = [extract_metadata(parsed_query, 'QUERY_TEXT') for parsed_query in parsed_queries.values()]
    table_names = extract_table_names(queries)

    table_counts = pd.Series(table_names).value_counts()
    table_chart = create_bar_chart(table_counts, 'Occurrences', 'Table', 'Occurrences of Tables', max_bars)
    return table_chart
