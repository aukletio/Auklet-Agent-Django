FROM python:3.6

RUN \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y build-essential && \
  apt-get install -y software-properties-common && \
  apt-get install -y wget

ADD ./auklet /auklet
ADD ./tests /tests
ADD ./setup.py /setup.py
ADD ./README.md /README.md
ADD ./config /config
ADD ./requirements.txt /requirements.txt
ADD ./tests.txt /tests.txt
ADD ./.coveragerc /.coveragerc
ADD ./compose/tests/initialize_test_environment.sh /initialize_test_environment.sh

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN apt-get -y install python3 && \
  python3 get-pip.py

RUN pip3 install -U setuptools
RUN pip3 install coverage

RUN python3 setup.py install