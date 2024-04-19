import streamlit as st
from streamlit_option_menu import option_menu
import os
from funciones import procesar_solicitud_anthropic


st.set_page_config(
    page_title="Consejos para escribir un ebook con IA",
    page_icon="😊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.aulasimple.ai',
        'Report a bug': "https://www.aulasimple.ai",
        'About': "### Desarrollado por aulasimple.ai"
    }
)

def read_text_file(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        data = file.read()
    return data


with st.sidebar:
    selected = option_menu("Índice", ["Prefacio","Contenido de Calidad", 'Originalidad','Conflicto Ético','Audiencia Objetivo','Limita la Creatividad','Reputación Dañada','Barrera Tecnológica','Derechos de Autor','Personalización','Mercado Inmaduro','Contenido Único','Asistente'], 
        icons=['caret-right', 'caret-right','caret-right','caret-right','caret-right','caret-right','caret-right','caret-right','caret-right','caret-right','caret-right','caret-right','bi-robot'], default_index=0)


fileaudio = selected + ".mp3"
# Validar si el archivo existe
if os.path.exists(fileaudio):
    # Abrir el archivo de audio
    with open(fileaudio, 'rb') as audio_file:
        audio_bytes = audio_file.read()

    # Mostrar el reproductor de audio
    st.audio(audio_bytes, format='audio/mp3', start_time=0)



file = selected + ".txt"
# Validar si el archivo existe
if os.path.exists(file):
    # Leer el contenido del archivo
    with open(file, 'r', encoding='utf-8') as file_handle:
        texto = file_handle.read()

    # Mostrar el contenido del archivo en la interfaz
    st.write(texto)



exclude_files = ['requirements.txt']
archivo_salida = "recopilafile"
# Determinar el modo de apertura basado en la existencia del archivo


if not os.path.exists(archivo_salida):
    modo_apertura = 'a' if os.path.exists(archivo_salida) else 'w'

    # Abrir el archivo de salida
    with open(archivo_salida, modo_apertura, encoding='utf-8') as file_out:
        # Recorrer todos los archivos en el directorio actual
        for archivo in os.listdir('.'):
            if archivo.endswith(".txt") and archivo not in exclude_files:
                # Abrir el archivo y leer su contenido
                with open(archivo, 'r', encoding='utf-8') as file_in:
                    contenido = file_in.read()
                    file_out.write(contenido + "\n")  # Escribir el contenido en el archivo de salida


with open(archivo_salida, 'r', encoding='utf-8') as file_handle:
     texto_archivo_salida = file_handle.read()


# Asegurarse de que texto_archivo_salida tiene contenido válido
prompt_system = f"""Eres un asistente que responde preguntas únicamente y exclusivamante relacionadas con la escritura de libros usando inteligencia artificial.
Utiliza negritas , cursiva y otros recursos para hacer el texto legible.
Utiliza el siguiente contenido para fundamentar y apoyar tus respuestas:
{texto_archivo_salida}"""  





if selected == "Asistente":
    prompt = st.chat_input("Tu Pregunta")
    if prompt:
        with st.spinner("Espera ..."):
            respuesta = procesar_solicitud_anthropic(prompt_system,prompt)
            st.session_state['respuesta'] = respuesta
st.write( st.session_state['respuesta'] )
