from google.cloud import bigquery
import pandas as pd
import matplotlib.pyplot as plt


# Set the path to your service account key JSON file
credentials_path = "C:\\Users\\Karthik\\p1_project\\json_con.json"

# Create a BigQuery client
client = bigquery.Client.from_service_account_json(credentials_path)
project_id = 'theta-cell-406519'
dataset_name = 'karthik_rev_stox'  # Replace with your dataset name

# Define your BigQuery datasets and tables
hdfc_table = f'{project_id}.{dataset_name}.hdfc'
wipro_table = f'{project_id}.{dataset_name}.wipro'

# Perform the BigQuery queries

# 1. hdfc
q1 = f"SELECT Date, Volume FROM {hdfc_table}"
q2 = f"SELECT Date, COUNT(*) AS num_trades FROM {hdfc_table} GROUP BY Date"
q3 = f"SELECT Date, volume, close FROM {hdfc_table} ORDER BY Date"
q4 = f"SELECT AVG(VWAP) AS avg_vwap FROM {hdfc_table}"
q5 = f"SELECT Date, SUM(turnover) AS daily_turnover FROM {hdfc_table} GROUP BY Date"

# 2. wipro
q6 = f"SELECT Date, Volume FROM {wipro_table}"
q7 = f"SELECT Date, COUNT(*) AS num_trades FROM {wipro_table} GROUP BY Date"
q8 = f"SELECT Date, volume, close FROM {wipro_table} ORDER BY Date"
q9 = f"SELECT AVG(VWAP) AS avg_vwap FROM {wipro_table}"
q10 = f"SELECT Date, SUM(turnover) AS daily_turnover FROM {wipro_table} GROUP BY Date"

# Fetch results from BigQuery
q1_result = client.query(q1).to_dataframe()
q2_result = client.query(q2).to_dataframe()
q3_result = client.query(q3).to_dataframe()
q4_result = client.query(q4).to_dataframe()
q5_result = client.query(q5).to_dataframe()

q6_result = client.query(q6).to_dataframe()
q7_result = client.query(q7).to_dataframe()
q8_result = client.query(q8).to_dataframe()
q9_result = client.query(q9).to_dataframe()
q10_result = client.query(q10).to_dataframe()

# Data Visualization
# Similar to your existing code for pandas visualization
# Convert 'date' column to datetime format
q1_result['Date'] = pd.to_datetime(q1_result['Date'])
q6_result['Date'] = pd.to_datetime(q6_result['Date'])

q1_yearly = q1_result.groupby(q1_result['Date'].dt.year)['Volume'].mean()
q2_yearly = q6_result.groupby(q6_result['Date'].dt.year)['Volume'].mean()

plt.figure(figsize=(10, 6))
plt.plot(q1_yearly.index, q1_yearly.values, label='HDFC', marker='o', linestyle='-', linewidth=2)
plt.plot(q2_yearly.index, q2_yearly.values, label='WIPRO', marker='o', linestyle='-', linewidth=2)

plt.xlabel('Year')
plt.ylabel('Average Volume')
plt.title('Relationship between Year and Average Volume')
plt.legend()
plt.grid(True)
plt.show()
