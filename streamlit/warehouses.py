import pandas as pd
import plotly.express as px


# Function to create bar chart
def create_bar_chart(data, x_label, y_label, title, max_bars=20):
    data = data.sort_values().tail(max_bars)  # Get the top N items
    chart = px.bar(data, x=data.values, y=data.index, orientation='h',
                   labels={'x': x_label, 'y': y_label}, title=title)
    chart.update_layout(yaxis=dict(tickmode='linear', tickfont=dict(size=10)),
                        height=600, margin=dict(l=200))
    return chart


# Function to process warehouses and create chart
def process_warehouses(parsed_queries, max_bars=20):
    warehouses = [parsed_query.get('metadata', {}).get('WAREHOUSE_NAME') for parsed_query in parsed_queries.values() if
                  'metadata' in parsed_query and 'WAREHOUSE_NAME' in parsed_query['metadata']]

    warehouse_counts = pd.Series(warehouses).value_counts()
    warehouse_chart = create_bar_chart(warehouse_counts, 'Occurrences', 'Warehouse', 'Occurrences of Warehouses',
                                       max_bars)
    return warehouse_chart