import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
# Leer el archivo Excel
load_dotenv()
file_path = 'geodir-ubigeo-inei.xlsx'
df = pd.read_excel(file_path)

# Convertir la columna 'Poblacion' a entero (eliminando las comas)
df['Poblacion'] = df['Poblacion'].replace({',': ''}, regex=True).astype(int)
df.columns = df.columns.str.lower()

# Motor de conexión para PgSQL, por ejemplo
engine = create_engine(os.getenv('DATABASE_URL'))

# Insertar los datos en la tabla 'ubigeo'
df.to_sql('ubigeo', con=engine, if_exists='append', index=False)