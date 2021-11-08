FROM python:3.6.5

RUN apt-get update && apt-get -y install netcat && apt-get clean

WORKDIR /app
ADD . ./

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x ./run.sh

EXPOSE 8000

CMD ["./run.sh"]