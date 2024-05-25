# OCR
import os
import docx2txt
import textract
import subprocess
import pytesseract

from pdf2image import convert_from_path

import zipfile
from PIL import Image
from io import BytesIO

# Generales
import re
import pandas as pd
import numpy as np

# Detección de Lenguaje
import nltk
nltk.download('punkt')
from langdetect import detect
from nltk.corpus import stopwords

#Traducción
from googletrans import Translator
translator = Translator()


# OCR
# Lectura de documentos .doc
def extract_text_from_doc(doc_path):
    text = textract.process(doc_path).decode('utf-8')
    if len(text) != 0:
        return text

    # Extraer imagenes de word
    z = zipfile.ZipFile(doc_path)
    all_files = z.namelist()

    imagenes_path = [x for x in all_files if x.startswith('word/media/')]

    text = ''
    for path in imagenes_path:
        imagen = z.open(path).read()
        imagen = Image.open(BytesIO(imagen))

        text += pytesseract.image_to_string(imagen)
    return text

# Lectura de documentos .docx
def extract_text_from_docx(docx_path):
    text = textract.process(docx_path).decode('utf-8')

    if len(text) != 0:
        return text

    # Extraer imagenes de word
    z = zipfile.ZipFile(docx_path)
    all_files = z.namelist()

    imagenes_path = [x for x in all_files if x.startswith('word/media/')]

    text = ''
    for path in imagenes_path:
        imagen = z.open(path).read()
        imagen = Image.open(BytesIO(imagen))

        text += pytesseract.image_to_string(imagen)

    return text

# Lectura de documentos .pdf
def extract_text_from_pdf(pdf_path):
    imagenes = convert_from_path(pdf_path)
    text = ''
    for imagen in imagenes:
        text += pytesseract.image_to_string(imagen)
    return text

# Extracción de texto
def extract_text_from_file(file_path):
    file_name, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()
    if file_extension == '.doc':
        return extract_text_from_doc(file_path)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    elif file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file type")

# Guardar el texto extraído
def extract_text_from_folders(folders):
    extracted_texts = []
    for folder in folders:
        for root, _, files in os.walk(folder):
            for filename in files:
                print(filename)
                if filename == '.gitignore':
                    continue
                file_path = os.path.join(root, filename)
                text = extract_text_from_file(file_path)
                label = folder.split('/')[-1]

                if translator.detect(text).lang == 'es':
                    text = translator.translate(text, src='es', dest='en').text
                
                extracted_texts.append({
                    'label': label,
                    'CV': text
                })

    return extracted_texts

# Creación de la base de datos
def create_dataframe_from_extracted_texts(extracted_texts):
    df = pd.DataFrame(extracted_texts)
    return df

# Limpieza de Datos
def cleanResume(txt):
    cleanText = re.sub('http\S+\s', ' ', txt)
    cleanText = re.sub('RT|cc', ' ', cleanText)
    cleanText = re.sub('#\S+\s', ' ', cleanText)
    cleanText = re.sub('@\S+', '  ', cleanText)
    cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText)
    cleanText = re.sub('\s+', ' ', cleanText)
    return cleanText

# Preprocesamiento de datos
# Descarga de stopwords en español e inglés
nltk.download('stopwords')
stop_words_english = set(stopwords.words('english'))
stop_words_spanish = set(stopwords.words('spanish'))

#Función de detección de texto
def preprocess_text(text):
    if not text or len(text) < 10:
        return ''
    try:
        lang = detect(text)
    except:
        lang = 'en'
    if lang == 'en':
        tokens = nltk.word_tokenize(text.lower())
        tokens = [word for word in tokens if word.isalpha() and word not in stop_words_english]
        return ' '.join(tokens)
    elif lang == 'es':
        tokens = nltk.word_tokenize(text.lower())
        tokens = [word for word in tokens if word.isalpha() and word not in stop_words_spanish]
        return ' '.join(tokens)
    else:
        return ''