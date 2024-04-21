import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_shadcn_ui as ui
import os
from funciones import procesar_solicitud_anthropic
import anthropic


       

st.set_page_config(
    page_title="Dominando la Revolución IA",
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
    selected = option_menu("Índice", ["Inicio","Ingeniería en Prompt", 'Marca Personal','Narrativa de Datos','Piensa Creativo','Estrategia Negocio','Gestión de Proyectos','Lenguaje Natural','Aprendizaje Continuo','Limitaciones','Conclusión','Asistente','Arbol de Conceptos'], 
        icons=['caret-right', 'caret-right','caret-right','caret-right','caret-right','caret-right','caret-right','caret-right','caret-right','caret-right','caret-right','bi-robot','ui-checks'], default_index=0)


fileaudio = selected + ".mp3"
# Validar si el archivo existe
if os.path.exists(fileaudio):
    # Abrir el archivo de audio
    with open(fileaudio, 'rb') as audio_file:
        audio_bytes = audio_file.read()

    # Mostrar el reproductor de audio
    st.audio(audio_bytes, format='audio/mp3', start_time=0)



file = selected + ".tldr"
# Validar si el archivo existe
if os.path.exists(file):
    # Leer el contenido del archivo
    with open(file, 'r', encoding='utf-8') as file_handle:
        texto = file_handle.read()
        with st.expander("TL;DR"):
            st.write("*"+texto+"*")




file = selected + ".txt"
# Validar si el archivo existe
if os.path.exists(file):
    # Leer el contenido del archivo
    with open(file, 'r', encoding='utf-8') as file_handle:
        texto = file_handle.read()
    st.markdown(texto)



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
                    print(archivo)
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



if selected == "Arbol de Conceptos":


    #if selected == "FAQ":
    #    st.write("Pronto Disponible ...")
    from streamlit_tree_select import tree_select

    st.title("🌳 Árbol de Conceptos")
    st.subheader("Deja que la IA conecte los conceptos")

    # Create nodes to display
    nodes = [
        {
            "label": "Ingeniería en Prompt",
            "value": "ingenieria_prompt",
            "children": [
                {"label": "Fundamentos de la Comunicación con la IA", "value": "fundamentos_comunicacion"},
                {"label": "Desarrollo de Prompts Efectivos", "value": "desarrollo_prompts"},
                {"label": "Habilidades Requeridas", "value": "habilidades_requeridas"}
            ]
        },
        {
            "label": "Marca Personal Potenciada por IA",
            "value": "marca_personal",
            "children": [
                {"label": "Elementos Visuales", "value": "elementos_visuales"},
                {"label": "Contenido Digital", "value": "contenido_digital"},
                {"label": "Interacción y Redes Sociales", "value": "interaccion_redes"},
                {"label": "Análisis y Mejora", "value": "analisis_mejora"}
            ]
        },
        {
            "label": "Pensamiento Creativo",
            "value": "pensamiento_creativo",
            "children": [
                {"label": "Arte y Música", "value": "arte_musica"},
                {"label": "Literatura y Diseño", "value": "literatura_diseno"},
                {"label": "Aplicaciones Profesionales", "value": "aplicaciones_profesionales"}
            ]
        },
        {
            "label": "Estrategia",
            "value": "estrategia",
            "children": [
                {"label": "Implementación de Negocios con IA", "value": "implementacion_negocios"},
                {"label": "Gestión de Riesgos", "value": "gestion_riesgos"}
            ]
        },
        {
            "label": "Gestión de Proyectos IA",
            "value": "gestion_proyectos",
            "children": [
                {"label": "Coordinación de Equipos", "value": "coordinacion_equipos"},
                {"label": "Visión de Implementación", "value": "vision_implementacion"},
                {"label": "Agilidad Organizacional", "value": "agilidad_organizacional"}
            ]
        },
        {
            "label": "Procesamiento del Lenguaje Natural (NLP)",
            "value": "procesamiento_lenguaje_natural",
            "children": [
                {"label": "Interacción Humano-Máquina", "value": "interaccion_humano_maquina"},
                {"label": "Aplicaciones en Diferentes Sectores", "value": "aplicaciones_sectores"},
                {"label": "Innovaciones en Creatividad", "value": "innovaciones_creatividad"}
            ]
        },
        {
            "label": "Curiosidad y Aprendizaje Continuo",
            "value": "curiosidad_aprendizaje",
            "children": [
                {"label": "Exploración de Nuevos Territorios", "value": "exploracion_territorios"},
                {"label": "Combinación de Conocimientos", "value": "combinacion_conocimientos"},
                {"label": "Comunidad y Colaboración", "value": "comunidad_colaboracion"}
            ]
        },
        {
            "label": "Entendiendo las Limitaciones de la IA",
            "value": "limitaciones_ia",
            "children": [
                {"label": "Realismo en Expectativas", "value": "realismo_expectativas"},
                {"label": "Ética y Sesgos", "value": "etica_sesgos"},
                {"label": "Colaboración Humano-IA", "value": "colaboracion_humano_ia"}
            ]
        }
    ]




    


    col1, col2 = st.columns([1, 2])

    with col1:
        return_select = tree_select(nodes)
        # st.write(return_select)
        textos = str(return_select)

    with col2:
        if st.button("Analizar Conceptos Seleccionados"):
           # st.write(textos)
            prompt_sistema = "Considera el siguente contenidos para que tengas el contexto de lo que debes responder: "+texto_archivo_salida
            prompt_usuario = "Crea un articulo para un blog que permita dar claridad de la relación pero solo entre los conceptos cuya key = 'checked'"
            prompt_usuario += "No consideres para el articulo los conceptos key = 'expanded'"
            prompt_usuario += "Busca en este JSON los conceptos "+textos
            print("===")
            print(prompt_sistema + prompt_usuario)
            stream_to_app(prompt_sistema,prompt_usuario)