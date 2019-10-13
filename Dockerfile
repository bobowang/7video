FROM python:2.7-alpine
ADD . /7video
WORKDIR /7video

RUN mkdir -p /data/7video
RUN mkdir ~/.pip
RUN echo "[global]" > ~/.pip/pip.conf
RUN echo "trusted-host=mirrors.aliyun.com" >> ~/.pip/pip.conf
RUN echo "index-url=http://mirrors.aliyun.com/pypi/simple" >> ~/.pip/pip.conf
RUN pip install -r requirements.txt
RUN python apps/sql.py init
CMD ["sh"]
#CMD ["gunicorn", "-w", "4", "-b" "0.0.0.0:5000" "app:app"]
