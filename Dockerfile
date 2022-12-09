FROM python:3

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt install -y git

RUN git clone https://github.com/Fefel76/reconnaissanceVideo.git

WORKDIR reconnaissanceVideo

RUN pip3 install -r requirements.txt

RUN ls -ltr

CMD [ "python3", "run.py" , "salon"]
