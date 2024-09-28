from langchain_community.embeddings import HuggingFaceBgeEmbeddings 
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os



# caragas las variables de entorno definidas en el archivo .env
load_dotenv()


pinecone_api_key = os.getenv('PINECONE_API_KEY') 


def retrievel():
    embeddings = HuggingFaceBgeEmbeddings(model_name="all-mpnet-base-v2")
    vector_store = PineconeVectorStore(index_name='victory', embedding=embeddings)
    retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 10, "lambda_mult": 0.6},
)
    
    return retriever