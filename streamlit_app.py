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
    run_prediction_app()
    

def run_prediction_app():
    st.subheader("Select pickup location")

    m = fl.Map(
        tiles="OpenStreetMap",
        zoom_start=11,
        location=[-6.1762, 106.8274],
    )
    m.add_child(fl.LatLngPopup())
    map_ny = st_folium(m, height=400, width=700)

    if map_ny["last_clicked"]:
        pickup_lat = map_ny["last_clicked"]["lat"]
        pickup_long = map_ny["last_clicked"]["lng"]

    st.subheader("Select dropoff location")

    m2 = fl.Map(
        tiles="OpenStreetMap",
        zoom_start=11,
        location=[-6.3762, 106.8274],
    )
    m2.add_child(fl.LatLngPopup())
    map_ny2 = st_folium(m2, height=400, width=700)

    if map_ny2["last_clicked"]:
        dropoff_lat = map_ny2["last_clicked"]["lat"]
        dropoff_long = map_ny2["last_clicked"]["lng"]

    if (map_ny["last_clicked"]) and (map_ny2["last_clicked"]):
        distance = haversine_array(pickup_long, pickup_lat, dropoff_long, dropoff_lat)
        st.write(f"Calculated Distance: {distance:.2f} km")

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