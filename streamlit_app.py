import streamlit as st
import pickle
import numpy as np
import folium as fl
from streamlit_folium import st_folium
from folium import Popup

with open('ModeloRL.pkl', 'rb') as file:
    ModeloRL = pickle.load(file)
    
with open('Padronizador.pkl', 'rb') as file:
    Padronizador = pickle.load(file)

def main():
    st.title("Coordinate Input Boxes with Change Tracking")

    # Initialize session state to track changes
    if "coordinates" not in st.session_state:
        st.session_state["coordinates"] = {
            "x1": 0.0, "y1": 0.0, "x2": 0.0, "y2": 0.0,
            "x3": 0.0, "y3": 0.0, "x4": 0.0, "y4": 0.0
        }

    # Function to check changes
    def check_changes(key, new_value):
        if st.session_state["coordinates"][key] != new_value:
            st.write("### Current Coordinates:")
            for key, value in st.session_state["coordinates"].items():
                st.write(f"{key.upper()}: {value}")

    # First Row
    st.subheader("First Row")
    col1_row1, col2_row1 = st.columns(2)
    with col1_row1:
        x1 = st.number_input("X1 (First Row, Col 1)", value=st.session_state["coordinates"]["x1"], key="x1", on_change=check_changes, args=("x1", st.session_state.get("x1")))
        y1 = st.number_input("Y1 (First Row, Col 1)", value=st.session_state["coordinates"]["y1"], key="y1", on_change=check_changes, args=("y1", st.session_state.get("y1")))

    with col2_row1:
        x2 = st.number_input("X2 (First Row, Col 2)", value=st.session_state["coordinates"]["x2"], key="x2", on_change=check_changes, args=("x2", st.session_state.get("x2")))
        y2 = st.number_input("Y2 (First Row, Col 2)", value=st.session_state["coordinates"]["y2"], key="y2", on_change=check_changes, args=("y2", st.session_state.get("y2")))

    # Second Row
    st.subheader("Second Row")
    col1_row2, col2_row2 = st.columns(2)
    with col1_row2:
        x3 = st.number_input("X3 (Second Row, Col 1)", value=st.session_state["coordinates"]["x3"], key="x3", on_change=check_changes, args=("x3", st.session_state.get("x3")))
        y3 = st.number_input("Y3 (Second Row, Col 1)", value=st.session_state["coordinates"]["y3"], key="y3", on_change=check_changes, args=("y3", st.session_state.get("y3")))

    with col2_row2:
        x4 = st.number_input("X4 (Second Row, Col 2)", value=st.session_state["coordinates"]["x4"], key="x4", on_change=check_changes, args=("x4", st.session_state.get("x4")))
        y4 = st.number_input("Y4 (Second Row, Col 2)", value=st.session_state["coordinates"]["y4"], key="y4", on_change=check_changes, args=("y4", st.session_state.get("y4")))

    # Display the entered coordinates
    if st.button('Predict Fare'):
        try:
            distance = Padronizador.transform([[distance]])
            fare_pred = ModeloRL.predict(distance)
            st.write(f"Predicted Fare: ${fare_pred[0]:.2f}")
        except:
            st.write("Please select pickup and dropoff location first.")

def haversine_array(pickup_long, pickup_lat, dropoff_long, dropoff_lat):
    pickup_long, pickup_lat, dropoff_long, dropoff_lat = map(lambda x: x/360.*(2*np.pi), [pickup_long, pickup_lat, dropoff_long, dropoff_lat])
    dlon = dropoff_long - pickup_long
    dlat = dropoff_lat - pickup_lat
    a = np.sin(dlat/2)**2 + np.cos(pickup_lat) * np.cos(dropoff_lat) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km

if __name__ == "__main__":
    main()