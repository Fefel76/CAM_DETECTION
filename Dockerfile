FROM python:3.8-slim-buster

WORKDIR /app

ARG username
ARG password

RUN git clone https://$(username):$(password)@github.com/Fefel76/reconnaissanceVideo.git

RUN pip3 install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y


CMD [ "python3", "run.py" , "salon"]
