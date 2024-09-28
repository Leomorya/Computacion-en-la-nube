# este dockerfile construye una aplicacion de RAG basica 

FROM fnndsc/python-poetry 

WORKDIR  /aplicacion 

COPY app.py database_funcion.py retrival.py .
COPY lanto.jpg .
COPY poetry.lock pyproject.toml .env .

# Instalar dependencias usando poetry
RUN poetry install --no-root

EXPOSE 8501

CMD ["poetry", "run", "streamlit", "run", "app.py"]


    


