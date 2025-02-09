import os
import pandas as pd

# Obtener la ruta base (un nivel arriba del script actual)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Definir carpetas de entrada y salida
input_folder = os.path.join(base_dir, "data", "raw")  # Carpeta de archivos CSV
output_folder = os.path.join(base_dir, "data", "processed")  # Carpeta para archivos procesados

# Crear la carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Obtener la lista de archivos que comienzan con "Trip" y terminan en ".csv"
file_names = [f for f in os.listdir(input_folder) if f.startswith("Trip") and f.endswith(".csv")]

# Lista para almacenar los DataFrames
dataframes = []

# Cargar todos los archivos CSV
for file_name in file_names:
    file_path = os.path.join(input_folder, file_name)
    try:
        # Leer el archivo CSV con codificación robusta
        df = pd.read_csv(file_path, encoding='latin1', sep=";")

        # Remover ".csv" del trip_name
        trip_name = file_name.replace(".csv", "")

        # Extraer la letra después de "Trip"
        trip_letter = trip_name[4] if len(trip_name) > 4 else ""

        # Agregar las nuevas columnas
        df["trip_name"] = trip_name
        df["trip_letter"] = trip_letter

        # Agregar al listado de DataFrames
        dataframes.append(df)
        # print(f"Cargado: {file_name}")
    except Exception as e:
        print(f"Error cargando {file_name}: {e}")

# Concatenar todos los DataFrames en uno solo
if dataframes:
    combined_df = pd.concat(dataframes, ignore_index=True)

    unnamed_cols = [col for col in combined_df.columns if "Unnamed" in col]
    if unnamed_cols:
        # print(f"⚠️ Eliminando columnas innecesarias: {unnamed_cols}")
        combined_df.drop(columns=unnamed_cols, inplace=True)

    # Definir ruta de salida
    output_file = os.path.join(output_folder, "combined_trips.csv")

    # Guardar en un archivo CSV
    combined_df.to_csv(output_file, index=False)

    print(f"✅ Archivo combinado guardado en: {output_file}")

    # Mostrar las primeras filas del DataFrame combinado
    print(combined_df.head())
else:
    print("❌ No se encontraron archivos CSV que comiencen con 'Trip' en la carpeta especificada.")
