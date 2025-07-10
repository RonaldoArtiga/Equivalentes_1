# app.py
import streamlit as st
import pandas as pd
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976

# Cargar datos
pantone = pd.read_csv("pantone.csv")
linea = pd.read_csv("abanico_linea.csv")
ambiance = pd.read_csv("abanico_ambiance.csv")
sensations = pd.read_csv("abanico_sensations.csv")
comex = pd.read_csv("comex.csv")
lanco = pd.read_csv("lanco.csv")
sherwin = pd.read_csv("sherwin.csv")

# Unir todos los catálogos externos en un solo DataFrame
catalogos_externos = pd.concat([
    pantone.rename(columns={"name": "name", "hex": "hex"}).assign(source="Pantone"),
    comex,
    lanco,
    sherwin
], ignore_index=True)

# Funciones

def hex_to_lab(hex_color):
    rgb = sRGBColor.new_from_rgb_hex(hex_color)
    lab = convert_color(rgb, LabColor)
    return lab

def encontrar_mas_cercano(hex_input, abanico):
    color_input_lab = hex_to_lab(hex_input)
    menor_delta = float("inf")
    mejor_color = None

    for _, row in abanico.iterrows():
        try:
            color_ab_hex = "#" + row["hexadecimal"].strip().lower()
            color_ab_lab = hex_to_lab(color_ab_hex)
            delta = delta_e_cie1976(color_input_lab, color_ab_lab)
            if delta < menor_delta:
                menor_delta = delta
                mejor_color = row
        except:
            continue

    return mejor_color

# Interfaz Streamlit
st.title("Buscador de equivalencia de color")
st.write("Ingresa un color en formato HEX o selecciona uno de los catálogos externos para obtener su equivalencia en tus abanicos.")

col1, col2 = st.columns(2)

with col1:
    hex_input = st.text_input("Ingresa código HEX:", value="#ffffff")
    if st.button("Buscar equivalencia por HEX"):
        resultado_linea = encontrar_mas_cercano(hex_input, linea)
        resultado_ambiance = encontrar_mas_cercano(hex_input, ambiance)
        resultado_sensations = encontrar_mas_cercano(hex_input, sensations)

        st.markdown(f"### Color de entrada")
        st.color_picker("", hex_input, label_visibility="collapsed")

        st.markdown("### Coincidencias:")

        st.subheader("Línea")
        st.color_picker("Color", "#" + resultado_linea["hexadecimal"], label_visibility="collapsed")
        st.write(f"**{resultado_linea['nombre']}** - {resultado_linea['codigo']} - {resultado_linea['cartilla']}")

        st.subheader("Ambiance")
        st.color_picker("Color", "#" + resultado_ambiance["hexadecimal"], label_visibility="collapsed")
        st.write(f"**{resultado_ambiance['nombre']}** - {resultado_ambiance['codigo']} - {resultado_ambiance['cartilla']}")

        st.subheader("Sensations")
        st.color_picker("Color", "#" + resultado_sensations["hexadecimal"], label_visibility="collapsed")
        st.write(f"**{resultado_sensations['codigo']}** - {resultado_sensations['cartilla']}")

with col2:
    opciones = catalogos_externos["name"].fillna(catalogos_externos["code"]).dropna().unique()
    seleccion = st.selectbox("Selecciona un color de catálogo externo:", sorted(opciones))

    if st.button("Buscar equivalencia por catálogo"):
        color_row = catalogos_externos[
            (catalogos_externos["name"] == seleccion) | (catalogos_externos["code"] == seleccion)
        ].iloc[0]
        hex_input = color_row["hex"]

        resultado_linea = encontrar_mas_cercano(hex_input, linea)
        resultado_ambiance = encontrar_mas_cercano(hex_input, ambiance)
        resultado_sensations = encontrar_mas_cercano(hex_input, sensations)

        st.markdown(f"### Color seleccionado: {seleccion}")
        st.color_picker("", hex_input, label_visibility="collapsed")

        st.markdown("### Coincidencias:")

        st.subheader("Línea")
        st.color_picker("Color", "#" + resultado_linea["hexadecimal"], label_visibility="collapsed")
        st.write(f"**{resultado_linea['nombre']}** - {resultado_linea['codigo']} - {resultado_linea['cartilla']}")

        st.subheader("Ambiance")
        st.color_picker("Color", "#" + resultado_ambiance["hexadecimal"], label_visibility="collapsed")
        st.write(f"**{resultado_ambiance['nombre']}** - {resultado_ambiance['codigo']} - {resultado_ambiance['cartilla']}")

        st.subheader("Sensations")
        st.color_picker("Color", "#" + resultado_sensations["hexadecimal"], label_visibility="collapsed")
        st.write(f"**{resultado_sensations['codigo']}** - {resultado_sensations['cartilla']}")