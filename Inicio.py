import streamlit as st
from streamlit_option_menu import option_menu


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
        icons=['caret-right', 'caret-right','caret-right'], default_index=0)


# Cargar un archivo de audio
fileaudio = selected+".mp3"
audio_file = open(fileaudio, 'rb')
audio_bytes = audio_file.read()

# Mostrar el reproductor de audio
st.audio(audio_bytes, format='audio/mp3', start_time=0)

file = selected+".txt"
texto = read_text_file(file)
st.write(texto)