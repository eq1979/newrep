import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Earthquake Dashboard", page_icon="🌎", layout="wide")

st.title("🌎 Earthquake Dashboard")
st.write("Real-time Earthquake data from USGS")

# Fetch earthquake data from USGS API
@st.cache_data
def fetch_earthquake_data():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
    response = requests.get(url)
    data = response.json()

    features = data["features"]
    records = []
    for feature in features:
        properties = feature["properties"]
        geometry = feature["geometry"]
        if geometry and "coordinates" in geometry:
            longitude, latitude, depth = geometry["coordinates"]
            records.append({
                "place": properties["place"],
                "magnitude": properties["mag"],
                "time": pd.to_datetime(properties["time"], unit='ms'),
                "latitude": latitude,
                "longitude": longitude,
                "depth_km": depth
            })
    return pd.DataFrame(records)

# Load data
df = fetch_earthquake_data()

# Show map
st.map(df[['latitude', 'longitude']])

# Show table
st.subheader("📋 Latest Earthquake Data")
st.dataframe(df.sort_values("time", ascending=False), use_container_width=True)
