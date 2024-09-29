# =================================================================
# == INSTITUTO TECNOLOGICO Y DE ESTUDIOS SUPERIORES DE OCCIDENTE ==
# ==         ITESO, UNIVERSIDAD JESUITA DE GUADALAJARA           ==
# ==                                                             ==
# ==            MAESTRÍA EN SISTEMAS COMPUTACIONALES             ==
# ==             PROGRAMACIÓN PARA ANÁLISIS DE DATOS             ==
# ==                 IMPLEMENTACIÓN EN STREAMLIT                 ==
# =================================================================

#----- Importación de Librerías -----------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import random
import math
from skimage import io


#------------------------------------------------------------------
#----- Configuración Inicial del Panel Central --------------------
#------------------------------------------------------------------

#----- Lectura de Imagenes ----------------------------------------
Logo = io.imread(r"./Imagenes/ITESO_Logo.png")
Logo_mibici = io.imread(r"./Imagenes/mibici.jpg")

#----- Renderizado de Imagen --------------------------------------
st.image(Logo, width = 500)

#----- Renderizado del Texto --------------------------------------
st.title("Proyecto de programación para minería de datos")
st.subheader(":blue[Se utilizaron datos de la plataforma oficial "
              "de *MiBici* para hacer un analisis de los mismos.]")

#----- Renderizado de Imagen --------------------------------------
st.image(Logo_mibici, width = 100)



#------------------------------------------------------------------
#----- Configuración de Texto y Elementos del Panel Central -------
#------------------------------------------------------------------

#----- Lectura de los Datos Desde el Archivo CSV ------------------
#Inicialización de la Lista
year2024=[]

#Asignación de los Archivos a la Lista
for tiempo in range(1, 8+1):
    year2024.append(pd.read_csv('./Datos/MiBici/datos_abiertos_2024_0{}.csv'.format(tiempo), index_col=0))
  
#Concatenación de los Elementos de la Lista a un DataFrame
datos_df=pd.concat(year2024) 

#----- Renderizado del Texto --------------------------------------
st.markdown(":violet[**DATAFRAME PARA EL MANEJO DE INFORMACIÓN DE CLIENTES**]")
st.markdown(":blue[Este **DataFrame** contiene información de varias personas, "
            "las ciudades donde viven, así como sus ganancias a lo largo de un año. "
            "En esta aplicación se generan los siguientes gráficos:]")
st.markdown(":blue[*- **Histograma** para cada uno de los Meses del **DataFrame**.*]")
st.markdown(":blue[*- **Ganancias** para cada persona del **DataFrame**.*]")
st.markdown(":blue[*- **Matriz de Correlación** para los Meses Seleccionados del **DataFrame**.*]")
st.markdown(":violet[El **DataFrame** es el siguiente:]")

#----- Renderizado del DataFrame ----------------------------------
st.dataframe(datos_df.head(10))
st.divider()
