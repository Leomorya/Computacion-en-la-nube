import pandas as pd
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import subprocess





def subtitulo(path_video: str, name_out: str, size_font: int, df: pd.DataFrame):
    img_pil = None
    # crea el objeto cap y le carga el video 
    cap = cv2.VideoCapture(path_video)
    # Verifica que se pueda abrir el archivo de video
    if not cap.isOpened():
        print("Error: No se pudo abrir el archivo de video.")
        exit()

    # Cantidad de fps del video
    fps = cap.get(cv2.CAP_PROP_FPS)
    # Ancho y alto del video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Configurar el archivo de salida de video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f"{name_out}.mp4", fourcc, fps, (width, height))

    # Procesar cada cuadro del video para colocar subtítulos
    while cap.isOpened():
        ret, frame = cap.read()

        # Si no se pudo leer el cuadro, salir del bucle
        if not ret:
            print("No se pudo leer el cuadro, probablemente se alcanzó el final del video.")
            break

        # Obtener el tiempo actual en el video en segundos
        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

        # Path de la fuente   
        font_path = "DejaVuSansCondensed.ttf"

        # Recorrer el DataFrame para verificar si hay subtítulo para el cuadro actual
        for index, row in df[['start', 'end', 'texto_traducido']].iterrows():
            start = row['start']
            end = row['end']
            text = row['texto_traducido']

            if start <= current_time <= end:
                # Convertir el cuadro de OpenCV (BGR) a Pillow (RGB)
                img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                # Crear objeto de dibujo sobre la imagen
                draw = ImageDraw.Draw(img_pil)

                # Usar la fuente
                font_size = size_font
                font = ImageFont.truetype(font_path, font_size)

                # Calcular la longitud del texto y la posición centrada
                len_text = draw.textlength(text, font)
                x_text = (width - len_text) // 2
                y_text = 0  # Coloca el texto cerca de la parte superior

                # Dibujar el fondo negro para el texto
                draw.rectangle(((x_text, y_text), (x_text + len_text, y_text + font_size + 5)), fill="black")

                # Agregar el texto a la imagen
                draw.text((x_text, y_text), text, font=font, fill="white")
                break

        # Convertir la imagen de vuelta a OpenCV (RGB a BGR)
        frame_with_text = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        out.write(frame_with_text)

    # Cerrar los archivos de video
    cap.release()
    out.release()



def video_subtilado_final(path_video:str,out_name_video, size_font: int=16):
    """
    Genera un video subtitulado a partir de un video original y un archivo CSV, 
    luego agrega el audio original al video subtitulado.

    Args:
        path_video (str): Ruta al archivo de video original.
        out_name_video (str): Nombre base para el video subtitulado (sin extensión).
        size_font (int, optional): Tamaño de la fuente de los subtítulos. 
            Valor predeterminado: 16.

    Proceso:
        1. Carga un archivo CSV llamado "dataframe.csv", que se espera que contenga
           información de los subtítulos.
        2. Llama a la función `subtitulo` para generar un video subtitulado con los
           parámetros proporcionados.
        3. Utiliza `ffmpeg` para combinar el video subtitulado con el audio original
           del video de entrada, creando un archivo de salida con el nombre 
           `<out_name_video>_audio.mp4`.

    Output:
        Genera dos archivos:
        - `<out_name_video>.mp4`: Video con subtítulos pero sin audio.
        - `<out_name_video>_audio.mp4`: Video subtitulado con el audio original incluido.

    Nota:
        Esta función depende de la función `subtitulo` y del archivo CSV "dataframe.csv".
        También requiere que `ffmpeg` esté instalado en el sistema.

    Example:
        video_subtilado_final("video_original.mp4", "video_subtitulado", size_font=20)
    """
        
    df = pd.read_csv("dataframe.csv")
    subtitulo(path_video, out_name_video, size_font, df)
    final_output_file = f'{out_name_video}_audio.mp4'
    # proceso que carga el audio original en el video subtitulado
    subprocess.run(['ffmpeg', '-i', f"{out_name_video}.mp4", '-i', path_video, '-c:v', 'copy', '-c:a', 'aac', '-map', '0:v:0', '-map', '1:a:0', final_output_file])    

