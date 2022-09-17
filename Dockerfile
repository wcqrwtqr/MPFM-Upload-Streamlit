FROM python:3.9-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY . /app

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir pandas Pillow plotly streamlit openpyxl plotly seaborn simpy 
# RUN pip install pandas Pillow plotly streamlit openpyxl plotly seaborn simpy 

EXPOSE 8501

# ENTRYPOINT ["streamlit","run"]

CMD ["streamlit","run","layout.py"]
