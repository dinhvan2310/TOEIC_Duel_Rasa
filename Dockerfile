FROM rasa/rasa-pro:3.12.18

USER root
WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y build-essential gcc

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5005

CMD ["run", "--enable-api", "--cors", "*"]