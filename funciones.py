def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()
    

from openai import OpenAI
import uuid
import os
# Función para convertir texto a voz
def text_to_speech_openai(text, voice):
    client = OpenAI()
    unique_filename = str(uuid.uuid4()) + ".mp3"

    # Define la ruta de la carpeta donde quieres guardar los archivos
    folder_path = "audios"

    # Verifica si la carpeta existe, si no, la crea
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Define la ruta completa del archivo de audio, incluyendo la carpeta
    speech_file_path = os.path.join(folder_path, unique_filename)

    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    response.stream_to_file(speech_file_path)
    
    # Devuelve la ruta completa del archivo y el nombre del archivo
    return speech_file_path, unique_filename






from anthropic import Anthropic
def procesar_solicitud_anthropic(prompt):
    client = Anthropic()
    response = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="claude-3-haiku-20240307",
    )
    return response.content[0].text





def solicitud_json_openai(promptsystem, promptuser):
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": promptsystem},
            {"role": "user", "content": promptuser}
        ]
    )
    return response.choices[0].message.content




import streamlit as st
import psycopg2
import pandas as pd
import requests
import psycopg2

def consulta_sql(consulta):
    # Datos de conexión a la base de datos
    conn_params = {
        "host": "dpg-ckkctjsl4vmc7397ns7g-a.oregon-postgres.render.com",
        "database": "basededatostest",
        "user": "basededatostest_user",
        "password": "UvkU6s7BmH2RlBtrpegRhsF7teMNNvPz"
    }
    try:
        # Establecer la conexión usando los parámetros definidos
        conn = psycopg2.connect(**conn_params)
        
        # Crear un nuevo cursor
        with conn.cursor() as cursor:
            # Ejecutar la consulta SQL proporcionada
            cursor.execute(consulta)
            
            # Obtener todos los resultados
            result = cursor.fetchall()
            
            # Cerrar la conexión
            conn.close()
            
            return result
    except psycopg2.Error as e:
        # En caso de error, imprimir el mensaje de error y retornar None
        print(f"Error al ejecutar consulta SQL: {e}")
        return None

