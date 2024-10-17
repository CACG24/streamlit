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

#----- GRAFICA DE BARRAS ------------------------------------------
st.sidebar.markdown("### Gráficas de barras")
#Variables
vars_ejeX = ['Day', 'Week', 'Month', 'Year']
vars_semana = ['NA', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
vars_mes = ['NA', 'January','February','March','April','May','June','July','August']
vars_ejeY = ['Cantidad', 'Duración', 'Edad', 'Distancia de ruta', 'Distancia geodesica', 'Velocidad de ruta', 'Velocidad geodesica', 'Tarifa']

#Caso especifico del eje X
default_barX = vars_ejeX.index('Day')
barX_selected = st.sidebar.selectbox('Elección del eje X para el Histograma:', vars_ejeX, index = default_barX)

if barX_selected=='Day':
  default_subbarX = vars_semana.index('NA')
  subbarX_selected = st.sidebar.selectbox('Elección del día de la semana:', vars_semana, index = default_subbarX)
elif barX_selected=='Month':
  default_subbarX = vars_mes.index('NA')
  subbarX_selected = st.sidebar.selectbox('Elección del mes:', vars_mes, index = default_subbarX)
else:
  subbarX_selected = barX_selected


#Caso especifico del eje Y
default_barY = vars_ejeY.index('Cantidad')
barY_selected = st.sidebar.selectbox('Elección del eje Y para el Histograma:', vars_ejeY, index = default_barY)

# Crear un interruptor
opt_MF = st.sidebar.toggle('M vs F')
  
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

#Lectura de archivo original
datos_df = pd.read_csv('./Datos/MiBici/datos_abiertos_2024_01.csv', index_col=0)

#----- Renderizado del Texto --------------------------------------
st.markdown(":violet[**DATAFRAME PARA EL MANEJO DE INFORMACIÓN DE USUARIOS DE MiBici**]")
st.markdown(":blue[Este **DataFrame** contiene información de todos los usuarios y "
            "los viajes que realizaron durante 2024:]")

#----- Renderizado del DataFrame ----------------------------------
st.dataframe(datos_df.head(10))

st.markdown(":blue[Este **DataFrame** fue tratado para eliminar datos inservibles e imputar "
            "datos faltantes. Se le agregaron nuevas columnas de tiempo total, dia de la semana, "
            "edad, distancia de ruta según GoogleMaps, distancia geodesica, velocidades promedio y "
            "tarifa estimada:]")

#Lectura de archivo modificado
datos_df = pd.read_csv('./Datos/MiBici/datos_tratados_2024_01.csv', index_col=0)

#Convertir las columnas a datetime
datos_df['tiempo_total'] = pd.to_timedelta(datos_df['tiempo_total'])

st.dataframe(datos_df.head(10))
st.divider()

#----- Renderizado de los DataFrames ------------------------------
#Datos de dia
data_dia_total = pd.read_csv('./Datos/MiBici/data_dia_total.csv', index_col=0)
data_dia_M = pd.read_csv('./Datos/MiBici/data_dia_M.csv', index_col=0)
data_dia_F = pd.read_csv('./Datos/MiBici/data_dia_F.csv', index_col=0)

#Datos de semana
data_semana = pd.read_csv('./Datos/MiBici/data_semana.csv', index_col=0)

#Datos de mes
data_mes_total = pd.read_csv('./Datos/MiBici/data_mes_total.csv', index_col=0)
data_mes_M = pd.read_csv('./Datos/MiBici/data_mes_M.csv', index_col=0)
data_mes_F = pd.read_csv('./Datos/MiBici/data_mes_F.csv', index_col=0)

#Datos de año
data_año = pd.read_csv('./Datos/MiBici/data_año.csv', index_col=0)

#----- HISTOGRAMA -------------------------------------------------
#Título para el gráfico
st.subheader('Histograma')

#Inicialización del gráfico
fig1, ax1 = plt.subplots()

#Día
if barX_selected=='Day':
  #M vs F
  if opt_MF:
    width = 0.35
    if barY_selected=='Cantidad':
      plt.bar(data_dia_M['horas']-width/2, data_dia_M['cantidad_{}'.format(subbarX_selected)], width=width, color='blue')
      plt.bar(data_dia_F['horas']+width/2, data_dia_F['cantidad_{}'.format(subbarX_selected)], width=width, color='pink')
      
    elif barY_selected=='Duración':
      plt.bar(data_dia_M['horas'], data_dia_M['duracion_{}'.format(subbarX_selected)], color='blue')
      plt.bar(data_dia_F['horas'], data_dia_F['duracion_{}'.format(subbarX_selected)], color='pink')
      
    elif barY_selected=='Edad':
      plt.bar(data_dia_M['horas'], data_dia_M['edad_{}'.format(subbarX_selected)], color='blue')
      plt.bar(data_dia_F['horas'], data_dia_F['edad_{}'.format(subbarX_selected)], color='pink')
      
    elif barY_selected=='Distancia de ruta':
      plt.bar(data_dia_M['horas'], data_dia_M['maproute_{}'.format(subbarX_selected)], color='blue')
      plt.bar(data_dia_F['horas'], data_dia_F['maproute_{}'.format(subbarX_selected)], color='pink')

    elif barY_selected=='Distancia geodesica':
      plt.bar(data_dia_M['horas'], data_dia_M['mapdis_{}'.format(subbarX_selected)], color='blue')
      plt.bar(data_dia_F['horas'], data_dia_F['mapdis_{}'.format(subbarX_selected)], color='pink')

    elif barY_selected=='Velocidad de ruta':
      plt.bar(data_dia_M['horas'], data_dia_M['velroute_{}'.format(subbarX_selected)], color='blue')
      plt.bar(data_dia_F['horas'], data_dia_F['velroute_{}'.format(subbarX_selected)], color='pink')

    elif barY_selected=='Velocidad geodesica':
      plt.bar(data_dia_M['horas'], data_dia_M['veldis_{}'.format(subbarX_selected)], color='blue')
      plt.bar(data_dia_F['horas'], data_dia_F['veldis_{}'.format(subbarX_selected)], color='pink')

    else:
      plt.bar(data_dia_M['horas'], data_dia_M['tarifa_{}'.format(subbarX_selected)], color='blue')
      plt.bar(data_dia_F['horas'], data_dia_F['tarifa_{}'.format(subbarX_selected)], color='pink')

  #No M vs F
  else:
    if barY_selected=='Cantidad':
      plt.bar(data_dia_total['horas'], data_dia_total['cantidad_{}'.format(subbarX_selected)], color='blue')
      
    elif barY_selected=='Duración':
      plt.bar(data_dia_total['horas'], data_dia_total['duracion_{}'.format(subbarX_selected)], color='blue')
      
    elif barY_selected=='Edad':
      plt.bar(data_dia_total['horas'], data_dia_total['edad_{}'.format(subbarX_selected)], color='blue')
      
    elif barY_selected=='Distancia de ruta':
      plt.bar(data_dia_total['horas'], data_dia_total['maproute_{}'.format(subbarX_selected)], color='blue')

    elif barY_selected=='Distancia geodesica':
      plt.bar(data_dia_total['horas'], data_dia_total['mapdis_{}'.format(subbarX_selected)], color='blue')

    elif barY_selected=='Velocidad de ruta':
      plt.bar(data_dia_total['horas'], data_dia_total['velroute_{}'.format(subbarX_selected)], color='blue')

    elif barY_selected=='Velocidad geodesica':
      plt.bar(data_dia_total['horas'], data_dia_total['veldis_{}'.format(subbarX_selected)], color='blue')

    else:
      plt.bar(data_dia_total['horas'], data_dia_total['tarifa_{}'.format(subbarX_selected)], color='blue')

#Semana
elif barX_selected=='Week':
  plt.bar(data_dia_total['horas'], data_dia_total['tarifa_NA'], color='blue')
#Mes
elif barX_selected=='Month':
  plt.bar(data_dia_total['horas'], data_dia_total['tarifa_NA'], color='blue')
#Año
elif barX_selected=='Year':
  plt.bar(data_dia_total['horas'], data_dia_total['tarifa_NA'], color='blue')
  
st.pyplot(fig1)
  


