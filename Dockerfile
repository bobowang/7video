FROM python:2.7
WORKDIR /7video
RUN mkdir -p /data/7video
ADD . .

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

RUN mkdir ~/.pip
RUN echo "[global]" > ~/.pip/pip.conf
RUN echo "trusted-host=mirrors.aliyun.com" >> ~/.pip/pip.conf
RUN echo "index-url=http://mirrors.aliyun.com/pypi/simple" >> ~/.pip/pip.conf
RUN pip install -r requirements.txt
CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf"]
