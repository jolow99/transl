# streamlit_app.py

import streamlit as st
from st_supabase_connection import SupabaseConnection

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = conn.query("*", table="allData", ttl="0").execute()
latest = rows.data[-1]

# Display current moisture, temperature, and humidity.
col1, col2, col3 = st.columns(3)
col1.metric("Moisture", str(latest["moisture"] * 100 ) + "%")
col2.metric("Temperature", str(latest["temperature"]) + "°C")
col3.metric("Humidity", str(latest["humidity"]) + "%")


# Display raw data
st.table(rows.data)