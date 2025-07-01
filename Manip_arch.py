import pandas as pd
import numpy as np
import os
from pathlib import Path
from io import BytesIO

def importar_csv(archivo):
    if archivo is not None:
        df_validaciones = pd.read_csv(archivo,sep=";")
        name_archivo=Path(archivo.name).stem
        return df_validaciones, name_archivo
    else:
        return None, None
    
def exportar_result(df_final,name_archivo):
    name_final=f"{name_archivo}_final.csv"
    buffer = BytesIO()
    df_final.to_csv(buffer,index=False,encoding='latin1')
    buffer.seek(0)
    return buffer, name_final