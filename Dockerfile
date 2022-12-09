FROM python:3.8-slim-buster

WORKDIR reconnaissanceVideo


RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt install -y git

RUN git clone https://github.com/Fefel76/reconnaissanceVideo.git

COPY . .

RUN python3 -m pip install --user virtualenv
RUN python3 -m venv env
RUN source env/bin/activate

RUN pip3 install -r ./requirements.txt

RUN ls -l

CMD [ "python3", "run.py" , "salon"]
