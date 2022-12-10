FROM python:3

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt install -y git

RUN git clone https://github.com/Fefel76/reconnaissanceVideo.git

WORKDIR reconnaissanceVideo

RUN pip3 install -r requirements.txt

RUN mkdir ./videos
RUN mkdir ./log
RUN ls -ltr

ENV CAM_VISU False
ENV CAM_RECORD False
ARG pwd
ENV CAM_PWD=${pwd}
ARG login
ENV CAM_login=${login}

CMD [ "python3", "run.py" , "salon"]
