FROM python:2.7
WORKDIR /7video
RUN mkdir -p /data/7video
ADD . .

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf"]
