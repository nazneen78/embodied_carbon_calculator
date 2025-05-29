import streamlit as st
import pandas as pd
from data_utils import load_data, calculate_embodied_carbon, suggest_alternative_with_density

st.title("Embodied Carbon Calculator App")

df = load_data()
st.write("Data Loaded. Preview:", df.head(2))

material = st.selectbox("Select Material", df["Material"].unique())
area = st.number_input("Surface Area (m²)", min_value=0.0, step=0.1)
thickness = st.number_input("Thickness (m)", min_value=0.0, step=0.01)


if st.button("Calculate"):
    result = calculate_embodied_carbon(df, material, area, thickness)
    st.write(f"Embodied Carbon: {result} kg CO2e")

    alternative = suggest_alternative_with_density(material, df)
    st.write("Recommended Lower-Carbon Alternative:", alternative)
