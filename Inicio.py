import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_shadcn_ui as ui
import os
from funciones import procesar_solicitud_anthropic
import anthropic


       

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
    selected = option_menu("Índice", ["Prefacio","Contenido de Calidad", 'Originalidad','Conflicto Ético','Audiencia Objetivo','Limita la Creatividad','Reputación Dañada','Barrera Tecnológica','Derechos de Autor','Personalización','Mercado Inmaduro','Contenido Único'], 
        icons=['caret-right', 'caret-right','caret-right','caret-right','caret-right','caret-right','caret-right','caret-right','caret-right','caret-right','caret-right'], default_index=0)


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


if 'respuesta' not in st.session_state:
    st.session_state['respuesta'] = ''

def anthropic_stream(system, user_input):
    st.session_state['respuesta']=''
    client = anthropic.Anthropic()
    prompt_final = system + " "+user_input
    # Crea el stream usando el cliente de Anthropic
    with client.messages.stream(
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt_final}],
        model="claude-3-haiku-20240307",
    ) as stream:
        # Itera sobre cada texto que llega del stream
        for text in stream.text_stream:
            st.session_state['respuesta'] += text
            yield text

def stream_to_app(system, user_input):
    # Función que pasa el generador a Streamlit para mostrar en la aplicación
    st.write_stream(anthropic_stream(system, user_input))

# Asegurarse de que texto_archivo_salida tiene contenido válido
prompt_system = f"""Utiliza el siguiente contenido para fundamentar y apoyar tus respuestas:
{texto_archivo_salida}"""  






if selected == "Asistente":
    if 'respuesta' not in st.session_state:
        st.session_state['respuesta'] = ''
    else:
        if st.session_state['respuesta'] != "":
            with st.chat_message("assistant"):
                 st.write(st.session_state['respuesta'])

    prompt = st.chat_input("Tu Pregunta")
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            stream_to_app(prompt_system,prompt)



#if selected == "FAQ":
#    st.write("Pronto Disponible ...")






