FROM python:3

WORKDIR reconnaissanceVideo


RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt install -y git

ENV USER=myuser
ENV UID=12345
ENV GID=23456
RUN adduser --disabled-password --ingroup "$USER" --no-create-home --uid "$UID" "$USER"
USER myuser

RUN git clone https://github.com/Fefel76/reconnaissanceVideo.git

COPY --chown=myuser:myuser . .

RUN python3 -m pip install virtualenv
RUN python3 -m venv env
RUN source env/bin/activate

RUN pip3 freeze > requirements.txt
RUN pip3 install -r requirements.txt

RUN ls -ltradd

CMD [ "python3", "run.py" , "salon"]
