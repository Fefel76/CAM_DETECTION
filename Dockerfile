FROM python:3.8-slim-buster

ARG username
ARG password

WORKDIR reconnaissanceVideo


RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt install -y git

RUN git clone https://$(username):$(password)@github.com/Fefel76/reconnaissanceVideo.git

RUN pip3 install -r requirements.txt
CMD [ "python3", "run.py" , "salon"]
