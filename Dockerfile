FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y netcat
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
ADD wait.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wait.sh
ENTRYPOINT ["/usr/local/bin/wait.sh"]
