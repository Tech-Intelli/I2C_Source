ARG BASE_IMAGE=ubuntu:latest

FROM --platform=linux/amd64 ${BASE_IMAGE}

RUN apt-get update && apt-get install -y python3-pip

WORKDIR /app/data

ENV OPENAI_API_KEY=''
ENV TELEGRAM_PERSONAL_USER=''
ENV TELEGRAM_BOT_TOKEN=''
ENV AWS_ACCESS_KEY_ID=''
ENV AWS_SECRET_ACCESS_KEY=''
ENV AWS_DEFAULT_REGION=''
ENV FLASK_SESSION_SECRET_KEY=''
ENV RITEKIT_API_KEY=''
ENV PYTORCH_MPS_DISABLE=1

COPY requirements.txt .
ENV PYTORCH_MPS_DISABLE=1

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN apt-get update && \
    apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev && \
    rm -rf /var/lib/apt/lists/*
COPY . .

WORKDIR /app/data/src

RUN which python3 && python3 --version
ENV CUDA_VISIBLE_DEVICES=
ENV PYTORCH_MPS_DISABLE=1
ENV STREAMLIT_SERVER_ENABLE_METRICS=false
ENV STREAMLIT_SERVER_PORT=8080
CMD ["/usr/bin/python3", "-m", "streamlit", "run", "app_streamlit.py"]
