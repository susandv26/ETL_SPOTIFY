from data.transformation import convertir_a_minuscula, convertir_a_mayuscula, extraer_fecha

# Función para aplicar las transformaciones a los datos
def transform_data(df, operacion):
    if operacion == 1:
        return convertir_a_minuscula(df)
    elif operacion == 2:
        return convertir_a_mayuscula(df)
    elif operacion == 3:
        return extraer_fecha(df)
    else:
        print("Operación no válida")
        return df