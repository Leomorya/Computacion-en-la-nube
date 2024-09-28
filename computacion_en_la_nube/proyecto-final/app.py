import streamlit as st
from dotenv import load_dotenv
import tempfile
import os
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from langchain_openai import ChatOpenAI


from database_funcion import enumerar_libros, subir_libros, cargar_documento_pinecone
from retrival import retrievel


# caragas las variables de entorno definidas en el archivo .env
load_dotenv()




openay_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-3.5-turbo-0125",
    temperature=1, api_key=openay_api_key )

# Prompt
prompt = hub.pull("rlm/rag-prompt")

st.set_page_config(page_title="Asistente lanto",page_icon="lanto.jpg")

def main():
    
    
# Utilizando hexadecimal
    st.markdown("<h1 style='color: #FF0000;'>Bienvenido a su asistente educativo Lanto</h1>", unsafe_allow_html=True)

    st.markdown("<h6 >Esta página proporciona un asistente educativo basado en nuestra base de datos de textos, para comunicar tema de manera acertada a nuestros estudiantes, profesores e interesados los contenidos</h1>", unsafe_allow_html=True)
    


    st.markdown("<h4 style='color: blue;'>En este apartado usted podra subir los libros que necesite, solo en archivo pdf </h1>", unsafe_allow_html=True)

    
    
    with st.expander("Subir un archivo PDF"):
    
        uploaded_file = st.file_uploader("Oprima el botón y suba de su computudora local el texto en pdf que usted desee, este proceso puede tardar varios minutos", type=["pdf"])

        bool = False
        
        if uploaded_file:
            
            
            
            
            # Crea un archivo temporal
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                tmp.write(uploaded_file.getbuffer())
                ruta_archivo = tmp.name
                
            #st.write(f"Ruta del archivo temporal: {ruta_archivo}")
            
            with st.spinner('Cargando el archivo...'):
                resultado, bool = subir_libros(uploaded_file.name, ruta_archivo)
            
                if bool:
                    cargar_documento_pinecone(ruta_archivo)
                    st.write("Archivo cargado en pinecone")

                else:
                    st.write("Archivo ya existente pinecone")

            
            
                st.write(resultado)


    st.markdown("<h4 style='color: blue;'>El listado de los libros en nuestra base de datos es: </h1>", unsafe_allow_html=True)


    libros = enumerar_libros()

    for libro in libros:
        st.write(libro.name)

    
    st.markdown("<h3 style='color: purple;'>Asistente Lanto</h1>", unsafe_allow_html=True)
    
    st.image("lanto.jpg", width=120)

    pregunta = st.text_input("Ingrese su pregunta contextualizada en los de nuestra base de datos")
    
    botom = st.button("Enviar")


    if botom:

        
        recupador = retrievel()

        docs = retrievel().invoke(pregunta)

        #st.write(docs)
        
        rag_chain = prompt | llm | StrOutputParser()


        generation = rag_chain.invoke({"context": docs, "question": pregunta})


             
        
        
        st.success(generation)

    
    #busqueda = retrievel().invoke("Dos es todo")
    #st.write(busqueda)



if __name__ == "__main__":
    main()