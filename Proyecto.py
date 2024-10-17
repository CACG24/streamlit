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

#Datos de estaciones
estaciones_origen = pd.read_csv('./Datos/MiBici/estaciones_origen.csv', index_col=0)
estaciones_destino = pd.read_csv('./Datos/MiBici/estaciones_destino.csv', index_col=0)

#----- HISTOGRAMA -------------------------------------------------
#Título para el gráfico
st.subheader('Histograma')

#Inicialización del gráfico
fig1, ax1 = plt.subplots()

#Día
if barX_selected=='Day':
  #M vs F
  if opt_MF:
    width = 0.4
    if barY_selected=='Cantidad':
      plt.bar(data_dia_M['horas']-width/2, data_dia_M['cantidad_{}'.format(subbarX_selected)], width=width, color='blue')
      plt.bar(data_dia_F['horas']+width/2, data_dia_F['cantidad_{}'.format(subbarX_selected)], width=width, color='pink')
      plt.title('Cantidad de viajes por hora y género - {}'.format(subbarX_selected))
      plt.ylabel('Cantidad de viajes')
      
    elif barY_selected=='Duración':
      plt.bar(data_dia_M['horas']-width/2, data_dia_M['duracion_{}'.format(subbarX_selected)], width=width, color='blue')
      plt.bar(data_dia_F['horas']+width/2, data_dia_F['duracion_{}'.format(subbarX_selected)], width=width, color='pink')
      plt.title('Duración de viajes por hora y género - {}'.format(subbarX_selected))
      plt.ylabel('Duración de viajes')
      
    elif barY_selected=='Edad':
      plt.bar(data_dia_M['horas']-width/2, data_dia_M['edad_{}'.format(subbarX_selected)], width=width, color='blue')
      plt.bar(data_dia_F['horas']+width/2, data_dia_F['edad_{}'.format(subbarX_selected)], width=width, color='pink')
      plt.title('Edad promedio por hora y género - {}'.format(subbarX_selected))
      plt.ylabel('Edad promedio')
      
    elif barY_selected=='Distancia de ruta':
      plt.bar(data_dia_M['horas']-width/2, data_dia_M['maproute_{}'.format(subbarX_selected)], width=width, color='blue')
      plt.bar(data_dia_F['horas']+width/2, data_dia_F['maproute_{}'.format(subbarX_selected)], width=width, color='pink')
      plt.title('Distancia de ruta por hora y género - {}'.format(subbarX_selected))
      plt.ylabel('Distancia de ruta')

    elif barY_selected=='Distancia geodesica':
      plt.bar(data_dia_M['horas']-width/2, data_dia_M['mapdis_{}'.format(subbarX_selected)], width=width, color='blue')
      plt.bar(data_dia_F['horas']+width/2, data_dia_F['mapdis_{}'.format(subbarX_selected)], width=width, color='pink')
      plt.title('Distancia geodesica por hora y género - {}'.format(subbarX_selected))
      plt.ylabel('Distancia geodesica')

    elif barY_selected=='Velocidad de ruta':
      plt.bar(data_dia_M['horas']-width/2, data_dia_M['velroute_{}'.format(subbarX_selected)], width=width, color='blue')
      plt.bar(data_dia_F['horas']+width/2, data_dia_F['velroute_{}'.format(subbarX_selected)], width=width, color='pink')
      plt.title('Velocidad de ruta por hora y género - {}'.format(subbarX_selected))
      plt.ylabel('Velocidad de ruta')

    elif barY_selected=='Velocidad geodesica':
      plt.bar(data_dia_M['horas']-width/2, data_dia_M['veldis_{}'.format(subbarX_selected)], width=width, color='blue')
      plt.bar(data_dia_F['horas']+width/2, data_dia_F['veldis_{}'.format(subbarX_selected)], width=width, color='pink')
      plt.title('Velocidad geodesica por hora y género - {}'.format(subbarX_selected))
      plt.ylabel('Velocidad geodesica de viajes')

    else:
      plt.bar(data_dia_M['horas']-width/2, data_dia_M['tarifa_{}'.format(subbarX_selected)], width=width, color='blue')
      plt.bar(data_dia_F['horas']+width/2, data_dia_F['tarifa_{}'.format(subbarX_selected)], width=width, color='pink')
      plt.title('Tarifa promedio por hora y género - {}'.format(subbarX_selected))
      plt.ylabel('Tarifa promedio de viajes')

  #No M vs F
  else:
    if barY_selected=='Cantidad':
      plt.bar(data_dia_total['horas'], data_dia_total['cantidad_{}'.format(subbarX_selected)], color='blue')
      plt.title('Cantidad de viajes por hora - {}'.format(subbarX_selected))
      plt.ylabel('Cantidad de viajes')
      
    elif barY_selected=='Duración':
      plt.bar(data_dia_total['horas'], data_dia_total['duracion_{}'.format(subbarX_selected)], color='blue')
      plt.title('Duración de viajes por hora - {}'.format(subbarX_selected))
      plt.ylabel('Duración de viajes')
      
    elif barY_selected=='Edad':
      plt.bar(data_dia_total['horas'], data_dia_total['edad_{}'.format(subbarX_selected)], color='blue')
      plt.title('Edad promedio por hora - {}'.format(subbarX_selected))
      plt.ylabel('Edad promedio')
      
    elif barY_selected=='Distancia de ruta':
      plt.bar(data_dia_total['horas'], data_dia_total['maproute_{}'.format(subbarX_selected)], color='blue')
      plt.title('Distancia de ruta por hora - {}'.format(subbarX_selected))
      plt.ylabel('Distancia de ruta')

    elif barY_selected=='Distancia geodesica':
      plt.bar(data_dia_total['horas'], data_dia_total['mapdis_{}'.format(subbarX_selected)], color='blue')
      lt.title('Distancia geodesica por hora - {}'.format(subbarX_selected))
      plt.ylabel('Distancia geodesica')

    elif barY_selected=='Velocidad de ruta':
      plt.bar(data_dia_total['horas'], data_dia_total['velroute_{}'.format(subbarX_selected)], color='blue')
      plt.title('Velocidad de ruta por hora - {}'.format(subbarX_selected))
      plt.ylabel('Velocidad de ruta')

    elif barY_selected=='Velocidad geodesica':
      plt.bar(data_dia_total['horas'], data_dia_total['veldis_{}'.format(subbarX_selected)], color='blue')
      plt.title('Velocidad geodesica por hora - {}'.format(subbarX_selected))
      plt.ylabel('Velocidad geodesica de viajes')

    else:
      plt.bar(data_dia_total['horas'], data_dia_total['tarifa_{}'.format(subbarX_selected)], color='blue')
      plt.title('Tarifa promedio por hora - {}'.format(subbarX_selected))
      plt.ylabel('Tarifa promedio de viajes')

  #Configuración de las gráficas
  plt.xticks(range(24), fontsize=8)
  plt.xlabel('Hora del día')
  
#Semana
elif barX_selected=='Week':
  #M vs F
  if opt_MF:
    width = 0.4
    if barY_selected=='Cantidad':
      plt.bar(data_semana['dia_semana'], data_semana['cantidad_M'], width=width, color='blue')
      plt.bar(data_semana['dia_semana'], data_semana['cantidad_F'], width=width, align='edge', color='pink')
      plt.title('Cantidad de viajes por día y género')
      plt.ylabel('Cantidad de viajes')
      
    elif barY_selected=='Duración':
      plt.bar(data_semana['dia_semana'], data_semana['duracion_M'], width=width, color='blue')
      plt.bar(data_semana['dia_semana'], data_semana['duracion_F'], width=width, align='edge', color='pink')
      plt.title('Duración de viajes por día y género')
      plt.ylabel('Duración de viajes')
      
    elif barY_selected=='Edad':
      plt.bar(data_semana['dia_semana'], data_semana['edad_M'], width=width, color='blue')
      plt.bar(data_semana['dia_semana'], data_semana['edad_F'], width=width, align='edge', color='pink')
      plt.title('Edad promedio por día y género')
      plt.ylabel('Edad promedio')
      
    elif barY_selected=='Distancia de ruta':
      plt.bar(data_semana['dia_semana'], data_semana['maproute_M'], width=width, color='blue')
      plt.bar(data_semana['dia_semana'], data_semana['maproute_F'], width=width, align='edge', color='pink')
      plt.title('Distancia de ruta por día y género')
      plt.ylabel('Distancia de ruta')

    elif barY_selected=='Distancia geodesica':
      plt.bar(data_semana['dia_semana'], data_semana['mapdis_M'], width=width, color='blue')
      plt.bar(data_semana['dia_semana'], data_semana['mapdis_F'], width=width, align='edge', color='pink')
      plt.title('Distancia geodesica por día y género')
      plt.ylabel('Distancia geodesica')

    elif barY_selected=='Velocidad de ruta':
      plt.bar(data_semana['dia_semana'], data_semana['velroute_M'], width=width, color='blue')
      plt.bar(data_semana['dia_semana'], data_semana['velroute_F'], width=width, align='edge', color='pink')
      plt.title('Velocidad de ruta por día y género')
      plt.ylabel('Velocidad de ruta')

    elif barY_selected=='Velocidad geodesica':
      plt.bar(data_semana['dia_semana'], data_semana['veldis_M'], width=width, color='blue')
      plt.bar(data_semana['dia_semana'], data_semana['veldis_F'], width=width, align='edge', color='pink')
      plt.title('Velocidad geodesica por día y género')
      plt.ylabel('Velocidad geodesica')

    else:
      plt.bar(data_semana['dia_semana'], data_semana['tarifa_M'], width=width, color='blue')
      plt.bar(data_semana['dia_semana'], data_semana['tarifa_F'], width=width, align='edge', color='pink')
      plt.title('Tarifa promedio por día y género')
      plt.ylabel('Tarifa promedio')

  #No M vs F
  else:
    if barY_selected=='Cantidad':
      plt.bar(data_semana['dia_semana'], data_semana['cantidad'], color='blue')
      plt.title('Cantidad de viajes por día')
      plt.ylabel('Cantidad de viajes')
      
    elif barY_selected=='Duración':
      plt.bar(data_semana['dia_semana'], data_semana['duracion'], color='blue')
      plt.title('Duración de viajes por día')
      plt.ylabel('Duración de viajes')
      
    elif barY_selected=='Edad':
      plt.bar(data_semana['dia_semana'], data_semana['edad'], color='blue')
      plt.title('Edad promedio por día')
      plt.ylabel('Edad promedio')
      
    elif barY_selected=='Distancia de ruta':
      plt.bar(data_semana['dia_semana'], data_semana['maproute'], color='blue')
      plt.title('Distancia de ruta por día')
      plt.ylabel('Distancia de ruta')

    elif barY_selected=='Distancia geodesica':
      plt.bar(data_semana['dia_semana'], data_semana['mapdis'], color='blue')
      plt.title('Distancia geodesica por día')
      plt.ylabel('Distancia geodesica')

    elif barY_selected=='Velocidad de ruta':
      plt.bar(data_semana['dia_semana'], data_semana['velroute'], color='blue')
      plt.title('Velocidad de ruta por día')
      plt.ylabel('Velocidad de ruta')

    elif barY_selected=='Velocidad geodesica':
      plt.bar(data_semana['dia_semana'], data_semana['veldis'], color='blue')
      plt.title('Velocidad geodesica por día')
      plt.ylabel('Velocidad geodesica')

    else:
      plt.bar(data_semana['dia_semana'], data_semana['tarifa'], color='blue')
      plt.title('Tarifa promedio por día')
      plt.ylabel('Tarifa promedio')

  #Configuración de las gráficas
  plt.xticks(rotation=45, fontsize=8)
  plt.xlabel('Día de la semana')
  
#Mes
elif barX_selected=='Month':
  #M vs F
  if opt_MF:
    width = 0.4
    if barY_selected=='Cantidad':
      plt.bar(data_mes_M['dias']-width/2, data_mes_M['cantidad_{}'.format(subbarX_selected)], width=width, color='blue')
      plt.bar(data_mes_F['dias']+width/2, data_mes_F['cantidad_{}'.format(subbarX_selected)], width=width, color='pink')
      plt.title('Cantidad de viajes por día y género - {}'.format(subbarX_selected))
      plt.ylabel('Cantidad de viajes')
      
    elif barY_selected=='Duración':
      plt.bar(data_mes_M['dias']-width/2, data_mes_M['duracion_{}'.format(subbarX_selected)], width=width, color='blue')
      plt.bar(data_dia_F['dias']+width/2, data_mes_F['duracion_{}'.format(subbarX_selected)], width=width, color='pink')
      plt.title('Duración de viajes por día y género - {}'.format(subbarX_selected))
      plt.ylabel('Duración de viajes')
      
    elif barY_selected=='Edad':
      plt.bar(data_mes_M['dias']-width/2, data_mes_M['edad_{}'.format(subbarX_selected)], width=width, color='blue')
      plt.bar(data_mes_F['dias']+width/2, data_mes_F['edad_{}'.format(subbarX_selected)], width=width, color='pink')
      plt.title('Edad promedio por día y género - {}'.format(subbarX_selected))
      plt.ylabel('Edad promedio')
      
    elif barY_selected=='Distancia de ruta':
      plt.bar(data_mes_M['dias']-width/2, data_mes_M['maproute_{}'.format(subbarX_selected)], width=width, color='blue')
      plt.bar(data_mes_F['dias']+width/2, data_mes_F['maproute_{}'.format(subbarX_selected)], width=width, color='pink')
      plt.title('Distancia de ruta por día y género - {}'.format(subbarX_selected))
      plt.ylabel('Distancia de ruta')

    elif barY_selected=='Distancia geodesica':
      plt.bar(data_mes_M['dias']-width/2, data_mes_M['mapdis_{}'.format(subbarX_selected)], width=width, color='blue')
      plt.bar(data_mes_F['dias']+width/2, data_mes_F['mapdis_{}'.format(subbarX_selected)], width=width, color='pink')
      plt.title('Distancia geodesica por día y género - {}'.format(subbarX_selected))
      plt.ylabel('Distancia geodesica')

    elif barY_selected=='Velocidad de ruta':
      plt.bar(data_mes_M['dias']-width/2, data_mes_M['velroute_{}'.format(subbarX_selected)], width=width, color='blue')
      plt.bar(data_mes_F['dias']+width/2, data_mes_F['velroute_{}'.format(subbarX_selected)], width=width, color='pink')
      plt.title('Velocidad de ruta por día y género - {}'.format(subbarX_selected))
      plt.ylabel('Velocidad de ruta')

    elif barY_selected=='Velocidad geodesica':
      plt.bar(data_mes_M['dias']-width/2, data_mes_M['veldis_{}'.format(subbarX_selected)], width=width, color='blue')
      plt.bar(data_mes_F['dias']+width/2, data_mes_F['veldis_{}'.format(subbarX_selected)], width=width, color='pink')
      plt.title('Velocidad geodesica por día y género - {}'.format(subbarX_selected))
      plt.ylabel('Velocidad geodesica de viajes')

    else:
      plt.bar(data_mes_M['dias']-width/2, data_mes_M['tarifa_{}'.format(subbarX_selected)], width=width, color='blue')
      plt.bar(data_mes_F['dias']+width/2, data_mes_F['tarifa_{}'.format(subbarX_selected)], width=width, color='pink')
      plt.title('Tarifa promedio por día y género - {}'.format(subbarX_selected))
      plt.ylabel('Tarifa promedio de viajes')

  #No M vs F
  else:
    if barY_selected=='Cantidad':
      plt.bar(data_mes_total['dias'], data_mes_total['cantidad_{}'.format(subbarX_selected)], color='blue')
      plt.title('Cantidad de viajes por día - {}'.format(subbarX_selected))
      plt.ylabel('Cantidad de viajes')
      
    elif barY_selected=='Duración':
      plt.bar(data_mes_total['dias'], data_mes_total['duracion_{}'.format(subbarX_selected)], color='blue')
      plt.title('Duración de viajes por día - {}'.format(subbarX_selected))
      plt.ylabel('Duración de viajes')
      
    elif barY_selected=='Edad':
      plt.bar(data_mes_total['dias'], data_mes_total['edad_{}'.format(subbarX_selected)], color='blue')
      plt.title('Edad promedio por día - {}'.format(subbarX_selected))
      plt.ylabel('Edad promedio')
      
    elif barY_selected=='Distancia de ruta':
      plt.bar(data_mes_total['dias'], data_mes_total['maproute_{}'.format(subbarX_selected)], color='blue')
      plt.title('Distancia de ruta por día - {}'.format(subbarX_selected))
      plt.ylabel('Distancia de ruta')

    elif barY_selected=='Distancia geodesica':
      plt.bar(data_mes_total['dias'], data_mes_total['mapdis_{}'.format(subbarX_selected)], color='blue')
      lt.title('Distancia geodesica por día - {}'.format(subbarX_selected))
      plt.ylabel('Distancia geodesica')

    elif barY_selected=='Velocidad de ruta':
      plt.bar(data_mes_total['dias'], data_mes_total['velroute_{}'.format(subbarX_selected)], color='blue')
      plt.title('Velocidad de ruta por día - {}'.format(subbarX_selected))
      plt.ylabel('Velocidad de ruta')

    elif barY_selected=='Velocidad geodesica':
      plt.bar(data_mes_total['dias'], data_mes_total['veldis_{}'.format(subbarX_selected)], color='blue')
      plt.title('Velocidad geodesica por día - {}'.format(subbarX_selected))
      plt.ylabel('Velocidad geodesica de viajes')

    else:
      plt.bar(data_mes_total['dias'], data_mes_total['tarifa_{}'.format(subbarX_selected)], color='blue')
      plt.title('Tarifa promedio por día - {}'.format(subbarX_selected))
      plt.ylabel('Tarifa promedio de viajes')

  #Configuración de las gráficas
  plt.xticks(range(32), fontsize=8)
  plt.xlabel('Día del mes')
  
#Año
elif barX_selected=='Year':
  #M vs F
  if opt_MF:
    width = 0.4
    if barY_selected=='Cantidad':
      plt.bar(data_año['mes'], data_año['cantidad_M'], width=width, color='blue')
      plt.bar(data_año['mes'], data_año['cantidad_F'], width=width, align='edge', color='pink')
      plt.title('Cantidad de viajes por mes y género')
      plt.ylabel('Cantidad de viajes')
      
    elif barY_selected=='Duración':
      plt.bar(data_año['mes'], data_año['duracion_M'], width=width, color='blue')
      plt.bar(data_año['mes'], data_año['duracion_F'], width=width, align='edge', color='pink')
      plt.title('Duración de viajes por mes y género')
      plt.ylabel('Duración de viajes')
      
    elif barY_selected=='Edad':
      plt.bar(data_año['mes'], data_año['edad_M'], width=width, color='blue')
      plt.bar(data_año['mes'], data_año['edad_F'], width=width, align='edge', color='pink')
      plt.title('Edad promedio por mes y género')
      plt.ylabel('Edad promedio')
      
    elif barY_selected=='Distancia de ruta':
      plt.bar(data_año['mes'], data_año['maproute_M'], width=width, color='blue')
      plt.bar(data_año['mes'], data_año['maproute_F'], width=width, align='edge', color='pink')
      plt.title('Distancia de ruta por mes y género')
      plt.ylabel('Distancia de ruta')

    elif barY_selected=='Distancia geodesica':
      plt.bar(data_año['mes'], data_año['mapdis_M'], width=width, color='blue')
      plt.bar(data_año['mes'], data_año['mapdis_F'], width=width, align='edge', color='pink')
      plt.title('Distancia geodesica por mes y género')
      plt.ylabel('Distancia geodesica')

    elif barY_selected=='Velocidad de ruta':
      plt.bar(data_año['mes'], data_año['velroute_M'], width=width, color='blue')
      plt.bar(data_año['mes'], data_año['velroute_F'], width=width, align='edge', color='pink')
      plt.title('Velocidad de ruta por mes y género')
      plt.ylabel('Velocidad de ruta')

    elif barY_selected=='Velocidad geodesica':
      plt.bar(data_año['mes'], data_año['veldis_M'], width=width, color='blue')
      plt.bar(data_año['mes'], data_año['veldis_F'], width=width, align='edge', color='pink')
      plt.title('Velocidad geodesica por mes y género')
      plt.ylabel('Velocidad geodesica')

    else:
      plt.bar(data_año['mes'], data_año['tarifa_M'], width=width, color='blue')
      plt.bar(data_año['mes'], data_año['tarifa_F'], width=width, align='edge', color='pink')
      plt.title('Tarifa promedio por mes y género')
      plt.ylabel('Tarifa promedio')

  #No M vs F
  else:
    if barY_selected=='Cantidad':
      plt.bar(data_año['mes'], data_año['cantidad'], color='blue')
      plt.title('Cantidad de viajes por mes')
      plt.ylabel('Cantidad de viajes')
      
    elif barY_selected=='Duración':
      plt.bar(data_año['mes'], data_año['duracion'], color='blue')
      plt.title('Duración de viajes por mes')
      plt.ylabel('Duración de viajes')
      
    elif barY_selected=='Edad':
      plt.bar(data_año['mes'], data_año['edad'], color='blue')
      plt.title('Edad promedio por mes')
      plt.ylabel('Edad promedio')
      
    elif barY_selected=='Distancia de ruta':
      plt.bar(data_año['mes'], data_año['maproute'], color='blue')
      plt.title('Distancia de ruta por mes')
      plt.ylabel('Distancia de ruta')

    elif barY_selected=='Distancia geodesica':
      plt.bar(data_año['mes'], data_año['mapdis'], color='blue')
      plt.title('Distancia geodesica por mes')
      plt.ylabel('Distancia geodesica')

    elif barY_selected=='Velocidad de ruta':
      plt.bar(data_año['mes'], data_año['velroute'], color='blue')
      plt.title('Velocidad de ruta por mes')
      plt.ylabel('Velocidad de ruta')

    elif barY_selected=='Velocidad geodesica':
      plt.bar(data_año['mes'], data_año['veldis'], color='blue')
      plt.title('Velocidad geodesica por mes')
      plt.ylabel('Velocidad geodesica')

    else:
      plt.bar(data_año['mes'], data_año['tarifa'], color='blue')
      plt.title('Tarifa promedio por mes')
      plt.ylabel('Tarifa promedio')
      
  #Configuración de las gráficas
  plt.xticks(rotation=45, fontsize=8)
  plt.xlabel('Mes')
  
st.pyplot(fig1)
  

fig2, ax2 = plt.subplots()
sns.barplot(data=estaciones_origen, x='inicio_del_viaje', y='cantidad_viajes', hue='origen_id', palette='Set1')
plt.title('Uso de Principales Estaciones por Mes')
plt.xlabel('Mes')
plt.ylabel('Cantidad de Viajes')
plt.xticks(rotation=45)
plt.legend(title='Estación', loc='upper right', labels=estaciones_origen['origen_id'].value_counts().nlargest(10).index)
plt.grid(False)


# Mostrar la gráfica
st.pyplot(fig2)
