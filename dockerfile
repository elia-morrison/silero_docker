FROM python:3.8

WORKDIR /usr/app

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
ADD requirements.txt .
RUN pip3 install -r requirements.txt
ADD ./ ./

RUN apt-get update --fix-missing && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y sox

EXPOSE 9898

CMD [ "python3", "-u", "./app.py" ]