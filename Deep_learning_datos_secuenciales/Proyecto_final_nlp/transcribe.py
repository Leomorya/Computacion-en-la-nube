import whisper
import pandas as pd
import torch
import gc






def transcribe_ingles(path_video: str):
    """
    Transcribe un video y traduce su contenido al inglés, almacenando los segmentos en un archivo CSV.

    Parámetros:
    -----------
    path_video : str
        Ruta al archivo de video que se desea transcribir y traducir.

    Descripción:
    ------------
    Esta función utiliza un modelo de transcripción para convertir el audio de un video en texto.
    El texto transcrito se traduce del idioma original (coreano) al inglés. 
    Luego, se organiza la información de los segmentos transcritos en un DataFrame de pandas y
    se guarda en un archivo CSV llamado 'dataframe.csv'.


    Salida:
    -------
    Crea un archivo CSV llamado 'dataframe.csv' con las columnas de los segmentos transcritos y traducidos.

    Ejemplo de uso:
    ---------------
    transcribe_ingles("ruta/al/video.mp4")
    """
    model = whisper.load_model("medium")
    result = model.transcribe(path_video, language="Korean", task="translate")
    df = pd.DataFrame(result["segments"])
    df.to_csv("dataframe.csv", index=False)

    del model

    torch.cuda.empty_cache()
    torch.cuda.memory_reserved(0)
    torch.cuda.memory_stats()
    gc.collect()