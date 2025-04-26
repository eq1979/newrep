import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests

st.set_page_config(page_title="Earthquake Correlation Dashboard", page_icon="🌎", layout="wide")
st.title("🌎 Earthquake Correlation Dashboard")
st.write("Analyze relationships between earthquake features")

@st.cache_data
def fetch_earthquake_data():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
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

st.subheader("📊 Raw Earthquake Data")
st.dataframe(df)

st.subheader("📈 Correlation Analysis")

# Choose columns for correlation
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

if len(numeric_cols) >= 2:
    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)
else:
    st.warning("Not enough numeric data to compute correlations.")
