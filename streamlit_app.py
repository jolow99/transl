# streamlit_app.py

import streamlit as st
from st_supabase_connection import SupabaseConnection
from datetime import datetime
import pandas as pd 

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = conn.query("*", table="allData", ttl="0").execute()

# Split data based on sensor
sensors_data = {}
for row in rows.data:
    sensor_id = row["sensor"]
    if sensor_id not in sensors_data:
        sensors_data[sensor_id] = []
    sensors_data[sensor_id].append(row)

# Display current moisture, temperature, and humidity of each sensor
for sensor_id, data in sensors_data.items():
    st.header(f"Sensor {sensor_id+1}")
    col1, col2, col3 = st.columns(3)
    latest = data[-1]
    
        # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Convert timestamp to datetime and set as index
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    # Current moisture, temperature, and humidity in 3 separate columns
    col1.metric("Moisture", str(round(latest["moisture"] * 100, 2)) + "%")
    col2.metric("Temperature", str(latest["temperature"]) + "°C")
    col3.metric("Humidity", str(latest["humidity"]) + "%")

    # Historical moisture, temperature, and humidity in 3 separate columns. 
    col1.line_chart(df["moisture"] * 100)
    col2.line_chart(df["temperature"])
    col3.line_chart(df["humidity"])


    # Last updated    
    st.write("Last Updated:", datetime.fromisoformat(latest["timestamp"]).strftime('%B %d, %Y, %H:%M'))


# Display raw data
st.table(rows.data)