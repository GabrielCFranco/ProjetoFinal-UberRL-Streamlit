import streamlit as st
import pickle
import numpy as np

# Load the trained model and scaler
with open('ModeloRL.pkl', 'rb') as file:
    ModeloRL = pickle.load(file)
    
with open('Padronizador.pkl', 'rb') as file:
    Padronizador = pickle.load(file)

def main():
    st.title("Previsão do preço do Uber")
    
    # Input for pickup coordinates
    st.subheader("Insira a coordenada incial")
    latitude1 = st.number_input("Latitude inicial", value=0.0, format="%.6f")
    longitude1 = st.number_input("Longitude inicial", value=0.0, format="%.6f")
    
    # Input for dropoff coordinates
    st.subheader("Insira a coordenada final")
    latitude2 = st.number_input("Latitude final", value=0.0, format="%.6f")
    longitude2 = st.number_input("Longitude final", value=0.0, format="%.6f")
    
    # Calculate the distance
    if st.button("Calcula a Distância"):
        distance = haversine_array(longitude1, latitude1, longitude2, latitude2)
        st.write(f"Distância Calculada: {distance:.2f} km")
    
    # Predict the fare
    if st.button('Previsão de Preço'):
        try:
            distance = haversine_array(longitude1, latitude1, longitude2, latitude2)
            distance_scaled = Padronizador.transform([[distance]])
            fare_pred = ModeloRL.predict(distance_scaled)
            st.write(f"Previsão de Preço: ${fare_pred[0]:.2f}")
        except Exception as e:
            st.write("Error:", e)
            st.write("Insira coordenadas válidas")

# Function to calculate distance using the haversine formula
def haversine_array(longitude1, latitude1, longitude2, latitude2):
    # Convert degrees to radians
    longitude1, latitude1, longitude2, latitude2 = map(
        lambda x: x / 360.0 * (2 * np.pi), 
        [longitude1, latitude1, longitude2, latitude2]
    )
    # Calculate differences
    dlon = longitude2 - longitude1
    dlat = latitude2 - latitude1
    # Haversine formula
    a = np.sin(dlat / 2) ** 2 + np.cos(latitude1) * np.cos(latitude2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    # Earth's radius in kilometers
    km = 6367 * c
    return km

if __name__ == "__main__":
    main()
