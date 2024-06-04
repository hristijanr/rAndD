import pandas as pd
import json
import os
import sqlglot

# Path to the CSV file containing queries
csv_file_path = '/Users/hristijanrahmanov/Downloads/selects.csv'
df = pd.read_csv(csv_file_path)

# Output directory to save parsed queries
output_directory = '/Users/hristijanrahmanov/Downloads/parsed_queries'
os.makedirs(output_directory, exist_ok=True)

# Function to save parsed query to a JSON file
def save_query_to_json(parsed_query, query_index, metadata):
    # Convert parsed query to dictionary
    if isinstance(parsed_query, dict):
        parsed_dict = parsed_query
    else:
        parsed_dict = parsed_query.__dict__

    # Include metadata
    parsed_dict['metadata'] = metadata

    # Save as JSON
    json_file_path = os.path.join(output_directory, f'query_{query_index}.json')
    with open(json_file_path, 'w') as json_file:
        json.dump(parsed_dict, json_file, indent=4, default=str)

# Extract and Parse Queries
queries = df[df.columns[0]].tolist()

# Initialize index for saving queries
saved_query_index = 0

# Loop through each query
for index, query in enumerate(queries):
    metadata = {
        "QUERY_TEXT": query,
        "DATABASE_NAME": df.loc[index, "DATABASE_NAME"],
        "SCHEMA_NAME": df.loc[index, "SCHEMA_NAME"],
        "USER_NAME": df.loc[index, "USER_NAME"],
        "ROLE_NAME": df.loc[index, "ROLE_NAME"],
        "WAREHOUSE_NAME": df.loc[index, "WAREHOUSE_NAME"],
        "TOTAL_ELAPSED_TIME": df.loc[index, "TOTAL_ELAPSED_TIME"],
        "BYTES_SCANNED": df.loc[index, "BYTES_SCANNED"],
        "CREDITS_USED_CLOUD_SERVICES": df.loc[index, "CREDITS_USED_CLOUD_SERVICES"]
    }

    if 'WHERE 1=0' in query:
        print(f"Query {index}: Skipped due to 'WHERE 1=0'")
        continue

    try:
        parsed_query = sqlglot.parse_one(query)
        save_query_to_json(parsed_query, saved_query_index, metadata)
        print(f"Query {index}: Parsed query")
        saved_query_index += 1
    except sqlglot.errors.ParseError as e:
        print(f"Error parsing query {index}: {query}")
        print(f"Error message: {e}")

print("Processing complete. Parsed queries are saved as JSON files.")
