FROM python:3.8-slim-buster


WORKDIR reconnaissanceVideo

RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt install -y git

RUN pip3 install -r requirements.txt
CMD [ "python3", "run.py" , "salon"]
