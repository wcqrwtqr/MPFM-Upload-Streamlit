FROM python:3.9-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY . /app

WORKDIR /app
# RUN pip install --upgrade pip
RUN pip install --upgrade pip && pip install --no-cache-dir pandas Pillow plotly streamlit openpyxl plotly seaborn simpy scipy matplotlib
# RUN pip install pandas Pillow plotly streamlit openpyxl plotly seaborn simpy 

EXPOSE 8501

RUN rm -rf .gitignore Procfile README.org README.md.bak reqirments_new.txt requirements.txt setup.sh __pycache__/

# ENTRYPOINT ["streamlit","run"]

CMD ["streamlit","run","layout.py"]
