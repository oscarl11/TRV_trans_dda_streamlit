import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib.dates import date2num
from datetime import datetime

def filtr_fechas(df_validaciones):
    df_validaciones["FECHA"]=pd.to_datetime(df_validaciones["FECHA"],format="%d/%m/%Y %H:%M:%S")
    fec_ran_min=df_validaciones["FECHA"].mean().normalize()+pd.Timedelta(hours=3, minutes=30)
    fec_ran_max=df_validaciones["FECHA"].mean().normalize()+pd.Timedelta(days=1,hours=3, minutes=30)
    df_fec_filtr=df_validaciones[(df_validaciones["FECHA"]>=fec_ran_min) & (df_validaciones["FECHA"]<=fec_ran_max)]
    return df_fec_filtr

def filtr_tarjeta(df_fec_filtr):
    conteo_tarj_df = df_fec_filtr["TARJETA"].value_counts().reset_index()
    filtr_tarj=conteo_tarj_df[conteo_tarj_df["FRECUENCIA"]<6]
    df_filtr_tarj=df_fec_filtr[df_fec_filtr["TARJETA"].isin(filtr_tarj["TARJETA"])]
    return df_filtr_tarj

def procesamiento(df_validaciones,cant_viajes):
    # 1. Copia del DataFrame original
    df_trabajo_2 = df_validaciones.copy()

    # 2. Limpieza de nulos
    df_trabajo_2 = df_trabajo_2.dropna(subset=["FECHA", "TIPO_VALIDACION", "RUTA"])
    df_trabajo_2["FECHA"] = pd.to_datetime(df_trabajo_2["FECHA"])

    # 3. Tarjetas con menos de n validaciones
    conteo_tarjetas = df_trabajo_2["TARJETA"].value_counts()
    tarjetas_menor_20 = conteo_tarjetas[conteo_tarjetas < cant_viajes].index

    # 4. Filtrar y ordenar
    df_filtrado_2 = df_trabajo_2[df_trabajo_2["TARJETA"].isin(tarjetas_menor_20)]
    df_ordenado_2 = df_filtrado_2.sort_values(by=["TARJETA", "FECHA"])

    # 5. ORDEN_VALIDACIONES (cadena tipo "ATT", "TTA", etc.)
    orden_validaciones = (
        df_ordenado_2.groupby("TARJETA")["TIPO_VALIDACION"]
        .apply(lambda x: ''.join(x.astype(str)))
        .reset_index(name="ORDEN_VALIDACIONES")
    )

    # 6. RUTAS en columnas RUTA_1, RUTA_2, ...
    rutas_expandidas = (
        df_ordenado_2.groupby("TARJETA")["RUTA"]
        .apply(lambda x: pd.Series(x.tolist()))
        .unstack()
    )
    rutas_expandidas.columns = [f"RUTA_{i+1}" for i in range(rutas_expandidas.shape[1])]

    # 7. FECHAS en columnas FECHA_1, FECHA_2, ...
    fechas_expandidas = (
        df_ordenado_2.groupby("TARJETA")["FECHA"]
        .apply(lambda x: pd.Series(x.tolist()))
        .unstack()
    )
    fechas_expandidas.columns = [f"FECHA_{i+1}" for i in range(fechas_expandidas.shape[1])]

    # 8. Unimos todo
    df_resultado_3 = (
        orden_validaciones
        .merge(rutas_expandidas, left_on="TARJETA", right_index=True)
        .merge(fechas_expandidas, left_on="TARJETA", right_index=True)
    )

    # 9. Contamos número de validaciones
    df_resultado_3["NUM_VALIDACIONES"] = df_resultado_3["ORDEN_VALIDACIONES"].str.len()

    return df_resultado_3
