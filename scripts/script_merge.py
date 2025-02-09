import pandas as pd
import glob
import os

# Rutas de los archivos
csv_folder = "../data/raw/"
overview_file = "../data/raw/Overview.xlsx"
output_file = "../data/processed/dataset_completo.csv"

# Cargar la tabla Overview con datos globales de cada viaje
df_overview = pd.read_excel(overview_file)

# Normalizar nombres de columnas para evitar problemas
df_overview.columns = df_overview.columns.str.strip().str.lower()  # Elimina espacios y pone en minúsculas
df_overview.rename(columns={"trip_id": "Trip_ID"}, inplace=True)  # Asegurar coincidencia de nombres

# Buscar todos los archivos CSV en la carpeta
csv_files = glob.glob(os.path.join(csv_folder, "*.csv"))

# 🔍 Verificar cuántos archivos encontró
print(f"Se encontraron {len(csv_files)} archivos CSV.")

# Leer cada CSV, agregar columna 'Trip_ID' y almacenarlo en una lista
df_list = []
for file in csv_files:
    df = pd.read_csv(file)  # Cargar CSV
    trip_id = os.path.basename(file).replace(".csv", "")  # Obtener nombre del archivo sin ".csv"
    df["Trip_ID"] = trip_id  # Agregar columna identificadora
    df_list.append(df)

# Asegurar que todos los DataFrames tengan las mismas columnas
all_columns = list(set().union(*(df.columns for df in df_list)))
df_list_aligned = [df.reindex(columns=all_columns) for df in df_list]

# Concatenar todos los archivos en un solo DataFrame
df_combined = pd.concat(df_list_aligned, ignore_index=True)

# Unir df_combined con df_overview usando Trip_ID como clave
df_final = df_combined.merge(df_overview, on="Trip_ID", how="left")

# Guardar el dataset combinado final
df_final.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f" Dataset combinado con Overview guardado en {output_file}")