import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.llms import OllamaLLM
from langchain_core.runnables import Runnable




def extraer_lista(traduccion_total):
    """
    Procesa la cadena de texto dada por la traducción de llama 
    Args:
        traduccion total(str): salida de la cadena de lanchain al traducir 
    
    """
    
    find_palabras = "traducciones_español = ["
    inicio_ = traduccion_total.find(find_palabras)
    final_ = traduccion_total.find("]")
    cadena_con_traduccion = traduccion_total[inicio_+len(find_palabras):final_-1]
    cadena_con_traduccion = cadena_con_traduccion.replace("'", '"')
    cadena_con_traduccion = cadena_con_traduccion.replace("\n    ", "")
    cadena_con_traduccion = cadena_con_traduccion.replace(' "', '"')
    cadena_con_traduccion = cadena_con_traduccion.replace('" ', '"')
    cadena_con_traduccion = cadena_con_traduccion.replace('""', '","')
    cadena_con_traduccion = cadena_con_traduccion.replace('"\n"', '","')
    text_list_traducido = cadena_con_traduccion.split('","')
    text_list_traducido[0] = text_list_traducido[0].replace('"','')
    text_list_traducido[-1] = text_list_traducido[-1].replace('"','')
       
    return text_list_traducido

def traducir(chain_, text_):
    
    """
    Traduce un texto utilizando un modelo o cadena de procesamiento y devuelve la lista de traducciones procesadas.

    Args:
        chain_ (obj): Cadena o modelo de procesamiento encargado de realizar la traducción.
        text_ (str): Texto que se desea traducir.

    Returns:
        list: Lista de traducciones extraídas del resultado del procesamiento.
    """
    longitud_ = len(text_)
    traduccion_= chain_.invoke({"longitud":longitud_, "text": text_})
    lista_traducida_ = extraer_lista(traduccion_)
    return lista_traducida_





def subtitulos_espanol(chain:Runnable, longitud:int, list_text:list):
    """
    Esta funcion traduce parcialmente lista de longitud =int y se asegura que el resultado de la lista traducida sea igual a la lista total, 
    para luego concatenar todas las litas y que la salida sea igual a la longitud total de la lista que se desea traducir 
    """


    # numero de listas a traducir
    n = len(list_text)//longitud
    lista_total_traducida = []
    print("Longitud de la lista a tradicir",len(list_text))
    for i in range(n): 
        texto = list_text[i*(longitud):(i+1)*longitud]
        lista_parcial = traducir(chain, texto)
        
        if len(lista_parcial)!= longitud:
            for j in range(50):
                print("entra al bucle interno")
                lista_parcial = traducir(chain, texto)
                x = lista_parcial
                print("Longitud de la lista traducida interna", len(lista_parcial))
                if len(lista_parcial) == longitud:
                   break
        lista_total_traducida = lista_total_traducida + lista_parcial
        print("rango de la traducción", i*(longitud),(i+1)*longitud)
        print("Longitud de la lista traducida", len(lista_parcial))
    
    texto = list_text[n*(longitud):(n+1)*longitud]
    txt_len = len(texto)
        
    if txt_len >=10:
        lista_parcial = traducir(chain, texto)
        if len(lista_parcial)!= txt_len:
            for j in range(30):
                print("entra al bucle interno 2")
                lista_parcial = traducir(chain, texto)
                x = lista_parcial
                print("Longitud de la lista traducida interna", len(lista_parcial))
                if len(lista_parcial) == txt_len:
                   break
        lista_total_traducida = lista_total_traducida + lista_parcial
    
    
    
    
    else: 
        texto =  list_text[-10:]
        lista_parcial = traducir(chain, texto)
        if len(lista_parcial)!= 10:
            for j in range(30):
                print("entra al bucle interno 3")
                lista_parcial = traducir(chain, texto)
                x = lista_parcial
                print("Longitud de la lista traducida interna", len(lista_parcial))
                if len(lista_parcial) == 10:
                   break


        lista_total_traducida = lista_total_traducida + lista_parcial[-txt_len:]
    print("Longitud de la lista traducida parcial final", len(lista_parcial[-txt_len:]))
    print("Longitud de la lista traducida final total", len(lista_total_traducida))
    return lista_total_traducida

    

import subprocess

def kill_process_using_gpu_memory(memory_threshold, sudo_password):
    """
    Mata los procesos que están usando más memoria GPU que el umbral especificado.
    
    :param memory_threshold: El umbral de memoria en MiB para filtrar los procesos.
    :param sudo_password: La contraseña de sudo para ejecutar el comando sin intervención del usuario.
    """
    # Ejecutar nvidia-smi para obtener la lista de procesos usando GPU
    result = subprocess.run(['nvidia-smi', '--query-compute-apps=pid,used_memory', '--format=csv,noheader,nounits'], capture_output=True, text=True)
    
    # Filtrar los procesos que superan el umbral de memoria
    for line in result.stdout.splitlines():
        pid, used_memory = map(int, line.split(','))
        if used_memory >= memory_threshold:
            print(f"Proceso con PID {pid} usa {used_memory} MiB de memoria GPU.")
            # Usar sudo con -S para leer la contraseña desde la entrada estándar
            subprocess.run(['sudo', '-S', 'kill', str(pid)], input=f"{sudo_password}\n", text=True)





def traduccion(longitud:int=40):
    
    """
    función final que da el resultado de la traducción del texto en ingles del dataframe traducido al español y 
    lo guarda el el mismo dataframe

      Args:
        longitud (int, optional): Longitud de la lista a traducir. 
            Valor predeterminado: 40.
    """
  

    
    
    
    
    llm = OllamaLLM(model="llama3.1", temperature=0.4)
    # sirve para llama 
    system_template = """eres un asistente que traduce al español, el siguiente texto trata de billar tres bandas,te paso una lista 
    con una longitud de {longitud}.
    Primero realiza la traducción como un todo y luego devuelve la tradución de cada elemento de la lista como una lista de python con nombre traducciones_español, 
    La lista debe tener el siguinte formato ["a","b","c"],
    no responde con la traducción completa, solo responde con la lista de python y nada mas, 
    recuerda que la lista traducida debe tener el mismo tamaño o longitud de la inicial.
    La palabra cushion traducela como banda."""
    prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
    )

    parser = StrOutputParser()

    chain = prompt_template | llm | parser
  
    
    df = pd.read_csv("dataframe.csv")
    lista_texto = df["text"].values
    lista_trad = subtitulos_espanol(chain,longitud,lista_texto)
    df["texto_traducido"] = lista_trad
    df.to_csv("dataframe.csv", index=False)
    
    # Llamar a la función con un umbral de memoria de 5000 MiB y tu contraseña de sudo
    kill_process_using_gpu_memory(5000, 'Khutumi')

    







