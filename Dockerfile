FROM python:2.7
ADD . /7video
WORKDIR /7video
RUN pip install -r requirements.txt
CMD ["gunicorn", "-w", "4", "-b" "0.0.0.0:5000" "app:app"]
