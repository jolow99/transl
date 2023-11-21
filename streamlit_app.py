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

# Pump Controls
st.header("Manual Pump Controls")

# Display current pump status
pump_statuses = conn.query("*", table="sprinkler", ttl="0").execute().data
# sort based on sensor number to ensure it always displays in the same order
pump_statuses = sorted(pump_statuses, key=lambda k: k['sensor_num'])

for status in pump_statuses: 
    pump_status = status["instruct"]
    sensor_num = status["sensor_num"]
    if pump_status:
        st.text(f"Pump {sensor_num} is currently switched on.")
        if st.button("Turn Pump Off", key=sensor_num):
            conn.table('sprinkler').update({"instruct": False}).filter("sensor_num", "eq", sensor_num ).execute()
            st.rerun()
    else:
        st.text(f"Pump {sensor_num} is currently switched off.")
        if st.button("Turn Pump On", key=sensor_num):
            conn.table('sprinkler').update({"instruct": True}).filter("sensor_num", "eq", sensor_num ).execute()
            st.rerun()

# Display raw data
st.table(rows.data)