FROM python:3.6-slim-buster
WORKDIR /opt/7video
RUN mkdir -p /data/7video
ADD . .

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
RUN pip install -i https://pypi.doubanio.com/simple --trusted-host pypi.doubanio.com -r requirements.txt
CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf"]
