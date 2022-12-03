FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . .

CMD [ "python3", "run.py" , "salon", "&"]
CMD [ "python3", "run.py" , "garage", "&"]
CMD [ "python3", "run.py" , "piscine", "&"]