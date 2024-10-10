

from langchain_pinecone import PineconeVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain.schema.runnable import RunnableLambda
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from dotenv import load_dotenv
import os

load_dotenv()

index_name = os.getenv("INDEX_NAME")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")







def remove_duplicate_documents(documents):
    """
    Elimina documentos duplicados de una lista basada en su contenido (atributo `page_content`).

    Parámetros:
    -----------
    documents : list
        Lista de documentos, donde cada documento tiene un atributo `page_content` que representa su contenido.

    Retorna:
    --------
    unique_documents : list
        Una lista de documentos que no contiene duplicados basados en el contenido de la página (`page_content`).
    """
    
    # Crear un conjunto para almacenar contenido ya visto
    seen_content = set()

    # Lista para almacenar documentos únicos
    unique_documents = []

    # Iterar sobre cada documento de la lista
    for doc in documents:
        # Si el contenido del documento no ha sido visto antes, agregarlo a la lista de únicos
        if doc.page_content not in seen_content:
            seen_content.add(doc.page_content)
            unique_documents.append(doc)

    # Retornar la lista de documentos únicos
    return unique_documents





def retriever_multi_query(query):
    """
    Función para realizar una búsqueda con consultas múltiples utilizando embeddings y un modelo de lenguaje, 
    aplicando un método de eliminación de duplicados en los resultados.

    Parámetros:
    -----------
    query : str
        La consulta o pregunta que se desea hacer para recuperar los documentos relevantes.

    Retorna:
    --------
    cadena : pipeline
        Un pipeline de procesamiento que incluye la búsqueda con múltiples consultas, eliminación de duplicados 
        y el retorno de los documentos procesados junto con la consulta original.

    """

    # Nombre del índice en Pinecone donde se almacenan los embeddings
    index_name = "lanto"

    # Inicializar el modelo de embeddings utilizando OllamaEmbeddings
    embed = OllamaEmbeddings(model="mxbai-embed-large")

    # Crear la base de datos vectorial en Pinecone utilizando los embeddings
    vector_store = PineconeVectorStore(embedding=embed, index_name=index_name)

    # Configurar el modelo de lenguaje LLM para generar las múltiples consultas
    llm = ChatOllama(model="llama3.1", temperature=0.5)

    # Crear el retriever que realiza búsquedas utilizando el modelo de lenguaje y el método MMR (Maximal Marginal Relevance)
    retriever_from_llm = MultiQueryRetriever.from_llm(
        retriever=vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5, "fetch_k": 10, "lambda_mult": 0.5}
        ), 
        llm=llm
    )

    # Definir una función que elimina los documentos duplicados utilizando RunnableLambda
    remove_duplicates_runnable = RunnableLambda(lambda docs: remove_duplicate_documents(docs))

    # Crear una cadena de procesamiento que realiza la búsqueda, elimina duplicados, y retorna los documentos con la consulta original
    cadena = retriever_from_llm | remove_duplicates_runnable | RunnableLambda(lambda docs: {"docs": docs, "query": query})

    # Retornar el pipeline resultante
    return cadena





def filtrado_relevante(docs, query):
    """
    Filtra documentos recuperados en función de su relevancia para una pregunta específica utilizando un modelo de lenguaje.

    Parámetros:
    -----------
    docs : list
        Lista de documentos que fueron recuperados.
        
    query : str
        La pregunta o consulta del usuario para la cual se evaluará la relevancia de los documentos.

    Retorna:
    --------
    doc_filtrados : list
        Lista de documentos que fueron considerados relevantes en función de la pregunta.
    """

    # Inicializar una lista vacía para almacenar los documentos filtrados como relevantes
    doc_filtrados = []

    # Definir el prompt del evaluador, que calificará la relevancia de un documento respecto a una pregunta
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Eres un evaluador que determina la relevancia de un documento recuperado respecto a una pregunta del usuario. No se requiere una prueba estricta. El objetivo es filtrar recuperaciones erróneas. Si el documento contiene palabras clave o significado semántico relacionado con la pregunta del usuario, califícalo como relevante.

        Proporciona una puntuación binaria ('0' o '1') para indicar si el documento es relevante para la pregunta."""),
        ("human", "Documento recuperado: {document}\nPregunta del usuario: {question}"),
    ])

    # Configurar el modelo de lenguaje (LLM) que evaluará los documentos
    llm = ChatOllama(model="llama3.1", temperature=0.0)

    # Crear la cadena de procesamiento que conecta el prompt con el modelo de lenguaje
    cadena2 = prompt | llm

    # Evaluar cada documento de la lista para determinar si es relevante
    for doc in docs:
        # Invocar el pipeline con la pregunta y el contenido del documento
        filtro = cadena2.invoke({"question": query, "document": doc})

        # Si la respuesta del modelo contiene un '1' (indicando que es relevante), agregar el documento a la lista de filtrados
        if "1" in filtro.content:
            doc_filtrados.append(doc)

    # Retornar la lista de documentos filtrados como relevantes
    return doc_filtrados



def retriever_filtrado_final(query):
    """
    Recupera documentos relevantes para una consulta con  con consultas múltiples utilizando embeddings y un modelo de lenguaje, 
    luego filtra aquellos que no son relevantes utilizando un modelo de lenguaje.

    Parámetros:
    -----------
    query : str
        La consulta o pregunta que se desea hacer para recuperar los documentos relevantes.

    Retorna:
    --------
    pipeline : pipeline
        Un pipeline que realiza una búsqueda multi-query, seguido de un filtro que elimina documentos irrelevantes.
    """

    # Crear una función que utiliza el filtro de relevancia para eliminar los documentos no relevantes
    remove_no_relevant_docs_runnable = RunnableLambda(
        lambda diccionario: filtrado_relevante(diccionario["docs"], diccionario["query"])
    )

    # Combinar el pipeline de recuperación de documentos con el filtro de relevancia
    return retriever_multi_query(query) | remove_no_relevant_docs_runnable





