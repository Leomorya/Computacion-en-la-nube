import streamlit as st
import pandas as pd 
import tempfile
from carga_libros import cargar_libros
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from funcion_retrievel import retriever_filtrado_final


def file_load():
    """
    Carga un archivo PDF a la base de datos vectorial, lo muestra en un listado junto con sus metadatos, y permite al usuario ver sus documentos almacenados.

    Esta función utiliza Streamlit para generar una interfaz gráfica donde el usuario puede cargar libros en formato PDF. Los documentos se almacenan en un archivo CSV que sirve como base de datos, y la lista de libros cargados se muestra en un dataframe interactivo.

    Parámetros:
    -----------
    - No recibe parámetros de entrada directamente, pero utiliza elementos interactivos proporcionados por Streamlit.
    
    Retorna:
    --------
    - No retorna valores explícitos, pero actualiza la interfaz de usuario y los datos almacenados en el archivo CSV.
    """
    
    # Título del módulo con formato en HTML que indica el propósito de la aplicación
    st.markdown("<h2 style='color: purple;'>Documentos para su asistente Lanto </h2>", unsafe_allow_html=True)

    # Muestra una imagen en la interfaz de usuario
    st.image("lanto.jpg", width=180)

    # Subtítulo del módulo con formato en HTML que describe la funcionalidad de carga de documentos
    st.markdown("<h3 style='color: blue;'>Modulo para cargar los documentos </h3>", unsafe_allow_html=True)

    # Descripción de las funcionalidades del módulo, informando al usuario sobre cómo cargar sus documentos PDF
    st.write("""En este apartado usted podra cargar sus libros a la base vectorial en formato pdf
                 y ver el listado de sus documentos en un dataframe""")

    # Carga el archivo CSV que contiene la lista de documentos previamente almacenados
    df = pd.read_csv("file_libros")

    # Si el DataFrame no está vacío, muestra los documentos cargados en un dataframe interactivo
    if not df.empty:
        st.write("Su listado de documentos es:")
        st.dataframe(df)  # Muestra el listado de documentos en un formato de tabla interactiva

    # Si no hay documentos cargados, informa al usuario que no tiene ningún documento en la base de datos
    else:
        st.write("Usted no tiene ningun documento cargado")

    # Expansión interactiva en la interfaz para que el usuario cargue un archivo PDF
    with st.expander("Subir un archivo PDF"):
        # Campo de entrada de texto para que el usuario ingrese el título del documento
        titulo = st.text_input("""Escriba el titulo de su documento, este debe ser único para evitar 
                                   pues es el identificador en la base de datos""")

        # Campo de entrada de texto para que el usuario agregue un comentario u observación sobre el documento
        comentario = st.text_input("Escriba un comentario o observación del documento a subir")

        # Permite al usuario cargar un archivo en formato PDF desde su computadora local
        uploaded_file = st.file_uploader("""Oprima el botón y suba de su computadora local el texto en pdf que 
                                         usted desee, este proceso puede tardar varios minutos, 
                                         la lista de documentos se actualiza automaticamente""", type=["pdf"])

        # Si el usuario ha subido un archivo PDF
        if uploaded_file:
            # Crea un archivo temporal para almacenar el PDF subido
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                tmp.write(uploaded_file.getbuffer())  # Escribe el contenido del archivo subido en el archivo temporal
                ruta_archivo = tmp.name  # Guarda la ruta temporal del archivo

                # Muestra un indicador de carga mientras se procesa el archivo
                with st.spinner('Cargando el archivo...'):
                    # Llama a la función 'cargar_libros' para procesar el archivo PDF
                    resultado_load = cargar_libros(ruta_archivo, titulo, comentario)
                    st.write(resultado_load)





def referencias_docs(docs):
    
    """
    Genera una cadena de referencias a partir de una lista de documentos.

    Args:
        docs (list): Lista de documentos, donde cada documento es un objeto con un atributo `metadata` que contiene información sobre la página y el origen.

    Returns:
        str: Cadena de referencias en formato "Título [fuente] y Página [página]", separadas por comas y espacios.

    Ejemplo:
        >>> docs = [doc1, doc2, doc3]
        >>> referencias = referencias_docs(docs)
        >>> print(referencias)
        Título El libro de oro.pdf y Página 28, Título El libro de oro.pdf y Página 71, Título El libro de oro.pdf y Página 32, Título El libro de oro.pdf y Página 1
    """
    
    referencia = []
    for doc in docs:
        referencia.append(f"Título {doc.metadata['source']}, página {doc.metadata['page']}")

    referencia = ", ".join(referencia)

    return referencia



def generation_retriever(query):
    """
    
     Un runnable para generar respuestas basadas en la consulta proporcionada y devolver la respuesta junto con las referencias utilizadas.
    Genera una respuesta basada en la consulta proporcionada y devuelve la respuesta junto con las referencias utilizadas.

    Esta función utiliza un modelo de lenguaje para generar respuestas concisas basadas en el contexto recuperado por el `retriever_filtrado_final`.
    También obtiene y devuelve las referencias (metadata) de los documentos utilizados para generar la respuesta, es un objeto Runable.

    Args:
        query (str): La pregunta o consulta del usuario.

     Returns:
        tuple: Una tupla con dos cadenas:
            - generation (str): La respuesta generada por el modelo.
            - referencias (str): Las referencias concatenadas en una cadena, que incluyen el título y la página de los documentos utilizados.
    """
    
        
    # Define el prompt del asistente con instrucciones para responder preguntas concisas.
    prompt = ChatPromptTemplate.from_messages([
        ("human", """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. Use 8 sentences maximum and keep the answer concise and ensure it contains relevant information.
        Question: {question} 
        Context: {context} 
        Answer:"""),
    ])

    # Define el modelo LLM a utilizar con una temperatura de 0 para respuestas determinísticas.
    llm = ChatOllama(
        model="llama3.1",
        temperature=0,
    )

    # Recupera los documentos filtrados con base en la consulta.
    resultado_final = retriever_filtrado_final(query)
    docs = resultado_final.invoke(query)

    # Obtiene las metadatas de los documentos recuperados.
    referencias = referencias_docs(docs)

    # Configura la cadena RAG (Retrieve and Generate).
    rag_chain = prompt | llm | StrOutputParser()
    
    # Genera la respuesta usando el contexto de los documentos y la pregunta del usuario.
    generation = rag_chain.invoke({"context": docs, "question": query})

    return generation, referencias
