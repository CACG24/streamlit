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
st.sidebar.markdown("### Gráfica de barras")
#Variables
vars_ejeX = ['Day', 'Week', 'Month', 'Year']
vars_semana = ['NA', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
vars_mes = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG']
vars_ejeY = ['Cantidad', 'Duración', 'Edad']

#Caso especifico del eje X
default_barX = vars_ejeX.index('Day')
barX_selected = st.sidebar.selectbox('Elección del eje X para el Histograma:', vars_ejeX, index = default_barX)

if barX_selected=='Day':
  default_subbarX = vars_semana.index('NA')
  subbarX_selected = st.sidebar.selectbox('Elección del día de la semana:', vars_semana, index = default_subbarX)
elif barX_selected=='Month':
  default_subbarX = vars_mes.index('JAN')
  subbarX_selected = st.sidebar.selectbox('Elección del mes:', vars_mes, index = default_subbarX)
else:
  subbarX_selected = barX_selected


#Caso especifico del eje Y
default_barY = vars_ejeY.index('Cantidad')
barY_selected = st.sidebar.selectbox('Elección del eje Y para el Histograma:', vars_ejeY, index = default_barY)

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

#----- Renderizado del Texto --------------------------------------
st.markdown(":violet[**DATAFRAME PARA EL MANEJO DE INFORMACIÓN DE USUARIOS DE MiBici**]")
st.markdown(":blue[Este **DataFrame** contiene información de todos los usuarios y "
            "los viajes que realizaron durante 2024:]")

#----- Renderizado del DataFrame ----------------------------------
st.dataframe(datos_df.head(10))

st.markdown(":blue[Este **DataFrame** fue tratado para eliminar datos inservibles y se "
            "le agregaron nuevas columnas de datos útiles extraidos de la información "
            "ya presente:]")

#Tratamiento de los datos
datos_df.rename(columns = {
        'Usuario_Id': 'Usuario',
        'Año_de_nacimiento': 'Año_nacimiento'
    }, inplace = True)

datos_df.columns = [col.lower() for col in datos_df]

#Eliminación de valores nulos
datos_df=datos_df.dropna()

#Años en enteros
datos_df['año_nacimiento']=datos_df['año_nacimiento'].astype(int)

#Eliminación de usuarios con años de nacimiento menores a 1940
datos_df=datos_df[datos_df['año_nacimiento'] >= 1940]

#Columnas en formato de fecha
datos_df['inicio_del_viaje'] = pd.to_datetime(datos_df['inicio_del_viaje'])
datos_df['fin_del_viaje'] = pd.to_datetime(datos_df['fin_del_viaje'])

#Creación de columnas con nuevos datos
datos_df['tiempo_total'] = datos_df['fin_del_viaje'] - datos_df['inicio_del_viaje']
datos_df['edad'] = 2024 - datos_df['año_nacimiento']
datos_df['dia_semana'] = datos_df['inicio_del_viaje'].dt.day_name()

st.dataframe(datos_df.head(10))
st.divider()

#----- HISTOGRAMA -------------------------------------------------
#Título para el gráfico
st.subheader('Histograma')

#Inicialización del gráfico
fig1, ax1 = plt.subplots()


if barX_selected=='Day':
  if subbarX_selected=='NA':
    if barY_selected=='Cantidad':
      data = datos_df.groupby(datos_df['inicio_del_viaje'].dt.hour).size().reset_index()
    elif barY_selected=='Duración':
      data = datos_df.groupby(datos_df['inicio_del_viaje'].dt.hour)['tiempo_total'].mean().reset_index()
      data['tiempo_total']=(data['tiempo_total'].dt.total_seconds()/60).astype(int)
    else:
      data = datos_df.groupby(datos_df['inicio_del_viaje'].dt.hour)['edad'].mean().reset_index()
  else:
    if barY_selected=='Cantidad':
      data = datos_df[datos_df['dia_semana']==subbarX_selected].groupby(datos_df['inicio_del_viaje'].dt.hour).size().reset_index(name='conteo_viajes')
    elif barY_selected=='Duración':
      data = datos_df[datos_df['dia_semana']==subbarX_selected].groupby(datos_df['inicio_del_viaje'].dt.hour)['tiempo_total'].mean().reset_index()
      data['tiempo_total']=(data['tiempo_total'].dt.total_seconds()/60).astype(int)   
    else:
      data = datos_df[datos_df['dia_semana']==subbarX_selected].groupby(datos_df['inicio_del_viaje'].dt.hour)['edad'].mean().reset_index()
  plt.xticks(range(24))
elif barX_selected=='Week':
  if barY_selected=='Cantidad':
    data = datos_df.groupby('dia_semana').size().reset_index()
  elif barY_selected=='Duración':
    data = datos_df.groupby('dia_semana')['tiempo_total'].mean().reset_index()
    data['tiempo_total']=(data['tiempo_total'].dt.total_seconds()/60).astype(int)
  else:
    data = datos_df.groupby('dia_semana')['edad'].mean().reset_index()
  orden_dias = vars_semana[1:]
  data['dia_semana'] = pd.Categorical(data['dia_semana'], categories=orden_dias, ordered=True)
  data = data.sort_values('dia_semana')

data.columns = ['x', 'y']
plt.bar(data['x'], data['y'], color='blue')
st.pyplot(fig1)

