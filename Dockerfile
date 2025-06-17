FROM python:3.10.7

USER root
WORKDIR /app
COPY . /app

# Cài đặt các thư viện hệ thống cần thiết
RUN apt-get update && apt-get install -y build-essential gcc

RUN pip install --no-cache-dir -r requirements.txt

# Train the Rasa model
RUN rasa train

EXPOSE 5005

CMD ["rasa", "run", "--enable-api", "--cors", "*"]