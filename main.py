import pandas as pd
import streamlit as st
from Manip_arch import *
from procesamiento import *

st.title("Procesador de validaciones")

uploaded_file = st.file_uploader("Sube el archivo aquí", type="csv")
cant_viajes=st.text_input("Indicar el filtro de validaciones por tarjeta en un día",key=6)
df_validaciones,name_archivo=importar_csv(uploaded_file)

if df_validaciones is not None:
    st.success(f"Archivo '{name_archivo}.csv' cargado correctamente.")
    st.dataframe(df_validaciones)

    df_resultado_3=procesamiento(df_validaciones,int(cant_viajes))

    buffer, nombre_salida = exportar_result(df_resultado_3, name_archivo)
    st.download_button(
        label="📥 Descargar archivo procesado",
        data=buffer,
        file_name=nombre_salida,
        mime="text/csv"
    )
