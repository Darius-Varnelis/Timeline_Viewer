import streamlit as st
import folium
from folium.plugins import HeatMap
from datetime import datetime, timezone
from streamlit_folium import st_folium
from collections import Counter
import json, math
from AVL_Implementation import importing_data, interval, min_time, max_time
st.set_page_config(
    page_title="Timeline visualization",
    layout="wide",
    page_icon="🗺️"
)
st.title("Google Maps Timeline Visualization")

# File upload
use_demo = st.button("Use Demo")
file = st.file_uploader("Upload JSON", type=["json"])

if use_demo:
    if st.session_state.get("last_file") != "demoTimeline.json":
        with st.spinner("Parsing data..."):
            with open("demoTimeline.json") as f:
                st.session_state.root = importing_data(json.load(f))
        st.session_state.last_file = "demoTimeline.json"
elif file:
    if st.session_state.get("last_file") != file.name:
        with st.spinner("Parsing data..."):
            st.session_state.root = importing_data(json.load(file))
        st.session_state.last_file = file.name


root = st.session_state.get("root")

if root:
    startDate = datetime.combine(
        st.date_input("Start date", min_value=min_time(root), max_value=max_time(root)),
        datetime.min.time(),
        tzinfo=timezone.utc
    )
    endDate = datetime.combine(
        st.date_input("End date", min_value=min_time(root), max_value=max_time(root)),
        datetime.max.time(),
        tzinfo=timezone.utc
    )
    choice = st.selectbox("Map type", ["HeatMap", "PolyLine"])

    if st.button("Generate map"):
        with st.spinner("Generating map..."):
            points = interval(root, startDate, endDate)
        if not points:
            st.error("No data found for the selected date range.")
        else:
            m = folium.Map(location=points[0], zoom_start=10)
            if choice == "HeatMap":
                counts = Counter((round(p[0], 4), round(p[1], 4)) for p in points)
                weighted = [[lat, lng, math.log1p(n)] for (lat, lng), n in counts.items()]
                HeatMap(weighted, radius=15, blur=10).add_to(m)
            elif choice == "PolyLine":
                folium.PolyLine(points, color="blue", weight=2).add_to(m)
            st.session_state.map = m
            st.session_state.map_generated = True

    if st.session_state.get("map_generated"):
        st_folium(st.session_state.map, width=700, height=500, returned_objects=[])