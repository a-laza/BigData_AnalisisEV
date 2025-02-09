import os
import pandas as pd

# Obtener la ruta base (un nivel arriba del script actual)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Definir carpetas de entrada y salida
input_folder = os.path.join(base_dir, "data", "raw")  # Carpeta donde está Overview.csv
processed_folder = os.path.join(base_dir, "data", "processed")  # Carpeta con combined_trips.csv

# Definir rutas de archivos
combined_trips_file = os.path.join(processed_folder, "combined_trips.csv")
overview_file = os.path.join(input_folder, "Overview.csv")
output_file = os.path.join(processed_folder, "all_data_trips.csv")

# Verificar que el archivo combinado existe
if not os.path.exists(combined_trips_file):
    print(f"❌ No se encontró el archivo {combined_trips_file}. Asegúrate de haber ejecutado el script anterior.")
    exit()

# Cargar el archivo combinado
try:
    combined_df = pd.read_csv(combined_trips_file, encoding='latin1')
    print(f"✅ Archivo cargado: {combined_trips_file}")
except Exception as e:
    print(f"❌ Error cargando {combined_trips_file}: {e}")
    exit()

# Verificar que el archivo Overview.csv existe
if not os.path.exists(overview_file):
    print(f"❌ No se encontró el archivo {overview_file}.")
    exit()

# Cargar el archivo Overview.csv
try:
    overview_df = pd.read_csv(overview_file, encoding='latin1', sep=";")
    print(f"✅ Archivo cargado: {overview_file}")
except Exception as e:
    print(f"❌ Error cargando {overview_file}: {e}")
    exit()

print(overview_df.head())


# Realizar el merge con la columna Trip (Overview) y trip_name (combined_df)
merged_df = combined_df.merge(overview_df, left_on="trip_name", right_on="Trip", how="left")

unnamed_cols = [col for col in merged_df.columns if "Unnamed" in col]
if unnamed_cols:
    # print(f"⚠️ Eliminando columnas innecesarias: {unnamed_cols}")
    merged_df.drop(columns=unnamed_cols, inplace=True)


# Guardar el resultado en un nuevo archivo CSV
merged_df.to_csv(output_file, index=False)

print(f"✅ Archivo final guardado en: {output_file}")