FROM python:3.9

WORKDIR /app/data

ENV OPENAI_API_KEY=
ENV TELEGRAM_PERSONAL_USER=
ENV TELEGRAM_BOT_TOKEN=
ENV AWS_ACCESS_KEY_ID=
ENV AWS_SECRET_ACCESS_KEY=
ENV AWS_DEFAULT_REGION=

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y libgl1-mesa-glx

COPY . .

WORKDIR /app/data/src

CMD ["streamlit", "run", "app_streamlit.py"]
