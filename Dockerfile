FROM python:3

#RUN apt-get update
#RUN apt-get install ffmpeg libsm6 libxext6  -y
#RUN apt install -y git
RUN groupadd -r user && useradd -r -g user user

RUN git clone https://github.com/Fefel76/reconnaissanceVideo.git
WORKDIR reconnaissanceVideo

USER user
RUN chown -R user *

RUN pip3 install -r requirements.txt

RUN mkdir ./videos
RUN mkdir ./log
RUN ls -ltr

ENV CAM_VISU False
ENV CAM_RECORD False
ARG pwd
ENV CAM_PWD=${pwd}
ARG login
ENV CAM_LOGIN=${login}

CMD [ "python3", "run.py" , "salon"]
