FROM python:3

RUN mkdir /IncidentBot_docker
COPY . /IncidentBot_docker/
WORKDIR /IncidentBot_docker

RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "bot.py" ]