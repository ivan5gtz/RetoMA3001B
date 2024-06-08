from utils import *

# Modelo de Machine Learning
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

import pickle

import random

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

df_augmented = df.copy(deep=True)

def shuffle_entry(x):
    entry = x.split()

    if len(entry) > 150:
        random_remove = random.sample(entry, 150)
        new_entry = [element for element in entry if element not in random_remove]
        random.shuffle(new_entry)
        return ' '.join(new_entry)
    
    random.shuffle(entry)
    return ' '.join(entry)


    
df_augmented['CV'] = df_augmented['CV'].apply(lambda x: shuffle_entry(x))

df_augmented = pd.concat([df, df_augmented]).reset_index(drop=True)

# Codificación de la columna de labels
le = LabelEncoder()
le.fit(df['label'])
df['label'] = le.transform(df['label'])

le = LabelEncoder()
le.fit(df_augmented['label'])
df_augmented['label'] = le.transform(df_augmented['label'])

# Vectorización de los textos
tfidf = TfidfVectorizer(preprocessor=preprocess_text)
tfidf_matrix = tfidf.fit_transform(df['CV'])

tfidf_augmented = TfidfVectorizer(preprocessor=preprocess_text)
tfidf_augmented_matrix = tfidf_augmented.fit_transform(df_augmented['CV'])

# Creacion de dataframe final
df_tokens = pd.DataFrame(tfidf_matrix.toarray())
df_final = pd.concat([df_tokens,df['label']], axis=1)

df_tokens_augmented = pd.DataFrame(tfidf_augmented_matrix.toarray())
df_final_augmented = pd.concat([df_tokens_augmented,df_augmented['label']], axis=1)

# Guardado de dataframe
df_final.to_csv('labeled_features.csv',index=False)
df_final_augmented.to_csv('labeled_features_augmented.csv',index=False)

# Mensaje final
print('#####FINISHED#####')



