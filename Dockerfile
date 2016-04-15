FROM centos:7
MAINTAINER zyfdegg@gmail.com

WORKDIR /usr/local/PythonServer/src

RUN yum update -y
RUN yum install -y python-setuptools
RUN yum install -y MySQL-python
RUN yum install -y python-pillow

RUN easy_install pip

RUN pip install tornado
RUN pip install flask
RUN pip install requests

COPY PythonServer /usr/local/PythonServer

EXPOSE 5000

ENTRYPOINT ["python","main.py"]
