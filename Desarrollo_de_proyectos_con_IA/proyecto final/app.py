import streamlit as st
from backen_funcions import file_load , generation_retriever
from langchain_ollama import ChatOllama
import pandas as pd


st.set_page_config(page_title="Asistente Lanto",page_icon="lanto.jpg")

llm = ChatOllama(model="llama3.1", temperature=0.5)

def main():

    
    st.sidebar.title("Menu de opciones")
    # Crear sidebar cerrada por defecto
    page = st.sidebar.radio("Seleccione la opción que necesita", ["Home","File load", "Contact"])

    # Mostrar contenido principal según la opción seleccionada
    if page == "Home":

        st.markdown("<h1 style='color: purple;'>Bienvenido a su asistente de recuperacion de información aumentada Lanto</h1>", unsafe_allow_html=True)  
        st.markdown("""<h6 >Esta aplicación proporciona un asistente para la recupacion de información y consulta de 
                   una base de datos de documentos pdf personalizada en su computadora local sin necesidad de internet,
                 en la parte superior izquierda hay una pestaña que te muetra tres opciones, para subir archivos a tu base de datos de usa
                    la opción File load.
                    </h1>""", unsafe_allow_html=True)
       
        st.image("lanto.jpg",width=150)

        st.markdown("""<h6 >Para recuperar información de sus documentos realice una pregunta acorde a los mismos, recuerde ser lo mas preciso y claro posible, 
                    si no obtiene resultados haga de nuevo la consula""", unsafe_allow_html=True)
       
        df = pd.read_csv("file_libros")

    
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "Hola, soy Lanto, ¿Que información buscas de tu base de datos de documentos?"}]
    
        prompt = st.chat_input('Pregunta de tus documentos...')

        if prompt:

            st.session_state["messages"].append({
            "role": "user",
            "content": prompt})

            generacion, referencias = generation_retriever(prompt)
            
            
            respuesta = f"""**Generacion**:{generacion}   

**referencias**:{referencias}
            """
     
            st.session_state["messages"].append({
            "role": "assistant",
            "content": respuesta})    

        for chat in st.session_state["messages"]:
            
            if chat["role"] == "assistant":
                
                st.chat_message(chat['role'], avatar="lanto.jpg").markdown(chat['content'])
            else:
                st.chat_message(chat['role']).markdown(chat['content'])
                
          
      
    elif page == "File load":

         file_load()


    elif page == "Contact":
        
        st.markdown("<h3 style='color: purple;'>Grupo conformado por:</h3>", unsafe_allow_html=True) 
        
        st.markdown("""<h6 >Leonardo Sánchez """, unsafe_allow_html=True)
        st.markdown("""<h6 >David Capera """, unsafe_allow_html=True)


    
main()




    
