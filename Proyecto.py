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
#----- Configuración de los Elementos del DashBoard ---------------
#------------------------------------------------------------------

#----- Renderizado de la Imagen y el Título en el Dashboard -------
st.sidebar.image(Logo, width = 200)
st.sidebar.markdown("## MENÚ DE CONFIGURACIÓN")
st.sidebar.divider()

#----- HISTOGRAMA POR MES -----------------------------------------
#----- Selector del Mes -------------------------------------------
vars_mes = ['ENE','FEB','MAR','ABR','MAY','JUN','JUL','AGO']
default_hist = vars_mes.index('ENE')
histo_selected = st.sidebar.selectbox('Elección del Mes para el Histograma:', vars_mes, index = default_hist)
st.sidebar.divider()

#----- GRÁFICO DE LÍNEAS PARA LAS GANANCIAS -----------------------
#----- Selector de las Personas -----------------------------------
vars_per = ['Iñaki González','María Cázares','José García','Jérémie Muñoz','Agnès Villalón','Bérénice Pitkämäki',
            'Geneviève Rukajärvi','Hélène Ñuñoz','Ñaguí Grönholm','Iván Földváry']
default_pers = vars_per.index('Iñaki González')
ganan_selected = st.sidebar.selectbox('Elección de Persona para Mostrar las Ganancias Personales:', vars_per, index = default_pers)
st.sidebar.divider()

#----- GRÁFICO DE CORRELACIÓN DE LOS MESES ------------------------
#----- Selector del Mapa de Color ---------------------------------
vars_cmap = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges',
             'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn',
             'YlGn', 'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter',
             'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
             'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic', 'twilight', 'twilight_shifted', 'hsv',
             'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b',
             'tab20c', 'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
             'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral', 'gist_ncar']
color_selected = st.sidebar.selectbox('Paleta de Color para la Matriz de Correlación:', vars_cmap)
if st.sidebar.button('Color Aleatorio') == True:
    color_selected = random.choice(vars_cmap)

#----- Selector de Valores de Correlación para el Gráfico ---------
selec_val_corr = st.sidebar.radio("Valores de Correlación:", options = ['Activo', 'Inactivo'])
if selec_val_corr == 'Activo':
    anotacion = True
elif selec_val_corr == 'Inactivo':
    anotacion = False

#----- Selector de los Meses para el Histograma -------------------
mes_multi_selected = st.sidebar.multiselect('Elementos de la Matriz de Correlación:', vars_mes, default = vars_mes)

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

#Tratamiento de los datos
datos_df.rename(columns = {
        'Usuario_Id': 'Usuario',
        'Año_de_nacimiento': 'Año_nacimiento'
    }, inplace = True)

datos_df.columns = [col.lower() for col in datos_df]

#Eliminación de usuarios con años de nacimiento menores a 1940
datos_df=datos_df[datos_df['año_nacimiento'] >= 1940]

#Eliminación de valores nulos
datos_df=datos_df.dropna()

#Creación de columnas con nuevos datos
datos_df['inicio_del_viaje'] = pd.to_datetime(datos_df['inicio_del_viaje'])
datos_df['fin_del_viaje'] = pd.to_datetime(datos_df['fin_del_viaje'])
datos_df['tiempo_total'] = ((datos_df['fin_del_viaje'] - datos_df['inicio_del_viaje']).dt.total_seconds()/3600)

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
