FROM mypython

#FROM python:3.8.16-slim
#ENV TZ="Europe/Paris"
#RUN apt-get update
#RUN apt install -y git
#RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN git clone https://github.com/Fefel76/CAM_DETECTION.git
WORKDIR CAM_DETECTION

RUN pip3 install -r requirements.txt
RUN mkdir ./videos && mkdir ./log mkdir ./conf

RUN groupadd -r user && useradd -r -g user user && chown -R user:user *
USER user


ENV CAM_VISU off
ENV CAM_RECORD on
ARG pwd
ENV CAM_PWD=${pwd}
ARG login
ENV CAM_LOGIN=${login}

CMD [ "python3", "run.py" , "salon"]
