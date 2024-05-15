from utils import *

# Modelo de Machine Learning
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

import pickle

# Lectura del folder de CVs para director
director_Folder = ['CVs/Nivel Director'] # Cambiar por la ruta de la carpeta
director_CVs = extract_text_from_folders(director_Folder)

# Lectura del folder de CVs para especialista
especialista_Folder = ['CVs/Nivel Especialista'] # Cambiar por la ruta de la carpeta
especialista_CVs = extract_text_from_folders(especialista_Folder)

# Lectura del folder de CVs para gerente
gerente_Folder = ['CVs/Nivel Gerente'] # Cambiar por la ruta de la carpeta
gerente_CVs = extract_text_from_folders(gerente_Folder)

# Converción de las listas a DFs
director_df = create_dataframe_from_extracted_texts(director_CVs)
especialista_df = create_dataframe_from_extracted_texts(especialista_CVs)
gerente_df = create_dataframe_from_extracted_texts(gerente_CVs)

# Concatenación de los DFs
df = pd.concat([director_df, especialista_df, gerente_df], ignore_index=True)

# Aplicación de funcion de limpieza
df['CV'] = df['CV'].apply(lambda x: cleanResume(x))

# Codificación de la columna de labels
le = LabelEncoder()
le.fit(df['label'])
df['label'] = le.transform(df['label'])

# Vectorización de los textos
tfidf = TfidfVectorizer(preprocessor=preprocess_text)
tfidf_matrix = tfidf.fit_transform(df['CV'])

# Creacion de dataframe final
df_tokens = pd.DataFrame(tfidf_matrix.toarray())
df_final = pd.concat([df_tokens,df['label']], axis=1)

# Guardado de dataframe
df_final.to_csv('labeled_features.csv',index=False)



