import pandas as pd


def load_data():
    file_path = "data/ICE DB Advanced V4.0 - Dec 2024.xlsx"  # relative path in your repo
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name="ICE_Tabular")
    df = pd.read_excel(xls, sheet_name='ICE_Tabular', skiprows=2)
    df_clean = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df_clean

def calculate_embodied_carbon(df, material, area, thickness):
    material_data = df[df["Material"] == material]
    carbon_per_kg = material_data["Embodied Carbon per kg (kg CO2e per kg)"].iloc[0]
    density = material_data["Density of material - kg per m3"].iloc[0]

    volume = area * thickness
    mass = volume * density
    embodied_carbon = mass * carbon_per_kg
    return round(embodied_carbon, 2)

def suggest_alternative_with_density(material, df, density_tolerance=0.3, top_n=5):
    # 1️⃣ Find the density range of the selected material
    selected_row = df[df['Material'] == material].iloc[0]
    selected_density = selected_row['Density of material - kg per m3']

    # 2️⃣ Calculate density bounds for realistic substitution
    lower_bound = selected_density * (1 - density_tolerance)
    upper_bound = selected_density * (1 + density_tolerance)

    # 3️⃣ Filter for materials with density in this range
    similar_density_df = df[
        (df['Density of material - kg per m3'] >= lower_bound) &
        (df['Density of material - kg per m3'] <= upper_bound)
    ]

    # 4️⃣ Sort by embodied carbon
    sorted_df = similar_density_df.sort_values('Embodied Carbon per kg (kg CO2e per kg)')

    # 5️⃣ Return top_n alternatives
    return sorted_df[['Material', 'Embodied Carbon per kg (kg CO2e per kg)', 'Density of material - kg per m3']].head(top_n)
