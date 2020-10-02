FROM oraclelinux:7-slim
RUN yum update -y
RUN yum install -y python2-pip.noarch python-devel.x86_64
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
