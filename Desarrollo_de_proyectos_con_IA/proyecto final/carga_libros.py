from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_ollama import OllamaEmbeddings
import pandas as pd
import ftfy

from dotenv import load_dotenv
import os

load_dotenv()

index_name = os.getenv("INDEX_NAME")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")



def cargar_libros(path_file, titulo, comentario):
    """
    Función para cargar un documento PDF, procesarlo y almacenarlo en una base de datos vectorial.

    Parámetros:
    -----------
    path_file : str
        Ruta al archivo PDF que se desea cargar y procesar.

    titulo :str
        Titulo del documento que se almacenara en la base de datos
        
    comentario : str
        Comentario asociado al documento que se almacenará junto a él en la base de datos.

    Retorna:
    --------
    str
        Un mensaje indicando si el documento fue cargado con éxito o si ya existe en la base de datos.

    """

    # Cargar el documento PDF desde la ruta especificada
    loader = PyPDFLoader(path_file)
    docs = loader.load()

    # Arreglar el texto de cada página del documento usando ftfy (soluciona problemas de codificación)
    # ademas adiciona el titulo proporcionado por el usario a los metadatos 
    for doc in docs:
        doc.page_content = ftfy.fix_text(doc.page_content)
        doc.metadata["source"] = titulo

    # Cargar el archivo CSV que contiene el registro de libros previamente cargados
    df = pd.read_csv("file_libros")

    # Contar el número de páginas del documento cargado
    npaginas = len(docs)

    # Agregar una nueva fila al DataFrame con el título, número de páginas y comentario del documento
    df.loc[len(df)] = [titulo, npaginas, comentario]

    # Verificar si el título ya está duplicado en la base de datos
    if df["Título"].duplicated().sum() != 0:
        # Si ya existe, retornar un mensaje indicando que el documento está duplicado
        return "Ya existe este documento en la base de datos vectorial"

    # Guardar el DataFrame actualizado en el archivo CSV
    df.to_csv("file_libros", index=False)

    # Configurar un divisor de texto que separa el contenido en fragmentos de 1000 caracteres con un solapamiento de 200
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Cargar el modelo de embeddings utilizando OllamaEmbeddings
    embed = OllamaEmbeddings(model="mxbai-embed-large")

    # Inicializar la base de datos vectorial utilizando Pinecone
    vector_store = PineconeVectorStore(embedding=embed, index_name=index_name)

    # Cargar los documentos procesados (fragmentos) en la base de datos vectorial con el embedding configurado
    vector_store.from_documents(splits, embedding=embed, index_name=index_name)

    # Retornar un mensaje de éxito indicando que el documento fue cargado correctamente
    return f"El documento {titulo} ha sido cargado con éxito"
