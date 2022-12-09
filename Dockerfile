FROM python:3.8-slim-buster

WORKDIR reconnaissanceVideo


RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt install -y git

RUN adduser -D myuser
USER myuser

RUN git clone https://github.com/Fefel76/reconnaissanceVideo.git

COPY --chown=myuser:myuser . .

RUN python3 -m pip install virtualenv
RUN python3 -m venv env
RUN source env/bin/activate

RUN pip3 freeze > requirements.txt
RUN pip3 install -r requirements.txt

RUN ls -ltr

CMD [ "python3", "run.py" , "salon"]
