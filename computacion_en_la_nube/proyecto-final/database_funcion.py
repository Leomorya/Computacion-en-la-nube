from azure.storage.blob import BlobServiceClient 
from azure.core.exceptions import ResourceExistsError
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings 
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os



# caragas las variables de entorno definidas en el archivo .env
load_dotenv()

connect_azure = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

pinecone_api_key = os.getenv('PINECONE_API_KEY') 

"""
funciones de azure

"""

def enumerar_libros():
    #os.environ["AZURE_STORAGE_CONNECTION_STRING"] = connection_string
    connect_str = connect_azure

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    
    container_name = "micontenedor"
    
    # Crea un cliente de contenedor
    container_client = blob_service_client.get_container_client(container_name)

    # iterador con los libros de azure
    blob_list = container_client.list_blobs()

    return blob_list 


def subir_libros(local_file_name, upload_file_path):
   
    connect_str = connect_azure
    container_name = "micontenedor"
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(container=container_name,
                                                  blob=local_file_name)
    

    resultado =""
    boleano = False

    # Sube el archivo PDF
    try:
        # Sube el archivo PDF
        with open(file=upload_file_path, mode="rb") as data:
            blob_client.upload_blob(data)
        resultado = f"Libro subido correctamente: {local_file_name}"
        boleano = True
    except ResourceExistsError:
       resultado = f"Error: El libro '{local_file_name}' ya existe en el almacenamiento."
    
    except Exception as e:
        resultado = f"Error inesperado: {e}"

    return resultado, boleano

"""
función de Pinecone
"""

def cargar_documento_pinecone(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    token_spliter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    splits = token_spliter.split_documents(docs)    
    embeddings = HuggingFaceBgeEmbeddings(model_name="all-mpnet-base-v2")
    vector_store = PineconeVectorStore.from_documents(splits, index_name='victory', embedding=embeddings)

