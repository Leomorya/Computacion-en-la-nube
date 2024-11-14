import streamlit as st
from transcribe import transcribe_ingles
from traduce import traduccion
from subtitulando import video_subtilado_final

st.set_page_config(page_title="Asistente Lanto",page_icon="lanto.jpg")


def main():
    
    
# Utilizando hexadecimal
    st.markdown("<h1 style='color: #FF0000;'>Bienvenido a su asistente Lanto</h1>", unsafe_allow_html=True)
    st.image("lanto.jpg",width=150)
    st.markdown("<h3 style='color: blue;'>Esta página traduce al español videos en coreano y lo subtitula. </h3>", unsafe_allow_html=True)
    st.markdown("<h5> Sube el video en el siguiente botom  </h5>", unsafe_allow_html=True)
    
    


    # Widget para cargar el archivo de video
    video_file = st.file_uploader("Sube un archivo de video", type=["mp4", "mov", "avi", "mkv"])

    # Verificar si se cargó un archivo
    if video_file is not None:
        # Guardar el archivo de manera segura
        temp_path = f"./{video_file.name}"
        with open(temp_path, "wb") as f:
            f.write(video_file.getbuffer())
            st.success(f"Video '{video_file.name}' subido con éxito!")
        
            # Entrada de texto
            user_input = st.text_input("Coloca el nombre del video de salida:")
            if st.button("enviar"):
                
                # Aquí puedes agregar tu lógica de procesamiento

                    path = temp_path
                    with st.spinner("Transcribiendo el video"):
                            transcribe_ingles(path)
                            st.success("¡Video transcrito exitosamente!")
                    with st.spinner("Traduciendo al español la transcripción del video"):
                            traduccion()
                            st.success("¡Traducción exitosa!")
                    
                    with st.spinner("Subtitulando el video"):
                            video_subtilado_final(path, user_input )
                            st.success("¡Video subtitulado exitosamente!")
                    st.markdown(f"<h4> Nombre del video subtitulado {user_input}_audio.mp4</h4>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
