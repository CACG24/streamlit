year2024=[]

for tiempo in range(1, 8+1):
    year2024.append(pd.read_csv('./Datos/MiBici/datos_abiertos_2024_0{}.csv'.format(tiempo), index_col=0))
    
datos_df=pd.concat(year2024)

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

datos_df.to_csv('./Datos/MiBici_2024.csv')
